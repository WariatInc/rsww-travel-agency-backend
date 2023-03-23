from typing import TypedDict
from uuid import UUID


class Example(TypedDict):
    """Document Representation"""

    uniq_id: UUID
    title: str
    author: str
