import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from modules.data_handler import DataHandler

# Настройка страницы
st.set_page_config(
    page_title="Дашборд склада",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Инициализация обработчика данных
@st.cache_data
def load_data():
    return DataHandler()

data_handler = load_data()

# Заголовок
st.title("📦 Дашборд склада")

# Боковая панель с фильтрами
st.sidebar.header("Фильтры")

# Фильтр периода
period = st.sidebar.selectbox(
    "Период",
    ["день", "неделя", "месяц", "год", "весь период"],
    index=2  # по умолчанию месяц
)

# Фильтр ABC
abc_filter = st.sidebar.selectbox(
    "ABC категория",
    ["Все", "A", "B", "C"],
    index=1  # по умолчанию A
)

# Фильтр размеров
sizes = ["Все", "XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"]
size_filter = st.sidebar.selectbox(
    "Размер",
    sizes,
    index=3  # по умолчанию M
)

# Основная область дашборда
st.markdown("---")

# Раздел 1: ТОВАРЫ ПРОДАЖИ
st.header("📈 ТОВАРЫ ПРОДАЖИ")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Продажи за месяц",
        value="3 154 шт",
        delta="+22%"
    )

with col2:
    st.metric(
        label="Упущенные продажи",
        value="570 шт"
    )

with col3:
    st.metric(
        label="Текущий остаток",
        value="13 454 шт"
    )

with col4:
    st.metric(
        label="Рекомендованный запас",
        value="16 000 шт"
    )

# График продаж по дням
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Продажи по дням")
    # Создание примера данных для графика
    dates = pd.date_range(start='2024-05-01', end='2024-06-30', freq='D')
    sales_data = np.random.randint(20, 60, len(dates))
    
    fig_sales = px.line(
        x=dates, 
        y=sales_data,
        title="Динамика продаж",
        labels={'x': 'Дата', 'y': 'Продажи (шт)'}
    )
    fig_sales.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_sales, use_container_width=True)

with col2:
    st.subheader("Фактический остаток и рекомендованный запас по размерам")
    # Данные для круговой диаграммы
    sizes_data = {
        'Размер': ['XS', 'S', 'M', 'L', 'XL', 'XXL'],
        'Процент': [15, 35, 33, 18, 14, 5]
    }
    
    fig_pie = px.pie(
        values=sizes_data['Процент'],
        names=sizes_data['Размер'],
        title="Распределение по размерам"
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Карточка товара
st.subheader("Карточка товара")
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image("https://via.placeholder.com/150x150?text=Фото+товара", caption="Фото товара")

with col2:
    st.write("**Заголовок карточки:** Футболка хлопок однотонная базовая")
    st.write("**Артикул:** tshirtwhite")
    st.write("**Количество товара в комплекте:** 1")
    st.write("**Код Wb:** 76280452")
    st.write("**Заказы (шт):** 5046")
    st.write("**Заказы по отношению к предыдущему периоду:** +347")
    st.write("**Размер:** M")

with col3:
    st.write("**План на месяц:** -")
    st.write("**План на день:** -")

st.markdown("---")

# Раздел 2: ТОВАРЫ НА СКЛАДЕ
st.header("📦 ТОВАРЫ НА СКЛАДЕ")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Информация о товаре")
    st.write("**Название:** Футболки")
    st.write("**Себестоимость товара:** ₽495,00")
    st.write("**На складе Wb:** -")
    st.write("**В пути к клиенту:** 1 577")
    st.write("**В пути от клиента:** 566")
    st.write("**На своих складах:** 3 500")
    st.write("**Товар в пути:** 15 510")

with col2:
    st.subheader("Прогнозы и планирование")
    st.write("**Поставка ожидается:** 30.08.25")
    st.write("**Стоимость товара:** ₽14 975 221")
    st.write("**Средняя продажа за период:** день")
    st.write("**Товара хватит:** 1497 дней")
    st.write("**Товар закончится:** 08.04.2029")
    st.write("**Дата обновления данных:** 23 минуты назад")

# Календарь наличия товара
st.subheader("Наличие товара по дням")
# Создание календарной тепловой карты
calendar_data = np.random.choice([0, 1, 2], size=(5, 7), p=[0.1, 0.3, 0.6])
fig_calendar = px.imshow(
    calendar_data,
    color_continuous_scale=['red', 'yellow', 'green'],
    title="Календарь наличия товара (красный - нет, желтый - мало, зеленый - достаточно)"
)
fig_calendar.update_layout(
    xaxis_title="Дни недели",
    yaxis_title="Недели"
)
st.plotly_chart(fig_calendar, use_container_width=True)

st.markdown("---")

# Раздел 3: ТОВАРЫ В ПУТИ
st.header("🚚 ТОВАРЫ В ПУТИ")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Название фабрики (поставщик)",
        value="-"
    )

with col2:
    st.metric(
        label="Количество",
        value="15 510"
    )

with col3:
    st.metric(
        label="Дата прибытия",
        value="30.08.25"
    )

with col4:
    st.metric(
        label="Статус",
        value="В пути"
    )

# Таблица остатков и прогнозов
st.subheader("Таблица остатков и прогнозов")
forecast_data = {
    'SKU': ['S10', 'S11', 'S21', 'S22', 'S23', 'S24'],
    'Средняя оценка': [3.8, 3.8, 5.9, 6.8, 5.7, 5.1],
    'Дни отсутствия': ['-', 3, 1, 8, 3, 8],
    'Упущенные продажи': [66, 119, 188, 228, 328, 528]
}

df_forecast = pd.DataFrame(forecast_data)
st.dataframe(df_forecast, use_container_width=True)

# Доля упущенных продаж
st.subheader("Доля упущенных продаж")
missed_sales_data = {
    'Размер': ['SS', 'M', 'XL', 'XXL', 'XXXL'],
    'Процент': [35, 33, 16, 14, 5]
}

fig_missed = px.pie(
    values=missed_sales_data['Процент'],
    names=missed_sales_data['Размер'],
    title="Распределение упущенных продаж по размерам"
)
st.plotly_chart(fig_missed, use_container_width=True)

st.markdown("---")

# Раздел 4: ОПЛАТА
st.header("💰 ОПЛАТА")

st.subheader("График оплат")
# Создание примера данных для графика оплат
payment_dates = pd.date_range(start='2024-01-01', end='2024-12-31', freq='M')
payment_amounts = np.random.randint(50000, 200000, len(payment_dates))

fig_payments = px.bar(
    x=payment_dates,
    y=payment_amounts,
    title="График оплат по месяцам",
    labels={'x': 'Месяц', 'y': 'Сумма оплат (₽)'}
)
fig_payments.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig_payments, use_container_width=True)

# Дополнительная информация об оплатах
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Общая сумма оплат",
        value="₽1 245 000"
    )

with col2:
    st.metric(
        label="Средняя оплата в месяц",
        value="₽103 750"
    )

with col3:
    st.metric(
        label="Следующая оплата",
        value="15.08.2024"
    )

# Футер
st.markdown("---")
st.markdown("*Дашборд обновлен: " + datetime.now().strftime("%d.%m.%Y %H:%M") + "*")

