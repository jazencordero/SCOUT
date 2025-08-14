# core/workflow.py
from typing import List
from data.models import FounderProfile
from data.scrapers import scrape_by_archetype
from core.enrichment import enrich_founder
from core.scoring import score_archetype

def generate_founders(limit: int = 20, live: bool = False, archetype: str = "Commercial", recall_mode: str = "balanced") -> List[FounderProfile]:
    # live flag now maps to using SERP (when key present); we always call archetype scraper
    leads = scrape_by_archetype(archetype=archetype, limit=limit, recall_mode=recall_mode)

    enriched: List[FounderProfile] = []
    for f in leads:
        # Use enrichment (optional) to produce signals; if OpenAI key missing, it returns a safe default
        enrich = enrich_founder(f.name, f.current_role or "", f.location or "", raw=f.source or "")
        f.archetype = enrich.get("archetype") or f.archetype or archetype
        f.key_signals = enrich.get("key_signals") or f.key_signals
        f.one_line_thesis = enrich.get("one_line_thesis")

        # Build a text blob for scoring (role + signals)
        signals_blob = " ".join(f.key_signals or []) + " " + (f.current_role or "")
        score, why = score_archetype(f.archetype, signals_blob)
        # prefer model's numeric score if present and higher fidelity
        model_score = enrich.get("score")
        f.score = float(model_score) if model_score is not None else score
        f.notes = (f.notes or "")
        if "Score why:" not in (f.notes or ""):
            f.notes = (f.notes + f"\nScore why: {why}").strip()

        enriched.append(f)

    enriched.sort(key=lambda x: (x.score or 0), reverse=True)
    return enriched
