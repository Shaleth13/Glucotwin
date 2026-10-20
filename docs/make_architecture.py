"""Render docs/architecture.pdf (run: python docs/make_architecture.py)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

fig, ax = plt.subplots(figsize=(11, 6))
ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis("off")
ax.set_title("GlucoTwin Architecture", fontsize=16, weight="bold")

def box(x, y, w, h, text, color):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                fc=color, ec="#333", lw=1.2))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=9)

def arrow(x1, y1, x2, y2):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="#333"))

box(0.2, 4.2, 2.4, 1.2, "Inputs\nProfile: age, BMI,\nfasting glucose, sleep, stress", "#e3f2fd")
box(0.2, 2.2, 2.4, 1.2, "Meal + Activity\ncarbs, protein, fat,\nfiber, post-meal walk", "#e3f2fd")
box(0.2, 0.3, 2.4, 1.2, "Future: CGM / wearable\n(Libre, Fitbit, Apple Health)", "#f5f5f5")
box(3.6, 2.6, 2.6, 1.8, "Feature Pipeline\n(src/generate_data.py)\nsynthetic data -> features", "#fff3e0")
box(3.6, 0.5, 2.6, 1.4, "Training\nGradient Boosting\n(src/train.py)", "#fff3e0")
box(7.0, 2.6, 3.7, 1.8, "Digital Twin Engine (src/twin.py)\nPredict glucose rise -> build curve\nWhat-if: walk, fiber, carb swap", "#e8f5e9")
box(7.0, 0.5, 3.7, 1.4, "Streamlit Dashboard (app.py)\nCurves, risk label, recommendation", "#f3e5f5")
arrow(2.6, 4.8, 3.6, 3.8); arrow(2.6, 2.8, 3.6, 3.2); arrow(2.6, 0.9, 3.6, 2.8)
arrow(4.9, 2.6, 4.9, 1.9); arrow(6.2, 1.2, 7.0, 3.0); arrow(6.2, 3.5, 7.0, 3.5)
arrow(8.85, 2.6, 8.85, 1.9)
plt.savefig("docs/architecture.pdf", bbox_inches="tight")
plt.savefig("docs/architecture.png", dpi=150, bbox_inches="tight")
print("Saved docs/architecture.pdf")
