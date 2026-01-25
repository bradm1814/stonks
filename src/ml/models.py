from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

def make_baseline_model(model_type: str = 'logistic'):
    if model_type == "logistic":
        return LogisticRegression(max_iter=1000)
    elif model_type == "rf":
        return RandomForestClassifier(
            n_estimators=200,
            max_depth=5,
            random_state=42,
        )
    else:
        raise ValueError(f"Unknown model_type: {model_type}")