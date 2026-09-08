import Link from 'next/link';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { deleteMeeting, type Meeting } from '@/lib/api';
import styles from './MeetingCard.module.css';

const AVATAR_COLORS = ['#7A5AF8', '#E85D8A', '#16A34A', '#F5A524', '#3B82F6'];

function formatDate(iso: string) {
    return new Date(iso).toLocaleDateString('en-US', {
        month: 'short', day: 'numeric', year: 'numeric',
    });
}

function formatDuration(secs: number) {
    if (!secs) return '—';
    const m = Math.floor(secs / 60);
    return `${m}m`;
}

interface Props {
    meeting: Meeting;
}

export default function MeetingCard({ meeting }: Props) {
    const qc = useQueryClient();
    const summary = (meeting.summary_overview && meeting.summary_overview.trim()) ||
        (meeting.description && meeting.description.trim()) ||
        'No summary available yet.';

    const deleteMut = useMutation({
        mutationFn: () => deleteMeeting(meeting.id),
        onSuccess: () => qc.invalidateQueries({ queryKey: ['meetings'] }),
    });

    const handleDelete = (e: React.MouseEvent) => {
        e.preventDefault();
        e.stopPropagation();
        if (confirm(`Are you sure you want to delete "${meeting.title}"?`)) {
            deleteMut.mutate();
        }
    };

    return (
        <Link href={`/meetings/${meeting.id}`} style={{ textDecoration: 'none' }}>
            <article className={styles.card}>
                <div className={styles.cardHeader}>
                    <h3 className={styles.title}>{meeting.title}</h3>
                    <button
                        className={styles.menuBtn}
                        onClick={handleDelete}
                        aria-label="Delete"
                        title="Delete Meeting"
                    >
                        🗑
                    </button>
                </div>

                <div className={styles.meta}>
                    <span className={styles.metaItem}>📅 {formatDate(meeting.meeting_date)}</span>
                    {meeting.duration_seconds > 0 && (
                        <span className={styles.metaItem}>⏱ {formatDuration(meeting.duration_seconds)}</span>
                    )}
                    <span className={styles.metaItem}>
                        👥 {meeting.participant_links.length} participants
                    </span>
                </div>

                <p className={styles.summary}>{summary}</p>

                <div className={styles.footer}>
                    <div className={styles.tags}>
                        {(meeting.tags || []).slice(0, 3).map((tag) => (
                            <span key={tag} className={styles.tag}>#{tag}</span>
                        ))}
                    </div>

                    <div className={styles.avatars}>
                        {meeting.participant_links.slice(0, 4).map((link, i) => (
                            <div
                                key={link.participant.id}
                                className={styles.avatarCircle}
                                title={link.participant.name}
                                style={{ background: AVATAR_COLORS[i % AVATAR_COLORS.length], zIndex: 10 - i }}
                            >
                                {link.participant.name.charAt(0).toUpperCase()}
                            </div>
                        ))}
                    </div>
                </div>
            </article>
        </Link>
    );
}
