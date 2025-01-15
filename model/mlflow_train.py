import sys
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import numpy as np
import mlflow
from mlflow.models import infer_signature

file_path = sys.argv[1]
data = pd.read_csv(file_path, delimiter=';', on_bad_lines='skip')

class InsuranceModel(mlflow.pyfunc.PythonModel):
    def __init__(self):
        self.preprocessor = None
        self.models = {}
        self.insurance_types = [
            'Liability Insurance',
            'Theft Insurance',
            'Premium Insurance',
            'Repair Insurance',
            'Premium Repair Insurance'
        ]

    def load_context(self, context):
        pass

    def predict(self, context, model_input, params):
        preprocessed = self.preprocessor.transform(model_input)

        predictions = {}
        for insurance in self.insurance_types:
            model = self.models[insurance]

            # predicted_price = np.clip(, y.min(), y.max())
            predicted_price = model.predict(preprocessed)
            predicted_price = predicted_price.clip(100, 5000)
            predictions[insurance] = predicted_price

        return predictions
    
def build_insurance_model():
    model_obj = InsuranceModel()

    features = ['Make', 'Model', 'Engine Power (HP)', 'Mileage (km)', 'Number of Accidents', 'Market Value ($)',
                'Total Owners', 'Has Dashcam', 'Vehicles in Family', 'Driving Experience', 'CAR_AGE',
                'AGE', 'HOMEKIDS', 'INCOME']

    if data['Has Dashcam'].dtype == 'object':
        data['Has Dashcam'] = data['Has Dashcam'].str.strip().str.lower().map({'true': 1, 'false': 0})

    for col in features + model_obj.insurance_types:
        if col in data.columns and data[col].dtype == 'object':
            data[col] = data[col].str.replace(',', '.').str.replace('[^0-9.]', '', regex=True)
            data[col] = pd.to_numeric(data[col], errors='coerce')

    numeric_features = [col for col in features if col not in ['Make', 'Model']]
    categorical_features = ['Make', 'Model']

    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    model_obj.preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features),
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    model_obj.models = {}

    X = data[features]
    
    model_obj.preprocessor.fit(X)

    preprocessed_X = model_obj.preprocessor.transform(X)

    for insurance in model_obj.insurance_types:
        y = data[insurance]

        X_train, X_test, y_train, y_test = train_test_split(preprocessed_X, y, test_size=0.2, random_state=42)

        model = GradientBoostingRegressor(random_state=42, n_estimators=300, learning_rate=0.03, max_depth=7)
        model.fit(X_train, y_train)

        # predict
        y_pred = model.predict(X_test)
        y_pred_clipped = np.clip(y_pred, y.min(), y.max())

        mse = mean_squared_error(y_test, y_pred_clipped)
        rmse = np.sqrt(mse)
        avg_diff = np.mean(y_pred_clipped - y_test)

        model_obj.models[insurance] = model

        mlflow.log_metric(insurance.replace(" ", "_") + "_MSE", mse)
        mlflow.log_metric(insurance.replace(" ", "_") + "_RMSE", rmse)
        mlflow.log_metric(insurance.replace(" ", "_") + "_AvgDiff", avg_diff)

    model.load_context(None)
    model_path = "insurance"
    model_input = make_input_from_single_entity_dict(single_entity)
    signature = infer_signature(model_input=model_input, model_output=model.predict(None, model_input, params={}), params={})
    
    print(signature)

    # export to mlflow
    mlflow.pyfunc.log_model(
        model_path,
        python_model=model,
        signature=signature,
        pip_requirements=["scikit-learn==1.5.2"],
        registered_model_name="insurance"
    )
    
def make_input_from_single_entity_dict(d):
    return pd.DataFrame.from_dict([d])[
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

single_entity = {
    'Make': 'Honda',
    'Model': 'Civic',
    'Engine Power (HP)': 202,
    'Mileage (km)': 40594,
    'Number of Accidents': 0,
    'Market Value ($)': 21440,
    'Total Owners': 1,
    'Has Dashcam': 1,
    'Vehicles in Family': 4,
    'Driving Experience': 3,
    'CAR_AGE': 18,
    'AGE': 60,
    'HOMEKIDS': 0,
    'INCOME': 67349
}

with mlflow.start_run():
    build_insurance_model()

# for insurance, metrics in model.metrics.items():
#     print(
#        f"{insurance} - MSE: {metrics['MSE']:.2f}, RMSE: {metrics['RMSE']:.2f}, Average Difference (Predicted - Real): {metrics['Average Difference (Predicted - Real)']:.2f}")