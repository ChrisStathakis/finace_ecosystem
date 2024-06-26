import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from keras.preprocessing.sequence import pad_sequences
from testing_folder.real_python.text import Tokenizer
from testing_folder.real_python.main2 import sentences_train, sentences_test, X_test, X_train, y_train, y_test, plot_history
from keras.models import Sequential
from keras import layers

cities = ['London', 'Berlin', 'Berlin', 'New York', 'London']

encoder = LabelEncoder()
city_labels = encoder.fit_transform(cities)
print(city_labels)

encoder = OneHotEncoder(sparse_output=False)
city_labels = city_labels.reshape((5, 1))
print(encoder.fit_transform(city_labels))

tokenizer = Tokenizer(num_words=5000)
tokenizer.fit_on_texts(sentences_train)
print(tokenizer.word_index)

X_train = tokenizer.texts_to_sequences(sentences_train)
X_test = tokenizer.texts_to_sequences(sentences_test)

vocab_size = len(tokenizer.word_index) + 1
print("Size: ", vocab_size)

maxlen = 100

X_train = pad_sequences(X_train, padding='post', maxlen=maxlen)
X_test = pad_sequences(X_test, padding='post', maxlen=maxlen)

print(X_train[0, :])

embedding_dim = 50
model = Sequential()
model.add(
    layers.Embedding(input_dim=vocab_size,
                     output_dim=embedding_dim,
                     input_length=maxlen
                     )
)
model.add(layers.Flatten())
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy']
              )

print(model.summary())

history = model.fit(X_train, y_train,
                    epochs=20,
                    verbose=False,
                    validation_data=(X_test, y_test),
                    batch_size=10
                    )

loss, accuracy = model.evaluate(X_train, y_train, verbose=False)
print("Training Accuracy: {:.4f}".format(accuracy))
loss, accuracy = model.evaluate(X_test, y_test, verbose=False)
print("Testing Accuracy:  {:.4f}".format(accuracy))

# plot_history(history)


def create_embedding_matrix(filepath, word_index, embedding_dim):
    vocab_size = len(word_index) + 1
    embedding_matrix = np.zeros((vocab_size, embedding_dim))
    with open(filepath, encoding="utf8") as f:

        for line in f:
            try:
                word, *vector = line.split()
                if word in word_index:
                    idx = word_index[word]
                    embedding_matrix[idx] = np.array(
                        vector, dtype=np.float32
                    )[:embedding_dim]
            except:
                print('ERROR!!')
                continue
    return embedding_matrix


embedding_matrix = create_embedding_matrix(
    'data/glove.6B.50d.txt',
    tokenizer.word_index,
    embedding_dim
)

model = Sequential()
model.add(layers.Embedding(vocab_size, embedding_dim,
                           weights=[embedding_matrix],
                           input_length=maxlen,
                           trainable=False))
model.add(layers.GlobalMaxPool1D())
model.add(layers.Dense(10, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))
model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
model.summary()