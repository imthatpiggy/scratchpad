
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
