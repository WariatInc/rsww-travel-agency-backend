from src.example.domain.dtos import ExampleDto
from src.example.infrastructure.storage.documents import Example


def example_dto_factory(example: Example) -> ExampleDto:
    return ExampleDto(
        uniq_id=example.get("uniq_id"),
        title=example.get("title"),
        author=example.get("author"),
    )
