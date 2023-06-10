from typing import TYPE_CHECKING

from src.offer.domain.dtos import OfferDto, TourDto

if TYPE_CHECKING:
    from src.offer.infrastructure.storage.models import Offer, Tour


def offer_dto_factory(offer: "Offer") -> OfferDto:
    return OfferDto(
        id=offer.id,
        number_of_kids=offer.number_of_kids,
        number_of_adults=offer.number_of_adults,
        room_type=offer.room_type,
        available=offer.available,
        tour_id=offer.tour_id,
        all_inclusive=offer.all_inclusive,
        breakfast=offer.breakfast,
    )


def tour_dto_factory(tour: "Tour") -> TourDto:
    return TourDto(
        id=tour.id,
        arrival_date=tour.arrival_date,
        description=tour.description,
        departure_city=tour.departure_city,
        departure_date=tour.departure_date,
        average_flight_cost=tour.average_flight_cost,
        average_night_cost=tour.average_night_cost,
        country=tour.country,
        operator=tour.operator,
        hotel=tour.hotel,
        thumbnail_url=tour.thumbnail_url,
        transport=tour.transport,
    )
