from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

def make_baseline_model(model_type: str = 'logistic'):
    # choose model type
    if model_type == "regression":
        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=6,
            random_state=42
        )
    elif model_type == "classification":
        model = RandomForestClassifier(
            n_estimators=300,
            max_depth=6,
            random_state=42
        )
    else:
        raise ValueError("model_type must be regression or classification")
    
    return model