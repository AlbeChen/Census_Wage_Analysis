import pandas as pd
import numpy as np

from .b_preprocessing_pipeline import preprocess_catagories, preprocess_modeling, OHE_no_WAGP
from .a_parse_yearly_df import parse_single
from .c_model_fitting import rfr_fit


#used to create a dummy dataframe that had all permutations of variables
#to be used to predict all possible combinations of variables
def create_df_all_variations(cat_df, model_fit):
    #create empty dataframe with all combinations
    grp_list = []
    for sex in list(cat_df.SEX.unique()):
        sex_keep = []
        sex_keep.append(sex)
        for edu in list(cat_df.EDU.unique()):
            edu_keep = sex_keep.copy()
            edu_keep.append(edu)
            for age in list(cat_df.AGE.unique()):
                age_keep = edu_keep.copy()
                age_keep.append(age)
                for race in list(cat_df.RACE.unique()):
                    race_keep = age_keep.copy()
                    race_keep.append(race)
                    for job in list(cat_df.JOB.unique()):
                        job_keep = race_keep.copy()
                        job_keep.append(job)
                        grp_list.append(job_keep)
    grp_list = pd.DataFrame(grp_list, columns =['SEX', 'EDU', 'AGE', 'RACE', 'JOB'])
    
    #use OHE_no_WAGP to convert dummy df to OHE and use a prior model fit to predict dummy df
    cat_df_cols = cat_df.drop(['WAGP'], axis=1)
    grp_list = grp_list[cat_df_cols.columns]
    all_var_model = OHE_no_WAGP(grp_list)
    pred_wages = model_fit.predict(all_var_model)
    predicted = pd.DataFrame({'Index': all_var_model.index,
                              'WAG': pred_wages}).set_index('Index')
    predicted = pd.concat([predicted, grp_list], axis=1, sort=False)
    
    #output of dummy df of all combintations with predicted wages for each depending on df the model fit to
    predicted['WAG'] = np.exp(predicted['WAG'])
    predicted = predicted.sort_values(by=['SEX', 'EDU', 'JOB', 'RACE', 'AGE'])
    predicted = predicted.reset_index(drop=True)
    return predicted


#agg data by wage to grab orignal df's population count of each combiation of person
def group_by_category(cat_df):
    grouped = cat_df.groupby(['SEX', 'EDU', 'JOB', 'RACE', 'AGE']) \
        .agg({'WAGP': ['count', 'mean']})
    
    #used to keep all combinations even if they have no one in them
    for level in range(-3,1):
        grouped = grouped.unstack(level=level, fill_value=0).stack()
    grouped = grouped.unstack(level=-4, fill_value=0).stack().reset_index()
    grouped.columns = grouped.columns.map('_'.join).str.strip('_')

    wage_to_numeric = ['WAGP_mean', 'WAGP_count']
    grouped[wage_to_numeric] = grouped[wage_to_numeric].apply(pd.to_numeric)

    grouped['WAGP_mean'] = np.exp(grouped['WAGP_mean'])
    grouped = grouped.sort_values(by=['SEX', 'EDU', 'JOB', 'RACE', 'AGE'])
    grouped = grouped.reset_index(drop=True)

    return grouped


#full summary of above functions ^^^^
#var_df is the dummy df with all possible combinations
#cat_grp is the raw df with mean and count of all combinations
def transform_for_scoring(raw_df):
    cat_df = preprocess_catagories(raw_df)
    mod_df = preprocess_modeling(raw_df)
    mod_fit = rfr_fit(mod_df)

    var_df = create_df_all_variations(cat_df, mod_fit)
    cat_grp = group_by_category(cat_df)
    cat_grp = cat_grp.drop(['SEX', 'EDU', 'JOB', 'RACE', 'AGE'], axis=1)
    grouped_df = pd.concat([var_df, cat_grp], axis=1, sort=False)
   
    return grouped_df
