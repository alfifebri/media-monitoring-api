import re
from datetime import datetime
from dateutil import parser

def strip_html(text: str | None) -> str | None:
    """Menghapus semua HTML tag seperti <p>, </p>, <a> dll."""
    if not text:
        return text
    clean_text = re.sub(r'<[^>]+>', '', text)
    return clean_text.strip()

def normalize_source(source: str | None) -> str:
    """Mengubah nama source menjadi lowercase dan rapi."""
    if not source:
        return "unknown"
    return source.strip().lower()

def parse_int(val) -> int:
    """Mengonversi angka string atau null menjadi integer aman."""
    if val is None:
        return 0
    try:
        return int(val)
    except (ValueError, TypeError):
        return 0

def parse_datetime(val: str | None) -> datetime | None:
    """Mengonversi berbagai format tanggal ISO menjadi datetime object."""
    if not val:
        return None
    try:
        return parser.parse(val)
    except Exception:
        return None