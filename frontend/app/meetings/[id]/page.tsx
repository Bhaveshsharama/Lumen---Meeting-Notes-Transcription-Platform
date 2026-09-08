'use client';
import React, { useRef, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import {
    getMeeting, getTranscript, getSummary, getActionItems,
    deleteMeeting, toggleActionItem, generateSummary, type TranscriptSegment, type ActionItem
} from '@/lib/api';
import { useRouter } from 'next/navigation';
import MeetingHeader from '@/components/meetings/MeetingHeader';
import styles from './detail.module.css';

// ── Sub-components ──────────────────────────────────────────────────────────

function formatTime(secs: number) {
    const m = Math.floor(secs / 60).toString().padStart(2, '0');
    const s = Math.floor(secs % 60).toString().padStart(2, '0');
    return `${m}:${s}`;
}

function AudioPlayer({ currentTime, duration, onSeek }: {
    currentTime: number; duration: number; onSeek: (val: number | ((prev: number) => number)) => void;
}) {
    const [playing, setPlaying] = useState(false);
    const [speed, setSpeed] = useState(1);
    // Use a ref so the interval doesn't restart every tick
    const currentTimeRef = React.useRef(currentTime);
    currentTimeRef.current = currentTime;

    React.useEffect(() => {
        if (!playing) return;
        // Check end via ref so we don't need currentTime in deps
        if (currentTimeRef.current >= duration && duration > 0) {
            setPlaying(false);
            return;
        }
        let lastTick = performance.now();
        const interval = setInterval(() => {
            const now = performance.now();
            const delta = (now - lastTick) / 1000;
            lastTick = now;
            if (currentTimeRef.current >= duration && duration > 0) {
                setPlaying(false);
                clearInterval(interval);
                return;
            }
            onSeek((prev: number) => Math.min(prev + delta * speed, duration));
        }, 100);
        return () => clearInterval(interval);
        // NOTE: currentTime intentionally excluded — use ref instead
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [playing, speed, duration, onSeek]);

    const pct = duration > 0 ? (currentTime / duration) * 100 : 0;
    return (
        <div className={styles.player}>
            <button className={styles.playBtn} onClick={() => setPlaying(!playing)} aria-label={playing ? 'Pause' : 'Play'}>
                {playing ? '⏸' : '▶'}
            </button>
            <span className={styles.playerTime}>{formatTime(currentTime)}</span>
            <input
                type="range" min={0} max={duration || 100} value={currentTime}
                className={styles.seekSlider}
                style={{ '--seek-pct': `${pct}%` } as React.CSSProperties}
                onChange={(e) => { onSeek(Number(e.target.value)); }}
                aria-label="Seek"
            />
            <span className={styles.playerTime}>{formatTime(duration)}</span>
            <select className={styles.speedSelect} value={speed} onChange={(e) => setSpeed(Number(e.target.value))}>
                <option value="0.5">0.5×</option>
                <option value="1">1×</option>
                <option value="1.5">1.5×</option>
                <option value="2">2×</option>
            </select>
        </div>
    );
}

function TranscriptPanel({ segments, currentTime, onSeek, searchQ }: {
    segments: TranscriptSegment[]; currentTime: number; onSeek: (t: number) => void; searchQ: string;
}) {
    // Find the segment whose window precisely contains the currentTime
    const exactMatch = segments.find((s) => s.start_time <= currentTime && s.end_time > currentTime);
    // Fallback: the LAST segment that has already started (most recent before cursor)
    const fallback = segments.reduce<TranscriptSegment | undefined>(
        (acc, s) => (s.start_time <= currentTime ? s : acc),
        undefined
    );
    // Only highlight if playback has actually moved past 0
    const activeId = currentTime > 0.01 ? (exactMatch?.id ?? fallback?.id) : undefined;

    const activeRef = useRef<HTMLDivElement>(null);

    React.useEffect(() => {
        if (activeRef.current) {
            activeRef.current.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
    }, [activeId]);

    const SPEAKER_COLORS: Record<string, string> = {};
    const colors = ['#7A5AF8', '#E85D8A', '#16A34A', '#F5A524', '#3B82F6'];
    let ci = 0;
    const getColor = (speaker: string) => {
        if (!SPEAKER_COLORS[speaker]) {
            SPEAKER_COLORS[speaker] = colors[ci++ % colors.length];
        }
        return SPEAKER_COLORS[speaker];
    };

    const filtered = searchQ
        ? segments.filter((s) => s.text.toLowerCase().includes(searchQ.toLowerCase()))
        : segments;

    const highlight = (text: string) => {
        if (!searchQ) return text;
        const idx = text.toLowerCase().indexOf(searchQ.toLowerCase());
        if (idx === -1) return text;
        return (
            <>
                {text.slice(0, idx)}
                <mark style={{ background: 'var(--highlight)', borderRadius: 2, padding: '0 1px' }}>
                    {text.slice(idx, idx + searchQ.length)}
                </mark>
                {text.slice(idx + searchQ.length)}
            </>
        );
    };

    return (
        <div className={styles.transcript}>
            {filtered.length === 0 && <p className={styles.empty}>No segments found.</p>}
            {filtered.map((seg) => {
                const speaker = seg.speaker_label || seg.speaker_id?.toString() || 'Unknown';
                const isActive = seg.id === activeId;
                return (
                    <div
                        key={seg.id}
                        ref={isActive ? activeRef : null}
                        className={`${styles.segment} ${isActive ? styles.activeSegment : ''}`}
                        onClick={() => onSeek(seg.start_time)}
                        role="button"
                        tabIndex={0}
                    >
                        <div className={styles.segmentLeft}>
                            <div
                                className={styles.speakerAvatar}
                                style={{ background: getColor(speaker) }}
                                title={speaker}
                            >
                                {speaker.charAt(0).toUpperCase()}
                            </div>
                        </div>
                        <div className={styles.segmentBody}>
                            <div className={styles.segmentMeta}>
                                <span className={styles.speakerName}>{speaker}</span>
                                <button
                                    className={`${styles.timestamp} mono`}
                                    title={`Seek to ${formatTime(seg.start_time)}`}
                                    onClick={(e) => { e.stopPropagation(); onSeek(seg.start_time); }}
                                    aria-label={`Seek to ${formatTime(seg.start_time)}`}
                                >
                                    {formatTime(seg.start_time)}
                                </button>
                            </div>
                            <p className={styles.segmentText}>{highlight(seg.text) as React.ReactNode}</p>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}

function SummaryPanel({ summary, meetingId, onRegenerate, isRegenerating }: {
    summary: { overview: string; topics: { id: number; title: string; start_time: number }[] } | null;
    meetingId: number;
    onRegenerate: () => void;
    isRegenerating: boolean;
}) {
    if (!summary) return <div className={styles.panelEmpty}>No summary generated yet.</div>;
    return (
        <div className={styles.summaryPanel}>
            <div className={styles.summaryHeader}>
                <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                    <span>✨</span>
                    <h3 className={styles.summaryTitle}>AI Summary</h3>
                </div>
                <button
                    onClick={onRegenerate}
                    disabled={isRegenerating}
                    style={{
                        padding: '4px 10px', fontSize: 12, fontWeight: 500,
                        background: 'var(--accent-lavender-bg)', color: 'var(--brand-primary)',
                        border: 'none', borderRadius: 'var(--radius-full)', cursor: isRegenerating ? 'not-allowed' : 'pointer',
                        opacity: isRegenerating ? 0.6 : 1, transition: 'opacity 0.2s', marginLeft: 'auto'
                    }}
                >
                    {isRegenerating ? 'Generating...' : '✨ Generate Summary'}
                </button>
            </div>
            <p className={styles.summaryText}>{summary.overview}</p>
            {summary.topics.length > 0 && (
                <div className={styles.topicsSection}>
                    <h4 className={styles.sectionLabel}>Topics</h4>
                    <div className={styles.topicChips}>
                        {summary.topics.map((t) => (
                            <span key={t.id} className={styles.topicChip}>
                                <span>🕐</span> {t.title}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
}

import { createActionItem, updateActionItem, deleteActionItem } from '@/lib/api';

function ActionItemsPanel({ items, meetingId }: { items: ActionItem[]; meetingId: number }) {
    const qc = useQueryClient();
    const [newItemText, setNewItemText] = useState('');
    const [editingId, setEditingId] = useState<number | null>(null);
    const [editText, setEditText] = useState('');

    const invalidate = () => qc.invalidateQueries({ queryKey: ['action-items', meetingId] });

    const toggleMut = useMutation({
        mutationFn: ({ id, completed }: { id: number; completed: boolean }) =>
            toggleActionItem(id, completed),
        onSuccess: invalidate,
    });

    const addMut = useMutation({
        mutationFn: (text: string) => createActionItem(meetingId, text),
        onSuccess: () => {
            invalidate();
            setNewItemText('');
        },
    });

    const updateMut = useMutation({
        mutationFn: ({ id, text }: { id: number; text: string }) => updateActionItem(id, { text }),
        onSuccess: () => {
            invalidate();
            setEditingId(null);
        },
    });

    const deleteMut = useMutation({
        mutationFn: (id: number) => deleteActionItem(id),
        onSuccess: invalidate,
    });

    const handleEditStart = (item: ActionItem) => {
        setEditingId(item.id);
        setEditText(item.text);
    };

    return (
        <div className={styles.actionItemsList}>
            {items.length === 0 && <div className={styles.panelEmpty}>No action items yet.</div>}
            {items.map((item) => (
                <div key={item.id} className={styles.actionItem}>
                    {editingId === item.id ? (
                        <div style={{ display: 'flex', width: '100%', gap: '8px' }}>
                            <input
                                autoFocus
                                value={editText}
                                onChange={e => setEditText(e.target.value)}
                                style={{ flex: 1, padding: '4px', borderRadius: '4px', border: '1px solid var(--border-light)' }}
                                onKeyDown={e => {
                                    if (e.key === 'Enter') updateMut.mutate({ id: item.id, text: editText });
                                    if (e.key === 'Escape') setEditingId(null);
                                }}
                            />
                            <button onClick={() => updateMut.mutate({ id: item.id, text: editText })}>Save</button>
                            <button onClick={() => setEditingId(null)}>Cancel</button>
                        </div>
                    ) : (
                        <>
                            <input
                                id={`ai-${item.id}`}
                                type="checkbox"
                                checked={item.is_completed}
                                className={styles.checkbox}
                                onChange={(e) => toggleMut.mutate({ id: item.id, completed: e.target.checked })}
                            />
                            <label htmlFor={`ai-${item.id}`} className={`${styles.actionText} ${item.is_completed ? styles.completed : ''}`}>
                                {item.text}
                            </label>
                            <div className={styles.actionActions} style={{ marginLeft: 'auto', display: 'flex', gap: '4px', opacity: 0.7 }}>
                                <button onClick={() => handleEditStart(item)} style={{ background: 'transparent', border: 'none', cursor: 'pointer' }}>✎</button>
                                <button onClick={() => { if (confirm('Delete?')) deleteMut.mutate(item.id); }} style={{ background: 'transparent', border: 'none', cursor: 'pointer', color: '#ea4335' }}>🗑</button>
                            </div>
                        </>
                    )}
                </div>
            ))}
            <div style={{ marginTop: '1rem', display: 'flex', gap: '8px' }}>
                <input
                    placeholder="New action item..."
                    value={newItemText}
                    onChange={e => setNewItemText(e.target.value)}
                    style={{ flex: 1, padding: '6px 8px', borderRadius: '6px', border: '1px solid var(--border-light)' }}
                    onKeyDown={e => {
                        if (e.key === 'Enter' && newItemText.trim()) addMut.mutate(newItemText);
                    }}
                />
                <button
                    onClick={() => { if (newItemText.trim()) addMut.mutate(newItemText); }}
                    disabled={!newItemText.trim()}
                    style={{ padding: '6px 12px', background: 'var(--brand-primary)', color: 'white', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
                >
                    Add
                </button>
            </div>
        </div>
    );
}

function OutlinePanel({ topics }: { topics: { id: number; title: string; start_time: number }[]; onSeek?: (t: number) => void; }) {
    if (topics.length === 0) return <div className={styles.panelEmpty}>No outline available.</div>;
    return (
        <div className={styles.outlineList}>
            {topics.map((t, i) => (
                <div key={t.id} className={styles.outlineItem}>
                    <span className={styles.outlineNum}>{i + 1}</span>
                    <span className={styles.outlineTitle}>{t.title}</span>
                    <span className={`${styles.outlineTime} mono`}>{formatTime(t.start_time)}</span>
                </div>
            ))}
        </div>
    );
}

function RightPanel({ meetingId, summary, actionItems }: {
    meetingId: number;
    summary: { overview: string; topics: { id: number; title: string; start_time: number }[] } | null;
    actionItems: ActionItem[];
}) {
    const qc = useQueryClient();
    const [activeTab, setActiveTab] = useState<'summary' | 'action-items' | 'outline'>('summary');
    const tabs = [
        { id: 'summary', label: 'Summary' },
        { id: 'action-items', label: 'Action Items' },
        { id: 'outline', label: 'Outline' },
    ] as const;

    const regenMut = useMutation({
        mutationFn: () => generateSummary(meetingId),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['summary', meetingId] });
            qc.invalidateQueries({ queryKey: ['action-items', meetingId] });
        }
    });

    return (
        <div className={styles.rightPanel}>
            <div className={styles.tabBar}>
                {tabs.map((tab) => (
                    <button
                        key={tab.id}
                        className={`${styles.tabBtn} ${activeTab === tab.id ? styles.activeTab : ''}`}
                        onClick={() => setActiveTab(tab.id)}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>
            <div className={styles.panelContent}>
                {activeTab === 'summary' && (
                    <SummaryPanel
                        summary={summary}
                        meetingId={meetingId}
                        isRegenerating={regenMut.isPending}
                        onRegenerate={() => regenMut.mutate()}
                    />
                )}
                {activeTab === 'action-items' && <ActionItemsPanel items={actionItems} meetingId={meetingId} />}
                {activeTab === 'outline' && <OutlinePanel topics={summary?.topics ?? []} />}
            </div>
        </div>
    );
}

// ── Page ────────────────────────────────────────────────────────────────────

export default function MeetingDetailPage({ params }: { params: Promise<{ id: string }> }) {
    const { id: idStr } = React.use(params);
    const id = parseInt(idStr, 10);
    const router = useRouter();
    const qc = useQueryClient();
    const [currentTime, setCurrentTime] = useState(0);
    const [searchQ, setSearchQ] = useState('');

    const { data: meeting, isError: mErr } = useQuery({
        queryKey: ['meeting', id],
        queryFn: () => getMeeting(id),
    });

    const { data: segments = [] } = useQuery({
        queryKey: ['transcript', id],
        queryFn: () => getTranscript(id),
        enabled: !!meeting,
    });

    const { data: summary } = useQuery({
        queryKey: ['summary', id],
        queryFn: () => getSummary(id),
        enabled: !!meeting,
    });

    const { data: actionItems = [] } = useQuery({
        queryKey: ['action-items', id],
        queryFn: () => getActionItems(id),
        enabled: !!meeting,
    });

    const deleteMut = useMutation({
        mutationFn: () => deleteMeeting(id),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['meetings'] });
            router.push('/meetings');
        },
    });

    if (mErr) notFound();
    if (!meeting) {
        return <div className={styles.loading}>Loading meeting…</div>;
    }

    const duration = segments.length > 0 ? Math.max(...segments.map((s) => s.end_time)) : 0;

    return (
        <div className={styles.page}>
            <MeetingHeader meeting={meeting} />

            {/* 2-column layout */}
            <div className={styles.columns}>
                {/* LEFT — Player + Transcript */}
                <div className={styles.leftCol}>
                    <AudioPlayer currentTime={currentTime} duration={duration} onSeek={setCurrentTime} />

                    <div className={styles.transcriptSearch}>
                        <span className={styles.searchIcon}>🔍</span>
                        <input
                            id="transcript-search"
                            type="text"
                            className={styles.searchInput}
                            placeholder="Search in transcript…"
                            value={searchQ}
                            onChange={(e) => setSearchQ(e.target.value)}
                        />
                    </div>

                    <TranscriptPanel
                        segments={segments}
                        currentTime={currentTime}
                        onSeek={setCurrentTime}
                        searchQ={searchQ}
                    />
                </div>

                {/* RIGHT — Tabs */}
                <div className={styles.rightCol}>
                    <RightPanel
                        meetingId={id}
                        summary={summary ?? null}
                        actionItems={actionItems}
                    />
                </div>
            </div>
        </div>
    );
}
