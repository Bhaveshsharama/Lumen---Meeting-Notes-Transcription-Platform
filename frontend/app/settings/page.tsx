import styles from './settings.module.css';

const cards = [
    {
        icon: '🤖',
        title: 'Live Bot',
        description: 'Automatically join and record meetings from Google Meet, Zoom, or Teams.',
        status: 'Coming Soon',
    },
    {
        icon: '🔗',
        title: 'Integrations',
        description: 'Connect your calendar, Slack, and other tools to streamline your workflow.',
        status: 'Coming Soon',
    },
    {
        icon: '👥',
        title: 'Team Sharing',
        description: 'Share meeting transcripts and summaries with your team members.',
        status: 'Coming Soon',
    },
];

export default function SettingsPage() {
    return (
        <div className={styles.page}>
            <div className={styles.header}>
                <h1 className={styles.title}>Settings</h1>
                <p className={styles.subtitle}>Manage your workspace preferences.</p>
            </div>

            <div className={styles.grid}>
                {cards.map((card) => (
                    <div key={card.title} className={styles.card}>
                        <div className={styles.cardIcon}>{card.icon}</div>
                        <h3 className={styles.cardTitle}>{card.title}</h3>
                        <p className={styles.cardDesc}>{card.description}</p>
                        <span className={styles.badge}>{card.status}</span>
                    </div>
                ))}
            </div>
        </div>
    );
}
