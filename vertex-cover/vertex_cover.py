import random


class Graph:
    def __init__(self, edges: list):
        self.edges = edges


def approx_vertex_cover(graph: Graph):
    vertex_cover = set()
    remaining_edges = graph.edges

    while remaining_edges:
        edge = random.choice(remaining_edges)
        vertex_cover.add(edge[0])
        vertex_cover.add(edge[1])
        remaining_edges = [e for e in remaining_edges if edge[0] not in e and edge[1] not in e]

    return vertex_cover


if __name__ == '__main__':
    edges = [(0, 1), (0, 3), (0, 4),
             (1, 4), (1, 5), (1, 2),
             (2, 3), (2, 6), (2, 7), (2, 5),
             (3, 7), (3, 6),
             (4, 7), (4, 5),
             (5, 8), (5, 6),
             (6, 7),
             (7, 8)]

    # adjacency_dict = {0: [1, 3, 4],
    #                   1: [0, 2, 4, 5],
    #                   2: [1, 3, 5, 6, 7],
    #                   3: [0, 2, 6, 7],
    #                   4: [0, 1, 5, 7],
    #                   5: [1, 2, 4, 6, 8],
    #                   6: [2, 3, 5, 7],
    #                   7: [2, 3, 4, 6, 8],
    #                   8: [5, 7]}
    #
    # adjacency_matrix = [[0, 1, 0, 1, 1, 0, 0, 0, 0],
    #                     [1, 0, 1, 0, 1, 1, 0, 0, 0],
    #                     [0, 1, 0, 1, 0, 1, 1, 1, 0],
    #                     [1, 0, 1, 0, 0, 0, 1, 0, 0],
    #                     [1, 1, 0, 0, 0, 1, 0, 1, 0],
    #                     [0, 1, 1, 0, 1, 0, 1, 0, 1],
    #                     [0, 0, 1, 1, 1, 0, 1, 0, 0],
    #                     [0, 0, 1, 1, 1, 0, 1, 0, 1],
    #                     [0, 0, 0, 0, 0, 1, 0, 1, 0]]

    graph = Graph(edges=edges)
    print(approx_vertex_cover(graph))
