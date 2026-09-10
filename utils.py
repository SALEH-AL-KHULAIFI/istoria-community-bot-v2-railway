import re, unicodedata
URL_RE = re.compile(r"(https?://|www\.|t\.me/|telegram\.me/|(?:[a-z0-9-]+\.)+[a-z]{2,})(?:\S*)", re.I)

def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text or "")
    text = re.sub(r"[\u200b-\u200f\u202a-\u202e\ufeff]", "", text)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.replace("أ","ا").replace("إ","ا").replace("آ","ا").replace("ى","ي").replace("ة","ه").lower().strip()

def compact_text(text: str) -> str:
    return re.sub(r"[\s\W_]+", "", normalize_text(text), flags=re.UNICODE)

def contains_url(text: str) -> bool:
    return bool(URL_RE.search(text or ""))

def tokens(text: str) -> list[str]:
    return re.findall(r"[\w\u0600-\u06ff]+", normalize_text(text), flags=re.UNICODE)
