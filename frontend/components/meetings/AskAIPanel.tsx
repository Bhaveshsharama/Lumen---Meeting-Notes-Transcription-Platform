'use client';
import { useState } from 'react';
import styles from './AskAIPanel.module.css';

export default function AskAIPanel() {
    const [showConnectCard, setShowConnectCard] = useState(true);
    const [inputValue, setInputValue] = useState('');

    return (
        <aside className={styles.panel}>
            <div className={styles.comingSoonOverlay}>
                <span className={styles.comingSoonBadge}>Coming Soon</span>
            </div>

            {/* Header */}
            <div className={styles.header}>
                <div className={styles.headerLeft}>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#7a5af8" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
                    <span className={styles.headerTitle}>Ask AI</span>
                </div>
                <div className={styles.headerActions}>
                    <button className={styles.iconBtn} title="Chat">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg>
                    </button>
                    <button className={styles.iconBtn} title="New">
                        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
                    </button>
                </div>
            </div>

            {/* Connect Card */}
            {showConnectCard && (
                <div className={styles.connectCard}>
                    <div className={styles.connectCardContent}>
                        <div className={styles.connectIcons}>
                            <span className={styles.integrationIcon}>Sl</span>
                            <span className={styles.integrationIcon} style={{ background: '#ea4335' }}>G</span>
                        </div>
                        <div className={styles.connectText}>
                            <p><strong>Connect Slack and Gmail</strong> — get answers with full context.</p>
                            <button className={styles.connectLink}>Connect →</button>
                        </div>
                    </div>
                    <button className={styles.closeBtn} onClick={() => setShowConnectCard(false)}>
                        <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>
                    </button>
                </div>
            )}

            {/* Greeting */}
            <div className={styles.greeting}>
                <div className={styles.greetingStar}>
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#7a5af8" strokeWidth="2"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
                </div>
                <h3 className={styles.greetingText}>Hi Alice!<br />Get ready for your meeting</h3>
                <div className={styles.channelBadge}># My Meetings</div>
            </div>

            {/* Quick prompts */}
            <div className={styles.quickPrompts}>
                <button className={styles.promptBtn}>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="#7a5af8" stroke="none"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" /></svg>
                    Summarize insights from last week
                </button>
                <button className={styles.promptBtn}>
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#7a5af8" strokeWidth="2"><line x1="8" y1="6" x2="21" y2="6" /><line x1="8" y1="12" x2="21" y2="12" /><line x1="8" y1="18" x2="21" y2="18" /><line x1="3" y1="6" x2="3.01" y2="6" /><line x1="3" y1="12" x2="3.01" y2="12" /><line x1="3" y1="18" x2="3.01" y2="18" /></svg>
                    List pending action items
                </button>
            </div>

            <div className={styles.spacer} />

            {/* Input */}
            <div className={styles.inputArea}>
                <div className={styles.chatInput}>
                    <input
                        type="text"
                        className={styles.messageInput}
                        placeholder="Ask anything. Type / to run AI skills."
                        value={inputValue}
                        onChange={(e) => setInputValue(e.target.value)}
                    />
                    <div className={styles.inputActions}>
                        <button className={styles.inputIconBtn}>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><line x1="12" y1="5" x2="12" y2="19" /><line x1="5" y1="12" x2="19" y2="12" /></svg>
                        </button>
                        <button className={styles.inputIconBtn}>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect x="2" y="3" width="20" height="14" rx="2" /><path d="M8 21h8" /><path d="M12 17v4" /></svg>
                        </button>
                        <button className={styles.inputIconBtn}>
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z" /><path d="M19 10v2a7 7 0 0 1-14 0v-2" /></svg>
                        </button>
                        <button
                            className={styles.sendBtn}
                            disabled={!inputValue.trim()}
                        >
                            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5"><line x1="22" y1="2" x2="11" y2="13" /><polygon points="22 2 15 22 11 13 2 9 22 2" /></svg>
                        </button>
                    </div>
                </div>
                <p className={styles.disclaimer}>AI can make mistakes. Verify important information.</p>
            </div>
        </aside>
    );
}
