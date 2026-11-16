import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configure page layouts
st.set_page_config(page_title="Olist E-Commerce Dashboard", layout="wide")

sns.set_theme(style="whitegrid")

# Load Data
@st.cache_data
def load_data():
    if os.path.exists("main_data.csv"):
        df = pd.read_csv("main_data.csv")
        df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
        return df
    return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Dataset 'main_data.csv' not found. Please verify the file exists.")
else:
    # Sidebar Filters
    st.sidebar.header("Filter Opsi")
    min_date = df["order_purchase_timestamp"].min()
    max_date = df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.sidebar.date_input(
        "Rentang Waktu",
        value=[min_date.date(), max_date.date()],
        min_value=min_date.date(),
        max_value=max_date.date()
    )
    
    # Filter dataframe based on selection
    filtered_df = df[
        (df["order_purchase_timestamp"].dt.date >= start_date) &
        (df["order_purchase_timestamp"].dt.date <= end_date)
    ]

    # Main Header
    st.title("✨ Olist E-Commerce Business Dashboard ✨")
    st.markdown("Dashboard interaktif untuk memonitor performa penjualan, keterlambatan logistik, dan segmentasi pelanggan.")

    # Top Metrics Row
    col1, col2, col3 = st.columns(3)
    with col1:
        total_orders = filtered_df["order_id"].nunique()
        st.metric("Total Orders", f"{total_orders:,}")
    with col2:
        total_revenue = filtered_df["payment_value"].sum()
        st.metric("Total GMV (Value)", f"R$ {total_revenue:,.2f}")
    with col3:
        avg_shipping = filtered_df["delivery_days"].mean()
        st.metric("Avg Delivery Time", f"{avg_shipping:.1f} Days" if not pd.isna(avg_shipping) else "N/A")

    # Section 1: Monthly Trends
    st.subheader("📈 Tren Bulanan Penjualan dan Pembayaran")
    
    monthly_sales = filtered_df.copy()
    monthly_sales["order_month"] = monthly_sales["order_purchase_timestamp"].dt.to_period("M").astype(str)
    
    sales_monthly = (
        monthly_sales.groupby("order_month")
        .agg(total_orders=("order_id", "nunique"), total_payment=("payment_value", "sum"))
        .reset_index()
    )
    
    fig, ax1 = plt.subplots(figsize=(12, 5))
    x_axis = range(len(sales_monthly))
    
    ax1.plot(x_axis, sales_monthly["total_orders"], marker="o", color="#1f77b4", label="Jumlah Pesanan")
    ax1.set_xlabel("Bulan")
    ax1.set_ylabel("Jumlah Pesanan", color="#1f77b4")
    ax1.tick_params(axis="y", labelcolor="#1f77b4")
    plt.xticks(x_axis, sales_monthly["order_month"], rotation=45)
    
    ax2 = ax1.twinx()
    ax2.plot(x_axis, sales_monthly["total_payment"], marker="s", color="orange", label="Total Pembayaran")
    ax2.set_ylabel("Total Pembayaran (R$)", color="orange")
    ax2.tick_params(axis="y", labelcolor="orange")
    
    plt.title("Perkembangan Transaksi dan GMV Bulanan")
    fig.tight_layout()
    st.pyplot(fig)

    # Section 2: Delivery performance
    st.subheader("🚚 Tingkat Keterlambatan Pengiriman per Negara Bagian")
    
    delivered = filtered_df[
        (filtered_df["order_status"] == "delivered") &
        filtered_df["is_late"].notna() &
        filtered_df["customer_state"].notna()
    ].copy()
    
    if not delivered.empty:
        delivery_by_state = delivered.groupby("customer_state").agg(
            delivered_orders=("order_id", "nunique"),
            late_orders=("is_late", "sum")
        ).reset_index()
        
        delivery_by_state["late_rate_pct"] = (
            delivery_by_state["late_orders"] / delivery_by_state["delivered_orders"] * 100
        )
        delivery_by_state = delivery_by_state.sort_values("late_rate_pct", ascending=True)
        
        fig2, ax = plt.subplots(figsize=(11, 6))
        sns.barplot(data=delivery_by_state, x="late_rate_pct", y="customer_state", palette="coolwarm", ax=ax)
        ax.set_xlabel("Pesanan Terlambat (%)")
        ax.set_ylabel("Negara Bagian Pelanggan")
        ax.set_title("Persentase Keterlambatan Pengiriman Berdasarkan Negara Bagian")
        st.pyplot(fig2)
    else:
        st.info("No delivered order data available for the selected dates.")

    # Section 3: Customer Segments (RFM)
    st.subheader("👥 Segmentasi Pelanggan")
    if os.path.exists("rfm_customer_segments.csv"):
        rfm = pd.read_csv("rfm_customer_segments.csv")
        segments = rfm["Segment"].value_counts().reset_index()
        segments.columns = ["Segment", "Total Customers"]
        
        col_left, col_right = st.columns([1, 2])
        with col_left:
            st.write("**Distribusi Segmen Pelanggan:**")
            st.dataframe(segments, use_container_width=True)
        with col_right:
            fig3, ax3 = plt.subplots(figsize=(8, 4))
            sns.barplot(data=segments, x="Total Customers", y="Segment", palette="viridis", ax=ax3)
            ax3.set_title("Jumlah Pelanggan per Segmen RFM")
            st.pyplot(fig3)
    else:
        st.warning("Segmentasi data RFM ('rfm_customer_segments.csv') tidak ditemukan.")
