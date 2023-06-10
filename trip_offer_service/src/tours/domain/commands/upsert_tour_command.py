from uuid import UUID

from src.tours.domain.ports import ITourRepository, IUpsertTourCommand


class UpsertTourCommand(IUpsertTourCommand):
    def __init__(self, tour_repository: ITourRepository) -> None:
        self._tour_repository = tour_repository

    def __call__(self, tour_id: UUID, **kwargs) -> None:
        self._tour_repository.upsert_tour(tour_id, **kwargs)
