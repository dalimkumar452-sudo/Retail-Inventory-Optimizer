import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# 1. Page Configuration
st.set_page_config(page_title="Retail Inventory Optimizer", layout="wide")
st.title("📦 Retail Inventory Dashboard")

# 2. File Path Setup
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
data_file = os.path.join(root_dir, "outputs", "inventory_recommendations.csv")

if os.path.exists(data_file):
    df = pd.read_csv(data_file)
    df['date'] = pd.to_datetime(df['date'])
    
    # Sidebar Filter
    product = st.sidebar.selectbox("Select Product", df['product_name'].unique())
    p_df = df[df['product_name'] == product].sort_values('date')
    
    # 3. Extract Inventory Metrics
    last_row = p_df.iloc[-1]
    current_stock = int(last_row['stock_on_hand'])
    forecast = int(last_row['forecasted_sales'])
    rop = int(last_row['reorder_point'])

    # 4. Main KPIs
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Current Stock on Hand 🏠", f"{current_stock} units")
    with col2:
        st.metric("Forecasted Sales (Tomorrow) 📈", f"{forecast} units")
    with col3:
        st.metric("Reorder Point (ROP) ⚠️", f"{rop} units")

    st.divider()

    # 5. Inventory Alert System (English Version)
    if current_stock <= rop:
        st.error(f"🚨 **ALERT:** Low stock level for **{product}**! Current stock ({current_stock}) is below the Reorder Point ({rop}). Please place a new order immediately.")
    else:
        st.success(f"✅ **STATUS:** {product} has healthy stock levels (Stock on Hand > ROP).")

    # 6. Sales Trend Analysis
    st.subheader(f"Sales Trend: {product}")
    st.line_chart(p_df.set_index('date')['sales_qty'])

    # 7. Actionable Data Table
    st.subheader("Inventory Action Table (Last 10 Days)")
    st.dataframe(p_df[['date', 'sales_qty', 'stock_on_hand', 'forecasted_sales', 'reorder_point']].tail(10), use_container_width=True)

else:
    st.error("Data file not found! Please run 'python src/model.py' first.")