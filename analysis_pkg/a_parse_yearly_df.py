import pandas as pd
import glob

def parse_group(start_year, end_year):
    end_year = end_year+1
    years = list(range(start_year, end_year))
    PUS_start = pd.DataFrame()
    for year in years:
        useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                    'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
        path = ('data/%s' % year)
        PUS_split = pd.concat([pd.read_csv(f, usecols=useful_cols)
                            for f in glob.glob(path + "/*.csv")], ignore_index=True)
        PUS_start = PUS_start.append(PUS_split)
    return PUS_start


def parse_single(year):
    PUS_start = pd.DataFrame()
    useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
    path = ('data/%s' % year)
    PUS_start = pd.concat([pd.read_csv(f, usecols=useful_cols)
                        for f in glob.glob(path + "/*.csv")], ignore_index=True)
    return PUS_start


def parse_skip_year(start_year, end_year):
    start_year = round((start_year)/2)
    end_year = round((end_year+1)/2)
    years = list(x*2 for x in range(start_year, end_year))
    PUS_start = pd.DataFrame()
    for year in years:
        useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                    'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
        path = ('data/%s' % year)
        PUS_split = pd.concat([pd.read_csv(f, usecols=useful_cols)
                            for f in glob.glob(path + "/*.csv")], ignore_index=True)
        PUS_start = PUS_start.append(PUS_split)
    return PUS_start