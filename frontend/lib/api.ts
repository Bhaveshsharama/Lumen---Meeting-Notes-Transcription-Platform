import axios from 'axios';

const api = axios.create({
    baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
    headers: { 'Content-Type': 'application/json' },
});

// ─── Types ───────────────────────────────────────────────────────────────────

export interface Participant {
    id: number;
    name: string;
    email: string;
    avatar_url: string | null;
}

export interface ParticipantLink {
    participant: Participant;
    role: string;
}

export interface Meeting {
    id: number;
    title: string;
    meeting_date: string;
    description: string | null;
    tags: string[];
    video_url: string | null;
    audio_url: string | null;
    duration_seconds: number;
    created_at: string;
    updated_at: string;
    summary_overview?: string | null;
    participant_links: ParticipantLink[];
}

export interface MeetingsPage {
    items: Meeting[];
    total: number;
    page: number;
    page_size: number;
}

export interface TranscriptSegment {
    id: number;
    meeting_id: number;
    sequence: number;
    start_time: number;
    end_time: number;
    speaker_id: number | null;
    speaker_label: string | null;
    text: string;
}

export interface Topic {
    id: number;
    meeting_id: number;
    title: string;
    start_time: number;
}

export interface Summary {
    meeting_id: number;
    overview: string;
    generated_at: string;
    topics: Topic[];
}

export interface ActionItem {
    id: number;
    meeting_id: number;
    text: string;
    assignee_id: number | null;
    is_completed: boolean;
    created_at: string;
}

export interface MeetingCreate {
    title: string;
    meeting_date: string;
    description?: string;
    tags?: string[];
    participant_ids?: number[];
}

// ─── Meetings ─────────────────────────────────────────────────────────────────

export const getMeetings = (params: {
    q?: string;
    participant_id?: number;
    sort?: string;
    page?: number;
    page_size?: number;
    date_from?: string;
    date_to?: string;
}) => api.get<MeetingsPage>('/meetings', { params }).then((r) => r.data);

export const getMeeting = (id: number) =>
    api.get<Meeting>(`/meetings/${id}`).then((r) => r.data);

export const createMeeting = (data: MeetingCreate) =>
    api.post<Meeting>('/meetings', data).then((r) => r.data);

export const updateMeeting = (id: number, data: Partial<MeetingCreate>) =>
    api.patch<Meeting>(`/meetings/${id}`, data).then((r) => r.data);

export const deleteMeeting = (id: number) =>
    api.delete(`/meetings/${id}`).then((r) => r.data);

export const getParticipants = (q?: string) =>
    api.get<Participant[]>('/participants', { params: { q } }).then((r) => r.data);

// ─── Transcript ───────────────────────────────────────────────────────────────

export const getTranscript = (meetingId: number) =>
    api.get<TranscriptSegment[]>(`/meetings/${meetingId}/transcript`).then((r) => r.data);

export const uploadTranscript = (meetingId: number, file: File) => {
    const form = new FormData();
    form.append('file', file);
    return api.post(`/meetings/${meetingId}/transcript/upload`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
    }).then((r) => r.data);
};

export const pasteTranscript = (meetingId: number, text: string, format: string) =>
    api.post(`/meetings/${meetingId}/transcript/paste`, { text, format }).then((r) => r.data);

export const searchTranscript = (meetingId: number, q: string) =>
    api.get<TranscriptSegment[]>(`/meetings/${meetingId}/transcript/search`, { params: { q } }).then((r) => r.data);

// ─── Summary ──────────────────────────────────────────────────────────────────

export const getSummary = (meetingId: number) =>
    api.get<Summary>(`/meetings/${meetingId}/summary`).then((r) => r.data);

export const generateSummary = (meetingId: number) =>
    api.post<Summary>(`/meetings/${meetingId}/summary/generate`, { source: 'llm' }).then((r) => r.data);

// ─── Action Items ─────────────────────────────────────────────────────────────

export const getActionItems = (meetingId: number) =>
    api.get<ActionItem[]>(`/meetings/${meetingId}/action-items`).then((r) => r.data);

export const exportMeetingPDF = (meetingId: number) => {
    const base = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';
    window.location.href = `${base}/meetings/${meetingId}/export/pdf`;
};

export const toggleActionItem = (id: number, is_completed: boolean) =>
    api.patch<ActionItem>(`/action-items/${id}`, { is_completed }).then((r) => r.data);

export const createActionItem = (meetingId: number, text: string) =>
    api.post<ActionItem>(`/meetings/${meetingId}/action-items`, { text }).then((r) => r.data);

export const updateActionItem = (id: number, data: { text?: string; assignee_id?: number | null; is_completed?: boolean }) =>
    api.patch<ActionItem>(`/action-items/${id}`, data).then((r) => r.data);

export const deleteActionItem = (id: number) =>
    api.delete(`/action-items/${id}`).then((r) => r.data);

export default api;
