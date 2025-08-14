import pandas as pd
import os
from typing import List
from .models import FounderProfile

COLUMNS = ["Name","LinkedIn","Email","Location","Current Role","Archetype","One-line Thesis","Key Signals","Traction","Fit","Source","Outreach Idea","Status","Priority","Notes","Score"]

LAST_SESSION_PATH = "data/last_session.csv"

def to_dataframe(founders: List[FounderProfile]) -> pd.DataFrame:
    rows = []
    for f in founders:
        rows.append({
            "Name": f.name,
            "LinkedIn": f.linkedin_url,
            "Email": f.email,
            "Location": f.location,
            "Current Role": f.current_role,
            "Archetype": f.archetype,
            "One-line Thesis": f.one_line_thesis,
            "Key Signals": "; ".join(f.key_signals) if f.key_signals else "",
            "Traction": f.traction,
            "Fit": f.fit_reason,
            "Source": f.source,
            "Outreach Idea": f.outreach_idea,
            "Status": f.status,
            "Priority": f.priority,
            "Notes": f.notes,
            "Score": f.score,
        })
    return pd.DataFrame(rows, columns=COLUMNS)

def save_csv(df: pd.DataFrame, path: str):
    df.to_csv(path, index=False)

def load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def save_last_session(df: pd.DataFrame):
    os.makedirs("data", exist_ok=True)
    save_csv(df, LAST_SESSION_PATH)

def load_last_session() -> pd.DataFrame:
    if os.path.exists(LAST_SESSION_PATH):
        return load_csv(LAST_SESSION_PATH)
    return pd.DataFrame(columns=COLUMNS)