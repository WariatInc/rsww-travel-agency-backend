from src.infrastructure.storage import SessionFactory
from src.payment.domain.ports import IPaymentUnitOfWork
from src.payment.infrastructure.storage.repository import PaymentRepository


class PaymentUnitOfWork(IPaymentUnitOfWork):
    def __init__(self, session_factory: SessionFactory):
        self._session_factory = session_factory

    def __enter__(self) -> None:
        self._session = self._session_factory.create_session()
        self.payment_repository = PaymentRepository(self._session)

    def __exit__(self, *args) -> None:
        self._session.close()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
