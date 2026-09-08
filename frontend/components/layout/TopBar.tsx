'use client';
import { useRouter } from 'next/navigation';
import styles from './TopBar.module.css';

interface TopBarProps {
    onNewMeeting?: () => void;
}

export default function TopBar({ onNewMeeting }: TopBarProps) {
    const router = useRouter();

    const handleSearch = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === 'Enter') {
            const q = (e.target as HTMLInputElement).value.trim();
            if (q) router.push(`/meetings?q=${encodeURIComponent(q)}`);
        }
    };

    return (
        <header className={styles.topbar}>
            <div className={styles.left}>
                <h1 className={styles.pageTitle}>Home</h1>
            </div>

            <div className={styles.center}>
                <div className={styles.searchWrapper}>
                    <span className={styles.searchIcon}>🔍</span>
                    <input
                        id="global-search"
                        type="text"
                        className={styles.searchInput}
                        placeholder="Search by title or keyword"
                        onKeyDown={handleSearch}
                    />
                    <span className={styles.kbdHint}>Ctrl + K</span>
                </div>
            </div>

            <div className={styles.right}>
                <div className={styles.freeBadge}>
                    <span className={styles.freeIcon}>3</span>
                    Free meetings
                </div>
                <div className={styles.bellWrapper}>
                    <button className={styles.iconBtn} aria-label="Notifications">🔔</button>
                    <span className={styles.redDot}></span>
                </div>
                <button
                    id="new-meeting-btn"
                    className={styles.captureBtn}
                    onClick={onNewMeeting}
                >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginRight: '6px' }}><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>
                    Capture
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ marginLeft: '6px', opacity: 0.8 }}><polyline points="6 9 12 15 18 9"></polyline></svg>
                </button>
            </div>
        </header>
    );
}
