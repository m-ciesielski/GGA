import itertools
import random
import math


class Graph:
    def __init__(self, vertices: set, distance_matrix):
        # vertices are stored as list in order to allow indexing
        self.vertices = list(vertices)
        self._distance_matrix = distance_matrix

    def get_distance(self, i, j):
        return self._distance_matrix[i][j]


def generate_asymmetrical_distance_matrix(vertices: set):
    distance_matrix = []
    for vertex in vertices:
        distance_matrix_row = []
        for other_vertex in vertices:
            if vertex == other_vertex:
                distance_matrix_row.append(0)
            else:
                distance_matrix_row.append(random.randint(1, 10))

        distance_matrix.append(distance_matrix_row)

    return distance_matrix


def generate_symmetrical_distance_matrix(vertices: set):
    distance_matrix = [[0] * len(vertices) for i in range(len(vertices))]
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            distance_matrix[i][j] = distance_matrix[j][i] = random.randint(1, 10)

    return distance_matrix


def traveling_salesman(graph: Graph):
    """
    Implemented according to pseudo code provided in https://people.eecs.berkeley.edu/~vazirani/algorithms/chap6.pdf ,
    page 189.
    :param graph: Graph for traveling salesman problem
    :return: Optimal path, optimal path length
    """
    sub_solutions = {}
    backtrack_map = {}
    vertices_count = len(graph.vertices)
    sub_solutions[(0,), 0] = 0

    for subset_size in range(2, vertices_count + 1):
        for subset in (s for s in itertools.combinations(range(vertices_count), subset_size) if 0 in s):
            sub_solutions[subset, 0] = math.inf
            for k in (i for i in subset if i != 0):
                min_dist = math.inf
                for m in subset:
                    if m == k:
                        continue
                    dist = sub_solutions[tuple(set(subset) - {k}), m] + graph.get_distance(m, k)
                    if dist < min_dist:
                        min_dist = dist
                        sub_solutions[subset, k] = dist
                        backtrack_map[subset, k] = m

    possible_solutions = [
        ((tuple(range(vertices_count)), k),
         sub_solutions[tuple(range(vertices_count)), k] + graph.get_distance(k, 0)) for k in range(vertices_count)
        ]

    optimal_solution = min(possible_solutions, key=lambda p: p[1])
    optimal_path_length = optimal_solution[1]

    # Backtrack optimal solution
    optimal_path = [0]
    backtracked_solution = optimal_solution[0]
    successor = backtrack_map.get(backtracked_solution)
    while successor:
        optimal_path.append(backtracked_solution[1])
        successor = backtrack_map.get(backtracked_solution)
        backtracked_solution = (tuple(set(backtracked_solution[0]) - {backtracked_solution[1]}), successor)
    optimal_path.append(0)

    # Reverse backtracked optimal path
    optimal_path = list(reversed(optimal_path))

    backtracked_path_length = 0
    for i in range(len(optimal_path) - 1):
        backtracked_path_length += graph.get_distance(optimal_path[i], optimal_path[i + 1])

    assert backtracked_path_length == optimal_path_length
    return optimal_path, optimal_path_length


def main():
    vertices = {0, 1, 2, 3, 4}
    graph = Graph(vertices, generate_asymmetrical_distance_matrix(vertices))
    print(traveling_salesman(graph))

if __name__ == '__main__':
    main()
