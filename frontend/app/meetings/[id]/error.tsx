'use client';

export default function MeetingDetailError({ error, reset }: { error: Error; reset: () => void }) {
    return (
        <div style={{ padding: 48, textAlign: 'center' }}>
            <p style={{ color: 'var(--danger)', marginBottom: 16, fontSize: 14 }}>
                ⚠️ Could not load this meeting: {error.message}
            </p>
            <button
                onClick={reset}
                style={{
                    padding: '8px 20px',
                    background: 'var(--brand-primary)',
                    color: 'white',
                    border: 'none',
                    borderRadius: 'var(--radius-md)',
                    cursor: 'pointer',
                    fontWeight: 600,
                    fontSize: 13,
                }}
            >
                Retry
            </button>
        </div>
    );
}
