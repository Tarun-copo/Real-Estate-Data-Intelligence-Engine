import pandas as pd
import matplotlib
matplotlib.use("Agg")          # saves charts as image files, no pop-up windows
import matplotlib.pyplot as plt
import os

os.makedirs("charts", exist_ok=True)
df = pd.read_csv("data/properties_segmented.csv")
colors = {"Low budget": "tab:green", "Mid range": "tab:orange", "High": "tab:red"}

# Chart 1: every property as a dot, coloured by segment
plt.figure(figsize=(8, 5))
for seg, color in colors.items():
    d = df[df["segment"] == seg]
    plt.scatter(d["price_per_sqft"], d["asking_price"] / 1e7, label=seg, color=color, alpha=0.7)
plt.xlabel("Price per sq ft (Rs)")
plt.ylabel("Total price (Rs crore)")
plt.title("Property segments (synthetic data)")
plt.legend()
plt.tight_layout()
plt.savefig("charts/segments_scatter.png", dpi=150)
plt.close()

# Chart 2: median price per sq ft by locality
med = df.groupby("locality")["price_per_sqft"].median().sort_values()
plt.figure(figsize=(8, 5))
med.plot(kind="barh", color="steelblue")
plt.xlabel("Median price per sq ft (Rs)")
plt.title("How expensive is each locality? (synthetic data)")
plt.tight_layout()
plt.savefig("charts/locality_price.png", dpi=150)
plt.close()

# Chart 3: mix of segments inside each locality
mix = pd.crosstab(df["locality"], df["segment"], normalize="index")[["Low budget", "Mid range", "High"]] * 100
mix.plot(kind="bar", stacked=True, color=[colors[c] for c in mix.columns], figsize=(8, 5))
plt.ylabel("% of properties")
plt.title("Segment mix by locality (synthetic data)")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig("charts/locality_mix.png", dpi=150)
plt.close()
print("Saved 3 charts in the charts folder")