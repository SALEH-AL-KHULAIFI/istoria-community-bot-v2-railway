import json
from pathlib import Path
from utils import normalize_text, compact_text, contains_url, tokens
DATA = Path(__file__).resolve().parent.parent / "data"
with open(DATA / "bad_words.json", encoding="utf-8") as f:
    BAD_WORDS = [normalize_text(x) for x in json.load(f).get("words", []) if x.strip()]
BAD_COMPACT = {compact_text(x) for x in BAD_WORDS}

def has_link(text): return contains_url(text)
def has_bad_word(text):
    token_set = set(tokens(text))
    if any(w in token_set for w in BAD_WORDS): return True
    compact = compact_text(text)
    return any(w and len(w) >= 4 and w in compact for w in BAD_COMPACT)
