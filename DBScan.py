from enum import Enum
import pygame
import numpy as np


class Color(Enum):
    BLACK = 'black'
    RED = 'red'
    GREEN = 'green'
    YELLOW = 'yellow'
    WHITE = 'white'


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = Color.BLACK.value
        self.distances = {}

    def __eq__(self, other_point):
        if self.color == other_point.color and self.x == other_point.x and self.y == other_point.y:
            return True
        else:
            return False

    def __hash__(self):
        return hash((self.x, self.y, self.color))

    def __str__(self):
        return f'Point({self.x}, {self.y}, {Color(self.color)})'

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {Color(self.color)})'

    def set_color(self, color):
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

    def dist(self,point):
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    # У точки высчитываем расстояния до других точек, сортируем до ближайших
    def add_distance(self, point):
        dist = self.dist(point)
        self.distances[point] = dist
        self.distances = dict(sorted(self.distances.items(), key=lambda x: x[1]))

    def get_neighbours(self, dist):
        neighbours = []
        for element, point_dist in self.distances.items():
            if point_dist <= dist:
                neighbours.append(element)

        return neighbours


def clusterize():
    for point1 in points_copy:
        for point2 in points_copy:
            if point1 != point2 and point2 not in point1.distances:
                point1.add_distance(point2)

            if point1 != point2 and point1 not in point2.distances:
                point2.add_distance(point1)

    while len(points_copy) != 0:
        for point in points_copy:
            if len(point.get_neighbours(eps)) < minPts:
                singles.append(point)
                points_copy.remove(point)
            else:
                points_copy.remove(point)
                point.set_color(Color.GREEN.value)
                group = [point]
                for n in point.get_neighbours(eps):
                    if n in singles or len(n.get_neighbours(eps)) < minPts:
                        if n in singles:
                            singles.remove(n)
                        n.set_color(Color.YELLOW.value)
                        group.append(n)
                        if n in points_copy:
                            points_copy.remove(n)
                    if len(n.get_neighbours(eps)) >= minPts:
                        n.set_color(Color.GREEN.value)
                        group.append(n)
                        if n in points_copy:
                            points_copy.remove(n)

                groups.append(group)

    for single in singles:
        single.set_color(Color.RED.value)

    # Проверка на объединение,
    # Объединаем в одну если пересекаются
    for group1 in groups:
        for group2 in groups:
            if group1 != group2:
                c = list(set(group1) & set(group2))
                if len(c) > 0:
                    group1 += group2
                    groups.remove(group2)

    for group in groups:
        x_sum = sum([point.x for point in group])
        y_sum = sum([point.y for point in group])
        count_points = len(group)

        centroid = [int(x_sum / count_points), int(y_sum / count_points)]
        max_centroid_dist = 0

        for point in group:
            dist = np.sqrt((point.x - centroid[0]) ** 2 + (point.y - centroid[1]) ** 2)
            if max_centroid_dist < dist:
                max_centroid_dist = dist

        centroid.append(max_centroid_dist + 5)
        centroids.append(centroid)

    colors = {
        0: 'violet',
        1: 'blue',
        2: 'yellow',
        3: 'green',
        4: 'black',
        5: 'brown',
    }

    for idx, group in enumerate(groups):
        for point in group:
            point.color = colors[idx]


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('dbscan')
    font = pygame.font.Font(None, 30)

    exit = False
    points = []
    points_copy = []
    groups = []
    singles = []
    centroids = []
    eps = 100
    minPts = 3
    points_count = 0

    while not exit:
        screen.fill((255, 255, 255))

        if len(points_copy) == points_count:
            for point in points:
                point.draw(screen)
        else:
            for center in centroids:
                pygame.draw.circle(screen, Color.BLACK.value, (center[0], center[1]), center[2])
                pygame.draw.circle(screen, Color.WHITE.value, (center[0], center[1]), center[2] - 2)
                pygame.draw.circle(screen, Color.BLACK.value, (center[0], center[1]), 1)

            for group in groups:
                for point in group:
                    point.draw(screen)

            for point in singles:
                point.draw(screen)

            for point in points:
                point.draw(screen)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit = True
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                coors = event.pos
                point = Point(coors[0], coors[1])
                points.append(point)
                points_copy.append(point)
                point.draw(screen)
                points_count += 1
                print(points_count)

            if event.type == pygame.KEYDOWN:
                points_copy += points
                points_copy = list(set(points_copy))
                if event.key == pygame.K_RETURN and len(points) == points_count:
                    clusterize()
                    pygame.display.update()

    pygame.display.quit()