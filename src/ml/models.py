from xgboost import XGBClassifier, XGBRegressor

def make_baseline_model(model_type: str = 'logistic'):
    # choose model type
    if model_type == "xgb_class":
        model = XGBClassifier(
            n_estimators=300, # this is number of boosted trees in the model
            max_depth=5, # this is how deep each individual tree is too deep and it overfits. 5 is very conservative to learn more broad structures rather than noise
            learning_rate = 0.05, #shrinks each trees contribution helping it ignore random spikes
            subsample=0.8, #makes sure each tree trains on %80 of the rows
            colsample_bytree=0.8, # each tree trains on %80 of the features
            objective="binary:logistic", #this creates an output between 0 and 1 which is good because it is the probability that the price direciton is going up or down
            eval_metric="logloss", # logloss penalizes confident wrong predictions
            tree_method="hist", #ensures gpu usage
            device="cuda",
            n_jobs=-1
        )
    elif model_type == "xgb_reg":
        model = XGBRegressor(
            n_estimators=300,
            max_depth=5,
            learning_rate = 0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            objective="reg:squarederror",
            eval_metric="rmse",
            tree_method="hist",
            device="cuda",
            n_jobs=-1
        )
    else:
        raise ValueError("model_type must be xgb_class or xgb_reg")
    
    return model