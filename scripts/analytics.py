import os
import pandas as pd
import json
from statsmodels.tsa.seasonal import seasonal_decompose
from sklearn.linear_model import LinearRegression
from scipy.interpolate import CubicSpline
import numpy as np

# Define base directory for input/output
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../public/analytics'))
INPUT_PATH = os.path.join(BASE_DIR, 'input_data.json')
OUTPUT_PATH = os.path.join(BASE_DIR, 'output.json')

# Step 1: Load the input data
try:
    df = pd.read_json(INPUT_PATH)
    print(f"Loaded {len(df)} records from {INPUT_PATH}")
except Exception as e:
    print("Error loading input data:", e)
    exit(1)

# Step 2: Preprocessing
try:
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date')  # Ensure date order
    df.set_index('date', inplace=True)
    df = df.asfreq('MS')  # Monthly frequency
except Exception as e:
    print("Error processing date/time:", e)
    exit(1)

# Step 3: Decomposition
try:
    decomposition = seasonal_decompose(df['quantity'], model='additive', period=12)
except Exception as e:
    print("Decomposition error:", e)
    exit(1)

# Step 4: Linear Regression (trend line)
try:
    df_clean = df[df['quantity'].notna()].copy()
    df_clean['timestamp'] = df_clean.index.astype(np.int64) // 10**9
    X = df_clean[['timestamp']]
    y = df_clean['quantity']
    model = LinearRegression()
    model.fit(X, y)
    df_clean['trend_lr'] = model.predict(X)
except Exception as e:
    print("Linear regression error:", e)
    exit(1)

# Step 5: Cubic Spline Smoothing
try:
    x = np.arange(len(df_clean))
    y = df_clean['quantity'].values
    cs = CubicSpline(x, y, extrapolate=True)
    df_clean['spline'] = cs(x)
except Exception as e:
    print("Cubic spline error:", e)
    exit(1)

# Step 6: Compile and save results
# Step 6: Compile results
# Step 6: Compile results
try:
    results = {
        'original': {str(k): v for k, v in df_clean['quantity'].to_dict().items()},
        'trend': {str(k): v for k, v in decomposition.trend.dropna().to_dict().items()},
        'seasonal': {str(k): v for k, v in decomposition.seasonal.dropna().to_dict().items()},
        'residual': {str(k): v for k, v in decomposition.resid.dropna().to_dict().items()},
        'trend_lr': {str(k): v for k, v in df_clean['trend_lr'].to_dict().items()},
        'spline': {str(k): v for k, v in df_clean['spline'].to_dict().items()}
    }

    print(" Results dictionary keys:", results.keys())
    print(" Number of original records:", len(results['original']))

    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f" Analysis complete. Results saved to {OUTPUT_PATH}")
except Exception as e:
    print(" Error saving output:", str(e))
    exit(1)
