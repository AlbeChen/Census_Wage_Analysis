import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap_basecat(cat_full, var):
    color_dict = {'SEX': 'coolwarm', 'JOB': 'RdPu',
                    'AGE': 'YlGn', 'RACE': 'Oranges',
                    'EDU': 'Blues'}
    color = color_dict[var]
    plt.figure(figsize=(7,7))
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]
    heatmap_group = heatmap_group.groupby(['Category', 'Base_Category']) \
        ['Ratio_vs_Base'].agg(['count','mean','std']).reset_index()
    heatmap_group = heatmap_group.pivot('Category', 'Base_Category', 'mean')
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False, 
                cmap = color, fmt='.1f')


def plot_heatmap_lineplot(cat_full, yearly_sex_full, var):
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(18, 5))

    color_dict = {'SEX': 'coolwarm', 'JOB': 'RdPu',
                    'AGE': 'YlGn', 'RACE': 'Oranges',
                    'EDU': 'Blues'}
    color = color_dict[var]
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]
    heatmap_group = heatmap_group.groupby(['Category', 'Base_Category']) \
        ['Ratio_vs_Base'].agg(['count','mean','std']).reset_index()
    heatmap_group = heatmap_group.pivot('Category', 'Base_Category', 'mean')
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False, 
                cmap = color, fmt='.1f', ax=ax[0])
    ax[0].title.set_text('Heatmap of %s' % var)

    ratio_yearly = yearly_sex_full.loc[(yearly_sex_full.Variable == var)]
    sns.lineplot(x='Year', y='F_M_Ratio_Avg', hue='Category', data=ratio_yearly, ax=ax[1])
    ax[1].get_legend().remove()
    ax[1].title.set_text('Wage for each %s over 2008 - 2018' % var)

    ratio_yearly = yearly_sex_full.loc[(yearly_sex_full.Variable == var)]
    sns.lineplot(x='Year', y='F_Pct_Ct', hue='Category', data=ratio_yearly, ax=ax[2])
    ax[2].legend(bbox_to_anchor=(1, 1))
    ax[2].title.set_text('Wage for each %s over 2008 - 2018' % var)


def plot_ratio_ordered(sex_full):
    sns.set_palette(sns.color_palette('hls', 8))
    palette ={'SEX': 'C6', 'JOB': 'C1',
                'AGE': 'C3', 'RACE': 'C0',
                'EDU': 'C4'}

    sex_full_sort = sex_full.groupby(['Category']).agg('mean').reset_index()
    sex_full_sort = sex_full_sort.sort_values(by=['F_M_Ratio_Avg'])
    sex_full_list = sex_full_sort['Category'].tolist()
    sns.catplot(y='F_M_Ratio_Avg', x='Category', hue='Variable', data=sex_full,
                dodge=False, kind='bar', palette=palette,
                height=4, aspect=3, order=sex_full_list)
    plt.xticks(rotation=60)
    plt.ylim(0,1)
    plt.ylabel('Wage Female / Wage Male (\$ /\$)')
    plt.title('\$ Wage Female / \$ Wage Male (Female Basis)')

    