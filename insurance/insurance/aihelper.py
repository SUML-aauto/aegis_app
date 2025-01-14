import pandas as pd
import skops.io as sio
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.base import BaseEstimator
from django.conf import settings

insurance_types = [
    'Liability Insurance',
    'Theft Insurance',
    'Premium Insurance',
    'Repair Insurance',
    'Premium Repair Insurance'
]

class ModelsStorage:
    def __init__(self):
        self.models: GradientBoostingClassifier | None = None
        self.preprocessor: BaseEstimator | None = None

    def ensure_loaded(self):
        if self.models is not None:
            return

        self.models = sio.load(settings.BASE_DIR / 'model2.skops', trusted=[
            'sklearn._loss.link.Interval', 
            'sklearn._loss.link.LogitLink',
            'sklearn._loss.loss.HalfBinomialLoss',
            'sklearn.compose._column_transformer._RemainderColsList',
            'numpy.dtype',
            'sklearn._loss.link.IdentityLink',
            'sklearn._loss.loss.HalfSquaredError'
        ])

        self.preprocessor = self.models['preprocessor']

models_storage = ModelsStorage()
    
def predict_insurance_pricing(data):
    models_storage.ensure_loaded()

    single_entity = pd.DataFrame.from_dict([data])[
        [
            'Make',
            'Model',
            'Engine Power (HP)',
            'Mileage (km)',
            'Number of Accidents',
            'Market Value ($)',
            'Total Owners',
            'Has Dashcam',
            'Vehicles in Family',
            'Driving Experience',
            'CAR_AGE',
            'AGE',
            'HOMEKIDS',
            'INCOME'
        ]
    ]
    single_entity_preprocessed = models_storage.preprocessor.transform(single_entity)

    single_entity_predictions = {}
    for insurance in insurance_types:
        model = models_storage.models[insurance]

        # predicted_price = np.clip(, y.min(), y.max())
        predicted_price = model.predict(single_entity_preprocessed)[0]
        if predicted_price < 100:
            predicted_price = 100
        if predicted_price >= 5000:
            predicted_price = 5000
        single_entity_predictions[insurance] = predicted_price

    return single_entity_predictions
