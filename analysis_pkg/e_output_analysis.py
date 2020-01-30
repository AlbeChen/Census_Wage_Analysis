import pandas as pd

from .a_parse_yearly_df import parse_single
from .d_df_transform import df_transform_for_scoring


def score_ratio(grouped_df, var, base_cat):
    output_sep = []
    output_grp = []
    cat_list = list(grouped_df[var].unique())
    
    if var == 'SEX':
        f_cat = grouped_df[(grouped_df['SEX'] == 'Female')].reset_index()
        m_cat = grouped_df[(grouped_df['SEX'] == 'Male')].reset_index()

        temp = pd.DataFrame({'f_wage': f_cat.WAG, 'f_ct': f_cat.WAGP_count,
                            'm_wage': m_cat.WAG, 'm_ct': m_cat.WAGP_count})
        temp = temp.loc[(temp['f_ct'] >= 1) & (temp['m_ct'] >= 1)]

        temp['mx_wage'] = temp['m_wage'] * temp['f_ct'] / temp['f_ct'].sum()
        temp['fx_wage'] = temp['f_wage'] * temp['f_ct'] / temp['f_ct'].sum()
        temp['m_ratio'] = temp['m_wage'] / temp['m_wage'] * temp['f_ct'] / temp['f_ct'].sum()
        temp['f_ratio'] = temp['f_wage'] / temp['m_wage'] * temp['f_ct'] / temp['f_ct'].sum()
        m_ct = temp['m_ct'].sum()
        f_ct = temp['f_ct'].sum()
        m_ratio = round(temp['m_ratio'].sum(), 3)
        f_ratio = round(temp['f_ratio'].sum(), 3)
        m_wage = round(temp['mx_wage'].sum(), 3)
        f_wage = round(temp['fx_wage'].sum(), 3)
        m_summary = [var, 'Male', base_cat, m_wage, m_ratio, 'Male', m_ct]
        f_summary = [var, 'Female', base_cat, f_wage, f_ratio, 'Female', f_ct]
        output_sep.append(m_summary)
        output_sep.append(f_summary)
        
        t_ct = f_ct + m_ct
        diff = (m_wage - f_wage) / f_wage
        summary = [var, base_cat, 'F/M', diff, t_ct, m_wage, m_ratio, m_ct, f_wage, f_ratio, f_ct]
        output_grp.append(summary)
        
    else:
        for n in cat_list:
            m_ncat = grouped_df[(grouped_df[var] == n) & (grouped_df['SEX'] == 'Male')].reset_index()
            f_ncat = grouped_df[(grouped_df[var] == n) & (grouped_df['SEX'] == 'Female')].reset_index()
            m_base = grouped_df[(grouped_df[var] == base_cat) & (grouped_df['SEX'] == 'Male')].reset_index()

            temp = pd.DataFrame({'m_cat_wage': m_ncat.WAG, 'm_cat_ct': m_ncat.WAGP_count,
                                 'f_cat_wage': f_ncat.WAG, 'f_cat_ct': f_ncat.WAGP_count,
                                 'm_bas_wage': m_base.WAG, 'm_bas_ct': m_base.WAGP_count})
            temp = temp.loc[(temp['m_cat_ct'] >= 1) & (temp['f_cat_ct'] >= 1) & (temp['m_bas_ct'] >= 1)]

            temp['mx_wage'] = temp['m_cat_wage'] * temp['f_cat_ct'] / temp['f_cat_ct'].sum()
            temp['mx_ratio'] = temp['m_cat_wage'] / temp['m_bas_wage'] * temp['m_cat_ct'] / temp['m_cat_ct'].sum()
            m_ct = temp['m_cat_ct'].sum()
            m_wage = round(temp['mx_wage'].sum(), 3)
            m_ratio = round(temp['mx_ratio'].sum(), 3)
            m_summary = [var, n, base_cat, m_wage, m_ratio, 'Male', m_ct]
            output_sep.append(m_summary)

            temp['fx_wage'] = temp['f_cat_wage'] * temp['f_cat_ct'] / temp['f_cat_ct'].sum()
            temp['fx_ratio'] = temp['f_cat_wage'] / temp['m_bas_wage'] * temp['f_cat_ct'] / temp['f_cat_ct'].sum()
            f_ct = temp['f_cat_ct'].sum()
            f_wage = round(temp['fx_wage'].sum(), 3)
            f_ratio = round(temp['fx_ratio'].sum(), 3)
            f_summary = [var, n, base_cat, f_wage, f_ratio,'Female', f_ct]
            output_sep.append(f_summary)

            t_ct = f_ct + m_ct
            diff = (m_wage - f_wage) / f_wage
            summary = [var, n, base_cat, diff, t_ct, m_wage, m_ratio, m_ct, f_wage, f_ratio, f_ct]
            output_grp.append(summary)
    
    output_sep = pd.DataFrame(output_sep, columns = ['Variable', 'Category', 'Base_Category','Wage', 'Ratio', 'Sex', 'Count'])
    output_grp = pd.DataFrame(output_grp, columns = ['Variable', 'Category', 'Base_category', 'Percent_Difference', 'Total_Count',
                                                     'Male_Wage', 'Male_Ratio', 'Male_Count',
                                                     'Female_Wage', 'Female_Ratio', 'Female_Count'])
    return (output_sep, output_grp)

def singlebase_analysis(grouped_df):
    catagories = [['SEX', 'Male'], ['AGEB', '26-35'], ['EDU', 'BS'],
                  ['JOB', 'SAL'], ['RACE', 'WHT/MIX']]
    sep_full = pd.DataFrame()
    grp_full = pd.DataFrame()
    for n in catagories:
        score_cat = score_ratio(grouped_df, n[0], n[1])
        sep_full = pd.concat([sep_full, score_cat[0]])
        grp_full = pd.concat([grp_full, score_cat[1]])
    return (sep_full, grp_full)


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


def singleyear_multibase_analysis(year, mod_fit):
    raw_year = parse_single(year)
    group_df = df_transform_for_scoring(raw_year, mod_fit)
    sep_full, grp_full = multibase_analysis(group_df)
    
    return (sep_full, grp_full)


