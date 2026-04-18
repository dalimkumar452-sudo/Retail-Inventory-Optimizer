import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error
from scipy.stats import norm
import joblib
import os

def train_inventory_model():
    # ১. ডেটা লোড করা
    data_path = 'data/retail_sales_history.csv'
    if not os.path.exists(data_path):
        print("Error: data/retail_sales_history.csv not found!")
        return

    df = pd.read_csv(data_path)
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(['product_id', 'date'])

    print("Engineering features...")

    # ২. ফিচার ইঞ্জিনিয়ারিং
    df['lag_1'] = df.groupby('product_id')['sales_qty'].shift(1)
    df['lag_7'] = df.groupby('product_id')['sales_qty'].shift(7)
    df['rolling_mean_7'] = df.groupby('product_id')['sales_qty'].transform(lambda x: x.shift(1).rolling(7).mean())
    df['day_of_week'] = df['date'].dt.dayofweek
    df['month'] = df['date'].dt.month

    df = df.dropna()

    # ৩. ডেটা স্প্লিটিং
    train = df[df['date'] < df['date'].max() - pd.Timedelta(days=30)]
    test = df[df['date'] >= df['date'].max() - pd.Timedelta(days=30)]

    features = ['lag_1', 'lag_7', 'rolling_mean_7', 'day_of_week', 'month']
    target = 'sales_qty'

    X_train, y_train = train[features], train[target]
    X_test, y_test = test[features], test[target]

    # ৪. মডেল ট্রেনিং
    print("Training XGBoost model...")
    model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5)
    model.fit(X_train, y_train)

    # ৫. পারফরম্যান্স চেক
    preds = model.predict(X_test)
    error = mean_absolute_error(y_test, preds)
    print(f"Model Trained! MAE: {round(error, 2)}")

    # ৬. ইনভেন্টরি অপ্টিমাইজেশন
    std_dev = np.std(y_test - preds)
    lead_time = 3
    service_level = 0.95
    z_score = norm.ppf(service_level)

    safety_stock = z_score * std_dev * np.sqrt(lead_time)
    
    test = test.copy()
    test['forecasted_sales'] = preds.astype(int)
    test['reorder_point'] = (test['forecasted_sales'] * lead_time) + safety_stock
    test['reorder_point'] = test['reorder_point'].astype(int)

    # ৭. ফোল্ডার চেক ও সেভ
    if not os.path.exists('models'): os.makedirs('models')
    if not os.path.exists('outputs'): os.makedirs('outputs')

    joblib.dump(model, 'models/retail_model.pkl')
    test.to_csv('outputs/inventory_recommendations.csv', index=False)
    
    print("-" * 30)
    print("Success: Model and Recommendations saved!")
    # এই লাইনে ইমোজি বাদ দেওয়া হয়েছে যাতে এনকোডিং এরর না হয়
    print("Recommended Safety Stock: " + str(int(safety_stock)) + " units")
    print("-" * 30)

if __name__ == "__main__":
    train_inventory_model()