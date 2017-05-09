class Point:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x}, {self.y})'

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y


class Line:
    """
    Line passing through two given points.
    """
    def __init__(self, p1: Point, p2: Point):
        self.p1 = p1
        self.p2 = p2
        try:
            self.slope = (p1[1] - p2[1]) / (p1[0] - p2[0])
        except ZeroDivisionError:
            self.slope = 0

    def __repr__(self):
        return f'Line({self.p1}, {self.p2})'

    def __getitem__(self, item):
        if item == 0:
            return self.p1
        elif item == 1:
            return self.p2

    def is_point_above_line(self, point: Point) -> bool:
        y = self.slope * (point[0] - self.p1[0]) + self.p1[1]
        return point[1] > y

    def is_point_below_line(self, point: Point) -> bool:
        y = self.slope * (point[0] - self.p1[0]) + self.p1[1]
        return point[1] < y


class Polygon:
    def __init__(self, upper_chain: set, lower_chain: set):
        self.upper_chain = set(upper_chain) if upper_chain else set()
        self.lower_chain = set(lower_chain) if lower_chain else set()
        self.verticles = self.upper_chain.union(self.lower_chain)

    def __repr__(self):
        return f'Polygon({self.upper_chain}, {self.lower_chain})'

    def get_verticle_chain(self, verticle: Point):
        if verticle in self.upper_chain:
            return self.upper_chain
        elif verticle in self.lower_chain:
            return self.lower_chain

    def get_verticle_chain_label(self, verticle: Point):
        if verticle in self.upper_chain:
            return "upper"
        elif verticle in self.lower_chain:
            return "lower"


def sort_verticles_by_x(verticles: set):
    return sorted(verticles, key=lambda x: x[0])


def is_diagonal_possible(point1: Point, point2: Point, diagonal_point: Point, chain_label: str) -> bool:
    l = Line(point1, point2)
    if chain_label == 'lower':
        return l.is_point_above_line(diagonal_point)
    else:
        return l.is_point_below_line(diagonal_point)


def triangulate_polygon(polygon: Polygon) -> set:
    diagonals = set()

    verticles = sort_verticles_by_x(polygon.verticles)
    assert len(verticles) >= 3

    stack = [v for v in verticles[:2]]

    for i in range(2, len(verticles) - 1):
        if polygon.get_verticle_chain(verticles[i]) != polygon.get_verticle_chain(stack[-1]):
            for v in reversed(stack[1:]):
                diagonals.add((v, verticles[i]))
            stack = [stack[-1], verticles[i]]
        else:
            last_popped_verticle = stack.pop()
            for v in reversed(stack):
                if is_diagonal_possible(v, last_popped_verticle, verticles[i],
                                        polygon.get_verticle_chain_label(verticles[i])):
                    diagonals.add((v, verticles[i]))
                    last_popped_verticle = stack.pop()

            stack.append(last_popped_verticle)
            stack.append(verticles[i])

    for v in reversed(stack[1:-1]):
        diagonals.add((v, verticles[-1]))

    return diagonals


def main():
    # upper_chain = {Point(1, 2), Point(3, 4), Point(4, 3), Point(6, 5)}
    # lower_chain = {Point(2, 1), Point(5, 2), Point(7, 1), Point(9, 2)}

    # upper_chain = {Point(2, 8), Point(4, 6), Point(6, 5), Point(10, 8), Point(11, 6)}
    # lower_chain = {Point(0, 6), Point(1, 1), Point(3, 4), Point(5, 1), Point(8, 4)}

    # I
    # upper_chain = {Point(0, 10), Point(2, 14), Point(6, 18), Point(12, 20), Point(18, 18), Point(22, 14)}
    # lower_chain = {Point(1, 4), Point(5, 2), Point(11, 0), Point(17, 2), Point(21, 6), Point(24, 10)}

    # II
    upper_chain = {Point(2, 4), Point(3, 1), Point(4, 1), Point(5, 4), Point(6, 1), Point(7, 1), Point(8, 4),
                   Point(9, 1), Point(10, 1), Point(11, 4), Point(12, 1), Point(13, 1), Point(14, 4)}
    lower_chain = {Point(1, 0), Point(15, 0)}

    # III
    # upper_chain = {Point(0, 0), Point(4, 2), Point(8, 2), Point(11, 5), Point(14, 6), Point(15, 9), Point(18, 10), Point(19, 13),
    #                Point(22, 16), Point(23, 21), Point(24, 24)}
    # lower_chain = {Point(26, 0)}

    polygon = Polygon(upper_chain, lower_chain)
    diagonals = triangulate_polygon(polygon)
    for diag in diagonals:
        print(diag)


if __name__ == '__main__':
    main()
