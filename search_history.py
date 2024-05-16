from attr import dataclass

@dataclass(frozen=True)
class Search:
    tour: list[int]
    cost: float

    def __hash__(self) -> int:
        return "".join(self.tour)

class SearchHistory:
    def __init__(self) -> None:
        self.history: list[Search] = []

    def append(self, tour: list[int], cost: float):
        self.history.append(Search(tour, cost))

    def find(self, tour: list[int]) -> float | None:
        for search in self.history:
            if search.tour == tour:
                return search.cost

        return None
