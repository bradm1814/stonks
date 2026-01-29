from xgboost import XGBClassifier, XGBRegressor

def make_baseline_model(model_type: str = 'logistic'):
    # choose model type
    if model_type == "xgb_class":
        model = XGBClassifier(
            n_estimators=300,
            max_depth=5,
            learning_rate = 0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="binary:logistic",
            eval_metric="logloss",
            n_jobs=-1
        )
    elif model_type == "xgb_reg":
        model = XGBRegressor(
            n_estimators=300,
            max_depth=5,
            learning_rate = 0.05,
            subsample=0.8,
            objective="reg:squarederror",
            eval_metric="logloss",
            n_jobs=-1
        )
    else:
        raise ValueError("model_type must be xgb_class or xgb_reg")
    
    return model