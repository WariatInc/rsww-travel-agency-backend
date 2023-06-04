from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional


@dataclass
class SearchOptions:
    page: int = 1
    page_size: int = 25
    country: Optional[str] = None
    operator: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    transport: Optional[str] = None
    adults: Optional[str] = None
    kids: Optional[str] = None
    departure_city: Optional[str] = None
