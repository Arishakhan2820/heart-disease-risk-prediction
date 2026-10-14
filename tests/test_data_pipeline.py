from src.data_loader import clean_data, load_raw_data
from src.preprocessing import build_preprocessor
from src.predict import predict_risk
import numpy as np
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from src.explain_model import create_local_explainer, explain_local_prediction


class DemoPipeline:
    classes_ = np.array([0, 1])

    def predict_proba(self, frame):
        assert list(frame.columns) == ["age"]
        return np.array([[0.2, 0.8]])


class ReversedClassPipeline(DemoPipeline):
    classes_ = np.array([1, 0])

    def predict_proba(self, frame):
        assert list(frame.columns) == ["age"]
        return np.array([[0.8, 0.2]])

def test_supplied_data_loads():
    data = load_raw_data("data/raw/heart.csv")
    assert data.shape == (1025, 14)
    assert set(data.target.unique()) == {0, 1}

def test_cleaning_and_preprocessing():
    data = clean_data(load_raw_data("data/raw/heart.csv"))
    assert len(data) == 302
    transformed = build_preprocessor().fit_transform(data.drop(columns="target"))
    assert transformed.shape[0] == len(data)


def test_prediction_contract():
    probability, category = predict_risk(DemoPipeline(), {"age": 55})
    assert probability == 0.8
    assert category == "High"


def test_prediction_selects_positive_class_from_classes_order():
    probability, category = predict_risk(ReversedClassPipeline(), {"age": 55})
    assert probability == 0.8
    assert category == "High"


def test_local_shap_uses_each_input_and_matches_model_score():
    model = joblib.load("models/best_model.pkl")
    data = pd.read_csv("data/processed/clean_heart_disease.csv")
    features = data.drop(columns="target")
    target = data["target"].astype(int)
    training, held_out = train_test_split(
        features,
        test_size=0.20,
        stratify=target,
        random_state=42,
    )
    preprocessor = model.named_steps["preprocessor"]
    columns = list(preprocessor.feature_names_in_)
    explainer = create_local_explainer(model, training)
    first_input = held_out.iloc[[0]].loc[:, columns]
    second_input = held_out.iloc[[1]].loc[:, columns]

    first = explain_local_prediction(model, explainer, first_input)
    second = explain_local_prediction(model, explainer, second_input)
    estimator = model.named_steps["model"]
    first_score = estimator.decision_function(preprocessor.transform(first_input))[0]
    second_score = estimator.decision_function(preprocessor.transform(second_input))[0]

    assert first.values.shape == (len(preprocessor.get_feature_names_out()),)
    assert first.feature_names[0] == "Age (years)"
    assert not np.allclose(first.values, second.values)
    assert np.isclose(first.base_values + first.values.sum(), first_score)
    assert np.isclose(second.base_values + second.values.sum(), second_score)
