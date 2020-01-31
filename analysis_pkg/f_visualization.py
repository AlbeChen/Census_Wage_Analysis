import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap_basecat(grp_full, var):
    plt.figure(figsize=(7,7))
    heatmap_group = grp_full.loc[(grp_full.Variable == var)]
    heatmap_group = heatmap_group.pivot("Category", "Base_Category", 'Ratio_vs_Base')
    heatmap_group['sum'] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=['sum'], ascending=False)
    heatmap_group = heatmap_group.drop(columns=['sum'])
    heatmap_group = heatmap_group[list(heatmap_group.index)] #[::-1]
    ax = sns.heatmap(heatmap_group, annot=True, linewidths=.5, cbar=False)