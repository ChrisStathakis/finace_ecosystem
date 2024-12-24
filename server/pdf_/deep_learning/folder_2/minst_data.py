import tensorflow as tf
import matplotlib.pyplot as plt

plt.gray()

mnist_dataset = tf.keras.datasets.mnist.load_data()
(X_train, y_train), (X_test, y_test) = mnist_dataset

image = X_train[0]

plt.imshow(image)
plt.show()

# 25