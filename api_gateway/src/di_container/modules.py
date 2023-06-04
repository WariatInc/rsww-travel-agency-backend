from src.infrastructure.di_container.modules import InfrastructureModule
from src.reservation.di_container.modules import ReservationModule
from src.user.di_container.modules import UserModule

all_modules = [InfrastructureModule, ReservationModule, UserModule]
