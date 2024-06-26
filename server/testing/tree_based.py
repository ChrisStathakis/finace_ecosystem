import matplotlib.pyplot as plt
import numpy as np

pos_fraction = np.linspace(0.00, 1.00, 1000)
gini = 1 - pos_fraction**2 - (1-pos_fraction)**2
ent = -  (pos_fraction * np.log2(pos_fraction) + (1 - pos_fraction) * np.log2(1 - pos_fraction))


plt.plot(pos_fraction, ent)
plt.ylim(0, 1)
plt.xlabel("Positive fraction")
plt.ylabel("Gini Impurity")
# plt.show()


def gini_impurity(labels):
    if not labels:
        return 0
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return 1 - np.sum(fractions ** 2)


def entropy(labels):
    if not labels:
        return 0
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return - np.sum(fractions * np.log2(fractions))


labels = [1, 0, 0, 1, 0]
print("Gini", gini_impurity(labels))
print("Entropy", entropy(labels))

criterion_function = {
    "gini": gini_impurity,
    "entropy": entropy
}



def gini_impurity_np(labels):
    if labels.size == 0:
        return 0
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return 1 - np.sum(fractions ** 2)


def entropy_np(labels):
    if labels.size == 0:
        return 0
    counts = np.unique(labels, return_counts=True)[1]
    fractions = counts / float(len(labels))
    return - np.sum(fractions * np.log2(fractions))


criterion_function_np = {
    "gini": gini_impurity_np,
    "entropy": entropy_np
}

def weighted_impurity(groups, criterion="gini"):
    total = sum(len(group) for group in groups)
    weighted_sum = 0.0
    for group in groups:
        weighted_sum += len(group) / float(total) * criterion_function_np[criterion](group)

    return weighted_sum


def split_node(X: np.ndarray, y: np.ndarray, index: int, value: any):
    x_index = X[:, index]
    if X[0, index].dtype.kind in ['i', "f"]:
        mask = x_index >= value
    else:
        mask = x_index == value

    left = [X[~mask, :], y[~mask]]
    right = [X[mask, :] ,y[mask]]
    return left, right


def get_best_split(X, y, criterion):
    best_index, best_value, best_score, children = None, None, 1, None

    for index in range(len(X[0])):
        for value in np.sort(np.unique(X[:, index])):
            groups = split_node(X, y, index, value)
            impurity = weighted_impurity(groups[0][1], groups[1][1], criterion)
            if impurity < best_score:
                best_index, best_value, best_score, children = index, value, impurity, groups
    return {
        "index": best_index,
        "value": best_value,
        "children": children
    }

# 200

def get_leaf(labels):
    return np.bincount(labels).argmax()


def split(node, max_depth, min_size, depth, criterion):
    left, right = node['children']
    del (node['children'])
    if left[1].size == 0:
        node['right'] = get_leaf(right[1])
        return
    if right[1].size == 0:
        node['left'] = get_leaf(left[1])
        return

    if depth >= max_depth:
        node['le']


children_1 = [[1, 0, 1], [0, 1]]
children_2 = [[1, 1], [0, 0, 1]]

print("Entropy Spit 1: ", weighted_impurity(children_1, "entropy"))