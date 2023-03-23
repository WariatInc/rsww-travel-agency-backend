from src.example.domain.dtos import ExampleDto
from src.example.domain.ports import IExamplesView, IGetExamplesListQuery


class GetExamplesListQuery(IGetExamplesListQuery):
    def __init__(self, examples_view: IExamplesView):
        self.examples_view = examples_view

    def __call__(self) -> list[ExampleDto]:
        return self.examples_view.get_list()
