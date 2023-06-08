from uuid import UUID

from src.offers.domain.ports import IOfferRepository, IUpdateOffer


class UpdateOffer(IUpdateOffer):
    def __init__(self, repo: IOfferRepository) -> None:
        self.repo = repo

    def __call__(self, offer_id: UUID, **fields) -> None:
        self.repo.upsert_offer(offer_id, **fields)
