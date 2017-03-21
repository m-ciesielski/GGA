class Area:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def __repr__(self):
        return f'X: {self.x_min} - {self.x_max}, Y: {self.y_min} - {self.y_max}'

    def is_intersecting(self, other_area):
        return (self.x_min <= other_area.x_max and other_area.x_min <= self.x_max or
                self.y_min <= other_area.y_max and other_area.y_min <= self.y_max)

    def is_subarea(self, other_area):
        return (self.x_min >= other_area.x_min and self.x_max <= other_area.x_max and
                self.y_min >= other_area.y_min and self.y_max <= other_area.y_max)

    def is_point_within_area(self, point: tuple):
        return self.x_min <= point[0] <= self.x_max and self.y_min <= point[1] <= self.y_max


class Node:
    def __init__(self, area: Area, point: tuple=None, split_line=None, left_child=None, right_child=None):
        self.point = point
        self.split_line = split_line
        self.area = area
        self.left_child = left_child
        self.right_child = right_child

    def __str__(self, level=0):
        if self.point:
            ret = "\t" * level + repr(self.point) + "\n"
        else:
            ret = "\t" * level + repr(self.split_line) + "\n"
        for child in filter(None, (self.left_child, self.right_child)):
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        if self.point:
            return f'{self.point}'
        else:
            return f'{self.split_line}'

    def is_leaf(self):
        if not self.left_child and not self.right_child:
            return True
        else:
            return False


def inorder_traversal_leaves(node: Node):
    if node.left_child:
        for left_child in (n for n in inorder_traversal_leaves(node.left_child) if n.is_leaf()):
            yield left_child
    if node.is_leaf():
        yield node
    if node.right_child:
        for right_child in (n for n in inorder_traversal_leaves(node.right_child) if n.is_leaf()):
            yield right_child


def sort_points_by_axes(points: list):
    """
    Sortowanie listy punktów wg współrzędnych x i y. Złożoność obliczeniowa: O(n log n).
    :param points: Lista krotek zawierających współrzędne punktów - [(x1, y1), (x2, y2),..., (xn, yn)]
    :return: Krotka zawierająca listę punktów posortowanych leksykograficznie wg współrzędnej x oraz
             listę punktów posortowanych wg współrzędnej y - ([punkty posortowane wg x], [punkty posortowane wg y])
    """
    points_sorted_by_x = sorted(points, key=lambda point: (point[0], point[1]))
    points_sorted_by_y = sorted(points, key=lambda point: point[1])
    return points_sorted_by_x, points_sorted_by_y


def split_points_list(points_x: list, points_y: list, split_axis: int):
    assert split_axis == 0 or split_axis == 1
    if split_axis == 0:
        other_axis = 1
    else:
        other_axis = 0

    points_sorted_by_split_axis = [points_x, points_y][split_axis]
    points_sorted_by_other_axis = [points_x, points_y][other_axis]
    median = len(points_sorted_by_split_axis) // 2
    splitting_point = points_sorted_by_split_axis[median]
    splitting_line = splitting_point[split_axis]
    left_axis_points, right_axis_points = points_sorted_by_split_axis[:median], points_sorted_by_split_axis[median:]
    left_other_points = [p for p in points_sorted_by_other_axis if p[split_axis] < splitting_point[split_axis]
                         or (p[split_axis] == splitting_point[split_axis]
                             and p[other_axis] < splitting_point[other_axis])]
    right_other_points = [p for p in points_sorted_by_other_axis if p[split_axis] > splitting_point[split_axis]
                          or (p[split_axis] == splitting_point[split_axis]
                              and p[other_axis] >= splitting_point[other_axis])]

    return splitting_line, left_axis_points, right_axis_points, left_other_points, right_other_points


def kdtree(points_x: list, points_y: list, depth=0):
    if not points_x or not points_y:
        return None

    assert len(points_x) == len(points_y)

    if len(points_x) == len(points_y) == 1:
        return Node(point=points_x[0],
                    area=Area(points_x[0][0], points_x[0][0], points_x[0][1], points_x[0][1]),
                    left_child=None,
                    right_child=None)

    # Zakładamy, że wszystkie punkty mają tyle samo wymiarów co pierwszy
    dim = len(points_x[0])
    assert dim > 0

    # Wyznaczamy oś podziału (axis == 0 - poziomo, axis === 1 - pionowo)
    axis = depth % dim

    # Wyznaczamy indeks środkowego punktu oraz dzielimy zbiór na pół wg osi podziału
    if axis == 0:
        splitting_line, left_points_x, right_points_x, left_points_y, right_points_y = split_points_list(points_x,
                                                                                                         points_y,
                                                                                                         axis)
    else:
        splitting_line, left_points_y, right_points_y, left_points_x, right_points_x = split_points_list(points_x,
                                                                                                         points_y,
                                                                                                         axis)

    assert len(left_points_x) == len(left_points_y)
    assert len(right_points_x) == len(right_points_y)

    # Zwracamy węzeł i rekurencyjnie wyznaczamy poddrzewa
    return Node(split_line=splitting_line,
                area=Area(points_x[0][0], points_x[-1][0], points_y[0][1], points_y[-1][1]),
                left_child=kdtree(left_points_x, left_points_y, depth + 1),
                right_child=kdtree(right_points_x, right_points_y, depth + 1))


def query_kdtree(node: Node, query_area: Area) -> set:
    if not node:
        return set()
    if node.is_leaf() and query_area.is_point_within_area(node.point):
        return {node}
    if node.area.is_subarea(query_area):
        return set(inorder_traversal_leaves(node))

    return query_kdtree(node.left_child, query_area).union(query_kdtree(node.right_child, query_area))


def main():
    point_list = [(2, 3), (5, 4), (9, 6), (4, 7), (8, 1), (7, 2)]
    points_x, points_y = sort_points_by_axes(point_list)
    tree = kdtree(points_x, points_y)
    print(tree)
    print(query_kdtree(tree, Area(x_min=4, x_max=7, y_min=2, y_max=7)))


if __name__ == '__main__':
    main()
