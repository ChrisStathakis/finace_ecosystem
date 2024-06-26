import numpy as np
from sklearn import datasets
from sklearn import preprocessing
from sklearn.neural_network import MLPRegressor
from sklearn.datasets import fetch_california_housing


nn_scikit = MLPRegressor(hidden_layer_sizes=(20, 8),
                         activation="logistic",
                         solver="lbfgs",
                         learning_rate_init=0.1,
                         random_state=42,
                         max_iter=2000

                         )


scaler = preprocessing.StandardScaler()
boston = fetch_california_housing()
num_test = 10

X_train = boston.data[:-num_test, :]
X_train = scaler.fit_transform(X_train)
y_train = boston.target[:-num_test].reshape(-1, 1)
X_test = boston.data[-num_test:, :]
X_test = scaler.transform(X_test)
y_test = boston.target[-num_test:]

nn_scikit.fit(X_train, y_train)
predictions = nn_scikit.predict(X_test)

print(predictions)


