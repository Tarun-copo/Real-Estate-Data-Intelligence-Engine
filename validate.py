import pandas as pd

df = pd.read_csv("data/properties.csv")

# --- Break a few rows on purpose (to simulate messy real data) ---
df.loc[5, "area_sqft"] = None            # missing area
df.loc[10, "area_sqft"] = 50000          # impossible area
df.loc[15, "price_per_sqft"] = 90000     # price far too high
df = pd.concat([df, df.iloc[[20]]])      # duplicate row
df = df.reset_index(drop=True)

# --- Checks ---
print("Total rows:", len(df))

print("\n1. Missing values per column:")
print(df.isnull().sum())

print("\n2. Duplicate listings:", df.duplicated(subset=["listing_id"]).sum())

print("\n3. Area outside 300-5000 sq ft:")
bad_area = df[(df["area_sqft"] < 300) | (df["area_sqft"] > 5000)]
print(bad_area[["listing_id", "locality", "area_sqft"]])

print("\n4. Price per sq ft outside 3000-25000:")
bad_price = df[(df["price_per_sqft"] < 3000) | (df["price_per_sqft"] > 25000)]
print(bad_price[["listing_id", "locality", "price_per_sqft"]])

# --- Clean ---
clean = df.drop_duplicates(subset=["listing_id"])
clean = clean.dropna(subset=["area_sqft"])
clean = clean[clean["area_sqft"].between(300, 5000)]
clean = clean[clean["price_per_sqft"].between(3000, 25000)]

clean.to_csv("data/properties_clean.csv", index=False)
print("\nRows after cleaning:", len(clean))