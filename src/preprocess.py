import pandas as pd
import numpy as np

def generate_data():
    dates = pd.date_range(start="2024-01-01", periods=500, freq='D')
    items = ['Product_A', 'Product_B']
    data = []

    for item in items:
        base_sales = 50 if item == 'Product_A' else 30
        for d in dates:
            # Add seasonality (higher sales on weekends) and noise
            weekday_effect = 1.5 if d.weekday() >= 5 else 1.0
            sales = int(base_sales * weekday_effect + np.random.normal(0, 5))
            data.append([d, item, max(0, sales)])

    df = pd.DataFrame(data, columns=['date', 'item_id', 'sales'])
    
    # Feature Engineering
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month
    for i in range(1, 8): # Lags: Sales from 1 to 7 days ago
        df[f'lag_{i}'] = df.groupby('item_id')['sales'].shift(i)
    
    return df.dropna()

if __name__ == "__main__":
    df = generate_data()
    df.to_csv("data/processed_data.csv", index=False)
    print("Simulation Data Created!")