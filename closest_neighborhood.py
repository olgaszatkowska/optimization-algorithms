from tsplib95.models import StandardProblem
import random


def _get_closest(node: int, problem: StandardProblem, candidates: list[int]) -> int:
    min_distance = problem.get_weight(node, candidates[0])
    best_candidate = candidates[0]

    for candidate in candidates:
        candidate_distance = problem.get_weight(node, candidate)

        if candidate_distance < min_distance:
            min_distance = candidate_distance
            best_candidate = candidate

    return best_candidate


def get_closest_neighbors(problem: StandardProblem) -> list[int]:
    nodes = list(problem.get_nodes())
    total_nodes_len = len(nodes)
    random_starting_point = random.choice(nodes)
    current_node = random_starting_point
    closest_neighbors = [random_starting_point]
    nodes.remove(random_starting_point)

    while len(closest_neighbors) != total_nodes_len:
        closest_neighbor = _get_closest(current_node, problem, nodes)
        closest_neighbors.append(closest_neighbor)
        nodes.remove(closest_neighbor)
        current_node = closest_neighbor

    assert len(set(closest_neighbors)) == total_nodes_len

    return closest_neighbors
