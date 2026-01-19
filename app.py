import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Настройка на страницата
st.set_page_config(page_title="Калкулатор за денивелация", layout="centered")

st.title("📐 Изчисляване на денивелация")
st.write("Изчисляване на вертикалното отместване въз основа на **хоризонтално разстояние** и наклон.")

# Входни данни
col_in1, col_in2 = st.columns(2)

with col_in1:
    l_horiz = st.number_input("Хоризонтална дължина (L):", min_value=0.0, value=100.0, step=1.0)
    
with col_in2:
    slope_type = st.selectbox("Задаване на наклон чрез:", ["Проценти (%)", "Градуси (°)"])
    if slope_type == "Проценти (%)":
        slope_val = st.number_input("Наклон (%):", value=5.0, step=0.1)
        # h = L * (slope / 100)
        h_diff = l_horiz * (slope_val / 100)
        angle_deg = np.degrees(np.arctan(slope_val / 100))
    else:
        angle_val = st.number_input("Ъгъл (°):", min_value=0.0, max_value=89.9, value=2.86)
        # h = L * tan(angle)
        h_diff = l_horiz * np.tan(np.radians(angle_val))
        slope_val = (h_diff / l_horiz) * 100
        angle_deg = angle_val

# Изчисляване на хипотенузата (реалната дължина на пътя)
l_hypotenuse = np.sqrt(l_horiz**2 + h_diff**2)

# Резултати
st.divider()
res1, res2, res3 = st.columns(3)
res1.metric("Денивелация (h)", f"{h_diff:.3f}")
res2.metric("Наклон", f"{slope_val:.2f} %")
res3.metric("Дължина по наклон", f"{l_hypotenuse:.2f}")

# Визуализация
fig, ax = plt.subplots(figsize=(10, 5))

# Точки на триъгълника
x = [0, l_horiz, l_horiz, 0]
y = [0, 0, h_diff, 0]

ax.plot(x, y, 'black', linewidth=1, alpha=0.5)  # Контур
ax.fill([0, l_horiz, l_horiz], [0, 0, h_diff], color='#1f77b4', alpha=0.2) # Запълване

# Подчертаване на хипотенузата (реалния път)
ax.plot([0, l_horiz], [0, h_diff], color='red', linewidth=3, label='Наклонена отсечка')

# Етикети
ax.text(l_horiz/2, -h_diff*0.05, f"L (хоризонтал): {l_horiz}", ha='center', fontweight='bold')
ax.text(l_horiz + (l_horiz*0.02), h_diff/2, f"h: {h_diff:.3f}", va='center', color='blue', fontweight='bold')
ax.set_title(f"Схема на наклона: {slope_val:.2f}% ({angle_deg:.2f}°)")

# Скриване на излишни оси за по-чист вид
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_aspect('equal') # Важно за реалното визуално възприятие на ъгъла
ax.grid(True, linestyle='--', alpha=0.5)

st.pyplot(fig)
