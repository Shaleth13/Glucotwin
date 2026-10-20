"""GlucoTwin: a virtual replica of a person's post-meal glucose response."""
from dataclasses import dataclass, asdict
import joblib
import numpy as np
import pandas as pd

from src.generate_data import FEATURES


@dataclass
class Profile:
    age: int = 35
    bmi: float = 27.0
    fasting_glucose: float = 100.0
    sleep_hours: float = 6.5
    stress: int = 5


@dataclass
class Meal:
    carbs_g: float = 80
    protein_g: float = 15
    fat_g: float = 10
    fiber_g: float = 4
    post_meal_walk_min: int = 0


class GlucoseTwin:
    def __init__(self, model_path: str = "models/glucose_model.joblib"):
        self.model = joblib.load(model_path)

    def predict_rise(self, p: Profile, m: Meal) -> float:
        row = pd.DataFrame([{**asdict(p), **asdict(m)}])[FEATURES]
        return float(max(self.model.predict(row)[0], 0))

    def curve(self, p: Profile, m: Meal, minutes: int = 180) -> pd.DataFrame:
        """Parametric glucose curve: baseline + rise shaped by time-to-peak."""
        rise = self.predict_rise(p, m)
        t_peak = 45 + 0.15 * m.fat_g + 0.3 * m.protein_g - 0.25 * m.post_meal_walk_min
        t_peak = float(np.clip(t_peak, 30, 90))
        t = np.arange(0, minutes + 1, 5)
        g = p.fasting_glucose + rise * (t / t_peak) * np.exp(1 - t / t_peak)
        return pd.DataFrame({"minutes": t, "glucose": g}).set_index("minutes")

    @staticmethod
    def risk_label(peak: float) -> str:
        if peak >= 180:
            return "High spike"
        if peak >= 140:
            return "Elevated"
        return "Healthy range"

    def what_if(self, p: Profile, m: Meal, walk: int = 15, extra_fiber: float = 6,
                carb_cut_pct: float = 0.25) -> dict:
        base = self.curve(p, m)
        alt_meal = Meal(m.carbs_g * (1 - carb_cut_pct), m.protein_g, m.fat_g,
                        m.fiber_g + extra_fiber, max(m.post_meal_walk_min, walk))
        alt = self.curve(p, alt_meal)
        return {"baseline": base, "optimized": alt, "alt_meal": alt_meal,
                "peak_base": float(base.glucose.max()), "peak_alt": float(alt.glucose.max())}
