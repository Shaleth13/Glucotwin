"""Generate a synthetic post-meal glucose dataset (no real patient data)."""
import numpy as np
import pandas as pd

FEATURES = ["carbs_g", "protein_g", "fat_g", "fiber_g", "sleep_hours", "stress",
            "age", "bmi", "fasting_glucose", "post_meal_walk_min"]


def generate(n: int = 6000, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    df = pd.DataFrame({
        "carbs_g": rng.uniform(5, 140, n),
        "protein_g": rng.uniform(0, 60, n),
        "fat_g": rng.uniform(0, 50, n),
        "fiber_g": rng.uniform(0, 20, n),
        "sleep_hours": rng.normal(6.8, 1.2, n).clip(3, 10),
        "stress": rng.integers(1, 11, n),
        "age": rng.integers(18, 70, n),
        "bmi": rng.normal(26.5, 4.5, n).clip(17, 45),
        "fasting_glucose": rng.normal(98, 12, n).clip(70, 140),
        "post_meal_walk_min": rng.choice([0, 0, 5, 10, 15, 20, 30], n),
    })
    net = (df.carbs_g - 0.6 * df.fiber_g).clip(lower=0)
    sensitivity = (1 + 0.025 * (df.bmi - 25) + 0.012 * (df.fasting_glucose - 90)
                   + 0.06 * (7 - df.sleep_hours) + 0.015 * df.stress + 0.004 * (df.age - 40))
    delta = (0.78 * net * sensitivity - 0.12 * df.protein_g - 0.06 * df.fat_g
             - 1.1 * df.post_meal_walk_min + rng.normal(0, 6, n))
    df["glucose_rise"] = delta.clip(lower=5)  # mg/dL rise above fasting at peak
    return df


if __name__ == "__main__":
    data = generate()
    data.to_csv("data/synthetic_glucose.csv", index=False)
    print(f"Saved {len(data)} rows -> data/synthetic_glucose.csv")
