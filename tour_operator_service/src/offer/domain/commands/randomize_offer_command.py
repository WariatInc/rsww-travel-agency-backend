import logging
import random as rd

from src.consts import RoomType
from src.offer.domain.ports import (
    IOfferUnitOfWork,
    IRandomizeOfferCommand,
    IUpdateOfferCommand,
)

logger = logging.getLogger("TourOperator")


class RandomizeOfferCommand(IRandomizeOfferCommand):
    def __init__(
        self, uow: IOfferUnitOfWork, update_offer_command: IUpdateOfferCommand
    ) -> None:
        self._uow = uow
        self._update_offer_command = update_offer_command

    def __call__(self) -> None:
        changes = dict()

        if rd.uniform(0, 1) < 0.1:
            changes["room_type"] = rd.choice(
                [room_type.value for room_type in RoomType]
            )

        if rd.uniform(0, 1) < 0.1:
            changes["available"] = False

        if rd.uniform(0, 1) < 0.1:
            rand = rd.uniform(0, 1)
            if rand < 0.33:
                changes["all_inclusive"] = True
                changes["breakfast"] = False
            elif rand < 0.66:
                changes["all_inclusive"] = False
                changes["breakfast"] = True
            else:
                changes["all_inclusive"] = False
                changes["breakfast"] = False

        if not changes:
            return

        with self._uow:
            offer = self._uow.offer_repository.get_random_offer()

        logger.info(
            f"Randomizing offer with id {offer.id}, changes: {changes}"
        )
        self._update_offer_command(offer.id, **changes)
