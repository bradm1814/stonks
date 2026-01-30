import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, accuracy_score, mean_absolute_error, mean_squared_error, r2_score
import joblib
from pathlib import Path
import os

from src.ml.models import make_baseline_model
from src.ml.features import build_feature_matrix
from src.ml.labeling import make_directional_labels

def prepare_ml_dataset(price_df: pd.DataFrame, label_func, **label_kwargs):
    """
    This aligns the input X and the target y to a common index 'date' that are aligned based on the horizon used to generate direcitonal labels.
    Masks any values that are NaN
    
    :param price_df: Description
    :type price_df: pd.DataFrame
    """
    X = build_feature_matrix(price_df) #Add all features to the original df creating a training matrix
    y = label_func(price_df, **label_kwargs) #applies labels to the original df creating a testing matrix. it is variable and can call different functions for different label generation taking the respective keyword arguments

    if isinstance(y, pd.DataFrame): 
        y = y.iloc[:, -1]#because the returned item is the df with appended label column, this creates only a series with that appended column which is the target for the ML

    # Align on index interstection

    common_index = X.index.intersection(y.index) #this identifies the indeces in which these dataframes intersect
    X = X.loc[common_index] #make sure the Training Dataset is composed of intersecting data
    y = y.loc[common_index] #make sure the label Dataset is composed of intersecting data

    # drop any remaining NaNs

    mask = X.notna().all(axis=1) # make sure there are no NaN values since they wont work for Training
    X=X[mask]
    y=y[mask]

    return X,y

def print_training_metrics(model_training_metrics):
    print("\n=== Strategy Evaluation ===\n")
    for key, value in model_training_metrics.items():
        print(f"{key:25}: {value}")
    print("\n===========================\n")

def train_ml_model(price_df, label_func, model_type, model_name, model_dir = "data/models", **label_kwargs):

    # build Dataset
    X, y = prepare_ml_dataset(price_df, label_func,  **label_kwargs) # prepare a dataset with given label_func and its respective arguments


    #split the data 80-20 %80 train, %20 to measure metrics and performance. useful for tuning hyperparameters
    X_train, X_test, y_train, y_test = train_test_split(
        X, 
        y,
        test_size=0.2,
        shuffle=False #because the data is time series sensitive you don't want to shuffle
    )

    model = make_baseline_model(model_type=model_type) #creates a model given the model type
    model.fit(X_train, y_train) #runs model training sequence on the training dataset with the target dataset

    #classfiication metrics
    if model_type== "xgb_class":
        y_proba = model.predict_proba(X_test)[:, 1] #has the model predict probability of directional change for each row
        y_pred = (y_proba > 0.5).astype(int) #turns it's answer into 1 or 0 for up or down

        metrics = {
            "accuracy": accuracy_score(y_test, y_pred), #scikit metric that measures between label and guess
            "roc_auc": roc_auc_score(y_test, y_proba) #this determines out of how many actual positive days is it probable that the model predicts a positive day
        }
    #regression metrics
    else:
        y_pred = model.predict(X_test)

        metrics ={
            "mae": mean_absolute_error(y_test, y_pred), #average absolute error between test and prediction
            "rmse": mean_squared_error(y_test, y_pred) **0.5, # rmse shows how bad the worst ones are
            "r2": r2_score(y_test, y_pred) # tells whether or not the model is actually learning anything and how much it correlates to the data or explains anything
        }


    # save model

    if model_name is None: # creates a model name if none was given
        label_name = label_func.__name__
        model_name = f"{label_name}_{model_type}"

    Path(model_dir).mkdir(parents=True, exist_ok=True)
    model_path = Path(model_dir) / f"{model_name}.joblib"
    joblib.dump(model, model_path)

    print_training_metrics(metrics)

    return X, model, metrics, model_path
