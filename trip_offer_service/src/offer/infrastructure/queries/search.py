from typing import Optional, Any
from dataclasses import dataclass


@dataclass
class SearchOptions:
    max_offers: int = 200
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
