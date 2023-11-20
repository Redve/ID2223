import os
import modal
    
LOCAL=False

if LOCAL == False:
   stub = modal.Stub("wine_inference_pipeline")
   hopsworks_image = modal.Image.debian_slim().pip_install(["hopsworks","joblib","seaborn","scikit-learn==1.3.0","dataframe-image"])
   @stub.function(image=hopsworks_image, schedule=modal.Period(days=1), secret=modal.Secret.from_name("HOPSWORKS_API_KEY"))
   def f():
       g()


def g():
    import pandas as pd
    import hopsworks
    import joblib
    import datetime
    from PIL import Image
    from datetime import datetime
    import dataframe_image as dfi
    from sklearn.metrics import confusion_matrix
    from matplotlib import pyplot
    import seaborn as sns
    import requests
    import numpy as np

    project = hopsworks.login()
    fs = project.get_feature_store()

    mr = project.get_model_registry()
    model = mr.get_model("wine_model", version=5)
    model_dir = model.download()
    
    model = joblib.load(model_dir + "/wine_model.pkl")

    feature_view = fs.get_feature_view(name="winequality", version=8)
    batch_data = feature_view.get_batch_data()

    y_pred = model.predict(batch_data)

    offset = 1
    wine = y_pred[y_pred.size-offset]
    print("Wine Quality: " + str(wine))
    quality_url = "https://raw.githubusercontent.com/Redve/ID2223/main/Lab1/Task2/assets/" + str(wine) + ".png"
    img = Image.open(requests.get(quality_url, stream=True).raw)
    img.save("./latest_wine.png")
    dataset_api = project.get_dataset_api()
    dataset_api.upload("./latest_wine.png", "Resources/wine/images", overwrite=True)

    wine_fg = fs.get_feature_group(name="winequality", version=8)
    df = wine_fg.read()
    label = str(df.iloc[-offset]["quality"])
    label = label.replace(".0", "")
    print("Wine Quality: " + label)

    label_url = "https://raw.githubusercontent.com/Redve/ID2223/main/Lab1/Task2/assets/" + str(label) + ".png"
    img = Image.open(requests.get(label_url, stream=True).raw)
    img.save("./actual_wine.png")
    dataset_api.upload("./actual_wine.png", "Resources/wine/images", overwrite=True)
    monitor_fg = fs.get_or_create_feature_group(name="wine_predictions",
                                                version=3,
                                                primary_key=["datetime"],
                                                description="Wine Quality Prediction/Outcome Monitoring")
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    data = {
        "prediction": [wine],
        "label": [label],
        "datetime": [now]
    }
    monitor_df = pd.DataFrame(data)
    monitor_fg.insert(monitor_df, write_options={"wait_for_job" : False})

    history_df = monitor_fg.read()

    df_recent = history_df.tail(4)
    dfi.export(df_recent, './df_recent.png', table_conversion = 'matplotlib')
    dataset_api.upload("./df_recent.png", "Resources/wine/images", overwrite=True)
    
    predictions = history_df[['prediction']]
    labels = history_df[['label']] 

    print("Uploaded pictures")


if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        stub.deploy("wine_inference")
        with stub.run():
            f()

