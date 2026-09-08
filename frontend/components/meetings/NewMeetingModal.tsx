'use client';
import { useState, useRef } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useRouter } from 'next/navigation';
import { createMeeting, uploadTranscript, pasteTranscript, generateSummary } from '@/lib/api';
import styles from './NewMeetingModal.module.css';

interface Props { onClose: () => void; }

export default function NewMeetingModal({ onClose }: Props) {
    const [tab, setTab] = useState<'upload' | 'paste'>('upload');
    const [title, setTitle] = useState('');
    const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
    const [pasteText, setPasteText] = useState('');
    const [file, setFile] = useState<File | null>(null);
    const [errorMsg, setErrorMsg] = useState<string | null>(null);
    const fileRef = useRef<HTMLInputElement>(null);
    const router = useRouter();
    const qc = useQueryClient();

    const createMut = useMutation({
        mutationFn: async () => {
            // 1. Create meeting
            const meeting = await createMeeting({ title, meeting_date: date });
            // 2. Ingest transcript
            if (tab === 'upload' && file) {
                await uploadTranscript(meeting.id, file);
            } else if (tab === 'paste' && pasteText.trim()) {
                let format = pasteText.trim().startsWith('{') ? 'json' : 'txt';
                let finalPasteText = pasteText;

                // Auto-detect VTT syntax even if missing header
                if (pasteText.includes('-->')) {
                    format = 'vtt';
                    if (!pasteText.trim().startsWith('WEBVTT')) {
                        finalPasteText = 'WEBVTT\n\n' + pasteText;
                    }
                }

                await pasteTranscript(meeting.id, finalPasteText, format);
            }
            // 3. Generate summary (llm)
            try { await generateSummary(meeting.id); } catch { }
            return meeting;
        },
        onSuccess: (meeting) => {
            qc.invalidateQueries({ queryKey: ['meetings'] });
            onClose();
            router.push(`/meetings/${meeting.id}`);
        },
        onError: (err: any) => {
            const detail = err?.response?.data?.detail;
            if (Array.isArray(detail)) {
                setErrorMsg(detail.map((d: any) => d.msg).join(', '));
            } else if (typeof detail === 'string') {
                setErrorMsg(detail);
            } else {
                setErrorMsg('Failed to create meeting. Try again.');
            }
        },
    });

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (!title.trim()) return;
        createMut.mutate();
    };

    return (
        <div className={styles.overlay} onClick={(e) => e.target === e.currentTarget && onClose()}>
            <div className={styles.modal} role="dialog" aria-modal="true" aria-label="Create Meeting">
                <div className={styles.modalHeader}>
                    <h2 className={styles.modalTitle}>New Meeting</h2>
                    <button className={styles.closeBtn} onClick={onClose} aria-label="Close">✕</button>
                </div>

                <form onSubmit={handleSubmit}>
                    <div className={styles.field}>
                        <label htmlFor="meeting-title" className={styles.label}>Meeting Title *</label>
                        <input
                            id="meeting-title"
                            className={styles.input}
                            type="text"
                            placeholder="e.g. Weekly Engineering Sync"
                            value={title}
                            onChange={(e) => setTitle(e.target.value)}
                            required
                        />
                    </div>

                    <div className={styles.field}>
                        <label htmlFor="meeting-date" className={styles.label}>Date</label>
                        <input
                            id="meeting-date"
                            className={styles.input}
                            type="date"
                            value={date}
                            onChange={(e) => setDate(e.target.value)}
                        />
                    </div>

                    <div className={styles.tabs}>
                        <button
                            type="button"
                            className={`${styles.tab} ${tab === 'upload' ? styles.activeTab : ''}`}
                            onClick={() => setTab('upload')}
                        >
                            ⬆ Upload Transcript
                        </button>
                        <button
                            type="button"
                            className={`${styles.tab} ${tab === 'paste' ? styles.activeTab : ''}`}
                            onClick={() => setTab('paste')}
                        >
                            📋 Paste Transcript
                        </button>
                    </div>

                    {tab === 'upload' ? (
                        <div
                            className={styles.dropzone}
                            onClick={() => fileRef.current?.click()}
                        >
                            <input
                                ref={fileRef}
                                type="file"
                                accept=".txt,.vtt,.json"
                                style={{ display: 'none' }}
                                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                            />
                            {file ? (
                                <span className={styles.fileName}>📄 {file.name}</span>
                            ) : (
                                <>
                                    <div className={styles.dropzoneIcon}>⬆</div>
                                    <p>Click to upload .txt, .vtt, or .json</p>
                                    <p className={styles.dropzoneHint}>or skip and add later</p>
                                </>
                            )}
                        </div>
                    ) : (
                        <textarea
                            className={styles.textarea}
                            placeholder="Paste your transcript text here..."
                            rows={6}
                            value={pasteText}
                            onChange={(e) => setPasteText(e.target.value)}
                        />
                    )}

                    {(createMut.isError || errorMsg) && (
                        <p className={styles.errorText}>⚠️ {errorMsg || 'Failed to create meeting. Try again.'}</p>
                    )}

                    <div className={styles.actions}>
                        <button type="button" className={styles.cancelBtn} onClick={onClose}>
                            Cancel
                        </button>
                        <button
                            type="submit"
                            className={styles.submitBtn}
                            disabled={createMut.isPending || !title.trim()}
                        >
                            {createMut.isPending ? 'Creating…' : 'Create Meeting'}
                        </button>
                    </div>
                </form>
            </div>
        </div>
    );
}
