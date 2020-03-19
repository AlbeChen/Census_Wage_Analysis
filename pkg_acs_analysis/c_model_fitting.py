from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import (
    GridSearchCV,
    cross_val_score,
    StratifiedKFold,
    train_test_split,
)

from .b_preprocessing_pipeline import preprocess_modeling
from .a_parse_yearly_df import parse_skip_year, parse_single, parse_group

# fitting model with simle rfr model
def rfr_fit(modeling_df):
    # kfold = StratifiedKFold(n_splits=3) #if smaller dataset
    y_full = modeling_df["WAGP"]
    x_full = modeling_df.drop(["WAGP"], axis=1)

    # splitting for testing set
    x_train_valid, x_test, y_train_valid, y_test = train_test_split(
        x_full, y_full, test_size=0.5, random_state=0
    )
    # splitting for validation set
    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train_valid, y_train_valid, test_size=0.02, random_state=0
    )

    # checking to see if df is too small so min 1 mil points are used
    if len(x_train.index) > 1000000:
        x_train = x_train.sample(n=1000000, random_state=1)
        y_train = y_train.sample(n=1000000, random_state=1)

    # rfr hyper parameters simple split scoring with MAE
    RFR = RandomForestRegressor(random_state=1, n_jobs=4)
    rfr_param_grid = {
        "n_estimators": [75, 100, 125],
        "min_samples_split": [3, 5, 7],
        "min_samples_leaf": [15, 20, 25],
    }
    gsRFR = GridSearchCV(
        RFR,
        param_grid=rfr_param_grid,
        verbose=0,
        n_jobs=4,
        scoring="neg_mean_absolute_error",
    )
    gsRFR.fit(x_valid, y_valid)
    # print(gsRFR.best_score_)
    RFR_best = gsRFR.best_estimator_

    RFR_best.fit(x_train, y_train)

    # Used prior for testing model orignally when tunning hyper parameters
    # test_prediction = RFR_best.predict(x_test)
    # print(mean_absolute_error(y_test, test_prediction))

    return RFR_best
