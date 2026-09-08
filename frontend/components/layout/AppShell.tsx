'use client';
import { useState } from 'react';
import Sidebar from './Sidebar';
import TopBar from './TopBar';
import NewMeetingModal from '@/components/meetings/NewMeetingModal';
import styles from './AppShell.module.css';

export default function AppShell({ children }: { children: React.ReactNode }) {
    const [showModal, setShowModal] = useState(false);

    return (
        <div className={styles.shell}>
            <Sidebar />
            <div className={styles.main}>
                <TopBar onNewMeeting={() => setShowModal(true)} />
                <main className={styles.content}>{children}</main>
            </div>
            {showModal && <NewMeetingModal onClose={() => setShowModal(false)} />}
        </div>
    );
}
