import os
import modal
    
LOCAL=False

if LOCAL == False:
   stub = modal.Stub()
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

    

if __name__ == "__main__":
    if LOCAL == True :
        g()
    else:
        with stub.run():
            f()

