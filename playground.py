from tabu_search import TabuSearch
from problem import get_problem
from closest_neighborhood import get_closest_neighbors

problem = get_problem("rbg443.atsp")
initial_solution = get_closest_neighbors(problem)
searcher_closest = TabuSearch(problem, initial_solution)

searcher_closest.run(
    iterations=100,
    tabu_size=15,
    search_space_percent=30,
    aspiration_criteria=100,
    max_stuck_iterations=3,
)