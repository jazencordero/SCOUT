from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class FounderProfile:
    name: str
    linkedin_url: Optional[str] = None
    email: Optional[str] = None
    location: Optional[str] = None
    current_role: Optional[str] = None
    archetype: Optional[str] = None  # Commercial / Technical / Domain
    one_line_thesis: Optional[str] = None
    key_signals: List[str] = field(default_factory=list)
    traction: Optional[str] = None
    fit_reason: Optional[str] = None
    source: Optional[str] = None
    outreach_idea: Optional[str] = None
    status: Optional[str] = None     # Not Contacted / Contacted / Warm / Declined / Interested
    priority: Optional[str] = None   # H / M / L
    score: Optional[float] = None
    notes: Optional[str] = None
