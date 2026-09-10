import json
from pathlib import Path
from utils import normalize_text
with open(Path(__file__).resolve().parent.parent / "data/intents.json", encoding="utf-8") as f:
    INTENTS = json.load(f)

def detect_intent(text):
    norm = normalize_text(text)
    candidates = []
    for name, cfg in INTENTS.items():
        for phrase in cfg.get("phrases", []):
            p = normalize_text(phrase)
            if p and p in norm: candidates.append((cfg.get("priority",0),len(p),name))
        for keyword in cfg.get("keywords", []):
            k = normalize_text(keyword)
            if k and k in norm: candidates.append((cfg.get("priority",0),len(k),name))
    if not candidates: return None
    candidates.sort(reverse=True)
    return candidates[0][2]
