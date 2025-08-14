import os, json, re, requests

OPENAI_URL = "https://api.openai.com/v1/chat/completions"
MODEL = "gpt-4o-mini"  # change if needed

def enrich_founder(name: str, role: str, location: str, raw: str = "") -> dict:
    """
    Returns dict: {archetype, key_signals [3], one_line_thesis, score}
    Falls back to mock if no key set.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {
            "archetype": "Commercial",
            "key_signals": ["Led growth team", "Closed enterprise deals", "Built GTM engine"],
            "one_line_thesis": f"{name or 'This person'} looks like a strong commercial founder in {location or 'Finland'}.",
            "score": 4.0
        }

    prompt = f"""
You are a VC scout for Antler (Nordics). Output STRICT JSON ONLY with keys:
archetype (Commercial/Technical/Domain), key_signals (array of 3 short strings),
one_line_thesis (string), score (number 0-5).

INPUT:
Name: {name}
Role: {role}
Location: {location}
Raw snippet: {raw}
"""
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    body = {"model": MODEL, "messages":[{"role":"user","content":prompt}], "temperature":0.2}
    resp = requests.post(OPENAI_URL, headers=headers, json=body, timeout=30)
    if resp.status_code != 200:
        # common beginner safeguard: fall back gracefully
        return {
            "archetype": "Commercial",
            "key_signals": ["Growth leader", "Deal maker", "Team builder"],
            "one_line_thesis": f"{name or 'This person'} shows commercial founder signals.",
            "score": 3.7
        }
    text = resp.json()["choices"][0]["message"]["content"]
    m = re.search(r"\{.*\}", text, re.S)
    payload = json.loads(m.group(0) if m else text)
    return payload
