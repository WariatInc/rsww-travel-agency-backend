from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from uuid import UUID

if TYPE_CHECKING:
    from src.consts import PaymentItem, PaymentState
    from src.payment.domain.dtos import PaymentDto


class IPaymentRepository(ABC):
    @abstractmethod
    def check_if_item_is_paid(self, item_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def check_if_item_payment_is_in_pending_state(self, item_id: UUID) -> bool:
        raise NotImplementedError

    @abstractmethod
    def create_payment(
        self, item_id: UUID, item: "PaymentItem", state: "PaymentState"
    ) -> "PaymentDto":
        raise NotImplementedError

    @abstractmethod
    def update_payment(self, payment_id: UUID, **update_kwargs) -> None:
        raise NotImplementedError


class IPaymentUnitOfWork(ABC):
    payment_repository = IPaymentRepository

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError


class IProcessReservationPaymentCommand(ABC):
    @abstractmethod
    def __call__(self, item_id: UUID) -> "PaymentState":
        raise NotImplementedError
