'use client';

export default function MeetingsError({ error, reset }: { error: Error; reset: () => void }) {
    return (
        <div style={{ padding: 32, textAlign: 'center' }}>
            <p style={{ color: 'var(--danger)', marginBottom: 16 }}>
                ⚠️ Could not load meetings: {error.message}
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
                }}
            >
                Retry
            </button>
        </div>
    );
}
