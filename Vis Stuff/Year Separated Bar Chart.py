import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

Uwhatever_df = pd.read_csv('u21_mins (TEs).csv')

Uwhatever_df.loc[:,['U21','U20','U19','U18','U17','U16']].plot.bar(stacked=True, figsize=(10,7), title='U21 Minutes By Year, Separated By Age Allotted')

labels = ['2010','2011','2012','2013','2014','2015','2016','2017','2018']

locs, l = plt.xticks()
plt.xticks(locs, labels)
plt.xlabel('Year')

plt.show()