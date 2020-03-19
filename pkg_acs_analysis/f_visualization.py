import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# plotting wage ratio for each catagory in each variable and orginizing by ratio
def plot_ratio_ordered(sex_full):
    dict_color = {
        "SEX": "C4",
        "JOB": "C3",
        "AGE": "C2",
        "RACE": "C1",
        "EDU": "C0",
        "DIV": "C5",
    }
    sns.set_style("whitegrid")
    sex_full_sort = sex_full.groupby(["Category"]).agg("mean").reset_index()
    sex_full_sort = sex_full_sort.sort_values(by=["F_M_Ratio_Avg"])
    sex_full_list = sex_full_sort["Category"].tolist()
    sns.catplot(
        y="F_M_Ratio_Avg",
        x="Category",
        hue="Variable",
        data=sex_full,
        dodge=False,
        kind="bar",
        palette=dict_color,
        height=4,
        aspect=3,
        order=sex_full_list,
    )
    plt.xticks(rotation=60)
    plt.ylim(0, 1)
    plt.ylabel("Gendered Wage Ratio (F/M)")
    plt.title("Wage Ratio vs. Categories")
    plt.savefig(
        "images/Wage_Ratio_Ordered.png", bbox_inches="tight", pad_inches=0.2, dpi=1000
    )


# simple catplot looking at sex wage difference for each variable
def plot_sex_n_cat(yearly_sex_sep):
    sns.catplot(
        y="Wage_Avg",
        x="Sex",
        hue="Category",
        col="Variable",
        aspect=0.3,
        height=6,
        data=yearly_sex_sep,
    )
    plt.savefig(
        "images/Wage_Category_Plot.png", bbox_inches="tight", pad_inches=0.2, dpi=1000
    )


# 3 plots thats unique for each variable
def plot_heatmap_lineplot(cat_full, yearly_sex_full, var):
    # 3 subplots
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(16, 5))

    color_dict = {
        "SEX": "coolwarm",
        "JOB": "RdPu",
        "AGE": "YlGn",
        "RACE": "Oranges",
        "EDU": "Blues",
        "DIV": "Purples",
    }
    color = color_dict[var]

    # PLOT 1: heatmap for each variable - to show each catagory vs. a base catagory
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]

    # used to rename education str to shorter versions
    if var == "EDU":
        edu_dict = {
            "No_Highschool": "N_HS",
            "Highschool": "HS",
            "Some_College": "CLG",
            "B.S._Degree": "BS",
            "M.S._Degree": "MS",
            "PhD_or_Prof": "PhD",
        }
        heatmap_group["Category"] = heatmap_group["Category"].map(edu_dict)
        heatmap_group["Base_Category"] = heatmap_group["Base_Category"].map(edu_dict)

    # rename job str to shorter versions
    elif var == "JOB":
        job_dict = {
            "Business": "BUS",
            "Science": "SCI",
            "Art": "ART",
            "Healthcare": "HLC",
            "Services": "SRV",
            "Sales": "SAL",
            "Maintenance": "MTN",
            "Production": "PRD",
            "Transport": "TRP",
            "Military": "MTY",
        }
        heatmap_group["Category"] = heatmap_group["Category"].map(job_dict)
        heatmap_group["Base_Category"] = heatmap_group["Base_Category"].map(job_dict)

    elif var == "DIV":
        job_dict = {
            "East North Central": "NE-C",
            "East South Central": "SE-C",
            "Middle Atlantic": "M-Atl",
            "Mountain": "MTN",
            "New England": "NE",
            "Pacific": "PCF",
            "South Atlantic": "S-Alt",
            "West North Central": "NW-C",
            "West South Central": "SW-C",
        }
        heatmap_group["Category"] = heatmap_group["Category"].map(job_dict)
        heatmap_group["Base_Category"] = heatmap_group["Base_Category"].map(job_dict)

    # grouping each category vs base category and mapped out vs. each other
    heatmap_group = (
        heatmap_group.groupby(["Category", "Base_Category"])["Ratio_vs_Base"]
        .agg(["count", "mean", "std"])
        .reset_index()
    )
    heatmap_group = heatmap_group.pivot("Category", "Base_Category", "mean")
    heatmap_group["sum"] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=["sum"], ascending=False)
    heatmap_group = heatmap_group.drop(columns=["sum"])
    heatmap_group = heatmap_group[list(heatmap_group.index)]

    sns.heatmap(
        heatmap_group,
        annot=True,
        linewidths=0.5,
        cbar=False,
        cmap=color,
        fmt=".1f",
        ax=ax[0],
    )
    ax[0].title.set_text("Wage Difference of Categories in %s" % var)

    sns.set_style("whitegrid")

    ratio_yearly = yearly_sex_full.loc[(yearly_sex_full.Variable == var)]

    # PLOT 2: lineplot to show yearly change in f/m wage difference for each cat in var
    sns.lineplot(
        x="Year", y="F_M_Ratio_Avg", hue="Category", data=ratio_yearly, ax=ax[1]
    )
    ax[1].set(xlim=(2008, 2018), ylim=(0.70, 0.93))
    ax[1].get_legend().remove()
    ax[1].set_ylabel("Wage Ratio (F/M)")
    ax[1].title.set_text("Wage F / Wage M per %s (2008-2018)" % var)

    # PLOT 3: lineplot to shower yearly change %F in the work force for each cat in var
    sns.lineplot(x="Year", y="F_Pct_Ct", hue="Category", data=ratio_yearly, ax=ax[2])
    if var == "JOB":
        ax[2].set(xlim=(2008, 2018))
    else:
        ax[2].set(xlim=(2008, 2018), ylim=(0.25, 0.55))
    ax[2].legend(bbox_to_anchor=(1, 1))
    ax[2].set_ylabel("Percent Female")
    ax[2].title.set_text("Percent Female per %s (2008-2018)" % var)

    path = "images/heatmap_lineplot_%s.png" % var
    fig.savefig(path, bbox_inches="tight", pad_inches=0.2, dpi=1000)


# basic heatmap plotting for single var
def plot_heatmap_basecat(cat_full, var):
    color_dict = {
        "SEX": "coolwarm",
        "JOB": "RdPu",
        "AGE": "YlGn",
        "RACE": "Oranges",
        "EDU": "Blues",
    }
    color = color_dict[var]
    plt.figure(figsize=(7, 7))
    heatmap_group = cat_full.loc[(cat_full.Variable == var)]
    heatmap_group = (
        heatmap_group.groupby(["Category", "Base_Category"])["Ratio_vs_Base"]
        .agg(["count", "mean", "std"])
        .reset_index()
    )
    heatmap_group = heatmap_group.pivot("Category", "Base_Category", "mean")
    heatmap_group["sum"] = heatmap_group.iloc[:, :].sum(axis=1)
    heatmap_group = heatmap_group.sort_values(by=["sum"], ascending=False)
    heatmap_group = heatmap_group.drop(columns=["sum"])
    heatmap_group = heatmap_group[list(heatmap_group.index)]
    sns.heatmap(
        heatmap_group, annot=True, linewidths=0.5, cbar=False, cmap=color, fmt=".1f"
    )
