"""GlucoTwin Streamlit dashboard. Run: streamlit run app.py"""
import os
import pandas as pd
import streamlit as st

from src.twin import GlucoseTwin, Meal, Profile

st.set_page_config(page_title="GlucoTwin", page_icon="🩺", layout="wide")
st.title("🩺 GlucoTwin: Your Metabolic Digital Twin")
st.caption("AI-powered what-if simulator for post-meal glucose. Educational prototype, "
           "not medical advice. Uses synthetic training data.")

if not os.path.exists("models/glucose_model.joblib"):
    st.error("Model not found. Run `python -m src.train` first.")
    st.stop()

twin = GlucoseTwin()

with st.sidebar:
    st.header("Your profile")
    p = Profile(
        age=st.slider("Age", 18, 70, 35),
        bmi=st.slider("BMI", 17.0, 45.0, 27.0),
        fasting_glucose=st.slider("Fasting glucose (mg/dL)", 70, 140, 100),
        sleep_hours=st.slider("Last night's sleep (h)", 3.0, 10.0, 6.0),
        stress=st.slider("Stress (1-10)", 1, 10, 6),
    )
    st.header("Your meal")
    m = Meal(
        carbs_g=st.slider("Carbs (g)", 5, 140, 90),
        protein_g=st.slider("Protein (g)", 0, 60, 15),
        fat_g=st.slider("Fat (g)", 0, 50, 10),
        fiber_g=st.slider("Fiber (g)", 0, 20, 3),
        post_meal_walk_min=0,
    )

res = twin.what_if(p, m)
c1, c2, c3 = st.columns(3)
c1.metric("Predicted peak (as eaten)", f"{res['peak_base']:.0f} mg/dL",
          twin.risk_label(res["peak_base"]), delta_color="off")
c2.metric("Predicted peak (twin's plan)", f"{res['peak_alt']:.0f} mg/dL",
          f"{res['peak_alt'] - res['peak_base']:.0f} mg/dL")
c3.metric("Plan", "15-min walk + more fiber", "-25% carbs", delta_color="off")

chart = pd.DataFrame({"As eaten": res["baseline"].glucose,
                      "Twin's plan": res["optimized"].glucose})
chart["Elevated threshold (140)"] = 140
st.line_chart(chart, y_label="Glucose (mg/dL)", x_label="Minutes after meal")

st.subheader("Twin's recommendation")
a = res["alt_meal"]
st.write(f"Cut carbs to **{a.carbs_g:.0f} g**, raise fiber to **{a.fiber_g:.0f} g**, and "
         f"walk **{a.post_meal_walk_min} min** after eating. Your twin predicts the peak "
         f"drops by **{res['peak_base'] - res['peak_alt']:.0f} mg/dL**.")
st.info("Tip: connect a CGM or wearable to personalise the twin (see roadmap in README).")
