'use client';
import { useState } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import NewMeetingModal from '@/components/meetings/NewMeetingModal';
import styles from './MeetingsSidebar.module.css';

interface MeetingsSidebarProps {
    activeFilter: 'my' | 'all';
    onFilterChange: (f: 'my' | 'all') => void;
}

export default function MeetingsSidebar({ activeFilter, onFilterChange }: MeetingsSidebarProps) {
    const [showUploadModal, setShowUploadModal] = useState(false);

    return (
        <aside className={styles.sidebar}>
            <nav className={styles.nav}>
                <button
                    className={`${styles.navItem} ${activeFilter === 'my' ? styles.active : ''}`}
                    onClick={() => onFilterChange('my')}
                >
                    <span className={styles.navIcon}>#</span>
                    My Meetings
                </button>
                <button
                    className={`${styles.navItem} ${activeFilter === 'all' ? styles.active : ''}`}
                    onClick={() => onFilterChange('all')}
                >
                    <svg className={styles.navIcon} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z" /></svg>
                    All Meetings
                </button>
                <button className={styles.navItem} disabled style={{ opacity: 0.6 }}>
                    <svg className={styles.navIcon} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" /><path d="M19 10v2a7 7 0 0 1-14 0v-2" /><line x1="12" y1="19" x2="12" y2="22" /></svg>
                    Voice Agent Meetings (Coming Soon)
                </button>
                <button className={styles.navItem} onClick={() => setShowUploadModal(true)}>
                    <svg className={styles.navIcon} width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" /><polyline points="17 8 12 3 7 8" /><line x1="12" y1="3" x2="12" y2="15" /></svg>
                    Uploads
                </button>
            </nav>



            {showUploadModal && <NewMeetingModal onClose={() => setShowUploadModal(false)} />}
        </aside >
    );
}
