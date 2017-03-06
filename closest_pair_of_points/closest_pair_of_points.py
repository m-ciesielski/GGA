import argparse
import math


def distance(point_a, point_b):
    return math.sqrt((point_a[0] - point_b[0]) ** 2 + (point_a[1] - point_b[1]) ** 2)


def find_closest_points_naive(points):
    """
    Naiwny algorytm wyznaczający parę najbliższych punktów w podanym zbiorze. Złożoność obliczeniowa: O(n**2).
    :param points: Lista punktów w postaci dwuelementowych krotek.
    :return: Dwuelementowa krotka zawierająca najkrótszy dystans między punktami oraz parę najbliższych punktów.
    """
    min_distance = None
    closest_points = None
    for i in range(len(points) - 1):
        for j in range(i + 1, len(points)):
            point_a, point_b = points[i], points[j]
            dist = distance(point_a, point_b)
            if not min_distance or dist < min_distance:
                min_distance = dist
                closest_points = (point_a, point_b)
    return min_distance, closest_points


def sort_points_by_axes(points):
    """
    Sortowanie listy punktów wg współrzędnych x i y. Złożoność obliczeniowa: O(n log n).
    :param points: Lista krotek zawierających współrzędne punktów - [(x1, y1), (x2, y2),..., (xn, yn)]
    :return: Krotka zawierająca listę punktów posortowanych leksykograficznie wg współrzędnej x oraz
             listę punktów posortowanych wg współrzędnej y - ([punkty posortowane wg x], [punkty posortowane wg y])
    """
    points_sorted_by_x = sorted(points, key=lambda point: (point[0], point[1]))
    points_sorted_by_y = sorted(points, key=lambda point: point[1])
    return points_sorted_by_x, points_sorted_by_y


def find_closest_points(sorted_points):
    """
    Znajduje parę najbliższych punktów w zbiorze sorted_points w czasie O(n log n).
    :param sorted_points: Dwuelementowa krotka zawierająca listę punktów posortowanych wg współrzędnej x oraz listę
    punktów posortowanych wg współrzędnej y.
    :return: Dwuelementowa krotka zawierająca najkrótszy dystans między punktami oraz parę najbliższych punktów.
    """
    points_sorted_by_x = sorted_points[0]
    points_sorted_by_y = sorted_points[1]

    # Jeśli w zbiorze są tylko 3 punkty, znajdujemy parę najbliższych punktów metodą naiwną
    if len(points_sorted_by_x) <= 3:
        return find_closest_points_naive(points_sorted_by_x)

    # Dzielimy zbiór wejściowy na pół względem współrzędnej x
    left_points_sorted_by_x = points_sorted_by_x[:len(points_sorted_by_x) // 2]
    right_points_sorted_by_x = points_sorted_by_x[len(points_sorted_by_x) // 2:]

    # Zmienna dividing line przechowuję współrzędną osi X względem której dokonano podziału na dwa zbiory
    dividing_line = left_points_sorted_by_x[-1][0]

    # Wyznaczamy zbiory posortowane wg współrzędnej y odpowiadające podziałowi zbioru względem współrzędnej x
    left_points_sorted_by_y = [p for p in points_sorted_by_y if p[0] <= dividing_line]
    right_points_sorted_by_y = [p for p in points_sorted_by_y if p[0] > dividing_line]

    left_points = (left_points_sorted_by_x, left_points_sorted_by_y)
    right_points = (right_points_sorted_by_x, right_points_sorted_by_y)

    # Znajdujemy najbliższą parę punktów w obu zbiorach
    left_min_distance, left_closest_points = find_closest_points(left_points)
    right_min_distance, right_closest_points = find_closest_points(right_points)

    # Wyznaczamy najmniejszy dystans i najbliższą parę punktów w lewym i prawym zbiorze
    closest_distance, closest_points = min((left_min_distance, left_closest_points),
                                           (right_min_distance, right_closest_points),
                                           key=lambda p: p[0])

    # Zbiór middle_points przechowuje punkty, które znajdują się w odległości closest_distance,
    # określonej przez najmniejszy dystans między punktami w lewym i prawym zbiorze, od linii podziału zbiorów.
    middle_points = [p for p in points_sorted_by_x if abs(p[0] - dividing_line) <= closest_distance]
    left_middle_points = [p for p in middle_points if (p[0] - dividing_line) <= 0]
    right_middle_points = [p for p in middle_points if (p[0] - dividing_line) > 0]

    # Indeksy wskazujące na następny niesprawdzony punkt w zbiorach left_middle_points i right_middle_points
    left_middle_points_v_index = 0
    right_middle_points_v_index = 0

    for point in middle_points:
        # Sprawdzamy po której strony linii przecięcia leży punkt, zmienna neighbour_points zawiera listę
        # punktów po przeciwległej stronie linii przecięcia
        if (point[0] - dividing_line) <= 0:
            neighbour_points = right_middle_points
            neighbour_v_index = right_middle_points_v_index
            left_middle_points_v_index += 1
        else:
            neighbour_points = left_middle_points
            neighbour_v_index = left_middle_points_v_index
            right_middle_points_v_index += 1

        # Porównujemy punkt z czteroma sąsiadami po przeciwległej stronie linii podziału
        for neighbour_point in [p for p in neighbour_points if p][neighbour_v_index:neighbour_v_index + 4]:
            dist = distance(point, neighbour_point)
            if dist < closest_distance:
                closest_distance = dist
                closest_points = (point, neighbour_point)

    return closest_distance, closest_points


def arg_point(s):
    try:
        s = s.replace('(', '')
        s = s.replace(')', '')
        x, y = map(int, s.split(','))
        return x, y
    except:
        raise argparse.ArgumentTypeError('Podaj listę punktów w formacie (x1,y1) (x2,y2) ... (xn,yn)')


def parse_args():
    parser = argparse.ArgumentParser(description='Wyznacza parę najbliższych punktów w podanym zbiorze.')
    parser.add_argument('points', metavar='point', type=arg_point, nargs='+',
                        help='Lista punktów należących do zbioru. \n'
                             'Podaj listę punktów w formacie'
                             ' (x1,y1) (x2,y2) ... (xn,yn)')
    return parser.parse_args()


def main():
    args = parse_args()
    points = args.points
    print(find_closest_points(sort_points_by_axes(points)))


if __name__ == '__main__':
    main()
