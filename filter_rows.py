# define function to seperate people who've worked more than 40 weeks / year
def full_time_detect(df):
    # remove rows of people who work under 40 weeks in a year
    df = df.loc[df.WKW < 4].copy()
    # remove rows of people who work under 35 hours a week
    df = df.loc[df.WKHP >= 35].copy()
    # remove rows of people below 18 and above 70
    df = df.loc[df.AGEP >= 18].copy()
    df = df.loc[df.AGEP <= 70].copy()
    return df


def outlier_wage(df):
    # remove rows of outlier upper wages and below poverty $
    wage_iqr = np.percentile(df.WAGP, 75) - np.percentile(df.WAGP, 25)
    wage_upper = np.percentile(df.WAGP, 75) + wage_iqr * 3
    df = df.loc[df.WAGP >= 12500].copy()
    df = df.loc[df.WAGP <= wage_upper].copy()
    return df
