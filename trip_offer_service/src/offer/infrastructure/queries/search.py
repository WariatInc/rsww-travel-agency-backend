from dataclasses import dataclass
from typing import Optional


@dataclass
class SearchOptions:
    page: int = 0
    page_size: int = 25
    operator: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    date_start: Optional[str] = None
    date_end: Optional[str] = None
    transport: Optional[str] = None
    adults: Optional[str] = None
    kids: Optional[str] = None
    room: Optional[str] = None
    available: Optional[str] = None
