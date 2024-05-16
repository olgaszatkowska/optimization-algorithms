from random import randint, shuffle
from search_history import SearchHistory
from tsplib95.models import StandardProblem


class TabuSearch:
    def __init__(self, problem: StandardProblem, initial_solution: list[int]) -> None:
        self.initial_solution = initial_solution
        self.problem = problem

    def _tour_cost(self, vertexes: list[int]) -> float:
        return self.problem.trace_tours([vertexes])[0]

    def _log_progress(self, best_solution: list[int], iteration: int):
        tour_distance = self._tour_cost(best_solution)
        print(f"{iteration} {tour_distance}")

    @staticmethod
    def _get_tour_options(
        tour: list[int], search_space_percent: int, randomize: bool
    ) -> list[int]:
        tour_options = []
        options_size = int((search_space_percent / 100) * len(tour))
        for _ in range(options_size):
            vertex_idx_1 = 0
            vertex_idx_2 = 0

            while vertex_idx_1 == vertex_idx_2:
                vertex_idx_1 = randint(1, len(tour) - 1)
                vertex_idx_2 = randint(1, len(tour) - 1)

            if vertex_idx_1 > vertex_idx_2:
                swap = vertex_idx_1
                vertex_idx_1 = vertex_idx_2
                vertex_idx_2 = swap

            neighborhood_tour = tour[vertex_idx_1:vertex_idx_2]
            new_neighborhood_tour = neighborhood_tour[::-1]
            if randomize:
                shuffle(new_neighborhood_tour)

            tour_option = (
                tour[:vertex_idx_1] + new_neighborhood_tour + tour[vertex_idx_2:]
            )
            tour_options.append(tour_option)

        return tour_options

    def _get_cached_cost(self, search_history: SearchHistory, tour: list[int]):
        saved_search = search_history.find(tour)

        if saved_search != None:
            return saved_search

        tour_cost = self._tour_cost(tour)
        search_history.append(tour, tour_cost)
        return tour_cost

    def run(
        self,
        iterations: int,
        tabu_size: int,
        search_space_percent: int,
        aspiration_criteria: float,
        max_stuck_iterations,
    ) -> list[int]:
        best_solution = self.initial_solution
        best_candidate = self.initial_solution
        tabu_list = [self.initial_solution]
        search_history = SearchHistory()
        stuck_iterations = 0

        for iteration in range(iterations):
            exceeded_stuck_limit = stuck_iterations >= max_stuck_iterations

            tour_options = self._get_tour_options(
                best_candidate,
                search_space_percent,
                exceeded_stuck_limit,
            )
            best_candidate = tour_options[0]

            for candidate in tour_options:
                candidate_tour_cost = self._get_cached_cost(search_history, candidate)
                best_candidate_tour_cost = self._get_cached_cost(
                    search_history, best_candidate
                )

                is_candidate_better = candidate_tour_cost < best_candidate_tour_cost
                is_candidate_tabu = candidate in tabu_list

                can_tabu_candidate_aspire = (
                    (best_candidate_tour_cost - candidate_tour_cost) >= aspiration_criteria
                    if is_candidate_tabu
                    else False
                )

                if can_tabu_candidate_aspire or (
                    is_candidate_better and not is_candidate_tabu
                ):
                    best_candidate = candidate

                if can_tabu_candidate_aspire:
                    tabu_list.remove(best_candidate)

            is_best_candidate_better = self._get_cached_cost(
                search_history, best_candidate
            ) < self._get_cached_cost(search_history, best_solution)

            if is_best_candidate_better:
                best_solution = best_candidate
                self._log_progress(best_solution, iteration)
                stuck_iterations = 0
            else:
                stuck_iterations += 1

            tabu_list.append(best_candidate)
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            

        return best_solution
