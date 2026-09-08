import Link from 'next/link';

export default function MeetingNotFound() {
    return (
        <div style={{ padding: 64, textAlign: 'center' }}>
            <div style={{ fontSize: 48, marginBottom: 16 }}>🔍</div>
            <h2 style={{ fontSize: 20, fontWeight: 700, marginBottom: 8, color: 'var(--text-primary)' }}>
                Meeting not found
            </h2>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 24, fontSize: 14 }}>
                This meeting may have been deleted or the link is incorrect.
            </p>
            <Link
                href="/meetings"
                style={{
                    display: 'inline-block',
                    padding: '9px 20px',
                    background: 'var(--brand-primary)',
                    color: 'white',
                    borderRadius: 'var(--radius-md)',
                    fontWeight: 600,
                    fontSize: 13,
                }}
            >
                ← Back to Meetings
            </Link>
        </div>
    );
}
