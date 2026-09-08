import io
from app.models.meeting import Meeting
from app.models.summary import Summary

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
except ImportError:
    pass

class PDFExportService:
    @staticmethod
    def generate_meeting_pdf(meeting: Meeting, summary: Summary = None, action_items: list = None, topics: list = None) -> io.BytesIO:
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
        
        styles = getSampleStyleSheet()
        title_style = styles['Heading1']
        title_style.textColor = colors.HexColor("#7A5AF8")
        
        h2_style = styles['Heading2']
        h2_style.textColor = colors.HexColor("#333333")
        
        body_style = styles['Normal']
        body_style.fontSize = 10
        body_style.leading = 14
        
        story = []
        
        # Title & Meta
        story.append(Paragraph(f"Meeting: {meeting.title}", title_style))
        story.append(Spacer(1, 10))
        story.append(Paragraph(f"Date: {meeting.meeting_date.strftime('%Y-%m-%d %H:%M:%S')}", body_style))
        story.append(Spacer(1, 20))
        
        # Summary Overview
        if summary and summary.overview:
            story.append(Paragraph("AI Summary", h2_style))
            story.append(Spacer(1, 10))
            story.append(Paragraph(summary.overview, body_style))
            story.append(Spacer(1, 20))
            
        # Topics
        if topics:
            story.append(Paragraph("Topics Covered", h2_style))
            story.append(Spacer(1, 10))
            for t in topics:
                story.append(Paragraph(f"• {t.title}", body_style))
            story.append(Spacer(1, 20))
            
        # Action Items
        if action_items:
            story.append(Paragraph("Action Items", h2_style))
            story.append(Spacer(1, 10))
            for ai in action_items:
                status = "[x]" if ai.is_completed else "[ ]"
                story.append(Paragraph(f"{status} {ai.text}", body_style))
            story.append(Spacer(1, 20))
            
        # Transcript
        if meeting.segments:
            story.append(Paragraph("Transcript", h2_style))
            story.append(Spacer(1, 10))
            for seg in meeting.segments:
                speaker = seg.speaker_label or "Unknown"
                text = f"<b>{speaker}:</b> {seg.text}"
                story.append(Paragraph(text, body_style))
                story.append(Spacer(1, 4))
                
        doc.build(story)
        buffer.seek(0)
        return buffer
