class Node:
    def __init__(self, left_child=None, right_child=None, point=None):
        self.left_child = left_child
        self.right_child = right_child
        self.point = point

    def is_leaf(self):
        return not self.left_child and not self.right_child

    def __str__(self, level=0):
        if self.point:
            ret = "\t" * level + repr(self.point) + "\n"
        else:
            ret = "\t" * level + repr(self.median) + "\n"
        for child in filter(None, (self.left_child, self.right_child)):
            ret += child.__str__(level + 1)
        return ret

    def __repr__(self):
        if self.point:
            return f'{self.point}'
        else:
            return f'Node'


class IntervalNode(Node):
    def __init__(self, median: float, point=None, median_points_left=None, median_points_right=None,
                 left_child=None, right_child=None):
        super().__init__(left_child, right_child, point)
        self.median = median
        self.median_points_left = median_points_left if median_points_left else []
        self.median_points_right = median_points_right if median_points_right else []


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


def create_interval_tree(intervals_left: list, intervals_right: list) -> IntervalNode:
    """
    :param intervals_left: Lista przedziałów posortowanych wg lewych końców
    :param intervals_right: Lista przediałów posortowanych wg prawych końcow
    :return: Korzeń drzewa przediałów
    """

    if not intervals_left or not intervals_right:
        return None

    assert len(intervals_left) == len(intervals_right)

    median = intervals_left[len(intervals_left) // 2][0]
    median_points_l, intervals_left_of_median_l, intervals_right_of_median_l = [], [], []

    for interval in intervals_left:
        if interval[0] <= median <= interval[1]:
            median_points_l.append(interval)
        elif interval[0] < median:
            intervals_left_of_median_l.append(interval)
        else:
            intervals_right_of_median_l.append(interval)

    median_points_r, intervals_left_of_median_r, intervals_right_of_median_r = [], [], []

    for interval in intervals_right:
        if interval[0] <= median <= interval[1]:
            median_points_r.append(interval)
        elif interval[1] < median:
            intervals_left_of_median_r.append(interval)
        else:
            intervals_right_of_median_r.append(interval)

    node = IntervalNode(median=median, median_points_left=median_points_l, median_points_right=median_points_r,
                        left_child=create_interval_tree(intervals_left_of_median_l, intervals_left_of_median_r),
                        right_child=create_interval_tree(intervals_right_of_median_l, intervals_right_of_median_r))
    return node


def query_internal_tree(root: IntervalNode, query_point: float) -> set:
    if not root:
        return set()

    result = set()
    if query_point <= root.median:
        for l_interval in root.median_points_left:
            if l_interval[0] <= query_point <= l_interval[1]:
                result.add(l_interval)
            else:
                break
        result = result.union(query_internal_tree(root.left_child, query_point))
    else:
        for r_interval in root.median_points_right:
            if r_interval[0] <= query_point <= r_interval[1]:
                result.add(r_interval)
            else:
                break
        result = result.union(query_internal_tree(root.right_child, query_point))

    return result


def main():
    # intervals = [(0, 1), (1, 5), (2, 20), (3, 4), (10, 12), (11, 18)]
    intervals = [(2, 4), (6, 12), (2, 4), (6, 12), (2, 8), (10, 12),
                 (2, 8), (10, 12)]
    # intervals = [(-5, 0), (1, 2), (4, 10), (5, 6), (7, 20), (15, 16)]
    intervals_left, intervals_right = sort_points_by_axes(intervals)
    interval_tree_root = create_interval_tree(intervals_left, intervals_right)
    print(interval_tree_root)
    print('Result: {}'.format(query_internal_tree(interval_tree_root, 3)))

if __name__ == '__main__':
    main()

