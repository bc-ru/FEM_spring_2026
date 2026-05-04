import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
from matplotlib.lines import Line2D

st.set_page_config(
    page_title="Геометрическая модель | Обтекание шара",
    page_icon="🏛️",
    layout="wide"
)

st.title("Геометрическая модель")

st.markdown(r"""
## Расчетная область

**Цилиндрические координаты** \( (r, z) \)

- \( D \) – сечение шара
- \( a \) – радиус шара
- $( \Omega ) $ – расчетная область
- $( \Gamma_1 ) $ – внешняя граница расчетной области
- $( R ) $ – радиус внешней границы
- $( \Gamma_{\gamma 1} )$, $( \Gamma_{\gamma 2} )$ – границы симметрии

**Направление оси $( z )$:** справа → налево (навстречу потоку)
""")

# Параметры
a = 1.0      # радиус шара
R = 3.0      # внешний радиус

# Создание фигуры
fig, ax = plt.subplots(figsize=(10, 10))

# 1. Шар D
sphere = Circle((0, 0), a, facecolor='lightgray', edgecolor='black', 
                linewidth=2.5, alpha=0.8, zorder=2)
ax.add_patch(sphere)

# 2. Внешняя граница Γ₁
outer = Circle((0, 0), R, fill=False, edgecolor='red', 
               linewidth=2, linestyle='--', zorder=2)
ax.add_patch(outer)

# 3. Расчётная область Ω (заливка точками)
# Правильное создание сетки для заливки
r_fill = np.linspace(a, R, 50)
z_fill = np.linspace(-R, R, 100)
R_fill_grid, Z_fill_grid = np.meshgrid(r_fill, z_fill)

# Маска: только точки вне шара (r² + z² ≥ a²) и r ≥ 0
mask = (R_fill_grid**2 + Z_fill_grid**2 >= a**2) & (R_fill_grid >= 0)

# Применяем маску
R_plot = R_fill_grid[mask]
Z_plot = Z_fill_grid[mask]

ax.scatter(Z_plot, R_plot, c='lightblue', alpha=0.25, s=2, zorder=0)

# 4. Границы симметрии Γγ₁ и Γγ₂
# Γγ₁ - луч под углом 45°
ax.plot([0, R*np.cos(np.pi/4)], [0, R*np.sin(np.pi/4)], 
        'g--', linewidth=2, alpha=0.8, zorder=2)
# Γγ₂ - ось r = 0 (вертикальная линия)
ax.plot([0, 0], [0, R], 'g--', linewidth=2, alpha=0.8, zorder=2)

# 5. Направление оси z и потока (справа налево)
# Стрелка оси z
ax.annotate('', xy=(-R+0.5, -0.3), xytext=(R-0.5, -0.3),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
ax.text(0, -0.5, '$z$', fontsize=14, color='gray', ha='center')

# Стрелка потока
ax.annotate('', xy=(-R+0.8, 0.4), xytext=(R-0.8, 0.4),
            arrowprops=dict(arrowstyle='->', color='darkred', lw=2.5))
ax.text(0, 0.65, '$u_\\infty$', fontsize=14, color='darkred', ha='center', fontweight='bold')

# 6. Подписи
ax.text(a/2, -a/3, '$D$', fontsize=18, fontweight='bold', 
        ha='center', va='center')
ax.text(R+0.1, 0.15, '$\\Gamma_1$', fontsize=14, color='red', fontweight='bold')
ax.text(0.15, R-0.2, '$\\Gamma_{\\gamma 2}$', fontsize=12, color='green', fontweight='bold')
ax.text(1.2, 1.3, '$\\Gamma_{\\gamma 1}$', fontsize=12, color='green', fontweight='bold')
ax.text(1.8, 1.6, '$\\Omega$', fontsize=20, fontweight='bold', 
        color='darkblue', alpha=0.6)
ax.text(-R-0.2, -0.2, '$-R$', fontsize=11, ha='center')
ax.text(R+0.1, -0.2, '$R$', fontsize=11, ha='center')

# 7. Подписи осей
ax.set_xlabel('$z$ (осевая координата) → направление потока', fontsize=13)
ax.set_ylabel('$r$ (радиальная координата)', fontsize=13)
ax.set_title('Расчётная область в цилиндрических координатах $(r, z)$', 
             fontsize=14, fontweight='bold')

# 8. Настройки отображения
ax.set_aspect('equal')
ax.set_xlim(-R-0.5, R+0.5)
ax.set_ylim(-0.2, R+0.3)
ax.grid(True, alpha=0.2, linestyle=':')
ax.axhline(0, color='black', linewidth=0.5, alpha=0.3)

# 9. Легенда
legend_elements = [
    Line2D([0], [0], color='black', linewidth=2.5, label='Сечение шара $D$ (радиус $a$)'),
    Line2D([0], [0], color='red', linestyle='--', linewidth=2, label='Внешняя граница $\\Gamma_1$ (радиус $R$)'),
    Line2D([0], [0], color='green', linestyle='--', linewidth=2, label='Границы симметрии $\\Gamma_{\\gamma 1}, \\Gamma_{\\gamma 2}$'),
    Line2D([0], [0], color='darkred', linewidth=2.5, label='Направление потока $u_\\infty$'),
    plt.scatter([], [], c='lightblue', alpha=0.5, s=80, label='Расчётная область $\\Omega$')
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=10, framealpha=0.95)

# Отображение в Streamlit
col1, col2 = st.columns([2, 1])

with col1:
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown(r"""
    ### Обозначения
    
    | Обозначение | Смысл |
    |-------------|-------|
    | $D$ | сечение шара |
    | $a$ | радиус шара |
    | $\Omega$ | расчётная область |
    | $\Gamma_1$ | внешняя граница |
    | $R$ | радиус внешней границы |
    | $\Gamma_{\gamma 1}, \Gamma_{\gamma 2}$ | границы симметрии |
    
    ### Направление оси $z$
    
    Ось $z$ направлена **справа → налево**.
    
    Поток набегает из области $z > 0$ в область $z < 0$.
    """)

st.markdown("---")
st.markdown(
    '<div style="text-align: center; color: gray;">'
    '<p> <strong>Цилиндрические координаты (r, z) | Осесимметричная задача | Потенциальное обтекание шара</strong></p>'
    '<p>  Направление оси z: справа налево | Поток: $u_\\infty$ вдоль $-z$</p>'
    '</div>',
    unsafe_allow_html=True
)
