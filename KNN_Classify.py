from sklearn import datasets
from sklearn.neighbors import KNeighborsClassifier
import numpy as np
import matplotlib.pyplot as plt
import random
import scipy.stats as ss
"""
I implemented a custom K Nearest Neighbor Classify and compared the resutls with sklearn knn imlementation
"""

def distance(p1, p2):
    """
    Compute the Eucliden distance between n dimensional vectors
    p1 and p2
    """
    return np.sqrt(np.sum(np.power(p1-p2, 2)))


def majority_vote(votes):
    """
    Input: A list of vote 
    Output: Return the item with the highest counts
    """
    vote_counts = {}
    for vote in votes:
        if vote in vote_counts:
            vote_counts[vote] += 1
        else:
            vote_counts[vote] = 1

    winners = []
    max_counts = max(vote_counts.values())
    for vote, count in vote_counts.items():
        if count == max_counts:
            winners.append(vote)

    return random.choice(winners)


def majority_vote_v2(vote):
    """ Anothe version of find the item in a list with higeest count """

    vote, counts = ss.mstats.mode(vote)

    return random.choice(vote)


def find_nearest_nbrs(p, points, k=5):
    """ Returns indices of the k nearest neighbors """

    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i] = distance(points[i], p)

    ind = np.argsort(distances)
    return ind[:k]


def knn_predict(p, points, outcomes, k=5):
    """Precict the class point p belongs """

    ind = find_nearest_nbrs(p, points, k)

    return majority_vote(outcomes[ind])

# Generating synthetic data


def generate_synth_data(n=50):
    """
    """
    # predictors

    points = np.concatenate(
        (ss.norm(0, 1).rvs((n, 2)), ss.norm(1, 1).rvs((n, 2))), axis=0)

    # outcomes
    outcomes = np.concatenate((np.repeat(0, n), np.repeat(1, n)), axis=0)
    return (points, outcomes)


def make_prediction_grid(predictors, outcomes, limits, h, k):
    """ Classify each point on the prediction grid """
    (xmin, xmax, ymin, ymax) = limits

    xs = np.arange(xmin, xmax, h)
    ys = np.arange(ymin, ymax, h)
    xx, yy = np.meshgrid(xs, ys)

    prediction_grid = np.zeros(xx.shape, dtype=int)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            p = np.array([x, y])
            prediction_grid[j, i] = knn_predict(p, predictors, outcomes, k)

    return (xx, yy, prediction_grid)


def plot_prediction_grid(xx, yy, prediction_grid,  predictors, outcomes, filename):
    """ Plot KNN predictions for every point on the grid."""

    from matplotlib.colors import ListedColormap

    background_colormap = ListedColormap(
        ["hotpink", "lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap(["red", "blue", "green"])
    plt.figure(figsize=(10, 10))
    plt.pcolormesh(xx, yy, prediction_grid,
                   cmap=background_colormap, alpha=0.5)
    plt.scatter(predictors[:, 0], predictors[:, 1],
                c=outcomes, cmap=observation_colormap, s=50)
    plt.xlabel('Variable 1')
    plt.ylabel('Variable 2')
    plt.xticks(())
    plt.yticks(())
    plt.xlim(np.min(xx), np.max(xx))
    plt.ylim(np.min(yy), np.max(yy))
    plt.savefig(filename)
    plt.show()


# =============================================================================
# Using my KNN predictor on real data sets and comparing it accuracy with
#   sklearn classify
# =============================================================================
if __name__ == '__main__':
    iris = datasets.load_iris()

    predictors = iris.data[:, 0:2]
    outcomes = outcomes = iris.target

    plt.plot(predictors[outcomes == 0][:, 0],
             predictors[outcomes == 0][:, 1], 'ro')
    plt.plot(predictors[outcomes == 1][:, 0],
             predictors[outcomes == 1][:, 1], 'bo')
    plt.plot(predictors[outcomes == 2][:, 0],
             predictors[outcomes == 2][:, 1], 'mo')

    plt.savefig('dataset.png')

    # testing KNN_predict on datasets

    k = 5
    filename = 'iris_grid.png'
    limits = (4, 8, 1.5, 4.5)
    h = 0.1
    (xx, yy, prediction_grid) = make_prediction_grid(
        predictors, outcomes, limits, h, k)
    plot_prediction_grid(xx, yy, prediction_grid,
                         predictors, outcomes, filename)

    # Using sklearn KNeighborsClassifier on datasets
    knn = KNeighborsClassifier(n_neighbors=5)
    knn.fit(predictors, outcomes)
    sk_predictions = knn.predict(predictors)

    my_predictions = np.array(
        [knn_predict(p, predictors, outcomes) for p in predictors])

    sk_predictions == my_predictions

    # Compute % of agreeement
    print(
        f'sk_knn and custom_knn agree by: {100*np.mean(sk_predictions == my_predictions)}')

    # Compute frequently my predictions and sklearn prediction equal to actual outcome

    print(f'custom_knn_accuracy: {100*np.mean(sk_predictions == outcomes)}')
    print(f'sk_knn_accuracy: {100*np.mean(my_predictions == outcomes)}')
