'use client';
import { useState, useRef, useEffect } from 'react';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { updateMeeting, getParticipants, deleteMeeting, exportMeetingPDF, type Meeting } from '@/lib/api';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import styles from './MeetingHeader.module.css';

export default function MeetingHeader({ meeting }: { meeting: Meeting }) {
    const qc = useQueryClient();
    const router = useRouter();

    const [isEditingTitle, setIsEditingTitle] = useState(false);
    const [titleVal, setTitleVal] = useState(meeting.title);

    const [showAddParticipant, setShowAddParticipant] = useState(false);
    const [participantQ, setParticipantQ] = useState('');

    const titleInputRef = useRef<HTMLInputElement>(null);

    // Queries & Mutations
    const { data: searchResults = [] } = useQuery({
        queryKey: ['participants', participantQ],
        queryFn: () => getParticipants(participantQ),
        enabled: showAddParticipant,
    });

    const updateMut = useMutation({
        mutationFn: (data: any) => updateMeeting(meeting.id, data),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['meeting', meeting.id] });
            qc.invalidateQueries({ queryKey: ['meetings'] });
        }
    });

    const delMut = useMutation({
        mutationFn: () => deleteMeeting(meeting.id),
        onSuccess: () => {
            qc.invalidateQueries({ queryKey: ['meetings'] });
            router.push('/meetings');
        }
    });

    useEffect(() => {
        if (isEditingTitle && titleInputRef.current) {
            titleInputRef.current.focus();
        }
    }, [isEditingTitle]);

    const handleTitleSave = () => {
        setIsEditingTitle(false);
        if (titleVal.trim() !== meeting.title && titleVal.trim() !== '') {
            updateMut.mutate({ title: titleVal.trim() });
        } else {
            setTitleVal(meeting.title);
        }
    };

    const handleRemoveParticipant = (pId: number) => {
        const currentIds = meeting.participant_links.map(l => l.participant.id);
        const newIds = currentIds.filter(id => id !== pId);
        updateMut.mutate({ participant_ids: newIds });
    };

    const handleAddParticipant = (pId: number) => {
        const currentIds = meeting.participant_links.map(l => l.participant.id);
        if (!currentIds.includes(pId)) {
            updateMut.mutate({ participant_ids: [...currentIds, pId] });
        }
        setShowAddParticipant(false);
        setParticipantQ('');
    };

    return (
        <div className={styles.headerContainer}>
            <div className={styles.breadcrumb}>
                <Link href="/meetings" className={styles.breadcrumbLink}>← Meetings</Link>
                <span className={styles.sep}>/</span>

                {isEditingTitle ? (
                    <input
                        ref={titleInputRef}
                        className={styles.titleInput}
                        value={titleVal}
                        onChange={e => setTitleVal(e.target.value)}
                        onBlur={handleTitleSave}
                        onKeyDown={e => {
                            if (e.key === 'Enter') handleTitleSave();
                            if (e.key === 'Escape') {
                                setTitleVal(meeting.title);
                                setIsEditingTitle(false);
                            }
                        }}
                    />
                ) : (
                    <span
                        className={styles.breadcrumbCurrent}
                        onClick={() => setIsEditingTitle(true)}
                        title="Click to edit title"
                    >
                        {meeting.title}
                        <span className={styles.editIcon}>✎</span>
                    </span>
                )}
            </div>

            <div className={styles.actionsBox}>
                <div className={styles.participants}>
                    {meeting.participant_links.map(link => (
                        <div key={link.participant.id} className={styles.participantAvatarGroup}>
                            <div className={styles.avatar} title={link.participant.name}>
                                {link.participant.name.charAt(0).toUpperCase()}
                            </div>
                            <button
                                className={styles.removeParticipantBtn}
                                onClick={() => handleRemoveParticipant(link.participant.id)}
                                title={`Remove ${link.participant.name}`}
                            >×</button>
                        </div>
                    ))}

                    <div className={styles.addParticipantWrapper}>
                        <button
                            className={styles.addParticipantBtn}
                            onClick={() => setShowAddParticipant(!showAddParticipant)}
                            title="Add participant"
                        >
                            +
                        </button>
                        {showAddParticipant && (
                            <div className={styles.dropdown}>
                                <input
                                    autoFocus
                                    placeholder="Search..."
                                    value={participantQ}
                                    onChange={e => setParticipantQ(e.target.value)}
                                    className={styles.dropdownInput}
                                />
                                <div className={styles.dropdownList}>
                                    {searchResults.map((p: any) => (
                                        <div
                                            key={p.id}
                                            className={styles.dropdownItem}
                                            onClick={() => handleAddParticipant(p.id)}
                                        >
                                            <div className={styles.dropdownItemAvatar}>{p.name.charAt(0).toUpperCase()}</div>
                                            <div className={styles.dropdownItemInfo}>
                                                <span className={styles.dropdownItemName}>{p.name}</span>
                                                <span className={styles.dropdownItemEmail}>{p.email}</span>
                                            </div>
                                        </div>
                                    ))}
                                    {searchResults.length === 0 && <div className={styles.dropdownEmpty}>No users found.</div>}
                                </div>
                            </div>
                        )}
                    </div>
                </div>

                <div className={styles.divider} />

                <button
                    className={styles.deleteBtn}
                    onClick={() => exportMeetingPDF(meeting.id)}
                    style={{ background: 'transparent', border: '1px solid var(--border-light)', color: 'var(--text-secondary)', padding: '6px 12px', borderRadius: '6px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontSize: 13 }}
                >
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                        <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path>
                        <polyline points="7 10 12 15 17 10"></polyline>
                        <line x1="12" y1="15" x2="12" y2="3"></line>
                    </svg>
                    Export PDF
                </button>

                <button
                    className={styles.deleteBtn}
                    onClick={() => { if (confirm('Delete this meeting?')) delMut.mutate(); }}
                >
                    🗑 Delete
                </button>
            </div>
        </div>
    );
}
