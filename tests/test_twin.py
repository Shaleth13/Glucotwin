import os
import pytest
from src.twin import GlucoseTwin, Meal, Profile

pytestmark = pytest.mark.skipif(not os.path.exists("models/glucose_model.joblib"),
                                reason="train model first")


def test_walk_reduces_peak():
    t = GlucoseTwin()
    p = Profile()
    assert t.predict_rise(p, Meal(post_meal_walk_min=20)) < t.predict_rise(p, Meal(post_meal_walk_min=0))


def test_more_carbs_raises_peak():
    t = GlucoseTwin()
    p = Profile()
    assert t.predict_rise(p, Meal(carbs_g=120)) > t.predict_rise(p, Meal(carbs_g=30))


def test_curve_starts_at_baseline():
    c = GlucoseTwin().curve(Profile(), Meal())
    assert c.glucose.iloc[0] == pytest.approx(Profile().fasting_glucose)
