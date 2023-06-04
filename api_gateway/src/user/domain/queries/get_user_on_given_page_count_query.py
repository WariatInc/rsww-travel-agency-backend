from src.user.domain.ports import (
    IGetUserOnGivenPageCountQuery,
    IUserOnGivenPageCountView,
)


class GetUserOnGivenPageCountQuery(IGetUserOnGivenPageCountQuery):
    def __init__(
        self, user_on_given_page_count_view: IUserOnGivenPageCountView
    ) -> None:
        self._user_on_given_page_count_view = user_on_given_page_count_view

    def get(self, page: str) -> int:
        return self._user_on_given_page_count_view.get(page)
