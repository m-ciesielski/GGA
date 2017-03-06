import pytest

from closest_pair_of_points import find_closest_points_naive, find_closest_points, sort_points_by_axes


# Zbiory testowe, pierwszy i drugi element zbioru to para najbliższych punktów
TEST_SETS = [
    [(7, 5), (6, 7), (3, 3), (0, 1), (4, 9), (10, 0), (0, 10)],
    [(0, 0), (1, 1), (8, 9), (3, 7), (9, 0), (6, 6), (1, 8)],
    [(5, 6), (6, 5), (0, 1), (2, 3), (10, 12), (15, 16), (3, 10)],
    [(5, 6), (6, 5)],
]


@pytest.fixture(params=TEST_SETS)
def points_with_closest_pair(request):
    """
    :return: Krotka zawierająca parę najbliższych punktów oraz pełny zbiór punktów.
     (set(najbliższe punkty), [pełny zbiór])
    """
    points = request.param
    return set(points[:2]), points


def test_find_closest_points_naive(points_with_closest_pair):
    closest_pair, points = points_with_closest_pair
    _, found_closest_pair = find_closest_points_naive(points)
    assert set(found_closest_pair) == closest_pair


def test_find_closest_points(points_with_closest_pair):
    closest_pair, points = points_with_closest_pair
    sorted_points = sort_points_by_axes(points)
    _, found_closest_pair = find_closest_points(sorted_points)
    assert set(found_closest_pair) == closest_pair
