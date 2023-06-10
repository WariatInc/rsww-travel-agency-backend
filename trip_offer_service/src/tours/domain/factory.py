from uuid import UUID

from src.tours.domain.dtos import TourDto


def tour_dto_factory(tour: dict) -> TourDto:
    return TourDto(
        id=UUID(tour.get("id")),
        country=tour.get("country"),
        city=tour.get("city"),
        hotel=tour.get("hotel"),
        description=tour.get("description"),
        arrival_date=tour.get("arrival_date"),
        departure_date=tour.get("departure_date"),
        transport=tour.get("transports"),
        lowest_price=tour.get("lowest_price"),
        departure_city=tour.get("departure_city"),
        thumbnail_url=tour.get("thumbnail_url"),
    )
