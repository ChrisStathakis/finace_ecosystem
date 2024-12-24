from sklearn import datasets
import numpy as np
from matplotlib import pyplot as plt
from copy import deepcopy
from sklearn.cluster import KMeans

iris = datasets.load_iris()
X = iris.data[:, 2:4]
y = iris.target

y_0 = np.where(y==0)
y_1 = np.where(y==1)
y_2 = np.where(y==2)

plt.scatter(X[y_0, 0], X[y_0, 1])
plt.scatter(X[y_1, 0], X[y_1, 1])
plt.scatter(X[y_2, 0], X[y_2, 1])


def visualize_centroids(X, centroids):
    plt.scatter(X[:, 0], X[:, 1])
    plt.scatter(centroids[:, 0], centroids[:, 1], marker="*", s=200, c="#050505")
    plt.show()


def dist(a, b):
    return np.linalg.norm(a - b, axis=1)


def assign_cluster(x, centroids):
    distances = dist(x, centroids)
    cluster = np.argmin(distances)
    return cluster


def update_centroids(X, centroids, clusters):
    for i in range(k):
        cluster_i = np.where(clusters == i)
        centroids[i] = np.mean(X[cluster_i], axis=0)


tol, max_iter = 0.0001, 10
iter, centroids_dif = 0, 100000
clusters = np.zeros(len(X))
k = 3
random_index = np.random.choice(range(len(X)), k)
centroids = X[random_index]

while iter < max_iter and centroids_dif > tol:
    for i in range(len(X)):
        clusters[i] = assign_cluster(X[i], centroids)
        centroids_prev = deepcopy(centroids)
        iter += 1
        centroids_dif = np.linalg.norm(centroids - centroids_prev)
        print(f"Iteration: {iter}")
        print(f"Centroids: {centroids}")
        print('Centroids move: {:5.4f}'.format(centroids_dif))
        visualize_centroids(X, centroids)


kmeans_sk = KMeans(n_clusters=3, random_state=42)
kmeans_sk.fit_transform(X)
clusters_sk = kmeans_sk.labels_
centroids_sk = kmeans_sk.cluster_centers_

