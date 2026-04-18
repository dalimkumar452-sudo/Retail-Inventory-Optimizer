import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta

def generate_retail_data():
    # ১. ফোল্ডার তৈরি (যদি না থাকে)
    if not os.path.exists('data'):
        os.makedirs('data')
    
    # ২. সেটিংস ঠিক করা
    start_date = datetime(2024, 1, 1)
    days = 600  # প্রায় ২০ মাসের ডেটা
    items = [
        {'id': 'PROD_001', 'name': 'Premium Rice', 'base_sales': 40, 'price': 120},
        {'id': 'PROD_002', 'name': 'Cooking Oil', 'base_sales': 25, 'price': 180},
        {'id': 'PROD_003', 'name': 'Organic Lentils', 'base_sales': 15, 'price': 210}
    ]
    
    all_data = []

    print("Generating realistic sales data...")

    # ৩. ডেটা তৈরি করা
    for item in items:
        for d in range(days):
            current_date = start_date + timedelta(days=d)
            
            # সিজনালিটি লজিক (শুক্রবার ও শনিবার বিক্রি ৩০-৪০% বেশি হবে)
            weekday = current_date.weekday()
            seasonality = 1.0
            if weekday >= 4:  # Friday and Saturday
                seasonality = 1.4
            
            # ট্রেন্ড লজিক (ধীরে ধীরে প্রতি মাসে বিক্রি ২% করে বাড়ছে)
            trend = 1 + (d / 30 * 0.02)
            
            # র‍্যান্ডম নয়েজ (যাতে ডেটা একদম নিখুঁত না হয়ে রিয়েলিস্টিক হয়)
            noise = np.random.normal(0, 3)
            
            # ফাইনাল সেলস ক্যালকুলেশন
            sales = int((item['base_sales'] * seasonality * trend) + noise)
            sales = max(0, sales) # বিক্রি কখনো নেগেটিভ হতে পারে না
            
            all_data.append({
                'date': current_date.strftime('%Y-%m-%d'),
                'product_id': item['id'],
                'product_name': item['name'],
                'unit_price': item['price'],
                'sales_qty': sales,
                'stock_on_hand': np.random.randint(50, 200) # স্যাম্পল স্টক লেভেল
            })

    # ৪. পান্ডাস ডেটাফ্রেমে রূপান্তর
    df = pd.DataFrame(all_data)
    
    # ৫. CSV ফাইল হিসেবে সেভ করা
    file_path = "data/retail_sales_history.csv"
    df.to_csv(file_path, index=False)
    
    print("-" * 30)
    print(f"✅ Success! Data generated at: {file_path}")
    print(f"📊 Total Rows: {len(df)}")
    print(f"📅 Date Range: {df['date'].min()} to {df['date'].max()}")
    print("-" * 30)

if __name__ == "__main__":
    generate_retail_data()