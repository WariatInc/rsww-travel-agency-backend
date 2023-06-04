from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class UserSessionDto:
    id: UUID
    ip_address: str
    webapp_page: str
    expires_in: int
    refreshed_at: datetime
    revoked: bool
