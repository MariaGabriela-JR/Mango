# core/metrics.py
from sklearn.metrics import accuracy_score, f1_score

def real_knn_metrics(y_true, y_pred):
    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average="weighted", zero_division=0)
    return acc, f1

