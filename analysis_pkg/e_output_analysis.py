import pandas as pd

from .a_parse_yearly_df import parse_single
from .d_df_transform import df_transform_for_scoring


def score_ratio(grouped_df, var):
    sex_sep = []
    sex_full = []
    cat_full = []

    cat_list = list(grouped_df[var].unique())
        
    for n in cat_list:
        if var == 'SEX' and n == 'Female':
            m_ncat = grouped_df[(grouped_df['SEX'] == 'Male')].reset_index()
            f_ncat = grouped_df[(grouped_df['SEX'] == 'Female')].reset_index()

            sex_df = pd.DataFrame({'m_wage': m_ncat.WAG, 'm_ct': m_ncat.WAGP_count,
                                'f_wage': f_ncat.WAG, 'f_ct': f_ncat.WAGP_count})

            m_ct = sex_df['m_ct'].sum()
            f_ct = sex_df['f_ct'].sum()
            t_ct = m_ct + f_ct

            sex_df['m_wage_f'] = sex_df['m_wage'] * sex_df['f_ct'] / f_ct
            sex_df['m_wage_m'] = sex_df['m_wage'] * sex_df['m_ct'] / m_ct
            sex_df['f_wage_m'] = sex_df['f_wage'] * sex_df['m_ct'] / m_ct
            sex_df['f_wage_f'] = sex_df['f_wage'] * sex_df['f_ct'] / f_ct

            m_wage_f = round(sex_df['m_wage_f'].sum(), 3)
            m_wage_m = round(sex_df['m_wage_m'].sum(), 3)
            f_wage_m = round(sex_df['f_wage_m'].sum(), 3)
            f_wage_f = round(sex_df['f_wage_f'].sum(), 3)
            
            f_m_ratio_f = round(f_wage_f / m_wage_f, 3)
            f_m_ratio_m = round(f_wage_m / m_wage_m, 3)

            m_summary = [var, 'SEX', m_wage_m, m_wage_f, 'Male', m_ct]
            f_summary = [var, 'SEX', f_wage_m, f_wage_f, 'Female', f_ct]
            sex_summary = [var, 'SEX', t_ct,
                m_wage_f, m_wage_m, m_ct,
                f_wage_m, f_wage_f, f_ct,
                f_m_ratio_f, f_m_ratio_m]

            sex_sep.append(m_summary)
            sex_sep.append(f_summary)
            sex_full.append(sex_summary)
        
        elif var == 'SEX' and n == 'Male':
            pass

        # GENDER ANALYSIS PER CATEGORY IN EACH VARIABLE
        else:
            m_ncat = grouped_df[(grouped_df[var] == n) & (grouped_df['SEX'] == 'Male')].reset_index()
            f_ncat = grouped_df[(grouped_df[var] == n) & (grouped_df['SEX'] == 'Female')].reset_index()

            sex_df = pd.DataFrame({'m_wage': m_ncat.WAG, 'm_ct': m_ncat.WAGP_count,
                                'f_wage': f_ncat.WAG, 'f_ct': f_ncat.WAGP_count})

            m_ct = sex_df['m_ct'].sum()
            f_ct = sex_df['f_ct'].sum()
            t_ct = m_ct + f_ct

            sex_df['m_wage_f'] = sex_df['m_wage'] * sex_df['f_ct'] / f_ct
            sex_df['m_wage_m'] = sex_df['m_wage'] * sex_df['m_ct'] / m_ct
            sex_df['f_wage_m'] = sex_df['f_wage'] * sex_df['m_ct'] / m_ct
            sex_df['f_wage_f'] = sex_df['f_wage'] * sex_df['f_ct'] / f_ct

            m_wage_f = round(sex_df['m_wage_f'].sum(), 3)
            m_wage_m = round(sex_df['m_wage_m'].sum(), 3)
            f_wage_m = round(sex_df['f_wage_m'].sum(), 3)
            f_wage_f = round(sex_df['f_wage_f'].sum(), 3)
            
            f_m_ratio_f = round(f_wage_f / m_wage_f, 3)
            f_m_ratio_m = round(f_wage_m / m_wage_m, 3)

            m_summary = [var, n, m_wage_m, m_wage_f, 'Male', m_ct]
            f_summary = [var, n, f_wage_m, f_wage_f, 'Female', f_ct]
            sex_summary = [var, n, t_ct,
                m_wage_f, m_wage_m, m_ct,
                f_wage_m, f_wage_f, f_ct,
                f_m_ratio_f, f_m_ratio_m]

            sex_sep.append(m_summary)
            sex_sep.append(f_summary)
            sex_full.append(sex_summary)

        # CATEGORY ANALYSIS PER EACH VARIABLE
        for base_cat in cat_list:
            n_cat = grouped_df[(grouped_df[var] == n)].reset_index()
            b_cat = grouped_df[(grouped_df[var] == base_cat)].reset_index()

            cat_df = pd.DataFrame({'n_wage': n_cat.WAG, 'n_ct': n_cat.WAGP_count,
                                    'b_wage': b_cat.WAG, 'b_ct': b_cat.WAGP_count})
            
            n_ct = cat_df['n_ct'].sum()
            b_ct = cat_df['b_ct'].sum()

            cat_df['n_wage_b'] = cat_df['n_wage'] * cat_df['b_ct'] / b_ct
            cat_df['b_wage_b'] = cat_df['b_wage'] * cat_df['b_ct'] / b_ct

            n_wage_b = round(cat_df['n_wage_b'].sum(), 3)
            b_wage_b = round(cat_df['b_wage_b'].sum(), 3)   
            n_ratio_b = round(n_wage_b / b_wage_b, 3)

            cat_summary = [var, n, base_cat, n_wage_b, n_ratio_b, n_ct, b_ct]
            cat_full.append(cat_summary)
    
    cat_full = pd.DataFrame(cat_full, columns = ['Variable', 'Category', 'Base_Category', 'Wage_vs_Base', 
                                                 'Ratio_vs_Base', 'n_Count', 'b_Count'])
    sex_sep = pd.DataFrame(sex_sep, columns = ['Variable', 'Category', 'Wage_m', 
                                                 'Wage_f', 'Sex', 'Count'])                                                
    sex_full = pd.DataFrame(sex_full, columns = ['Variable', 'Category', 'Total_Count', 
                                                 'M_Wage_f', 'M_Wage_m', 'M_Count',
                                                 'F_Wage_m', 'F_Wage_f', 'F_Count',
                                                 'F_M_Ratio_f', 'F_M_Ratio_m'])
    return (sex_sep, sex_full, cat_full)


def multibase_analysis(grouped_df):
    var_list = ['SEX', 'EDU', 'JOB', 'RACE', 'AGEB']
    sex_sep = pd.DataFrame()
    sex_full = pd.DataFrame()
    cat_full = pd.DataFrame()
    for var in var_list:
        score_cat = score_ratio(grouped_df, var)
        sex_sep = pd.concat([sex_sep, score_cat[0]])
        sex_full = pd.concat([sex_full, score_cat[1]])
        cat_full = pd.concat([cat_full, score_cat[2]])
    
    return (sex_sep, sex_full, cat_full)


def singleyear_multibase_analysis(single_year, mod_fit):
    group_df = df_transform_for_scoring(single_year, mod_fit)
    sex_sep, sex_full, cat_full = multibase_analysis(group_df)
    
    return (sex_sep, sex_full, cat_full)


'''
def multibase_analysis(grouped_df):
    var_list = ['EDU', 'JOB', 'AGEB', 'RACE']
    cat_combo = [['SEX', 'Male']]
    for var in var_list:
        var_cat = list(grouped_df[var].unique())
        for cat in var_cat:
            vat_cat_group = [var, cat]
            cat_combo.append(vat_cat_group)
    
    sep_full = pd.DataFrame()
    grp_full = pd.DataFrame()
    for n in cat_combo:
        score_cat = score_ratio(grouped_df, n[0], n[1])
        sep_full = pd.concat([sep_full, score_cat[0]])
        grp_full = pd.concat([grp_full, score_cat[1]])
    
    return (sep_full, grp_full)
'''