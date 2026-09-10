import json
from pathlib import Path
with open(Path(__file__).resolve().parent.parent / "data/faq.json", encoding="utf-8") as f:
    FAQ = json.load(f)
def answer_for(intent):
    return FAQ.get(intent)
