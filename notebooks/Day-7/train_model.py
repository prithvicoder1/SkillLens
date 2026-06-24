import pandas as pd
import numpy as np
import pickle

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor

# =========================
# 1. Load data
# =========================
df = pd.read_csv("laptop_data.csv")

# Drop extra unnamed column if present
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# =========================
# 2. Basic cleaning
# =========================
# Convert Ram to integer
df["Ram"] = df["Ram"].str.replace("GB", "", regex=False).astype(int)

# Convert Weight to float
df["Weight"] = df["Weight"].str.replace("kg", "", regex=False).astype(float)

# =========================
# 3. Feature engineering
# =========================

# Touchscreen
df["Touchscreen"] = df["ScreenResolution"].apply(lambda x: 1 if "Touchscreen" in x else 0)

# IPS
df["Ips"] = df["ScreenResolution"].apply(lambda x: 1 if "IPS" in x else 0)

# Extract resolution
new = df["ScreenResolution"].str.extract(r'(\d+)x(\d+)')
df["X_res"] = new[0].astype(int)
df["Y_res"] = new[1].astype(int)

# PPI
df["ppi"] = (((df["X_res"]**2) + (df["Y_res"]**2))**0.5 / df["Inches"]).astype(float)

# CPU brand
def fetch_cpu_brand(text):
    text = str(text)
    if text.startswith("Intel Core i5"):
        return "Intel Core i5"
    elif text.startswith("Intel Core i7"):
        return "Intel Core i7"
    elif text.startswith("Intel Core i3"):
        return "Intel Core i3"
    elif text.startswith("Intel Pentium"):
        return "Intel Pentium"
    elif text.startswith("Intel Celeron"):
        return "Intel Celeron"
    elif text.startswith("AMD"):
        return "AMD Processor"
    else:
        return "Other Intel Processor"

df["Cpu brand"] = df["Cpu"].apply(fetch_cpu_brand)

# Memory split
df["Memory"] = df["Memory"].astype(str).replace(r'\.0', '', regex=True)
df["Memory"] = df["Memory"].str.replace("GB", "", regex=False)
df["Memory"] = df["Memory"].str.replace("TB", "000", regex=False)

new = df["Memory"].str.split("+", n=1, expand=True)

df["first"] = new[0]
df["first"] = df["first"].str.strip()

df["second"] = new[1] if 1 in new.columns else "0"
df["second"] = df["second"].fillna("0").astype(str).str.strip()

# first drive flags
df["Layer1HDD"] = df["first"].apply(lambda x: 1 if "HDD" in x else 0)
df["Layer1SSD"] = df["first"].apply(lambda x: 1 if "SSD" in x else 0)
df["Layer1Hybrid"] = df["first"].apply(lambda x: 1 if "Hybrid" in x else 0)
df["Layer1Flash_Storage"] = df["first"].apply(lambda x: 1 if "Flash Storage" in x else 0)

# second drive flags
df["Layer2HDD"] = df["second"].apply(lambda x: 1 if "HDD" in x else 0)
df["Layer2SSD"] = df["second"].apply(lambda x: 1 if "SSD" in x else 0)
df["Layer2Hybrid"] = df["second"].apply(lambda x: 1 if "Hybrid" in x else 0)
df["Layer2Flash_Storage"] = df["second"].apply(lambda x: 1 if "Flash Storage" in x else 0)

# keep only numeric part
df["first"] = df["first"].str.replace(r"\D", "", regex=True)
df["second"] = df["second"].str.replace(r"\D", "", regex=True)

df["first"] = df["first"].replace("", "0").astype(int)
df["second"] = df["second"].replace("", "0").astype(int)

# Final HDD/SSD
df["HDD"] = (
    df["first"] * df["Layer1HDD"] +
    df["second"] * df["Layer2HDD"]
)

df["SSD"] = (
    df["first"] * df["Layer1SSD"] +
    df["second"] * df["Layer2SSD"]
)

# GPU brand
df["Gpu brand"] = df["Gpu"].apply(lambda x: str(x).split()[0])

# OS mapping
def cat_os(inp):
    inp = str(inp)
    if inp == "Windows 10" or inp == "Windows 7" or "Windows" in inp:
        return "Windows"
    elif inp in ["macOS", "Mac OS X"]:
        return "Mac"
    else:
        return "Others/No OS/Linux"

df["os"] = df["OpSys"].apply(cat_os)

# =========================
# 4. Final columns
# =========================
df = df[[
    "Company",
    "TypeName",
    "Ram",
    "Weight",
    "Touchscreen",
    "Ips",
    "ppi",
    "Cpu brand",
    "HDD",
    "SSD",
    "Gpu brand",
    "os",
    "Price"
]]

# =========================
# 5. Train model
# =========================
X = df.drop(columns=["Price"])
y = np.log(df["Price"])

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=2
)

step1 = ColumnTransformer(
    transformers=[
        ("col_tnf", OneHotEncoder(handle_unknown="ignore"), [0, 1, 7, 10, 11])
    ],
    remainder="passthrough"
)

step2 = RandomForestRegressor(
    n_estimators=200,
    random_state=42
)

pipe = Pipeline([
    ("step1", step1),
    ("step2", step2)
])

pipe.fit(X_train, y_train)

# =========================
# 6. Save files
# =========================
pickle.dump(df, open("df.pkl", "wb"))
pickle.dump(pipe, open("pipe.pkl", "wb"))

print("✅ New df.pkl and pipe.pkl generated successfully!")
