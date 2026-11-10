import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)

df = pd.read_csv("data/properties_clean.csv")

# Two things decide "budget level": how expensive the AREA is (price per sq ft)
# and how big the cheque is (total price). Use just these two.
X = StandardScaler().fit_transform(df[["price_per_sqft", "asking_price"]])

km = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = km.fit_predict(X)

# Name groups by their average total price
order = df.groupby("cluster")["asking_price"].mean().sort_values().index
df["segment"] = df["cluster"].map(dict(zip(order, ["Low budget", "Mid range", "High"])))

cols = ["asking_price", "price_per_sqft", "area_sqft", "bhk", "floor"]
print(df.groupby("segment")[cols].mean().round(0).loc[["Low budget", "Mid range", "High"]])
print()
print(df["segment"].value_counts())
print()

# Locality summary
df["high_rise"] = df["floor"] >= 20
df["low_budget"] = df["segment"] == "Low budget"
summary = df.groupby("locality").agg(
    properties=("listing_id", "count"),
    median_price_per_sqft=("price_per_sqft", "median"),
    median_price=("asking_price", "median"),
    pct_low_budget=("low_budget", "mean"),
    pct_high_rise=("high_rise", "mean"),
).round(2)
summary["pct_low_budget"] = (summary["pct_low_budget"] * 100).round(0)
summary["pct_high_rise"] = (summary["pct_high_rise"] * 100).round(0)
print(summary)
print()
print("Cheapest per sq ft  :", summary["median_price_per_sqft"].idxmin())
print("Most expensive      :", summary["median_price_per_sqft"].idxmax())
print("Most low-budget flats:", summary["pct_low_budget"].idxmax())
print("Most high-rise flats :", summary["pct_high_rise"].idxmax())

df.to_csv("data/properties_segmented.csv", index=False)
summary.to_csv("data/locality_summary.csv")