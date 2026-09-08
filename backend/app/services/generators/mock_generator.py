"""
services/generators/mock_generator.py — Rule-based mock summary generator.

Produces unique summaries by analysing keywords in the transcript text,
so each pre-seeded meeting gets a different, relevant summary.
"""
from typing import Dict, Any
from .base import SummaryGenerator


# Map of keyword → tailored summary payload
_SUMMARIES = [
    {
        "keywords": ["design", "component", "ui", "figma", "token", "handoff"],
        "overview": "The design and engineering teams completed the hand-off of the updated Design System. The discussion covered new component tokens, color palette revisions, and the deprecation of legacy button variants. Alice walked the team through Figma specifications and annotated interaction states for hover, focus, and disabled. Charlie raised concerns about mobile breakpoints for the card grid, and the team agreed to schedule a follow-up review once the responsive spec is finalized next sprint.",
        "topics": [
            {"title": "Component Token Review", "start_time": 0.0},
            {"title": "Color Palette Changes", "start_time": 95.0},
            {"title": "Mobile Breakpoint Discussion", "start_time": 220.0},
        ],
        "action_items": [
            {"text": "Finalize responsive spec for card grid", "source_timestamp": 225.0},
            {"text": "Deprecate legacy button variants in Storybook", "source_timestamp": 310.0},
        ],
    },
    {
        "keywords": ["planning", "roadmap", "okr", "quarter", "q3", "strategy", "goal"],
        "overview": "The leadership and product team aligned on the Q3 OKRs and product roadmap priorities. The primary focus for the quarter is accelerating the self-serve onboarding funnel and reducing time-to-value for new users. Bob presented data showing a 34% drop-off at the payment step, prompting a decision to A/B test a simplified checkout flow. The team also agreed to defer the enterprise SSO feature to Q4 given current engineering capacity constraints.",
        "topics": [
            {"title": "Q3 OKR Alignment", "start_time": 0.0},
            {"title": "Onboarding Funnel Analysis", "start_time": 140.0},
            {"title": "Enterprise SSO Deferral", "start_time": 320.0},
        ],
        "action_items": [
            {"text": "Set up A/B test for simplified checkout", "source_timestamp": 175.0},
            {"text": "Update roadmap doc with deferred SSO timeline", "source_timestamp": 330.0},
        ],
    },
    {
        "keywords": ["architecture", "backend", "solid", "service", "repository", "api", "dependency"],
        "overview": "The backend architecture review covered the current service layer design and its alignment with SOLID principles, specifically focusing on the Dependency Inversion and Open-Closed Principles. Bob demonstrated the new repository abstraction pattern which decouples business logic from raw SQLAlchemy queries. Charlie flagged a potential N+1 query issue in the meeting list endpoint. The team decided to adopt joinedload across all list queries and create a shared ADR documenting the pattern.",
        "topics": [
            {"title": "Repository Pattern Overview", "start_time": 0.0},
            {"title": "N+1 Query Issue", "start_time": 185.0},
            {"title": "ADR Decision", "start_time": 290.0},
        ],
        "action_items": [
            {"text": "Add joinedload to all list repository queries", "source_timestamp": 195.0},
            {"text": "Write ADR for repository abstraction pattern", "source_timestamp": 305.0},
        ],
    },
    {
        "keywords": ["incident", "hotfix", "prod", "bug", "outage", "fix", "triage", "urgent"],
        "overview": "The team convened for an emergency hotfix triage following a production incident that began at 02:14 UTC. The root cause was identified as a missing database index on the sessions table, causing query timeout cascades under peak load. Alice coordinated the rollback procedure while Bob deployed the emergency index migration to staging for validation. Charlie handled external communications, drafting a status page update and a preliminary customer-facing post-mortem. The patch was confirmed stable and promoted to production at 04:50 UTC.",
        "topics": [
            {"title": "Incident Timeline Review", "start_time": 0.0},
            {"title": "Root Cause: Missing DB Index", "start_time": 110.0},
            {"title": "Patch Validation & Deploy", "start_time": 240.0},
        ],
        "action_items": [
            {"text": "Write full post-mortem document", "source_timestamp": 250.0},
            {"text": "Audit all other tables for missing indexes", "source_timestamp": 310.0},
        ],
    },
    {
        "keywords": ["sync", "engineering", "weekly", "sprint", "standup", "blocker", "release"],
        "overview": "The weekly engineering sync covered sprint velocity, outstanding blockers, and the upcoming v2.0 release readiness. Alice noted that the caching layer implementation is on track but the Redis cluster provisioning is pending DevOps approval, which is blocking final integration tests. Bob raised a concern that two critical bug fixes are still in code review and may miss the release window. The team agreed to prioritize review bandwidth this week and push for a feature freeze by Thursday.",
        "topics": [
            {"title": "Sprint Velocity Review", "start_time": 0.0},
            {"title": "Redis Provisioning Blocker", "start_time": 130.0},
            {"title": "Release Readiness", "start_time": 270.0},
        ],
        "action_items": [
            {"text": "Escalate Redis provisioning request to DevOps", "source_timestamp": 145.0},
            {"text": "Clear code review queue before Thursday", "source_timestamp": 280.0},
        ],
    },
]

_DEFAULT = {
    "overview": "The team held a productive meeting covering key project updates, current blockers, and alignment on next steps. Participants shared progress across multiple workstreams and agreed on a set of action items to drive momentum into the next sprint cycle.",
    "topics": [
        {"title": "Project Updates", "start_time": 0.0},
        {"title": "Blockers & Risks", "start_time": 120.0},
        {"title": "Next Steps", "start_time": 250.0},
    ],
    "action_items": [
        {"text": "Send meeting notes to stakeholders", "source_timestamp": 260.0},
    ],
}


class MockSummaryGenerator(SummaryGenerator):
    def generate(self, transcript_text: str) -> Dict[str, Any]:
        lower = transcript_text.lower()
        for summary in _SUMMARIES:
            if any(kw in lower for kw in summary["keywords"]):
                result = dict(summary)
                del result["keywords"]
                return result
        return _DEFAULT
