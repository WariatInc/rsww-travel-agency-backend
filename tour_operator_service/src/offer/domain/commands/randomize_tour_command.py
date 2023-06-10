import logging
import random as rd

from src.offer.domain.ports import (
    IRandomizeTourCommand,
    ITourUnitOfWork,
    IUpdateTourCommand,
)

logger = logging.getLogger("TourOperator")


class RandomizeTourCommand(IRandomizeTourCommand):
    def __init__(
        self, uow: ITourUnitOfWork, update_tour_command: IUpdateTourCommand
    ) -> None:
        self._uow = uow
        self._update_tour_command = update_tour_command

    def __call__(self) -> None:
        with self._uow:
            tour = self._uow.tour_repository.get_random_tour()

        changes = dict()

        if rd.uniform(0, 1) < 0.1:
            changes["average_night_cost"] = tour.average_night_cost + (
                rd.choice([-1, 1]) * 0.1 * tour.average_night_cost
            )

        if rd.uniform(0, 1) < 0.1:
            changes["average_flight_cost"] = tour.average_flight_cost + (
                rd.choice([-1, 1]) * 0.1 * tour.average_flight_cost
            )

        if not changes:
            return

        logger.info(f"Randomizing tour with id {tour.id}, changes: {changes}")
        self._update_tour_command(tour.id, **changes)
