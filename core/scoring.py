# core/scoring.py
from typing import List, Tuple

COMM_KEYWORDS = ["growth","sales","partnership","revenue","enterprise","gtm","arr","expansion","pipeline","commercial"]
TECH_KEYWORDS = ["cto","staff","principal","ml","machine learning","ai","infra","distributed","systems","kubernetes","k8s","open-source","oss","patent","phd","compiler"]
DOMAIN_KEYWORDS = ["director","head","gm","operations","compliance","risk","regulatory","clinical","healthcare","fintech","energy","manufacturing","logistics"]

def _keyword_score(text: str, keywords: List[str], base: float = 3.0, per_hit: float = 0.35, cap: float = 5.0) -> float:
    if not text:
        return base
    s = text.lower()
    hits = sum(1 for kw in keywords if kw in s)
    return min(cap, base + hits * per_hit)

def score_archetype(archetype: str, title_or_signals: str) -> Tuple[float, str]:
    """
    Returns (score, explanation)
    """
    a = (archetype or "Commercial").lower()
    if a == "technical":
        score = _keyword_score(title_or_signals, TECH_KEYWORDS, base=3.0, per_hit=0.4)
        why = "Technical signals (CTO/staff/principal, ML/infra, OSS, advanced systems)."
    elif a == "domain":
        score = _keyword_score(title_or_signals, DOMAIN_KEYWORDS, base=3.0, per_hit=0.35)
        why = "Domain leadership signals (Head/Director/GM in regulated or deep industries)."
    else:
        score = _keyword_score(title_or_signals, COMM_KEYWORDS, base=3.0, per_hit=0.35)
        why = "Commercial GTM signals (growth/sales/ARR/enterprise/partnerships)."
    return score, why
