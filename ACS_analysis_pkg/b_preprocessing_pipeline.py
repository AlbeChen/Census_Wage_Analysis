import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

# filter df for full timers
def full_time_detect(df):
    df = df.loc[df.WKW < 4].copy() # more than 40 weeks a year is considered full time
    df = df.loc[df.WKHP >= 35].copy() # >=35 hr a week is considered full time
    df = df.loc[df.AGEP >= 18].copy() # lower limit age
    df = df.loc[df.AGEP <= 70].copy() # upper limit age 
    return df

# determine who is considered an outlier
def outlier_wage(df):
    #wage_iqr = np.percentile(df.WAGP, 75) - np.percentile(df.WAGP, 25)
    #wage_upper = np.percentile(df.WAGP, 75) + wage_iqr * 3
    df = df.loc[df.WAGP >= 12500].copy() # used because 12500 is poverty line
    df = df.loc[df.WAGP <= 400000].copy() # used as ~1% wage US population
    df['WAGP'] = np.log(df['WAGP'])
    return df

# mapping values according to technical document for data directory
def mapping_features(df):
    # Sex
    df['SEX'] = df['SEX'].map(lambda y: 'Male' if y == 1
                              else 'Female' if y == 2
                              else 'na')

    # Age
    df['AGE'] = df['AGEP'].map(lambda y: '18-22' if y <= 22
                                else '23-28' if y <= 28                        
                                else '29-36' if y <= 36
                                else '37-45' if y <= 45
                                else '46-55' if y <= 55
                                else '56-70' if y <= 70
                                else 'na')
    # Education
    df['EDU'] = df['SCHL'].map(lambda y: 'No_Highschool' if y <= 15
                               else 'Highschool' if y <= 17
                               else 'Some_College' if y <= 19
                               else 'Some_College' if y == 20
                               else 'B.S._Degree' if y == 21
                               else 'M.S._Degree' if y == 22
                               else 'PhD_or_Prof' if y <= 24
                               else 'na')

    # Occupation
    df['JOB'] = df['OCCP'].map(lambda y: "Business" if y <= 960
                               else "Science" if y <= 1980
                               else "Art" if y <= 2970
                               else "Healthcare" if y <= 3550
                               else "Services" if y <= 4655
                               else "Sales" if y <= 5940
                               else "Maintenance" if y <= 7640
                               else "Production" if y <= 8990
                               else "Transport" if y <= 9760
                               else "Military" if y <= 9830
                               else "na")
    # Race
    df['RAC1P'] = np.where(df['HISP'] == 1, df['RAC1P'], 10)
    df['RACE'] = df['RAC1P'].map(lambda y: 'White' if y == 1
                                 else 'Black' if y == 2
                                 else 'Native' if y <= 5
                                 else 'Asian' if y == 6 
                                 else 'Native' if y == 7
                                 else 'Mixed' if y <= 9
                                 else 'Hispanic' if y == 10
                                 else 'na')
    return df

# removing columns after mapping
def remove_col(df):
    remove_cols = ['SCHL', 'WKHP', 'WKW', 'HISP',
                   'OCCP', 'POWSP', 'RAC1P', 'AGEP', 'ST']
    df = df.drop(remove_cols, axis=1)
    return df

# one hot encoding all columns after mapping
def OHE_no_WAGP(df):
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    cat_col = [i for i in df.columns.tolist() if i not in ['WAGP']]
    OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(df[cat_col]))
    
    OHE_col = list(OH_encoder.get_feature_names(cat_col))
    
    OH_cols_train.index = df.index
    df = pd.concat([df, OH_cols_train], axis=1)
    df.drop(cat_col, axis=1, inplace=True)
    
    df.columns = OHE_col
    return df

# one hot encoding but wagp
def OHE_cat(df):
    OH_encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
    cat_col = [i for i in df.columns.tolist() if i not in ['WAGP']]
    OH_cols_train = pd.DataFrame(OH_encoder.fit_transform(df[cat_col]))
    
    OHE_col = list(OH_encoder.get_feature_names(cat_col))
    OHE_col.insert(0, 'WAGP')
    
    OH_cols_train.index = df.index
    df = pd.concat([df, OH_cols_train], axis=1)
    df.drop(cat_col, axis=1, inplace=True)
    
    df.columns = OHE_col
    return df

# summary of preprocessing ^^^ all functions above
def preprocess_modeling(df):
    df = (df
          .pipe(full_time_detect)
          .pipe(outlier_wage)
          .pipe(mapping_features)
          .pipe(remove_col)
          .pipe(OHE_cat)
          )
    return df

# summary of preprocessing BUT no OHE so maintain catagorical data
def preprocess_catagories(df):
    df = (df
          .pipe(full_time_detect)
          .pipe(outlier_wage)
          .pipe(mapping_features)
          .pipe(remove_col)
          )
    return df
