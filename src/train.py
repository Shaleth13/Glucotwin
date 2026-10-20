"""Train the glucose-response model that powers the digital twin."""
import json
import joblib
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

from src.generate_data import FEATURES, generate


def main():
    df = generate()
    df.to_csv("data/synthetic_glucose.csv", index=False)
    X_tr, X_te, y_tr, y_te = train_test_split(df[FEATURES], df["glucose_rise"],
                                              test_size=0.2, random_state=0)
    model = GradientBoostingRegressor(n_estimators=300, max_depth=3,
                                      learning_rate=0.08, random_state=0)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    metrics = {"mae_mg_dl": round(float(mean_absolute_error(y_te, pred)), 2),
               "r2": round(float(r2_score(y_te, pred)), 3)}
    joblib.dump(model, "models/glucose_model.joblib")
    with open("models/metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    print("Model saved.", metrics)


if __name__ == "__main__":
    main()
