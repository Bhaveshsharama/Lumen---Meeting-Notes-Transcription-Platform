'use client';
import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { getMeetings } from '@/lib/api';
import MeetingCard from '@/components/meetings/MeetingCard';
import NewMeetingModal from '@/components/meetings/NewMeetingModal';
import styles from './home.module.css';

const quickStartCards = [
  {
    id: 'schedule',
    icon: '📅',
    title: 'Schedule Meeting',
    bg: '#fdf2f8', // pink-50
    onClick: () => { },
  },
  {
    id: 'upload',
    icon: '⬆',
    title: 'Upload File',
    bg: '#f0fdf4', // green-50
    onClick: (openModal: () => void) => openModal(),
  },
  {
    id: 'capture',
    icon: '+',
    title: 'Capture Meeting',
    bg: '#f5f3ff', // purple-50
    onClick: () => { },
  },
];

export default function HomePage() {
  const [showModal, setShowModal] = useState(false);

  const { data } = useQuery({
    queryKey: ['meetings', '', 'recent', 1],
    queryFn: () => getMeetings({ sort: 'recent', page: 1, page_size: 3 }),
  });

  const recentMeetings = data?.items ?? [];

  return (
    <div className={styles.page}>
      {/* Welcome Hero */}
      <div className={styles.hero}>
        <div className={styles.heroText}>
          <h1 className={styles.heroTitle}>Welcome Aboard, Alice!</h1>
          <p className={styles.heroSubtitle}>
            Lumen is now ready to automate your meetings<br />
            and integrate with your favorite tools.
          </p>
        </div>
      </div>

      {/* Quick Start */}
      <section className={styles.section}>
        <h2 className={styles.sectionTitle}>Quick Start</h2>
        <p className={styles.sectionSubtitle}>Capture your first meeting or upload a recording to see Lumen in action.</p>
        <div className={styles.quickGrid}>
          {quickStartCards.map((card) => (
            <button
              key={card.id}
              id={`quickstart-${card.id}`}
              className={styles.quickCard}
              style={{ '--card-bg': card.bg } as React.CSSProperties}
              onClick={() => card.onClick(() => setShowModal(true))}
            >
              <div className={styles.quickIcon}>{card.icon}</div>
              <div className={styles.quickTitle}>{card.title}</div>
              <span className={styles.quickArrow}>›</span>
            </button>
          ))}
        </div>
      </section>

      {/* Tabs */}
      <div className={styles.tabsRow}>
        <div className={styles.tabsGroup}>
          <button className={`${styles.tabBtn} ${styles.tabActive}`}>Recent</button>
          <button className={styles.tabBtn}>Upcoming</button>
          <button className={styles.tabBtn}>AI Feed</button>
        </div>
        <button className={styles.settingsBtn}>⚙ Settings</button>
      </div>

      {/* Recent Meetings */}
      {recentMeetings.length > 0 && (
        <section className={styles.section}>
          <div className={styles.recentGrid}>
            {recentMeetings.map((m) => <MeetingCard key={m.id} meeting={m} />)}
          </div>
        </section>
      )}

      {showModal && <NewMeetingModal onClose={() => setShowModal(false)} />}
    </div>
  );
}
