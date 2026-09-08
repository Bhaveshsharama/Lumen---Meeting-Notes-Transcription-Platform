import Link from 'next/link';

export default function TasksPage() {
    return (
        <div style={{ padding: 32 }}>
            <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 8 }}>Tasks</h1>
            <p style={{ color: 'var(--text-secondary)', marginBottom: 24 }}>
                All action items across your meetings.
            </p>
            <p style={{ color: 'var(--text-secondary)', fontSize: 13 }}>
                Open a{' '}
                <Link href="/meetings" style={{ color: 'var(--brand-primary)' }}>meeting</Link>{' '}
                to view and manage action items from the detail page.
            </p>
        </div>
    );
}
