'use client';
import { useState, useEffect, Suspense } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'next/navigation';
import { getMeetings, getParticipants, type MeetingsPage } from '@/lib/api';
import MeetingCard from '@/components/meetings/MeetingCard';
import MeetingsSidebar from '@/components/meetings/MeetingsSidebar';
import AskAIPanel from '@/components/meetings/AskAIPanel';
import styles from './meetings.module.css';

function MeetingsContent() {
    const searchParams = useSearchParams();
    const [q, setQ] = useState(searchParams.get('q') || '');
    const [sort, setSort] = useState('recent');
    const [dateFilter, setDateFilter] = useState('all');
    const [participantFilter, setParticipantFilter] = useState('');
    const [page, setPage] = useState(1);
    const [activeTab, setActiveTab] = useState<'hosted' | 'shared'>('hosted');
    const [activeFilter, setActiveFilter] = useState<'my' | 'all'>('my');
    const PAGE_SIZE = 10;

    useEffect(() => { setPage(1); }, [q, sort, dateFilter, participantFilter]);

    let date_from: string | undefined = undefined;
    if (dateFilter === 'today') {
        const d = new Date(); d.setHours(0, 0, 0, 0); date_from = d.toISOString();
    } else if (dateFilter === '7days') {
        const d = new Date(); d.setDate(d.getDate() - 7); date_from = d.toISOString();
    } else if (dateFilter === '30days') {
        const d = new Date(); d.setDate(d.getDate() - 30); date_from = d.toISOString();
    }

    const { data, isLoading, isError } = useQuery<MeetingsPage>({
        queryKey: ['meetings', q, sort, dateFilter, participantFilter, page],
        queryFn: () => getMeetings({
            q: q || undefined,
            sort,
            page,
            page_size: PAGE_SIZE,
            date_from,
            participant_id: participantFilter ? parseInt(participantFilter, 10) : undefined
        }),
    });

    const { data: participants = [] } = useQuery({
        queryKey: ['participants'],
        queryFn: () => getParticipants(''),
    });

    const totalPages = data ? Math.ceil(data.total / PAGE_SIZE) : 1;

    return (
        <div className={styles.layout}>
            {/* Sub-sidebar */}
            <MeetingsSidebar activeFilter={activeFilter} onFilterChange={setActiveFilter} />

            {/* Main content */}
            <div className={styles.main}>
                {/* Inner top bar */}
                <div className={styles.topBar}>
                    <div className={styles.topBarLeft}>
                        <h1 className={styles.pageTitle}>Meetings</h1>
                    </div>
                    <div className={styles.topBarRight}>
                        <div className={styles.searchWrap}>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="11" cy="11" r="8" /><path d="m21 21-4.35-4.35" /></svg>
                            <input
                                id="meetings-search"
                                type="text"
                                className={styles.searchInput}
                                placeholder="Search by title or keyword"
                                value={q}
                                onChange={(e) => setQ(e.target.value)}
                            />
                            <kbd className={styles.kbd}>Ctrl+K</kbd>
                        </div>
                        <span className={styles.freeBadge}>
                            <svg width="10" height="10" viewBox="0 0 24 24" fill="#22c55e" stroke="none"><circle cx="12" cy="12" r="12" /></svg>
                            3 Free meetings
                        </span>
                    </div>
                </div>

                {/* Tab bar */}
                <div className={styles.tabBar}>
                    <div className={styles.tabs}>
                        <button
                            className={`${styles.tab} ${activeTab === 'hosted' ? styles.activeTab : ''}`}
                            onClick={() => setActiveTab('hosted')}
                        >
                            Hosted by me
                        </button>
                        <button
                            className={`${styles.tab} ${activeTab === 'shared' ? styles.activeTab : ''}`}
                            onClick={() => setActiveTab('shared')}
                            disabled
                            style={{ opacity: 0.5, cursor: 'not-allowed' }}
                            title="Coming Soon"
                        >
                            Shared with me (Coming Soon)
                        </button>
                    </div>
                    <div className={styles.tabActions}>
                        <select
                            className={styles.sortSelect}
                            value={participantFilter}
                            onChange={(e) => setParticipantFilter(e.target.value)}
                        >
                            <option value="">Any Participant</option>
                            {participants.map((p: any) => (
                                <option key={p.id} value={p.id}>{p.name}</option>
                            ))}
                        </select>
                        <select
                            className={styles.sortSelect}
                            value={dateFilter}
                            onChange={(e) => setDateFilter(e.target.value)}
                        >
                            <option value="all">All Date</option>
                            <option value="today">Today</option>
                            <option value="7days">Last 7 Days</option>
                            <option value="30days">Last 30 Days</option>
                        </select>
                        <select
                            className={styles.sortSelect}
                            value={sort}
                            onChange={(e) => setSort(e.target.value)}
                        >
                            <option value="recent">Sort: Most Recent</option>
                            <option value="oldest">Sort: Oldest</option>
                        </select>
                    </div>
                </div>

                {/* Content area */}
                <div className={styles.content}>
                    {isLoading && (
                        <div className={styles.skeletonList}>
                            {['K', 'A', 'R'].map((letter) => (
                                <div key={letter} className={styles.skeletonRow}>
                                    <div className={styles.skeletonAvatar}>{letter}</div>
                                    <div className={styles.skeletonLines}>
                                        <div className={styles.skeletonLine} style={{ width: '60%' }} />
                                        <div className={styles.skeletonLine} style={{ width: '40%' }} />
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {isError && (
                        <div className={styles.error}>
                            <p>⚠️ Could not load meetings. Make sure the backend is running.</p>
                        </div>
                    )}

                    {data && data.items.length === 0 && (
                        <div className={styles.empty}>
                            <div className={styles.emptyIconWrap}>
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#7a5af8" strokeWidth="1.5"><rect x="3" y="4" width="18" height="18" rx="2" /><line x1="16" y1="2" x2="16" y2="6" /><line x1="8" y1="2" x2="8" y2="6" /><line x1="3" y1="10" x2="21" y2="10" /></svg>
                                <div className={styles.emptyPlusBadge}>+</div>
                            </div>
                            <h3 className={styles.emptyTitle}>Looks like you haven&apos;t recorded a meeting yet</h3>
                            <p className={styles.emptySubtext}>
                                Once you record your first meeting with Lumen, it&apos;ll show up right here.
                            </p>
                            <button className={styles.captureBtn}>+ Capture</button>
                        </div>
                    )}

                    {data && data.items.length > 0 && (
                        <div className={styles.meetingList}>
                            {data.items.map((m) => (
                                <MeetingCard key={m.id} meeting={m} />
                            ))}
                        </div>
                    )}

                    {data && totalPages > 1 && (
                        <div className={styles.pagination}>
                            <button
                                className={styles.pageBtn}
                                disabled={page <= 1}
                                onClick={() => setPage((p) => p - 1)}
                            >
                                ← Prev
                            </button>
                            <span className={styles.pageInfo}>Page {page} of {totalPages}</span>
                            <button
                                className={styles.pageBtn}
                                disabled={page >= totalPages}
                                onClick={() => setPage((p) => p + 1)}
                            >
                                Next →
                            </button>
                        </div>
                    )}
                </div>
            </div>

            {/* Ask AI panel */}
            <AskAIPanel />
        </div>
    );
}

export default function MeetingsPage() {
    return (
        <Suspense fallback={<div>Loading...</div>}>
            <MeetingsContent />
        </Suspense>
    );
}
