# data/scrapers.py
import os, requests
from typing import List
from .models import FounderProfile

CITIES_FI = ["Finland"]  # we constrain to Finland per your spec

def serp_search_serper(query: str, num_results: int = 10):
    api_key = os.getenv("SERPER_API_KEY")
    if not api_key:
        return []  # gracefully fall back if no key
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
    payload = {"q": query, "num": num_results}
    resp = requests.post(url, json=payload, headers=headers, timeout=20)
    resp.raise_for_status()
    data = resp.json()
    return [{"title": o.get("title"), "link": o.get("link"), "snippet": o.get("snippet") or ""} for o in data.get("organic", [])]

def _parse_name_role_from_title(title: str):
    # e.g. "Jane Doe - VP Sales at X | LinkedIn"
    if not title:
        return "Unknown", None
    t = title.replace(" | LinkedIn", "")
    parts = t.split(" - ", 1)
    name = parts[0].strip()
    role = parts[1].strip() if len(parts) > 1 else None
    return name, role

# --------- SAMPLE SEEDS (used when no SERPER_API_KEY) ----------
SAMPLE_COMM = [
    dict(name="Anna Virtanen", linkedin_url="https://linkedin.com/in/anna-virtanen", location="Finland, Finland",
         current_role="Head of Sales at SaaSCo", archetype="Commercial",
         key_signals=["Scaled SaaS revenue 5x","Exited 1 startup","B2B growth specialist"], source="Sample"),
    dict(name="Ville Kallio", linkedin_url="https://linkedin.com/in/ville-kallio", location="Finland, Finland",
         current_role="VP Sales at FinTechCo", archetype="Commercial",
         key_signals=["Closed enterprise logos","Fintech domain","Built GTM team"], source="Sample"),
]

SAMPLE_TECH = [
    dict(name="Liisa Hautala", linkedin_url="https://linkedin.com/in/liisa-hautala", location="Finland, Finland",
         current_role="Staff ML Engineer at VisionAI", archetype="Technical",
         key_signals=["ML systems at scale","Ex-CTO at startup","OSS contributor"], source="Sample"),
    dict(name="Jussi Rantanen", linkedin_url="https://linkedin.com/in/jussi-rantanen", location="Finland, Finland",
         current_role="Principal Engineer (Infra) at CloudNordic", archetype="Technical",
         key_signals=["Distributed systems","K8s/SRE leadership","Authored internal frameworks"], source="Sample"),
]

SAMPLE_DOMAIN = [
    dict(name="Dr. Helena Korpi", linkedin_url="https://linkedin.com/in/helena-korpi", location="Finland, Finland",
         current_role="Head of Operations at HUS", archetype="Domain",
         key_signals=["Healthcare ops leadership","Clinical partnerships","Regulatory familiarity"], source="Sample"),
    dict(name="Petri Salonen", linkedin_url="https://linkedin.com/in/petri-salonen", location="Finland, Finland",
         current_role="Director of Risk at Nordea", archetype="Domain",
         key_signals=["Fintech/regulatory domain","Managed large teams","Policy & compliance"], source="Sample"),
]
# ---------------------------------------------------------------

def scrape_by_archetype(archetype: str, limit: int = 20, recall_mode: str = "balanced") -> List[FounderProfile]:
    """
    archetype: 'Commercial' | 'Technical' | 'Domain'
    recall_mode: 'precision' | 'balanced' | 'recall'
    """
    archetype = (archetype or "Commercial").capitalize()
    recall_mode = recall_mode.lower()
    per_query = 10 if recall_mode == "precision" else (15 if recall_mode == "balanced" else 20)

    # query banks (Finland only)
    if archetype == "Commercial":
        queries = [
            'site:linkedin.com/in ("VP Sales" OR "Head of Sales" OR "Commercial Director" OR "Head of Growth") Finland',
            'site:linkedin.com/in ("Head of Partnerships" OR "Go-to-Market" OR "Sales Leader") Finland',
        ]
    elif archetype == "Technical":
        queries = [
            'site:linkedin.com/in (CTO OR "Staff Engineer" OR "Principal Engineer" OR "ML Engineer") Finland',
            'site:linkedin.com/in ("Engineering Manager" OR "Head of Engineering") Finland',
            # Optional: broaden via GitHub profiles surfaced in Google
            # 'site:github.com ("Finland") ("Senior" OR "Staff" OR "CTO")'
        ]
    else:  # Domain
        queries = [
            'site:linkedin.com/in ("Head of Product" OR "Product Director" OR "General Manager" OR "Head of Operations") Finland',
            'site:linkedin.com/in ("Medical Director" OR "Director of Risk" OR "Head of Compliance") Finland',
        ]

    # If no SERPER_API_KEY -> return samples
    hits_total = []
    if not os.getenv("SERPER_API_KEY"):
        seeds = SAMPLE_COMM if archetype == "Commercial" else (SAMPLE_TECH if archetype == "Technical" else SAMPLE_DOMAIN)
        return [FounderProfile(**x) for x in seeds[:limit]]

    for q in queries:
        for h in serp_search_serper(q, num_results=per_query):
            title, link, snippet = h["title"] or "", h["link"], h["snippet"] or ""
            if not link:
                continue
            name, role = _parse_name_role_from_title(title)
            # crude Finland check (SERP already filtered)
            location = "Finland, Finland"
            hits_total.append(FounderProfile(
                name=name or "Unknown",
                linkedin_url=link,
                location=location,
                current_role=role or (archetype + " leader"),
                archetype=archetype,
                key_signals=[],
                source="Serper"
            ))

    # dedupe by link
    dedup = {}
    for f in hits_total:
        dedup[f.linkedin_url] = f
    results = list(dedup.values())
    return results[:limit]
