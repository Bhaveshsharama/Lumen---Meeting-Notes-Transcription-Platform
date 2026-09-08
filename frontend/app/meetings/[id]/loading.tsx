import styles from '../meetings.module.css';

export default function MeetingDetailLoading() {
    return (
        <div style={{ padding: '24px 32px' }}>
            <div style={{ height: 24, width: 280, background: '#e8e8f0', borderRadius: 6, marginBottom: 20 }} />
            <div style={{ display: 'grid', gridTemplateColumns: '60fr 40fr', gap: 24 }}>
                <div className={styles.skeleton} style={{ height: 500 }} />
                <div className={styles.skeleton} style={{ height: 500 }} />
            </div>
        </div>
    );
}
