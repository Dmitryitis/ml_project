import numpy as np
import matplotlib.pyplot as plt
import itertools


def points_dist(a, b):
    return np.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def generate_points(n):
    points = []
    for i in range(n):
        points.append([np.random.randint(0, 100), np.random.randint(0, 100)])
    return points


def find_radius(n):
    x_sum, y_sum= 0, 0
    R = 0
    points = generate_points(n)
    for i in range(n):
        x_sum += points[i][0]
        y_sum += points[i][1]
    circle_center = [x_sum / len(points), y_sum / len(points)]
    for i in range(len(points)):
        R = max(R, points_dist(circle_center, points[i]))
    return R, circle_center, points


def find_centroids_for_circle(R, k, x_sum, y_sum):
    centroids = []
    for i in range(k):
        centroids.append([x_sum + R * np.cos(2 * np.pi * i / k), y_sum + R * np.sin(2 * np.pi * i / k)])
    return centroids


def set_points_to_cluster(points, centroids):
    cluster_points = [[] for i in range(len(centroids))]

    for i in range(len(points)):
        min = 120
        for j in range(len(centroids)):
            dist = points_dist(points[i], centroids[j])
            if dist < min:
                min = dist
        for j in range(len(centroids)):
            dist = points_dist(points[i], centroids[j])
            if min == dist:
                cluster_points[j].append(points[i])
    return cluster_points


def count_dist_sum_to_centroid(cluster_points, centroids):
    dist_to_all_centroids_sum = 0
    for i in range(len(cluster_points)):
        dist_to_centroids_sum = 0
        for j in range(len(cluster_points[i])):
            dist = points_dist(cluster_points[i][j], centroids[i])
            dist_to_centroids_sum += dist
        dist_to_all_centroids_sum += dist_to_centroids_sum
    return dist_to_all_centroids_sum


def find_k_number(k_max, n):
    res = find_radius(n)
    R, center, points = res[0], res[1], res[2]
    k_dist_sum = []
    for i in range(1, k_max):
        centroids = find_centroids_for_circle(R, i, center[0], center[1])
        cluster_points = set_points_to_cluster(points, centroids)
        dist_to_all_centroids_sum = count_dist_sum_to_centroid(cluster_points, centroids)
        k_dist_sum.append(dist_to_all_centroids_sum)
    min = 1000
    k = 0
    for i in range(1, len(k_dist_sum) - 1):
        res = (k_dist_sum[i] - k_dist_sum[i + 1]) / (k_dist_sum[i - 1] - k_dist_sum[i])
        res_abs = abs(res)
        if res_abs < min:
            min = res_abs

    for i in range(1, len(k_dist_sum) - 1):
        res = (k_dist_sum[i] - k_dist_sum[i + 1]) / (k_dist_sum[i - 1] - k_dist_sum[i])
        res_abs = abs(res)
        if res_abs == min:
            k = i + 1
    return k, R, center, points


def find_centroids(cluster_points, k):
    centroids = []
    for i in range(k):
        x_sum, y_sum = 0, 0
        for j in range(len(cluster_points[i])):
            x_sum += cluster_points[i][j][0]
            y_sum += cluster_points[i][j][1]
        center = [x_sum / len(cluster_points[i]), y_sum / len(cluster_points[i])]
        centroids.append(center)
    return centroids


def plotting(centroids, cluster_points):
    colors = itertools.cycle(['b', 'y', 'm', 'g', 'c', 'k'])
    for k in range(len(centroids)):
        plt.scatter([i[0] for i in cluster_points[k]], [i[1] for i in cluster_points[k]], color=next(colors))
    plt.scatter([i[0] for i in centroids], [i[1] for i in centroids], color='r')
    plt.axis('scaled')
    plt.draw()
    plt.show()


def program(n, k_max):
    try:
        all = find_k_number(k_max, n)
        k = all[0]
        R = all[1]
        center = all[2]
        points = all[3]
        print('k =', k)

        print('______________')
        centroids_for_circle = find_centroids_for_circle(R, k, center[0], center[1])
        print('circle-centroids =', centroids_for_circle)
        cluster_points = set_points_to_cluster(points, centroids_for_circle)
        print('clustered-points', cluster_points)
        print('______________')

        plt.scatter([i[0] for i in centroids_for_circle], [i[1] for i in centroids_for_circle], color='r')
        circle = plt.Circle((center[0], center[1]), R, color='r', fill=False)
        ax = plt.gca()
        ax.add_patch(circle)
        plotting(centroids_for_circle, cluster_points)
        plt.show()

        centroids_list = []
        centroids_list.append(centroids_for_circle)

        for i in range(1000):
            print('iteration =', i)
            centroids = find_centroids(cluster_points, k)
            print('centroids =', centroids)
            cluster_points = set_points_to_cluster(points, centroids)
            print('clustered-points =', cluster_points)
            print('______________')
            centroids_list.append(centroids)

            if centroids_list[i] == centroids_list[i + 1]:
                break

            plotting(centroids, cluster_points)
    except:
        program(n, k_max)

if __name__ == "__main__":
  n = 400
  k = 15
  program(n, k)