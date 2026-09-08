import styles from './meetings.module.css';

export default function MeetingsLoading() {
    return (
        <div className={styles.page}>
            <div className={styles.header}>
                <div>
                    <div style={{ height: 28, width: 120, background: '#e8e8f0', borderRadius: 6, marginBottom: 8 }} />
                    <div style={{ height: 16, width: 80, background: '#f0f0f8', borderRadius: 4 }} />
                </div>
            </div>
            <div className={styles.grid}>
                {[...Array(4)].map((_, i) => (
                    <div key={i} className={styles.skeleton} />
                ))}
            </div>
        </div>
    );
}
