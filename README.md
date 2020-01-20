## American Community Survey (PUMS) Gender vs. Wage Analysis
**Quantifying the gender wage gap while normalizing for age, education, industry, region, and race** <br/>

**Language:** Python &emsp;&emsp;&emsp;**Libraries:** pandas, sklearn, seaborn, numpy, glob, time

The American Community Survey (ACS) Public Use Microdata Sample (PUMS) datasets contain information on anonymous individuals in the US that looks to mimic the wide berth of diversity in the country. This information includes family history, income from various sources, background, and more. This individual’s chosen to record responses in this survey were statistically selected to mimic the US and are equivalent to about one percent of the US's population in each year's datafile. Data from 2008 to 2018 was retrieved to compare any year by year changes.

The goals of this study is to **(1)** output a single score that most accurately represents the wage gap between genders while accounting for a person's age, education, industry, region, and race, **(2)** create a model to predict a person's wage given the same parameters while also being able to visualize it given user input, **(3)** manage large datasets efficiently create workflows and custom functions to accommodate.

Overall, the quantified age gap predicted was **81%** ( $ female / $ male ).

## Graphical Summary:
#### Year over Year $ Female / $ Male Wage:
![alt text](/images/wage_year.png "")

| Year | $ Female / $ Male |
|:----:|:-----------------:|
| 2008 | 0.840             |
| 2009 | 0.780             |
| 2010 | 0.818             |
| 2011 | 0.811             |
| 2012 | 0.784             |
| 2013 | 0.820             |
| 2014 | 0.824             |
| 2015 | 0.817             |
| 2016 | 0.812             |
| 2017 | 0.795             |
| 2018 | 0.818             |
#### Age vs. Wages:
![alt text](/images/age_wage.png "Age vs. Wage")
#### Age vs. Wages (Binned):

| &emsp; **(1)** = 18-25 &emsp; | &emsp; **(2)** = 26-35 &emsp; | &emsp; **(3)** = 36-45 or 66-70 &emsp; | &emsp; **(4)** = 46-65 &emsp; |

![alt text](/images/age_wage_sex.png "Age vs. Wage")
#### Industry vs. Wages:
![alt text](/images/job_wage.png "")
![alt text](/images/job_wage_sex.png "")
#### Education vs. Wages:
| &emsp; **(1)** = No HS or HS Equivalent &emsp; | &emsp; **(2)** = Some College or Associates &emsp; | &emsp; **(3)** = Bachelor’s Degree &emsp; |

| &emsp; **(4)** = Master’s Degree &emsp; | &emsp; **(5)** = Doctorate / Other Higher &emsp; |
![alt text](/images/edu_wage_sex.png "")
#### Region vs. Wages:
| &emsp; **(1)** = Northeast and Outlying Regions &emsp; | &emsp; **(2)** = Midwest &emsp; | &emsp; **(3)** = South &emsp; | &emsp; **(4)** = West &emsp; |
![alt text](/images/region_wage.png "")
![alt text](/images/region_wage_sex.png "")
#### Race vs. Wages:
![alt text](/images/race_wage.png "")
![alt text](/images/race_wage_sex.png "")
## Sections of Notebook:
1. Introduction <br/>
    1.1 Importing Data Files (2018 - 2008) <br/>
    1.2. Initial Data Analysis <br/>
2. Data Selection <br/>
    2.1. Full-Time Detection <br/>
    2.2. Outlier <br/>
3. Feature Transformation <br/>
    3.1. Age Bins <br/>
    3.2. Education Categorization <br/>
    3.3. Occupation Grouping <br/>
    3.4. State Observations <br/>
    3.5. Race <br/>
4. Dataframe Management <br/>
    4.1. Remove Columns <br/>
    4.2. OHE Columns <br/>
5. Preprocessing Pipeline <br/>
6. Modeling <br/>
    6.1. Random Forest <br/>
    6.2. Feature Selection <br/>
7. Analysis <br/>
    7.1. Scoring Rational <br/>
    7.2. Year to Year Analysis <br/>
    7.3. Simple Wage Predictor <br/>
