import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import confusion_matrix, precision_score, recall_score, f1_score, classification_report
import glob
import os

from pdf_.folder_3.utilities import is_letter_only, clean_text


cv = CountVectorizer(stop_words=None,
                     max_features=1000,
                     # max_df=2,
                     # min_df=0.5
                     )

emails, labels = [], []


for filename in glob.glob(os.path.join("enron1/spam", "*.txt")):
    with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
        emails.append(infile.read())
        labels.append(1)


for filename in glob.glob(os.path.join("enron1/ham", "*.txt")):
    with open(filename, "r", encoding="utf-8", errors="ignore") as infile:
        emails.append(infile.read())
        labels.append(0)


email_cleaned = clean_text(emails)
docs_cv = cv.fit_transform(email_cleaned)
# print(docs_cv[0])  # (row index, term index) term_frequency

terms = cv.get_feature_names_out()


X_train, X_test, Y_train, Y_test = train_test_split(
    email_cleaned, labels, test_size=0.33, random_state=42
)

terms_doc_train = cv.fit_transform(X_train)
terms_doc_test = cv.fit_transform(X_test)

clf = MultinomialNB(alpha=1.0, fit_prior=True)
clf.fit(terms_doc_train, Y_train)

prediction_prob = clf.predict_proba(terms_doc_test)
prediction = clf.predict(terms_doc_test)
print(prediction_prob[0:10])

accuracy = clf.score(terms_doc_test, Y_test)
print(f"Accuracy: {accuracy*100} %")
con_matrix = confusion_matrix(Y_test, prediction, labels=[0, 1])
classsification_accurancy = ((con_matrix[0][0] + con_matrix[0][1])/(con_matrix[0][0] + con_matrix[0][1] +
                                                                   con_matrix[1][0] + con_matrix[1][0]
                                                                   )) * 100


print(f"Classification Accurancy: {classsification_accurancy} %")
print(f"Classification Report:{classification_report(Y_test, prediction) * 100}")
precision = (con_matrix[1][1]/(con_matrix[1][1] + con_matrix[0][1])) * 100
print(f"Precision: {precision} %")
print(f"Precision score: {precision_score(Y_test, prediction, pos_label=1)*100} %")

print(recall_score(Y_test, prediction, pos_label=1))
print(f1_score(Y_test, prediction, pos_label=1))

k = 10
k_fold = StratifiedKFold(n_splits=k, random_state=42)
cleaned_emails_np = np.array(email_cleaned)
labels_np = np.array(labels)

max_features_option = [2000, 8000, None]
smoothing_factor_option = [0.5, 1.0, 2.0, 4.0]
fit_prior_option = [True, False]
auc_record = {}

# 133