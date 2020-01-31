import pandas as pd
import numpy as np

from .b_preprocessing_pipeline import preprocess_catagories, preprocess_modeling

def add_category_and_predicted(modeling_df, catagorical_df, model_fit):
    to_pred_df = modeling_df.drop(['WAGP'], axis=1)
    pred_wages = model_fit.predict(to_pred_df)
    predicted = pd.DataFrame({'Index': to_pred_df.index,
                              'WAG_pred': pred_wages}).set_index('Index')
    predicted = pd.concat([predicted, catagorical_df], axis=1, sort=False)

    predicted['WAG_pred'] = np.exp(predicted['WAG_pred'])
    predicted['WAGP'] = np.exp(predicted['WAGP'])

    return predicted


def group_by_category(pred_and_cat_df):
    grouped = pred_and_cat_df.groupby(['SEX', 'EDU', 'JOB', 'RACE', 'AGEB']) \
        .agg({'WAG_pred': ['mean'], 'WAGP': ['count', 'mean']})
    for level in range(-3,1):
        grouped = grouped.unstack(level=level, fill_value='0').stack()
    grouped = grouped.unstack(level=-4, fill_value='0').stack().reset_index()
    grouped.columns = grouped.columns.map('_'.join).str.strip('_')

    wage_to_numeric = ['WAG_pred_mean', 'WAGP_mean', 'WAGP_count']
    grouped[wage_to_numeric] = grouped[wage_to_numeric].apply(pd.to_numeric)
    grouped['WAG'] = grouped['WAG_pred_mean'] # + grouped['WAGP_mean'])/2

    return grouped


def df_transform_for_scoring(raw_df, model_fit):
    mod_df = preprocess_modeling(raw_df)
    cat_df = preprocess_catagories(raw_df)
    grouped_df = group_by_category(
        add_category_and_predicted(mod_df, cat_df, model_fit))

    return grouped_df