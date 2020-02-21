import pandas as pd
import glob

# grab grouped years to single csv for wholistic analysis
def parse_group(start_year, end_year):
    end_year = end_year+1
    years = list(range(start_year, end_year))
    PUS_start = pd.DataFrame()
    for year in years:
        useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                    'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
        path = ('data_raw/%s' % year)
        PUS_split = pd.concat([pd.read_csv(f, usecols=useful_cols)
                            for f in glob.glob(path + "/*.csv")], ignore_index=True)
        PUS_start = PUS_start.append(PUS_split)
    return PUS_start

# grab sinlge year df for yearly function later
def parse_single(year):
    PUS_start = pd.DataFrame()
    useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
    path = ('data_raw/%s' % year)
    PUS_start = pd.concat([pd.read_csv(f, usecols=useful_cols)
                        for f in glob.glob(path + "/*.csv")], ignore_index=True)
    return PUS_start

# used to grab a group of years, but if you wanted to skip every other year
def parse_skip_year(start_year, end_year):
    start_year = round((start_year)/2)
    end_year = round((end_year+1)/2)
    years = list(x*2 for x in range(start_year, end_year))
    PUS_start = pd.DataFrame()
    for year in years:
        useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
                    'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
        path = ('data_raw/%s' % year)
        PUS_split = pd.concat([pd.read_csv(f, usecols=useful_cols)
                            for f in glob.glob(path + "/*.csv")], ignore_index=True)
        PUS_start = PUS_start.append(PUS_split)
    return PUS_start

# initally used to make csv smaller with only the useful_cols
def shorten_raw_df(year):
    path = ('data_raw/%s' %year)
    useful_cols = ['WAGP', 'SEX', 'AGEP', 'RAC1P',
        'SCHL', 'WKW', 'WKHP', 'OCCP', 'POWSP', 'ST', 'HISP']
    raw_df = pd.concat([pd.read_csv(f, usecols = useful_cols) \
        for f in glob.glob(path + "/*.csv", recursive = True)], ignore_index=True)
    print (raw_df.shape)
    raw_df.to_csv((path + "/shorten_pus.csv"),index=False)
    return raw_df

# converted some errors in some year's files from str to int (0)
def convert_rows_num(raw_df):
    for x in ['WAGP', 'WKHP']:
        raw_df[x] = raw_df[x].map(lambda y: 0 if y == "0000000" 
                                        else 0 if y == ' '
                                        else y)
        raw_df[x] = pd.to_numeric(raw_df[x])
    return raw_df
