import numpy as np
import pandas as pd
import os

np.random.seed(42)                 # makes the "random" data the same every time
os.makedirs("data", exist_ok=True) # creates a folder called data

# Made-up average price per sq ft for each area (NOT real data)
base_price = {"Madhapur": 10000, "Khajaguda": 8000,
              "Nanakramguda": 9000, "Narsingi": 7500}
# Typical area in sq ft for each BHK type
avg_area = {1: 650, 2: 1100, 3: 1600, 4: 2400}

rows = []
for i in range(200):
    loc = np.random.choice(list(base_price))
    bhk = int(np.random.choice([1, 2, 3, 4], p=[0.1, 0.4, 0.35, 0.15]))
    area = int(avg_area[bhk] * np.random.normal(1, 0.1))
    pps = int(base_price[loc] * np.random.normal(1, 0.15))
    rows.append({
        "listing_id": i + 1,
        "locality": loc,
        "bhk": bhk,
        "area_sqft": area,
        "floor": int(np.random.randint(1, 31)),
        "price_per_sqft": pps,
        "asking_price": area * pps,
    })

df = pd.DataFrame(rows)
df.to_csv("data/properties.csv", index=False)

print(df.head())
print()
print(df.groupby("locality")["price_per_sqft"].mean().round(0))