import pytest

from kd_tree import Area, kdtree, sort_points_by_axes, query_kdtree

TEST_SETS = [
    {
        'points': [(7, 5), (6, 7), (3, 3), (0, 1), (4, 9), (10, 0), (0, 10)],
        'query_areas': [Area(x_min=3, x_max=4, y_min=0, y_max=9)],
        'query_results': [{(3, 3), (4, 9)}]
     },
    {
        'points': [(0, 0), (1, 1), (8, 9), (3, 7), (9, 0), (6, 6), (1, 8)],
        'query_areas': [Area(x_min=0, x_max=8, y_min=0, y_max=6)],
        'query_results': [{(0, 0), (1, 1), (6, 6)}]
    }
    ,
    {
        'points': [(5, 6), (6, 5), (0, 1), (2, 3), (10, 12), (15, 16), (3, 10)],
        'query_areas': [Area(x_min=10, x_max=15, y_min=12, y_max=16)],
        'query_results': [{(10, 12), (15, 16)}]
    }
    ,
    {
        'points': [(5, 6), (6, 5)],
        'query_areas': [Area(x_min=0, x_max=5, y_min=0, y_max=10), Area(x_min=7, x_max=7, y_min=5, y_max=6)],
        'query_results': [{(5, 6)}, set()]
    }

]


@pytest.fixture(params=TEST_SETS)
def points_with_query_areas(request):
    return request.param


def test_query_kdtree(points_with_query_areas):
    sorted_points_x, sorted_points_y = sort_points_by_axes(points_with_query_areas['points'])
    tree = kdtree(sorted_points_x, sorted_points_y)

    for query_area, query_result in zip(points_with_query_areas['query_areas'],
                                        points_with_query_areas['query_results']):
            assert {r.point for r in query_kdtree(tree, query_area)} == query_result
