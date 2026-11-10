import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

df = pd.read_csv("data/properties_clean.csv")

# 1. Pick the columns used to decide "budget level"
features = ["asking_price", "price_per_sqft", "area_sqft", "bhk", "floor"]

# 2. Put all columns on the same scale (otherwise big numbers dominate)
X = StandardScaler().fit_transform(df[features])

# 3. Ask KMeans to find 3 groups
km = KMeans(n_clusters=3, random_state=42, n_init=10)
df["cluster"] = km.fit_predict(X)

# 4. Name the groups: cheapest average price = Low, then Mid, then High
order = df.groupby("cluster")["asking_price"].mean().sort_values().index
names = dict(zip(order, ["Low budget", "Mid range", "High"]))
df["segment"] = df["cluster"].map(names)

# 5. Show what each group looks like
print(df.groupby("segment")[features].mean().round(0).loc[["Low budget", "Mid range", "High"]])
print()
print(df["segment"].value_counts())
print()

# 6. Which locality has which segments? (% of its properties)
table = pd.crosstab(df["locality"], df["segment"], normalize="index") * 100
print(table.round(0)[["Low budget", "Mid range", "High"]])

df.to_csv("data/properties_segmented.csv", index=False)