from dataclasses import dataclass
from datetime import datetime
from uuid import UUID
from typing import Optional

from src.consts import TransportType


@dataclass
class TourDto:
    id: UUID
    country: str
    city: str
    hotel: str
    description: str
    thumbnail_url: str
    arrival_date: datetime
    departure_date: datetime
    transport: TransportType
    departure_city: str
    lowest_price: Optional[float] = None
