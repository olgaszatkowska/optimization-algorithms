import tsplib95
from tsplib95.models import StandardProblem


def get_problem(file_name: str) -> StandardProblem:
    return tsplib95.load(file_name)
