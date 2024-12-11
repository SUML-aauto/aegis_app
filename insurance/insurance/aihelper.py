import pandas as pd
import skops.io as sio
from sklearn.ensemble import GradientBoostingClassifier
from django.conf import settings

pipeline: GradientBoostingClassifier = sio.load(settings.BASE_DIR / 'model.skops', trusted=[
    'sklearn._loss.link.Interval', 
    'sklearn._loss.link.LogitLink',
    'sklearn._loss.loss.HalfBinomialLoss',
    'sklearn.compose._column_transformer._RemainderColsList'
])

def predict_insurance_claim(data):
    row = pd.DataFrame.from_dict([data])

    return pipeline.predict(row[
        [
            'Make',
            'Fuel Type',
            # 'Model',
            'Engine Power (HP)',
            'Driving Experience',
            'INCOME',
            'GENDER',
            'CAR_TYPE',
        ]
    ])[0] > 0.5