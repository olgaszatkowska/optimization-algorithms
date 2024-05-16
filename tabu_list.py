from attr import dataclass


@dataclass
class TabuTour:
    tour: list[int]
    iterations: int

    def iterate(self):
        self.iterations += 1

    def __eq__(self, other: object) -> bool:
        if isinstance(other, TabuTour):
            return self.tour == other.tour
        return False


class TabuList:
    def __init__(self) -> None:
        self.tabu_tours: list[TabuTour] = []

    def _iterate(self):
        for tour in self.tabu_tours:
            tour.iterate()

    def remove_older_than(self, max_iterations):
        if self.tabu_tours[0].iterations < max_iterations:
            return
        self.tabu_tours = [
            tabu_tour
            for tabu_tour in self.tabu_tours
            if tabu_tour.iterations < max_iterations
        ]

    def add(self, tour):
        self.tabu_tours.append(TabuTour(tour, 0))
        self._iterate()

    def __contains__(self, key: object):
        if isinstance(key, list):
            saved_tours = [tabu_tour.tour for tabu_tour in self.tabu_tours]
            return key in saved_tours
        return False
