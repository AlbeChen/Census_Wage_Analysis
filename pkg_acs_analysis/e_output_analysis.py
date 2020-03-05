import pandas as pd
import time

from .a_parse_yearly_df import parse_single, parse_group
from .d_df_transform import transform_for_scoring


# extracting count and wage for grouped df - only looking at single variable (sex, age, etc)
def score_ratio(grouped_df, var):
    sex_sep = []
    sex_full = []
    cat_full = []

    cat_list = list(grouped_df[var].unique())

    for n in cat_list:
        # sex behaves differently since cant constrain of both M-F so output is off
        # look below for commnts on what's being processed
        if var == "SEX" and n == "Female":
            m_ncat = grouped_df[(grouped_df["SEX"] == "Male")].reset_index()
            f_ncat = grouped_df[(grouped_df["SEX"] == "Female")].reset_index()

            sex_df = pd.DataFrame(
                {
                    "m_wage": m_ncat.WAG,
                    "m_ct": m_ncat.WAGP_count,
                    "f_wage": f_ncat.WAG,
                    "f_ct": f_ncat.WAGP_count,
                }
            )

            m_ct = sex_df["m_ct"].sum()
            f_ct = sex_df["f_ct"].sum()
            t_ct = m_ct + f_ct
            m_per_ct = m_ct / t_ct
            f_per_ct = f_ct / t_ct

            sex_df["m_wage_f"] = sex_df["m_wage"] * sex_df["f_ct"] / f_ct
            sex_df["m_wage_m"] = sex_df["m_wage"] * sex_df["m_ct"] / m_ct
            sex_df["f_wage_m"] = sex_df["f_wage"] * sex_df["m_ct"] / m_ct
            sex_df["f_wage_f"] = sex_df["f_wage"] * sex_df["f_ct"] / f_ct

            m_wage_f = round(sex_df["m_wage_f"].sum(), 3)
            m_wage_m = round(sex_df["m_wage_m"].sum(), 3)
            m_wage_avg = round((m_wage_m + m_wage_f) / 2, 3)
            m_wage_dif = round((m_wage_m - m_wage_f), 3)

            f_wage_m = round(sex_df["f_wage_m"].sum(), 3)
            f_wage_f = round(sex_df["f_wage_f"].sum(), 3)
            f_wage_avg = round((f_wage_m + f_wage_f) / 2, 3)
            f_wage_dif = round((f_wage_m - f_wage_f), 3)

            f_m_ratio_f = round(f_wage_f / m_wage_f, 3)
            f_m_ratio_m = round(f_wage_m / m_wage_m, 3)
            f_m_ratio_avg = round((f_m_ratio_f + f_m_ratio_m) / 2, 3)
            f_m_ratio_dif = round((f_m_ratio_f - f_m_ratio_m), 3)

            m_summary = [
                var,
                n,
                m_wage_m,
                m_wage_f,
                m_wage_avg,
                m_wage_dif,
                "Male",
                m_ct,
            ]
            f_summary = [
                var,
                n,
                f_wage_m,
                f_wage_f,
                f_wage_avg,
                f_wage_dif,
                "Female",
                f_ct,
            ]
            sex_summary = [
                var,
                n,
                t_ct,
                m_wage_f,
                m_wage_m,
                m_wage_avg,
                m_wage_dif,
                m_ct,
                m_per_ct,
                f_wage_m,
                f_wage_f,
                f_wage_avg,
                f_wage_dif,
                f_ct,
                f_per_ct,
                f_m_ratio_f,
                f_m_ratio_m,
                f_m_ratio_avg,
                f_m_ratio_dif,
            ]

            sex_sep.append(m_summary)
            sex_sep.append(f_summary)
            sex_full.append(sex_summary)

        elif var == "SEX" and n == "Male":
            pass

        # GENDER ANALYSIS PER CATEGORY IN EACH VARIABLE
        else:
            # seperating by sex of each
            m_ncat = grouped_df[
                (grouped_df[var] == n) & (grouped_df["SEX"] == "Male")
            ].reset_index()
            f_ncat = grouped_df[
                (grouped_df[var] == n) & (grouped_df["SEX"] == "Female")
            ].reset_index()

            # new df looking at only wage and count for m and f
            sex_df = pd.DataFrame(
                {
                    "m_wage": m_ncat.WAG,
                    "m_ct": m_ncat.WAGP_count,
                    "f_wage": f_ncat.WAG,
                    "f_ct": f_ncat.WAGP_count,
                }
            )

            # extracting counts
            m_ct = sex_df["m_ct"].sum()
            f_ct = sex_df["f_ct"].sum()
            t_ct = m_ct + f_ct
            m_per_ct = m_ct / t_ct
            f_per_ct = f_ct / t_ct

            # extracting wage percents depening on counts for each row
            sex_df["m_wage_f"] = sex_df["m_wage"] * sex_df["f_ct"] / f_ct
            sex_df["m_wage_m"] = sex_df["m_wage"] * sex_df["m_ct"] / m_ct
            sex_df["f_wage_m"] = sex_df["f_wage"] * sex_df["m_ct"] / m_ct
            sex_df["f_wage_f"] = sex_df["f_wage"] * sex_df["f_ct"] / f_ct

            # summing each male columns to get weighted score
            m_wage_f = round(sex_df["m_wage_f"].sum(), 3)
            m_wage_m = round(sex_df["m_wage_m"].sum(), 3)
            m_wage_avg = round((m_wage_m + m_wage_f) / 2, 3)
            m_wage_dif = round((m_wage_m - m_wage_f), 3)

            # summing each female columns to get weighted score
            f_wage_m = round(sex_df["f_wage_m"].sum(), 3)
            f_wage_f = round(sex_df["f_wage_f"].sum(), 3)
            f_wage_avg = round((f_wage_m + f_wage_f) / 2, 3)
            f_wage_dif = round((f_wage_m - f_wage_f), 3)

            # getting ratios of each wage f/ wage m
            f_m_ratio_f = round(f_wage_f / m_wage_f, 3)
            f_m_ratio_m = round(f_wage_m / m_wage_m, 3)
            f_m_ratio_avg = round((f_m_ratio_f + f_m_ratio_m) / 2, 3)
            f_m_ratio_dif = round((f_m_ratio_f - f_m_ratio_m), 3)

            # orginizing values for sex based tables
            m_summary = [
                var,
                n,
                m_wage_m,
                m_wage_f,
                m_wage_avg,
                m_wage_dif,
                "Male",
                m_ct,
            ]
            f_summary = [
                var,
                n,
                f_wage_m,
                f_wage_f,
                f_wage_avg,
                f_wage_dif,
                "Female",
                f_ct,
            ]
            sex_summary = [
                var,
                n,
                t_ct,
                m_wage_f,
                m_wage_m,
                m_wage_avg,
                m_wage_dif,
                m_ct,
                m_per_ct,
                f_wage_m,
                f_wage_f,
                f_wage_avg,
                f_wage_dif,
                f_ct,
                f_per_ct,
                f_m_ratio_f,
                f_m_ratio_m,
                f_m_ratio_avg,
                f_m_ratio_dif,
            ]

            sex_sep.append(m_summary)
            sex_sep.append(f_summary)
            sex_full.append(sex_summary)

        # CATEGORY ANALYSIS PER EACH VARIABLE
        for base_cat in cat_list:
            # split according to base catagory within variable (ex: Cat = Dr, BS in Var = EDU)
            n_cat = grouped_df[(grouped_df[var] == n)].reset_index()
            b_cat = grouped_df[(grouped_df[var] == base_cat)].reset_index()

            cat_df = pd.DataFrame(
                {
                    "n_wage": n_cat.WAG,
                    "n_ct": n_cat.WAGP_count,
                    "b_wage": b_cat.WAG,
                    "b_ct": b_cat.WAGP_count,
                }
            )
            # counts
            n_ct = cat_df["n_ct"].sum()
            b_ct = cat_df["b_ct"].sum()

            # percent wages vs base catagory weighted by count of each
            cat_df["n_wage_b"] = cat_df["n_wage"] * cat_df["b_ct"] / b_ct
            cat_df["b_wage_b"] = cat_df["b_wage"] * cat_df["b_ct"] / b_ct

            # summing wages to quantify against weighted
            n_wage_b = round(cat_df["n_wage_b"].sum(), 3)
            b_wage_b = round(cat_df["b_wage_b"].sum(), 3)
            n_ratio_b = round(n_wage_b / b_wage_b, 3)

            cat_summary = [var, n, base_cat, n_wage_b, n_ratio_b, n_ct, b_ct]
            cat_full.append(cat_summary)

    # output full df of each for sex and cat
    cat_full = pd.DataFrame(
        cat_full,
        columns=[
            "Variable",
            "Category",
            "Base_Category",
            "Wage_vs_Base",
            "Ratio_vs_Base",
            "n_Count",
            "b_Count",
        ],
    )
    sex_sep = pd.DataFrame(
        sex_sep,
        columns=[
            "Variable",
            "Category",
            "Wage_m",
            "Wage_f",
            "Wage_Avg",
            "Wage_Diff",
            "Sex",
            "Count",
        ],
    )
    sex_full = pd.DataFrame(
        sex_full,
        columns=[
            "Variable",
            "Category",
            "Total_Count",
            "M_Wage_f",
            "M_Wage_m",
            "M_Wage_Avg",
            "M_Wage_Diff",
            "M_Count",
            "M_Pct_Ct",
            "F_Wage_m",
            "F_Wage_f",
            "F_Wage_Avg",
            "F_Wage_Diff",
            "F_Count",
            "F_Pct_Ct",
            "F_M_Ratio_f",
            "F_M_Ratio_m",
            "F_M_Ratio_Avg",
            "F_M_Ratio_Diff",
        ],
    )
    return (sex_sep, sex_full, cat_full)


# analysis for processsed df - all variables
def multibase_analysis(grouped_df):
    var_list = ["SEX", "EDU", "JOB", "RACE", "AGE"]
    sex_sep = pd.DataFrame()
    sex_full = pd.DataFrame()
    cat_full = pd.DataFrame()
    for var in var_list:
        score_cat = score_ratio(grouped_df, var)
        sex_sep = pd.concat([sex_sep, score_cat[0]])
        sex_full = pd.concat([sex_full, score_cat[1]])
        cat_full = pd.concat([cat_full, score_cat[2]])

    return (sex_sep, sex_full, cat_full)


# full analysis with processing df only needing to give year to look at
def singleyear_multibase_analysis(single_year):
    raw_df = parse_single(single_year)
    group_df = transform_for_scoring(raw_df)
    sex_sep, sex_full, cat_full = multibase_analysis(group_df)

    return (sex_sep, sex_full, cat_full, group_df)


# full analysis with processing df for each year between start - end (track years)
def yearly_multibase_analysis(start_year, end_year):
    sex_sep = pd.DataFrame()
    sex_full = pd.DataFrame()
    cat_full = pd.DataFrame()
    group_df = pd.DataFrame()
    end_year = end_year + 1
    year_range = list(range(start_year, end_year))

    for year in year_range:
        start_time = time.time()
        grouped_analysis = singleyear_multibase_analysis(year)
        for grouped in grouped_analysis:
            grouped["Year"] = year
        sex_sep = pd.concat([sex_sep, grouped_analysis[0]])
        sex_full = pd.concat([sex_full, grouped_analysis[1]])
        cat_full = pd.concat([cat_full, grouped_analysis[2]])
        group_df = pd.concat([group_df, grouped_analysis[3]])
        print(
            "Completed Year:",
            year,
            " (%s min)" % round(((time.time() - start_time) / 60), 2),
        )

    return (sex_sep, sex_full, cat_full, group_df)


# full analysis with processing df into single df from start - end (single df not tracking years)
def multiyear_multibase_analysis(start_year, end_year):
    start_time = time.time()
    raw_df = parse_group(start_year, end_year)
    group_df = transform_for_scoring(raw_df)
    sex_sep, sex_full, cat_full = multibase_analysis(group_df)
    print("Completed in: %s min)" % round(((time.time() - start_time) / 60), 2))
    return (sex_sep, sex_full, cat_full, group_df)

