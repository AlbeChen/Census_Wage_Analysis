from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import GridSearchCV, cross_val_score, StratifiedKFold, train_test_split

from .b_preprocessing_pipeline import preprocess_modeling
from .a_parse_yearly_df import parse_skip_year


def rfr_fit(modeling_df):
    #kfold = StratifiedKFold(n_splits=3)
    y_full = modeling_df['WAGP']
    x_full = modeling_df.drop(['WAGP'], axis=1)
    x_train_valid, x_test, y_train_valid, y_test = train_test_split(
        x_full, y_full, test_size=0.5, random_state=0)
    x_train, x_valid, y_train, y_valid = train_test_split(
        x_train_valid, y_train_valid, test_size=0.01, random_state=0)
    x_train = x_train.sample(n=500000, random_state=1)
    y_train = y_train.sample(n=500000, random_state=1)

    RFR = RandomForestRegressor(random_state=1)
    rfr_param_grid = {'n_estimators': [50, 100],
                      'min_samples_split': [2, 5, 10],
                      'min_samples_leaf': [5, 10, 20]}
    gsRFR = GridSearchCV(RFR, param_grid=rfr_param_grid, verbose=1,
                         scoring="neg_mean_absolute_error", n_jobs=4)
    gsRFR.fit(x_valid, y_valid)
    print(gsRFR.best_score_)
    RFR_best = gsRFR.best_estimator_

    RFR_best.fit(x_train, y_train)

    test_prediction = RFR_best.predict(x_test)
    print(mean_absolute_error(y_test, test_prediction))

    return RFR_best

def fit_spec_years(start_year, end_year):
    raw_df = parse_skip_year(start_year,end_year)
    mod_df = preprocess_modeling(raw_df)
    mod_fit = rfr_fit(mod_df)

    return mod_fit