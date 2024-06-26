from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from .main import emails_cleaned



clf = MultinomialNB(alpha=1.0, fit_prior=True)
