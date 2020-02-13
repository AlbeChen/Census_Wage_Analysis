## American Community Survey (ACS) Wage Analysis
**Quantifying the wage gap while normalizing for sex, age, education, industry, and race**

**Language:** Python (pandas, sklearn, matplotlib, seaborn, numpy) <br/>
**Software:** Tableau, Jupyter Notebook


The American Community Survey (ACS) Public Use Microdata Sample (PUMS) datasets contain information on anonymous individuals in the US that looks to mimic the wide berth of diversity in the country. Each year's dataset, is equivalent to about one percent of the US's population and contains information on family history, incomes, background, and more.

The objective of this study is to quantify the wage difference between various variables (Age, Education, Job Industry, Race, and Sex) and catagoires within each (ex: Education catagories would include - BS, No Highschool, ect.) by normalizing each subset of catagory and variable combinations. To achieve this the following was preformed:

    ** Main Files **
    - /ACS_analysis_pkg #analysis functions from preprocessing to final output
       |--__init__.py
       |--a_parse_yearly_df.py
       |--b_preprocessing_pipeline.py
       |--c_model_fitting.py
       |--d_df_transform.py
       |--e_output_analysis.py
       |--f_visualization.py
    - ACS_Notebook_Final_Analysis.ipynb #summary of results
    - ACS_Tableau_Visualization.pdf/twb #pivotable visualization
    
    ** Support Files **
    - /data_raw #download raw data and add into folder as needed
       |--2018
       |------
       |--2008
    - /data_output #output data from final analysis notebook
    - /images #images saved from final analysis
    - /initial_analysis #notebook and images of intial data exploration
    - /ACS_technical_documents #documentation on dataset
    


    
   
## Visual Summary (Figures)
#### Tableau Dashboards: pivots across different variables and years
![alt text](/images/ACS_Tableau_Visualization.jpg "ACS_Tableau_Visualization")
#### Python Seaborn Plots: functions to visualize given a specifed variable
![alt text](/images/heatmap_lineplot_JOB.png "heatmap_lineplot_JOB")
![alt text](/images/heatmap_lineplot_EDU.png "heatmap_lineplot_EDU")
