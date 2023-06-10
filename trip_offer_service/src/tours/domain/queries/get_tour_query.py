from uuid import UUID

from src.tours.domain.dtos import TourDto
from src.tours.domain.exceptions import TourNotFoundException
from src.tours.domain.ports import IGetTourQuery, ITourView


class GetTourQuery(IGetTourQuery):
    def __init__(self, get_tour_view: ITourView) -> None:
        self.get_tour_view = get_tour_view

    def get(self, tour_id: UUID) -> TourDto:
        if tour := self.get_tour_view.get(tour_id):
            return tour

        raise TourNotFoundException
