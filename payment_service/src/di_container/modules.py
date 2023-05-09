from src.infrastructure.di_container.modules import InfrastructureModule
from src.payment.di_container.modules import PaymentModule
from src.reservation_read_store.di_container.modules import \
    ReservationReadStoreModule

all_modules = [InfrastructureModule, ReservationReadStoreModule, PaymentModule]
