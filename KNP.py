import math
import random
from enum import Enum

import numpy as np
import pygame


class Color(Enum):
    BLACK = 'black'


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
        return f'Point({self.x}, {self.y}, {self.color})'

    def __repr__(self):
        return f'Point({self.x}, {self.y}, {self.color})'

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), 10)

    def is_isolation(self):
        return not self.distances

    def set_color(self, color):
        self.color = color

    def dist(self, point):
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def add_distance(self, point):
        dist = self.dist(point)
        self.distances[point] = dist
        self.distances = dict(sorted(self.distances.items(), key=lambda x: x[1]))


class Edge():
    def __init__(self, pair_point):
        self.point1 = pair_point[0]
        self.point2 = pair_point[1]

    def __str__(self):
        return f'Edge: ({self.point1.x},{self.point1.y}),({self.point2.x},{self.point2.y}), dist: {self.edge_dist}'

    def __hash__(self):
        return hash((self.point1.x, self.point1.y, self.point2.x, self.point2.y))

    @property
    def get_points(self):
        return [self.point1, self.point2]

    @property
    def edge_dist(self):
        return np.sqrt((self.point1.x - self.point2.x) ** 2 + (self.point1.y - self.point2.y) ** 2)

    def draw_edge(self, screen):
        pygame.draw.line(screen, (0, 0, 0), [self.point1.x, self.point1.y], [self.point2.x, self.point2.y], 4)


def add_edge(pair_point):
    pair_point[0].add_distance(pair_point[1])
    pair_point[1].add_distance(pair_point[0])
    edge = Edge(pair_point)

    edges.append(edge)


def has_isolation_point():
    flag = False
    for point in points_copy:
        if point.is_isolation():
            flag = True
            break

    return flag


def get_random_color():
    return tuple(random.randint(16, 253) for _ in range(3))


def get_isolation_point():
    isolation_point = None
    for point in points_copy:
        if point.is_isolation():
            isolation_point = point
            break

    return isolation_point


def dist_points():
    isolation_point = get_isolation_point()
    min_pair_point = None
    min_dist_points = math.inf

    for point in points_copy:
        if point != isolation_point and not point.is_isolation() and point.dist(isolation_point) < min_dist_points:
            min_pair_point = [isolation_point, point]
            min_dist_points = point.dist(isolation_point)

    if min_pair_point is not None:
        add_edge(min_pair_point)


def has_element_in_group(group):
    flag = False
    for item in new_edges[0]:
        if item.get_points[0] in group or item.get_points[1] in group:
            flag = True

    return flag


def set_groups(delete_edges):
    while len(delete_edges) != 0:
        cur_edge = delete_edges[0]
        cur_edge_point = cur_edge.get_points
        color = get_random_color()
        group = set()

        cur_point_1 = cur_edge_point[0]
        cur_point_1.set_color(color)

        cur_point_2 = cur_edge_point[1]
        cur_point_2.set_color(color)

        group.add(cur_point_1)
        group.add(cur_point_2)
        del delete_edges[0]

        while has_element_in_group(group):
            for idx,item in enumerate(delete_edges):
                if item.get_points[0] in group:
                    point_group = item.get_points[1]
                    point_group.set_color(color)

                    group.add(point_group)
                    del delete_edges[idx]
                elif item.get_points[1] in group:
                    point_group = item.get_points[0]
                    point_group.set_color(color)

                    group.add(point_group)
                    del delete_edges[idx]
        print(group)
        groups.append(list(group))


def clusterize(clusters):
    min_pair_point = None
    min_dist_points = math.inf

    for point1 in points_copy:
        for point2 in points_copy:
            if point1 != point2 and point1.dist(point2) < min_dist_points:
                min_pair_point = [point1, point2]
                min_dist_points = point1.dist(point2)

    if min_pair_point is not None:
        add_edge(min_pair_point)

        while has_isolation_point():
            dist_points()

        for edge in edges:
            edge.draw_edge(screen)


        sorted_edges = sorted(edges, key=lambda x: x.edge_dist, reverse=True)
        del sorted_edges[0:clusters]

        new_edges.append(sorted_edges)

        for edge in new_edges[0]:
            edge.draw_edge(screen)

        pygame.display.update()
        pygame.display.flip()
        pygame.event.pump()
        pygame.time.wait(1000)

        set_groups(new_edges[0])
        print(groups)


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((700, 500))
    pygame.display.set_caption('knp')
    font = pygame.font.Font(None, 30)

    exit = False
    points = []
    points_copy = []

    edges = []
    new_edges = []
    k = 5

    groups = []
    points_count = 0

    while not exit:
        screen.fill((255, 255, 255))

        if len(points) == points_count:
            for point in points:
                point.draw(screen)

            if len(groups) > 0:
                for group in groups:
                    for point in group:
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
                pygame.display.update()
                print(points_count)

            if event.type == pygame.KEYDOWN:
                points_copy += points
                points_copy = list(set(points_copy))
                if event.key == pygame.K_RETURN and len(points) == points_count:
                    clusterize(k)
                    pygame.display.update()

    pygame.display.quit()
