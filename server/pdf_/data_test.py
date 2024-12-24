import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np


class SentimentAnalyzer:
    def __init__(self, max_words=10000, max_len=200):
        self.max_words = max_words
        self.max_len = max_len
        self.tokenizer = Tokenizer(num_words=max_words)
        self.model = self._build_model()

    def _build_model(self):
        model = tf.keras.Sequential([
            tf.keras.layers.Embedding(self.max_words, 128),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=True)),
            tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(32)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.Dropout(0.5),
            tf.keras.layers.Dense(1, activation='sigmoid')
        ])

        model.compile(optimizer='adam',
                      loss='binary_crossentropy',
                      metrics=['accuracy'])
        return model

    def train(self, texts, labels, validation_split=0.2, epochs=15):
        self.tokenizer.fit_on_texts(texts)
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len)

        return self.model.fit(
            padded_sequences,
            np.array(labels),
            validation_split=validation_split,
            epochs=epochs
        )

    def predict(self, texts):
        sequences = self.tokenizer.texts_to_sequences(texts)
        padded_sequences = pad_sequences(sequences, maxlen=self.max_len)
        predictions = self.model.predict(padded_sequences)
        return [(text, "positive" if pred > 0.5 else "negative", float(pred))
                for text, pred in zip(texts, predictions)]


# Example usage
texts = [
    "This is amazing!",
    "I hate this product",
    "Pretty good experience"
]
labels = [1, 0, 1]  # 1 for positive, 0 for negative

analyzer = SentimentAnalyzer()
analyzer.train(texts, labels)

# Predict new texts
results = analyzer.predict(["This is great!", "Very disappointing"])
for text, sentiment, confidence in results:
    print(f"Text: {text}")
    print(f"Sentiment: {sentiment} (Confidence: {confidence:.2f})\n")