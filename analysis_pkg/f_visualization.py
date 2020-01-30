import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap_basecat(grp_full, var, Male_or_Female):
    sex_ratio = ("%s_Ratio" % Male_or_Female)
    plt.figure(figsize=(7,7))
    heatmap_group = grp_full.loc[(grp_full.Variable == var)]
    heatmap_group = heatmap_group.pivot("Category", "Base_category", sex_ratio)
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    ax = sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False)