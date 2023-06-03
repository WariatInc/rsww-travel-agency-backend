from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Optional
from uuid import UUID

if TYPE_CHECKING:
    from src.offer.domain.dtos import OfferDto


class IOfferRepository(ABC):
    @abstractmethod
    def update_offer(
        self, offer_id: UUID, update_dict: dict[str, Any]
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_offer(self, offer_id: UUID) -> Optional["OfferDto"]:
        raise NotImplementedError

    @abstractmethod
    def check_if_offer_can_be_reserved(self, offer_id: UUID) -> bool:
        raise NotImplementedError


class IOfferUnitOfWork(ABC):
    offer_repository = IOfferRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class IUpdateOfferCommand(ABC):
    @abstractmethod
    def __call__(self, offer_id: UUID, **update_kwargs) -> None:
        raise NotImplementedError


class IOfferReservationCommand(ABC):
    @abstractmethod
    def __call__(
        self,
        offer_id: UUID,
        reservation_id: UUID,
        kids_up_to_3: int,
        kids_up_to_10: int,
    ) -> None:
        raise NotImplementedError


class IOfferPriceView(ABC):
    @abstractmethod
    def get_offer_price(
        self, offer_id: UUID, kids_up_to_3: int, kids_up_to_10: int
    ) -> float:
        raise NotImplementedError


class IGetOfferPriceQuery(ABC):
    @abstractmethod
    def get(
        self, offer_id: UUID, kids_up_to_3: int, kids_up_to_10: int
    ) -> float:
        raise NotImplementedError
