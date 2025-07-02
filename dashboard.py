import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="AI Складской Дашборд", layout="wide")

# --- Моковые данные ---
np.random.seed(42)

skus = [f"SKU-{i:03d}" for i in range(1, 11)]
sizes = ["S", "M", "L", "XL"]
warehouses = ["Основной", "Маркет"]

# Остатки
stock_data = []
for sku in skus:
    for size in sizes:
        for wh in warehouses:
            stock_data.append({
                "Артикул": sku,
                "Размер": size,
                "Склад": wh,
                "Остаток": np.random.randint(0, 200)
            })
stock_df = pd.DataFrame(stock_data)

# Продажи по дням за 30 дней
sales_data = []
dates = [datetime.now() - timedelta(days=i) for i in range(30)]
for sku in skus:
    for size in sizes:
        for date in dates:
            sales_data.append({
                "Артикул": sku,
                "Размер": size,
                "Дата": date,
                "Продажи": np.random.poisson(3)
            })
sales_df = pd.DataFrame(sales_data)

# Прогноз (простая модель)
forecast_data = []
for sku in skus:
    for size in sizes:
        forecast = sales_df[(sales_df["Артикул"]==sku) & (sales_df["Размер"]==size)]["Продажи"].mean() * 7
        forecast_data.append({
            "Артикул": sku,
            "Размер": size,
            "Прогноз на 7 дней": int(forecast + np.random.randint(-2, 3))
        })
forecast_df = pd.DataFrame(forecast_data)

# Рекомендации (если остаток < прогноза)
reco_data = []
for idx, row in forecast_df.iterrows():
    sku, size, forecast = row["Артикул"], row["Размер"], row["Прогноз на 7 дней"]
    stock = stock_df[(stock_df["Артикул"]==sku) & (stock_df["Размер"]==size)]["Остаток"].sum()
    to_order = max(0, forecast - stock)
    if to_order > 0:
        reco_data.append({
            "Артикул": sku,
            "Размер": size,
            "Рекомендуем заказать": to_order,
            "Срок пополнения": (datetime.now() + timedelta(days=3)).strftime("%d.%m.%Y")
        })
reco_df = pd.DataFrame(reco_data)

# Алерты
alerts = []
for idx, row in stock_df.iterrows():
    if row["Остаток"] < 10:
        alerts.append(f"⚠️ Мало на складе: {row['Артикул']} {row['Размер']} ({row['Склад']}) — {row['Остаток']} шт.")
    elif row["Остаток"] > 180:
        alerts.append(f"ℹ️ Избыток: {row['Артикул']} {row['Размер']} ({row['Склад']}) — {row['Остаток']} шт.")

# --- Интерфейс ---
st.title("AI-дэшборд управления складом и закупками")

col1, col2 = st.columns([3, 1])
with col2:
    st.subheader("Алерты")
    if alerts:
        for alert in alerts:
            st.write(alert)
    else:
        st.success("Нет критических алертов")

with col1:
    st.subheader("Фильтры")
    sku_filter = st.multiselect("Артикул", skus, default=skus)
    size_filter = st.multiselect("Размер", sizes, default=sizes)
    wh_filter = st.multiselect("Склад", warehouses, default=warehouses)
    period = st.slider("Период (дней)", 7, 30, 14)

    filtered_sales = sales_df[
        (sales_df["Артикул"].isin(sku_filter)) &
        (sales_df["Размер"].isin(size_filter)) &
        (sales_df["Дата"] >= datetime.now() - timedelta(days=period))
    ]
    st.subheader("Динамика продаж")
    sales_pivot = filtered_sales.groupby(["Дата"]).agg({"Продажи": "sum"}).reset_index()
    st.line_chart(sales_pivot, x="Дата", y="Продажи")

    st.subheader("Остатки на складах")
    filtered_stock = stock_df[
        (stock_df["Артикул"].isin(sku_filter)) &
        (stock_df["Размер"].isin(size_filter)) &
        (stock_df["Склад"].isin(wh_filter))
    ]
    st.dataframe(filtered_stock, use_container_width=True)

    st.subheader("Рекомендации по закупкам")
    filtered_reco = reco_df[
        (reco_df["Артикул"].isin(sku_filter)) & (reco_df["Размер"].isin(size_filter))
    ]
    st.dataframe(filtered_reco, use_container_width=True)

