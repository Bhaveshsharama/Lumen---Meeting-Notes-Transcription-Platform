import os
import sys
from datetime import datetime, timedelta

# Hack to allow running directly from project root via python -m app.seed_loader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.db.session import engine, SessionLocal
from app.models.base import Base

# Services & Repositories
from app.repositories.meeting_repository import MeetingRepository
from app.repositories.transcript_repository import TranscriptRepository
from app.repositories.summary_repository import SummaryRepository
from app.repositories.action_item_repository import ActionItemRepository
from app.services.generators.base import SummaryGenerator
from app.services.generators.mock_generator import MockSummaryGenerator
from app.models.user import User

from app.services.meeting_service import MeetingService
from app.services.transcript_service import TranscriptService
from app.services.summary_service import SummaryService

def main():
    print("[1/5] Dropping and re-creating all database tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("[2/5] Connecting to database...")
    db = SessionLocal()

    try:
        # 1. Setup DI manually for the script
        meeting_repo = MeetingRepository(db)
        transcript_repo = TranscriptRepository(db)
        summary_repo = SummaryRepository(db)
        action_item_repo = ActionItemRepository(db)
        
        mock_generator = MockSummaryGenerator()
        
        meeting_service = MeetingService(meeting_repo, db)
        transcript_service = TranscriptService(transcript_repo, db)
        summary_service = SummaryService(summary_repo, transcript_repo, action_item_repo, mock_generator, db)

        print("[2.5] Seeding default owner user...")
        demo_user = User(email="demo@fireflies-clone.local", name="Demo User")
        db.add(demo_user)
        db.commit()
        db.refresh(demo_user)

        # 2. Pool of participants
        print("[3/5] Seeding participant pool...")
        participants_data = [
            {"name": "Alice Admin", "email": "alice@fireflies-clone.local"},
            {"name": "Bob Backend", "email": "bob@fireflies-clone.local"},
            {"name": "Charlie Client", "email": "charlie@fireflies-clone.local"}
        ]
        
        p_ids = []
        for pdata in participants_data:
            p = meeting_service.create_participant(pdata)
            p_ids.append(p.id)
            
        alice_id, bob_id, charlie_id = p_ids

        # 3. Skip reading the single transcript file here, we read it in the loop
        print("[4/5] Preparing meetings blueprints...")

        # 4. Create multiple meetings for dashboard
        meetings_blueprint = [
            {
                "title": "Weekly Engineering Sync",
                "description": "Discussing caching layer and 2.0 release blockers.",
                "meeting_date": datetime.now() - timedelta(days=2),
                "tags": ["engineering", "sync"],
                "participant_ids": [alice_id, bob_id, charlie_id],
                "vtt_file": "sample_transcript.vtt"
            },
            {
                "title": "Design System Hand-off",
                "description": "Reviewing standard components.",
                "meeting_date": datetime.now() - timedelta(days=5),
                "tags": ["design"],
                "participant_ids": [alice_id, charlie_id],
                "vtt_file": "transcript_design.vtt"
            },
            {
                "title": "Q3 Planning & Roadmaps",
                "description": "Finalizing the OKRs.",
                "meeting_date": datetime.now() - timedelta(days=12),
                "tags": ["planning", "strategy"],
                "participant_ids": [alice_id, bob_id],
                "vtt_file": "transcript_retro.vtt"
            },
            {
                "title": "Backend Architecture Review",
                "description": "Deep dive into solid principles and DI.",
                "meeting_date": datetime.now() - timedelta(days=20),
                "tags": ["engineering", "architecture"],
                "participant_ids": [bob_id, charlie_id],
                "vtt_file": "transcript_arch.vtt"
            },
            {
                "title": "Urgent Hotfix Triage",
                "description": "Addressing the prod incident.",
                "meeting_date": datetime.now() - timedelta(hours=5),
                "tags": ["incident", "engineering"],
                "participant_ids": [alice_id, bob_id, charlie_id],
                "vtt_file": "transcript_qa.vtt"
            }
        ]
        
        print("[5/5] Executing service layer simulation...")
        
        for data in meetings_blueprint:
            # Use a fresh session per meeting so a failure on one doesn't break others
            meeting_db = SessionLocal()
            try:
                m_repo = MeetingRepository(meeting_db)
                t_repo = TranscriptRepository(meeting_db)
                s_repo = SummaryRepository(meeting_db)
                ai_repo = ActionItemRepository(meeting_db)
                m_svc = MeetingService(m_repo, meeting_db)
                t_svc = TranscriptService(t_repo, meeting_db)
                s_svc = SummaryService(s_repo, t_repo, ai_repo, MockSummaryGenerator(), meeting_db)

                data["owner_id"] = demo_user.id
                vtt_filename = data.pop("vtt_file")
                vtt_path = os.path.join(os.path.dirname(__file__), "seed_data", vtt_filename)
                with open(vtt_path, "rb") as f:
                    vtt_bytes = f.read()

                meeting = m_svc.create_meeting(data)
                print(f"   Created meeting: {meeting.title} (ID: {meeting.id})")
                
                t_svc.ingest(meeting.id, vtt_bytes, format="vtt")
                s_svc.generate_summary(meeting.id)
                print(f"   Summary generated for: {meeting.title}")

            except Exception as e:
                print(f"   ERROR for meeting '{data.get('title', '?')}': {e}")
                meeting_db.rollback()
                raise e
            finally:
                meeting_db.close()

        print("\nSUCCESS: Seed completed successfully! Dashboard is ready.")

    except Exception as e:
        print(f"\nERROR: Seeding failed: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    main()
