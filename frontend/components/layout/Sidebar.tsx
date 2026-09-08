'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import styles from './Sidebar.module.css';

const NavItem = ({ href, label, icon, badge, active, highlighted, disabled }: any) => (
    <Link
        href={href}
        onClick={disabled ? (e) => e.preventDefault() : undefined}
        className={`${styles.navItem} ${active ? styles.active : ''} ${highlighted ? styles.highlighted : ''}`}
        style={disabled ? { cursor: 'default' } : undefined}
    >
        <span className={styles.navIcon}>{icon}</span>
        <span className={styles.navLabel}>{label}</span>
        {badge && <span className={styles.navBadge}>{badge}</span>}
    </Link>
);

export default function Sidebar() {
    const pathname = usePathname();
    const isActive = (path: string) => path === '/' ? pathname === '/' : pathname.startsWith(path);

    return (
        <aside className={styles.sidebar}>
            <div className={styles.logo}>
                <div className={styles.avatar} style={{ backgroundColor: '#cc4b14', borderRadius: '4px' }}>A</div>
                <span className={styles.logoText}>Alice</span>
            </div>

            <nav className={styles.navScroll}>
                <div className={styles.navGroup}>
                    <NavItem href="/" label="Home" active={isActive('/')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>} />
                    <NavItem disabled href="/ask-ai" label="AskAI" active={isActive('/ask-ai')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#8b5cf6" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>} />
                </div>

                <div className={styles.navDivider}></div>

                <div className={styles.navGroup}>
                    <NavItem href="/meetings" label="Meetings" active={isActive('/meetings')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="23 7 16 12 23 17 23 7"></polygon><rect x="1" y="5" width="15" height="14" rx="2" ry="2"></rect></svg>} />
                    <NavItem disabled href="/tasks" label="Tasks" active={isActive('/tasks')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>} />
                    <NavItem disabled href="/ai-skills" label="AI Skills" active={isActive('/ai-skills')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>} />
                </div>

                <div className={styles.navDivider}></div>

                <div className={styles.navGroup}>
                    <NavItem disabled href="/analytics" label="Analytics" active={isActive('/analytics')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><line x1="18" y1="20" x2="18" y2="10"></line><line x1="12" y1="20" x2="12" y2="4"></line><line x1="6" y1="20" x2="6" y2="14"></line></svg>} />
                    <NavItem disabled href="/voice-agents" label="Voice Agents" active={isActive('/voice-agents')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"></rect><circle cx="12" cy="5" r="2"></circle><path d="M12 7v4"></path><line x1="8" y1="16" x2="8" y2="16"></line><line x1="16" y1="16" x2="16" y2="16"></line></svg>} />
                </div>

                <div className={styles.navDivider}></div>

                <div className={styles.navGroup}>
                    <NavItem disabled href="/upgrade" label="Upgrade" active={isActive('/upgrade')} badge="40% OFF" icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon></svg>} />
                </div>

                <div style={{ marginTop: 'auto', display: 'flex', flexDirection: 'column', gap: '8px' }}>
                    <NavItem disabled href="/email-assistant" label="Try Email Assistant" active={isActive('/email-assistant')} highlighted={true} icon={
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M22 19V5C22 3.9 21.1 3 20 3H4C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H20C21.1 21 22 20.1 22 19Z" fill="#F2F2F2" />
                            <path d="M12 14L2 7V5L12 12L22 5V7L12 14Z" fill="#EA4335" />
                            <path d="M22 5L12 12L2 5V19H4V8.5L12 14.5L20 8.5V19H22V5Z" fill="#34A853" />
                            <path d="M4 3L2 5V19H4V3Z" fill="#4285F4" />
                            <path d="M20 3L22 5V19H20V3Z" fill="#FBBC04" />
                        </svg>
                    } />

                    <div className={styles.navGroup}>
                        <NavItem disabled href="/integrations" label="Integrations" active={isActive('/integrations')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 12 12 17 22 12"></polyline><polyline points="2 17 12 22 22 17"></polyline></svg>} />
                        <NavItem disabled href="/settings" label="Settings" active={isActive('/settings')} icon={<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>} />
                    </div>
                </div>
            </nav>

            <div className={styles.sidebarFooter}>
                <div className={styles.userRow}>
                    <div className={styles.avatar}>A</div>
                    <div>
                        <div className={styles.userName}>Alice Admin</div>
                        <div className={styles.userEmail}>alice@lumen.local</div>
                    </div>
                </div>
            </div>
        </aside>
    );
}
