#!/usr/bin/env python
###############################################################################
#
# Author: Wiley Winters (wwinters@regis.edu)
#
# Assignment: Week 6 Visualizations with Matplotlib
#
# Class: MSDS 670 Data Visualization
#
# Date: 2024-FEB-25
#
###############################################################################

#
# Import required packages and libraries
#
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib import rcParams
import numpy as np

# Suppress Warnings
import warnings
warnings.filterwarnings('ignore')

# Set seaborn autoconfig to True
rcParams.update({'figure.autolayout': True})

#
# Read dataset into Pandas DataFrame
#
jobs_df = pd.read_csv('../data/jobs_in_data.csv')

#
# Perform some basic EDA
#
print(jobs_df.info())
print('\nNaN Values:\n', jobs_df.isna().sum())
print('\nDuplicates: ', jobs_df.duplicated().sum())
print('\nSize: ', jobs_df.size)
print('\nDistribution:\n', jobs_df.describe().T)

#
# Remove duplicates
#
jobs_df.drop_duplicates(keep='first', inplace=True)

#
# EDA performed using Jupyter Lab indicated that some countries in
# the dataset do not have enough records to analyze using methods
# such as mean or average.
#
# I will remove them from the dataset
#
countries = ['United States', 'United Kingdom', 'Canada', 'Germany',
             'Spain', 'France', 'Portugal', 'Netherlands', 'Australia',
             'Brazil', 'Colombia', 'Italy', 'Greece']
jobs_df = jobs_df[jobs_df['company_location'].isin(countries)]
jobs_df = jobs_df[jobs_df['employee_residence'].isin(countries)]

#
# Create visualizations for analysis and pesentation
#

# Highest pay by employee_residence in USD.  Top 15
pay_residence = jobs_df.groupby('employee_residence').agg({'salary_in_usd': 'mean'}). \
                               sort_values('salary_in_usd', ascending=False).head(15)
fig, ax = plt.subplots(figsize=(10,6))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.set(xlabel='Employee\'s Country of Residence', ylabel='Average Annual Salary in USD', \
       title='Where You Live Determines Pay in USD (Top 15)', ylim=(0,250000))
sns.barplot(data=pay_residence, x='employee_residence', y='salary_in_usd')
plt.xticks(rotation=45, ha='right', rotation_mode='anchor')
textstr = '\n'.join(('United States has the highest average',
                     'pay out of the countries in this study'))
ax.annotate(textstr, xy=(0.2,170000), xytext=(0.7,225000), bbox=props, 
            fontsize=10, arrowprops=dict(facecolor='black', shrink=0.05))
ax.bar_label(ax.containers[0], fmt='${:,.0f}')
fig.savefig('../images/highResidenceUSD.png', bbox_inches='tight', dpi=300)

# Average salary based on company size
sizes = ('Small','Medium','Large')
size = jobs_df.groupby('company_size').agg({'salary_in_usd': 'mean'}). \
                        sort_values('company_size', ascending=False)
fig, ax = plt.subplots(figsize=(10,6))
sns.barplot(data=size, x='company_size', y='salary_in_usd')
ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
x_pos = np.arange(len(sizes))
ax.set_xticks(x_pos, labels=sizes)
ax.set(xlabel='Company Size', ylabel='Average Annual Salary in USD',
       title='Average Annual Salary based on Company Size',
       ylim=(0,180000))
textstr = '\n'.join(('Medium sized organizations',
                     'tend to pay more than smaller',
                     'and larger ones on average'))
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.7, 0.98, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)
ax.bar_label(ax.containers[0], fmt='${:,.0f}')
fig.savefig('../images/aveCompanySize.png', bbox_inches='tight', dpi=300)

# Average salary by job category and company size
fig, ax = plt.subplots(figsize=(12,8))
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.set(xlabel='Annual Average Salary in USD', ylabel='Job Category',
       title='Average Salary by Job Category and Company Size',
       xlim=(0,225000))
hue_order = ['S', 'M', 'L']
bar_colors = ['grey', 'olive', 'purple']
sns.barplot(data=jobs_df, x='salary_in_usd', y='job_category', hue='company_size',
            hue_order=hue_order, palette=bar_colors, ci=None)
ax.legend(['Small','Medium', 'Large'], title='Company Size')
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
text1 = '\n'.join(('As companies grow, they start',
                   'to view data as a resource',
                   'that requires specialized',
                   'planning and governance'))
text2 = '\n'.join(('Medium sized companies pay', 
                   'ML/AI engineers more than',
                   'managers. This may indicate',
                   'that ML/AI skills are more',
                   'valued'))
an1 = ax.annotate(text1, xytext=(172000,2.70), xy=(149000,1.4), bbox=props,
                  fontsize=9, arrowprops=dict(facecolor='black', shrink=0.05))
an2 = ax.annotate(text2, xytext=(172000,4.53), xy=(149000,3.2), bbox=props,
                  fontsize=9, arrowprops=dict(facecolor='black', shrink=0.05))
an3 = ax.annotate(text2, xytext=(172000,4.53), xy=(149000,5.0), bbox=props,
                  fontsize=9, arrowprops=dict(facecolor='black', shrink=0.05))
fig.savefig('../images/aveCatSize.png', bbox_inches='tight', dpi=300)

# Average Salary by job category and work setting
fig, ax = plt.subplots(figsize=(12,8))
ax.xaxis.set_major_formatter(mtick.StrMethodFormatter('${x:,.0f}'))
ax.set(xlabel='Annual Average Salary in USD', ylabel='Job Category',
       title='Average Salary by Job Category and Work Setting in USD', xlim=(0,225000))
hue_order = ['In-person', 'Hybrid', 'Remote']
bar_colors = ['lightgrey', 'burlywood', 'royalblue']
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
sns.barplot(data=jobs_df, x='salary_in_usd', y='job_category', hue='work_setting', 
            hue_order=hue_order, palette=bar_colors, ci=None)
ax.legend(title='Work Setting')
text1 = '\n'.join(('No longer do people have to',
                   'commute to the office to earn',
                   'a good salary'))
ax.text(0.7, 0.55, text1, transform=ax.transAxes, fontsize=9,
        verticalalignment='top', bbox=props)
fig.savefig('../images/aveCatWork.png', bbox_inches='tight', dpi=300)