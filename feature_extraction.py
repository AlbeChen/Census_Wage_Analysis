def mapping_features(df):
    # Sex
    df['SEX'] = df['SEX'].map(lambda y: 'Male' if y == 1
                              else 'Female' if y == 2
                              else 'na')

    # Age
    df['AGEB'] = df['AGEP'].map(lambda y: '18-25' if y <= 25
                                else '26-35' if y <= 35
                                else '36-45' if y <= 45
                                else '46-55' if y <= 55
                                else '56-70' if y <= 70
                                else 'na')
    # Education
    df['EDU'] = df['SCHL'].map(lambda y: 'No_HS' if y <= 15
                               else 'HSD' if y <= 17
                               else 'CLG' if y <= 19
                               else 'CLG' if y == 20
                               else 'BS' if y == 21
                               else 'MS' if y == 22
                               else 'DR+' if y <= 24
                               else 'na')

    # Occupation
    df['JOB'] = df['OCCP'].map(lambda y: "BUS" if y <= 960
                               else "SCI" if y <= 1980
                               else "ART" if y <= 2970
                               else "HLC" if y <= 3550
                               else "SVC" if y <= 4655
                               else "SAL" if y <= 5940
                               else "MTN" if y <= 7640
                               else "PRD" if y <= 8990
                               else "TRP" if y <= 9760
                               else "MLT" if y <= 9830
                               else "UN")
    # Race
    df['RAC1P'] = np.where(df['HISP'] == 1, df['RAC1P'], 10)
    df['RACE'] = df['RAC1P'].map(lambda y: 'WHT/MIX' if y == 1  # white
                                 else 'BLK' if y == 2  # black
                                 else 'HSP/NTV' if y <= 5  # native
                                 else 'ASN' if y == 6  # asian
                                 else 'HSP/NTV' if y == 7  # native
                                 else 'WHT/MIX' if y <= 9  # mixed
                                 else 'HSP/NTV' if y == 10  # hispanic
                                 else 'na')
    return df