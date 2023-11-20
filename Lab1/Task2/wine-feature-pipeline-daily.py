import os
import modal
    
LOCAL=False

if LOCAL == False:
   stub = modal.Stub("wine_daily_pipeline")
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn==1.3.0","dataframe-image"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()

def generate_wine():
    import pandas as pd
    import numpy as np

    wine_df = pd.read_csv('https://raw.githubusercontent.com/ID2223KTH/id2223kth.github.io/master/assignments/lab1/wine.csv')
    wine_df.columns = wine_df.columns.str.replace(' ', '_')
    wine_df.columns = wine_df.columns.str.lower()
    print(wine_df.head())

    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    wine_df['type'] = le.fit_transform(wine_df['type'])
    print(wine_df.head())
    wine_df_y = wine_df['quality']
    type_df = wine_df['type']
    wine_df = wine_df.drop(['type'], axis=1)
    wine_df = wine_df.drop(['quality'], axis=1)
    print(wine_df.head())
    import random
    random.seed(42)
    random_int = random.randint(1, len(wine_df))
    print(random_int)
    synth_data = wine_df.sample(n=random_int)
    print(synth_data.head())
    
    most_frequent = type_df.value_counts().idxmax()
    print(most_frequent)
    

    mean_data = pd.DataFrame(synth_data.mean()).transpose()
    print(mean_data.head())
    mean_data['ratio_sulfur_dioxide'] = mean_data['free_sulfur_dioxide']/mean_data['total_sulfur_dioxide']
    mean_data['skewness'] = mean_data.skew(axis = 1, skipna = True)
    mean_data['kurtosis'] = mean_data.kurtosis(axis = 1, skipna = True)
    mean_data['mean'] = mean_data.mean(axis = 1, skipna = True)
    mean_data['median'] = mean_data.median(axis = 1, skipna = True)
    mean_data['variance'] = mean_data.var(axis = 1, skipna = True)
    mean_data['std'] = mean_data.std(axis = 1, skipna = True)
    mean_data['cv'] = mean_data.std(axis = 1, skipna = True)/mean_data.mean(axis = 1, skipna = True)
    mean_data['range'] = mean_data.max(axis = 1, skipna = True) - mean_data.min(axis = 1, skipna = True)
    mean_data['iqr'] = mean_data.quantile(q=0.75, axis=1) - mean_data.quantile(q=0.25, axis=1)
    mean = [1.32617810e+00,1.64965628e-01,1.45381413e-01,
     4.75798474e+00,3.50417288e-02,1.77480338e+01,5.65175045e+01,
     2.99844222e-03,2.00322077e-01,1.49339305e-01,1.19261996e+00,
     1.24635133e-01,5.33233574e-01,3.10338694e+00,4.96250939e+00,
     5.59999753e-01,8.11946649e+02,1.90343823e+02,5.51748235e-01,
     8.11930146e+02,3.76404974e+00]
    std= [7.20547176e+00,3.39272741e-01,3.18574727e-01,
     5.44265045e+00,5.60243189e-02,3.05253194e+01,1.15744574e+02,
     9.94696634e-01,3.21393720e+00,5.30888102e-01,1.04918008e+01,
     2.86767940e-01,3.00198372e+00,1.03539209e+01,1.26173180e+01,
     2.70951027e+00,9.71837196e+02,2.28237885e+02,2.73221508e+00,
     9.71806016e+02,1.29150916e+01]
    
    df = (mean_data-mean)/std
    ## add wine_df_y to df
    df['quality'] = wine_df_y
    ## add type to df in the first column

    df.insert(0, 'type', type_df)
    print(df.head)




def g():
    import hopsworks
    import pandas as pd

    project = hopsworks.login()
    fs = project.get_feature_store()

    wine_df = generate_wine()

    # wine_fg = fs.get_feature_group(name="winequality",version=8)
    # wine_fg.insert(wine_df) 

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("iris_daily")
        with stub.run():
            f()

