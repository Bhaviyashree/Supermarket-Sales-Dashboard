import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px


st.set_page_config(page_title="Supermarket Sales Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom CSS for better styling, colors, and layout
st.markdown("""
    <style>
        /* Dark sidebar theme */
        [data-testid="stSidebar"] {
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            box-shadow: 2px 0 10px rgba(0, 0, 0, 0.3);
        }
        
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: #e0e0e0;
        }
        
        [data-testid="stSidebar"] .stSelectbox label,
        [data-testid="stSidebar"] .stMultiSelect label,
        [data-testid="stSidebar"] .st-date-input label {
            color: #ffffff !important;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        /* Main container */
        .main {
            background-color: #f5f7fa;
            padding: 2rem 1.5rem;
        }
        
        /* Main title styling */
        .main h1 {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            margin-bottom: 1rem !important;
            text-align: center;
        }
        
        /* Metric cards with unique colors */
        [data-testid="stMetric"] {
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 5px solid #667eea;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
            transition: all 0.3s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-6px);
            box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
        }
        
        /* Different colors for each metric */
        [data-testid="stMetric"]:nth-child(1) {
            border-left-color: #667eea;
        }
        [data-testid="stMetric"]:nth-child(2) {
            border-left-color: #f093fb;
        }
        [data-testid="stMetric"]:nth-child(3) {
            border-left-color: #4facfe;
        }
        [data-testid="stMetric"]:nth-child(4) {
            border-left-color: #43e97b;
        }
        [data-testid="stMetric"]:nth-child(5) {
            border-left-color: #fa709a;
        }
        [data-testid="stMetric"]:nth-child(6) {
            border-left-color: #fee140;
        }
        [data-testid="stMetric"]:nth-child(7) {
            border-left-color: #30b0fe;
        }
        [data-testid="stMetric"]:nth-child(8) {
            border-left-color: #a8edea;
        }
        
        [data-testid="stMetric"] label {
            font-weight: 700;
            color: #2c3e50;
            font-size: 0.95rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        /* Subheader styling */
        .main h2, .main h3 {
            color: #2c3e50;
            font-weight: 700;
            margin: 1.5rem 0 1rem 0;
            font-size: 1.5rem !important;
        }
        
        /* Divider styling */
        hr {
            margin: 1.5rem 0 !important;
            border-color: rgba(102, 126, 234, 0.2) !important;
        }
        
        /* Expander styling */
        [data-testid="stExpander"] {
            border: 1px solid #e0e0e0;
            border-radius: 10px;
            background-color: #fafbfc;
        }
        
        [data-testid="stExpander"]:hover {
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: scale(1.02);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        /* Info boxes */
        .stInfo, .stWarning, .stSuccess {
            border-radius: 10px;
            padding: 1rem;
            transition: all 0.3s ease;
        }
        
        .stInfo:hover, .stWarning:hover, .stSuccess:hover {
            transform: translateX(3px);
        }
        
        /* Column spacing */
        .row-widget {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data(path: str = "SuperMarket Analysis.csv") -> pd.DataFrame:
    df = pd.read_csv(path)
    # parse Date
    try:
        df["Date"] = pd.to_datetime(df["Date"])
    except Exception:
        df["Date"] = pd.to_datetime(df["Date"], dayfirst=False, errors='coerce')
    # parse Time
    try:
        df["Time"] = pd.to_datetime(df["Time"], format="%I:%M:%S %p")
    except Exception:
        df["Time"] = pd.to_datetime(df["Time"], errors='coerce')
    df["Day"] = df["Date"].dt.day_name()
    df["Hour"] = df["Time"].dt.hour
    return df




data = load_data()

st.markdown("<h1>🛒 Supermarket Sales Dashboard</h1>", unsafe_allow_html=True)

# Sidebar filters with styled header
st.sidebar.markdown("<h3 style='color: #ffffff; text-align: center; margin-bottom: 1.5rem;'>⚙️ Filters</h3>", unsafe_allow_html=True)
min_date = data["Date"].min()
max_date = data["Date"].max()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date))

city_options = list(data["City"].unique())
cities = st.sidebar.multiselect("City", options=city_options, default=city_options)

product_options = list(data["Product line"].unique())
products = st.sidebar.multiselect("Product line", options=product_options, default=product_options)

payment_options = list(data["Payment"].unique())
payments = st.sidebar.multiselect("Payment", options=payment_options, default=payment_options)

# Apply filters
start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
mask = (
    (data["Date"] >= start_date)
    & (data["Date"] <= end_date)
    & (data["City"].isin(cities))
    & (data["Product line"].isin(products))
    & (data["Payment"].isin(payments))
)
df = data.loc[mask].copy()

if df.empty:
    st.warning("No data for selected filters. Please adjust the filters.")
else:
    # KPI row
    total_sales = df["Sales"].sum()
    total_transactions = df.shape[0]
    avg_basket = df["Sales"].mean()
    avg_rating = df["Rating"].mean()
    total_quantity = df["Quantity"].sum() if "Quantity" in df.columns else 0
    unique_customers = df["Customer type"].nunique() if "Customer type" in df.columns else 0
    total_cogs = df["Cost of goods sold"].sum() if "Cost of goods sold" in df.columns else 0
    gross_profit = total_sales - total_cogs if "Cost of goods sold" in df.columns else total_sales * 0.3
    profit_margin = (gross_profit / total_sales * 100) if total_sales > 0 else 0

    # First row of KPIs
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("💰 Total Sales", f"${total_sales:,.2f}", delta=f"${avg_basket:,.2f} avg")
    k2.metric("📊 Transactions", f"{total_transactions:,}", delta=f"{avg_basket:.0f} items")
    k3.metric("⭐ Avg. Rating", f"{avg_rating:.2f}/5", delta=f"{(avg_rating/5*100):.0f}%")
    k4.metric("📦 Total Qty", f"{int(total_quantity):,}", delta="items sold")

    # Second row of KPIs
    k5, k6, k7, k8 = st.columns(4)
    k5.metric("💵 Gross Profit", f"${gross_profit:,.2f}")
    k6.metric("📈 Profit Margin", f"{profit_margin:.1f}%")
    k7.metric("👥 Customer Types", f"{unique_customers}")
    k8.metric("🛍️ Avg. Sale Value", f"${avg_basket:,.2f}")

    # Sales over time
    st.subheader("📈 Sales Over Time")
    sales_time = df.groupby("Date")["Sales"].sum().reset_index()
    fig_time = px.line(sales_time, x="Date", y="Sales", title="Sales trend")
    st.plotly_chart(fig_time, width='stretch')
    # Top products by revenue
    st.subheader("🏆 Top Products by Revenue")
    prod_rev = df.groupby("Product line")["Sales"].sum().sort_values(ascending=False).reset_index()
    fig_prod = px.bar(prod_rev, x="Product line", y="Sales", color="Sales", title="Revenue by Product line")
    st.plotly_chart(fig_prod, width='stretch')
    # Sales by payment method
    st.subheader("💳 Sales by Payment Method")
    pay_rev = df.groupby("Payment")["Sales"].sum().reset_index()
    fig_pay = px.pie(pay_rev, names="Payment", values="Sales", title="Sales by Payment")
    st.plotly_chart(fig_pay, width='stretch')
    # Heatmap: product vs day
    st.subheader("🔥 Product Sales by Day (Heatmap)")
    product_day = df.groupby(["Product line", "Day"])["Sales"].sum().unstack(fill_value=0)
    fig4, ax4 = plt.subplots(figsize=(10, 6))
    sns.heatmap(product_day, annot=False, fmt=".0f", cmap="YlGnBu", ax=ax4)
    ax4.set_xlabel("")
    st.pyplot(fig4)

    # Sales by hour
    st.subheader("🕐 Sales by Hour of Day")
    hour_rev = df.groupby("Hour")["Sales"].sum().reset_index()
    fig_hour = px.bar(hour_rev, x="Hour", y="Sales", title="Sales by Hour")
    st.plotly_chart(fig_hour, width='stretch')
    # Additional visualizations
    st.divider()
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("👤 Sales by Customer Type")
        if "Customer type" in df.columns:
            customer_sales = df.groupby("Customer type")["Sales"].sum().reset_index()
            fig_cust = px.bar(customer_sales, x="Customer type", y="Sales", color="Sales",
                            title="Sales by Customer Type", color_continuous_scale="Blues")
            st.plotly_chart(fig_cust, width='stretch')

    with col2:
        st.subheader("🏪 Sales by Branch")
        if "Branch" in df.columns:
            branch_sales = df.groupby("Branch")["Sales"].sum().reset_index()
            fig_branch = px.pie(branch_sales, names="Branch", values="Sales", title="Sales Distribution by Branch")
            st.plotly_chart(fig_branch, width='stretch')

    # Top performers
    st.divider()
    col3, col4 = st.columns(2)

    with col3:
        st.subheader("👑 Top 5 Products by Revenue")
        top_products = df.groupby("Product line")["Sales"].sum().nlargest(5).reset_index()
        fig_top_prod = px.bar(top_products, y="Product line", x="Sales", color="Sales",
                              color_continuous_scale="Viridis", title="Top 5 Products", orientation="h")
        st.plotly_chart(fig_top_prod, width='stretch')

    with col4:
        st.subheader("⭐ Top 5 Highest Rated Products")
        top_rated = df.groupby("Product line")["Rating"].mean().nlargest(5).reset_index()
        fig_rated = px.bar(top_rated, y="Product line", x="Rating", color="Rating",
                           color_continuous_scale="RdYlGn", title="Top 5 Rated Products", orientation="h")
        st.plotly_chart(fig_rated, width='stretch')

    # Quantity analysis
    st.divider()
    if "Quantity" in df.columns:
        col5, col6 = st.columns(2)
        with col5:
            st.subheader("📦 Quantity Sold by Product Line")
            qty_by_product = df.groupby("Product line")["Quantity"].sum().sort_values(ascending=False).reset_index()
            fig_qty = px.bar(qty_by_product, x="Product line", y="Quantity", color="Quantity",
                            color_continuous_scale="Teal", title="Units Sold by Product")
            st.plotly_chart(fig_qty, width='stretch')

        with col6:
            st.subheader("💰 Average Price by Product Line")
            avg_price = df.groupby("Product line")["Unit price"].mean().sort_values(ascending=False).reset_index() if "Unit price" in df.columns else None
            if avg_price is not None:
                fig_price = px.bar(avg_price, x="Product line", y="Unit price", color="Unit price",
                                  color_continuous_scale="Purples", title="Avg Price by Product")
                st.plotly_chart(fig_price, width='stretch')

    # Summary statistics
    st.divider()
    st.subheader("📋 Summary Statistics")
    summary_cols = st.columns(3)
    with summary_cols[0]:
        st.info(f"📈 **Max Sale:** ${df['Sales'].max():,.2f}")
    with summary_cols[1]:
        st.warning(f"📉 **Min Sale:** ${df['Sales'].min():,.2f}")
    with summary_cols[2]:
        st.success(f"🎯 **Std Dev:** ${df['Sales'].std():,.2f}")

    # Export section
    st.divider()
    st.subheader("⬇️ Export Data")
    col_export1, col_export2 = st.columns(2)
    with col_export1:
        csv = df.to_csv(index=False)
        st.download_button(label="💾 Download as CSV", data=csv, file_name="sales_data.csv", mime="text/csv")
    with col_export2:
        st.info("💡 Filtered data is ready for download with applied filters")

    # Data table
    with st.expander("📊 Show filtered data"):
        st.dataframe(df.reset_index(drop=True), width='stretch')

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #999; font-size: 0.85rem;'>🚀 Dashboard powered by Streamlit — adjust filters in the sidebar to explore sales</p>", unsafe_allow_html=True)
