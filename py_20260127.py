
# %%

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import urllib.request
import os
import zipfile
import os

# %%

def download_data(force=False):
    """Download and extract course data from Zenodo."""
    
    zip_path = 'data.zip'
    data_dir = './data'
    
    if not os.path.exists(zip_path) or force:
        print("Downloading course data...")
        urllib.request.urlretrieve(
            'https://zenodo.org/records/18235955/files/data.zip?download=1',
            zip_path
        )
        print("Download complete")
    
    if not os.path.exists(data_dir) or force:
        print("Extracting data files...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_dir)
        print("Data extracted")
    
    return data_dir



if __name__ == "__main__":
    download_data()

# %%

df = pd.read_csv('./data/craiglist_cville_cars_long.csv', encoding="latin1")
df.head()

# %%
sns.histplot(np.log(df['price']), bins=50)

df['price'].describe()

# %%
#how to read: essientally the more a value appears in a table, the higher its density
sns.kdeplot(df['price'])

# %%
#how to read: for example, about 40% of the population (cars) is below 5,000$
#better for getting probablity than kde
#great for getting say the median (start from the vertical axis and find the x-value), this is the same as using np.quantile(df['price'], .5)
sns.ecdfplot(df['price'])

# %%
#median is robust, meaning that changest to our highest/lowest values won't change it much, unlike mean

#IQR (interquartile range) is the distance between the .25 and the .75 range aka 50% of the observation
#Kinda like std. dev., essentially saying how spread out is the data based on its central tendencies

x = df['price']

#boxplot shows us which values are extreme and which arent!
#anything outside of the whiskers are outliers
sns.boxplot(x)

# %%
def outlier_analyze(x):
    q75 =np.quantile(x, .75) 
    q25 =np.quantile(x, .25) 

    iqr = q75 - q25
    upperWhisker = q75 + 1.5 * iqr
    lowerWhisker = q25 - 1.5 * iqr

    upperOutlier = ( x > upperWhisker).astype(int)

    lowerOutlier = ( x < lowerWhisker).astype(int)
    outlier = upperOutlier + lowerOutlier

    #locates/displays the rows that are upperOutlier aka when the upperOutlier is true/1
    df.loc[upperOutlier == 1, : ]

    winsorize = {
        upperOutlier * upperWhisker + #map upper outliers to upper whisker
        
        lowerOutlier * lowerWhisker + #map lower outliers to lower whisker
        
        (1 - outlier) * x #if neither, keep original value
    }

    return outlier, winsorize

# %%
outlier, winsorize = outlier_analyze(x)

#now instead of the upper outlier going all the way up to 38,000, it has been mapped to ~20,000

sns.scatterplot(x=x, y=winsorize)

sns.boxplot(x = winsorize)

# %%
#the violin plot combines boxplot and kde plot
sns.violinplot(x=x, fill=False, inner='quart')