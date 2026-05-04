import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(
    page_title="Streamlit: удобная python библиотека для визуализации",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
.block-container {
    padding-top: 1.4rem;
    padding-bottom: 2rem;
    max-width: 1350px;
}
.section-card {
    border: 1px solid rgba(120,120,120,0.18);
    border-radius: 18px;
    padding: 1rem 1.1rem;
    background: rgba(255,255,255,0.02);
    margin-bottom: 1rem;
}
.big-title {
    font-size: 2.7rem;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 0.15rem;
}
.subtitle {
    font-size: 1.1rem;
    color: #6b7280;
    margin-bottom: 1rem;
}
.small-muted {
    color: #6b7280;
    font-size: 0.95rem;
}
.code-note {
    font-size: 0.95rem;
    color: #6b7280;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
st.markdown("""
<style>
h1 {
    padding-top: 0.5rem;
}
.block-container {
    padding-top: 2rem;
}
</style>
""", unsafe_allow_html=True)

SLIDES = [
    "Общая характеристика",
    "Установка",
    "Текст (Markdown, LaTeX)",
    "Таблицы: основы",
    "Таблицы: интерактив",
    "Научная графика: Matplotlib",
    "Научная графика: Plotly",
    "Компоновка страницы",
    "Многостраничность",
    "GUI элементы",
    "Параметрический расчет",
]


with st.sidebar:
    st.title("🎓 Streamlit")
    slide = st.radio("📚 Содержание", SLIDES)
    st.divider()
    st.markdown("**Что входит**")
    st.markdown(
        "- Общая характеристика\n- Установка\n- Markdown и LaTeX\n- Таблицы\n- Научная графика\n- GUI\n- Параметрический расчёт\n- Компоновка и многостраничность"
    )


def hero(title: str, subtitle: str = ""):
    st.markdown(f'<div class="big-title">{title}</div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f'<div class="subtitle">{subtitle}</div>', unsafe_allow_html=True)
    st.divider()


def card_start():
    st.markdown('<div class="section-card">', unsafe_allow_html=True)


def card_end():
    st.markdown('</div>', unsafe_allow_html=True)


# ------------------- 1. МОИ СЛАЙДЫ -------------------
if slide == "Общая характеристика":
    hero("Общая характеристика", "Что такое Streamlit и где он применяется")

    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(
            """
            Streamlit — это Python-библиотека для создания **интерактивных веб-приложений** без отдельной фронтенд-разработки.

            Основная идея очень простая:
            - пишем обычный Python-скрипт;
            - добавляем элементы интерфейса через `streamlit`;
            - запускаем приложение командой `streamlit run ...`;
            - результат открывается в браузере.
            """
        )
        st.info(
            "Streamlit особенно удобен для учебных проектов, анализа данных, ML-демо, исследовательских интерфейсов и внутренних инструментов."
        )

    with col2:
        st.markdown("### Ключевые свойства")
        a, b = st.columns(2)
        a.metric("Язык", "Python")
        b.metric("Тип", "Web app")
        a.metric("Порог входа", "Низкий")
        b.metric("Сильная сторона", "Быстрый старт")

    st.markdown("### Обзор")
    left, right = st.columns(2)
    with left:
        st.success("Подходит для: дашбордов, научных демонстраций, прототипов, курсовых и лабораторных работ")
        st.markdown(
            """
            **Преимущества:**
            - простой API;
            - интерфейс строится прямо в Python;
            - есть таблицы, графики, формы, виджеты;
            - легко показывать код, текст, формулы и результаты вычислений.
            """
        )
    with right:
        st.warning("Не лучший выбор для очень сложных кастомных клиентских интерфейсов")
        st.markdown(
            """
            **Типичный сценарий использования:**
            1. написать модель или расчёт на Python;
            2. добавить поля ввода и кнопки;
            3. показать таблицу, график или формулу;
            4. получить готовое интерактивное приложение.
            """
        )

    st.markdown("### Минимальный пример")
    st.code(
        '''import streamlit as st

st.title("Привет, Streamlit!")
name = st.text_input("Введите имя")

if name:
    st.success(f"Привет, {name}!")
''',
        language="python",
    )

elif slide == "Установка":
    hero("Установка", "Как подготовить окружение и запустить первое приложение")

    tab1, tab2, tab3 = st.tabs(["Через pip", "Почему venv", "Структура проекта"])

    with tab1:
        st.markdown("### Рекомендуемый способ установки")
        st.markdown(
            "Перед установкой желательно создать **виртуальное окружение `venv`**, чтобы зависимости проекта были изолированы от глобального Python."
        )
        st.code(
            '''python -m venv .venv
source .venv/bin/activate   # Linux / macOS
# .venv\\Scripts\\activate    # Windows

pip install --upgrade pip
pip install streamlit
streamlit hello''',
            language="bash",
        )
        st.success("`streamlit hello` запускает встроенный демонстрационный пример.")

        st.markdown("### Запуск собственного приложения")
        st.code("streamlit run app.py", language="bash")

    with tab2:
        st.markdown("### Зачем использовать `venv`")
        st.markdown(
            """
            Виртуальное окружение полезно, потому что:
            - зависимости одного проекта не конфликтуют с другим;
            - легче повторить окружение на другом компьютере;
            - удобнее хранить точный список библиотек в `requirements.txt`;
            - проект становится аккуратнее и переносимее.
            """
        )
        st.info("Для учебного проекта пометка про `venv` — важная и правильная практика.")

        st.markdown("### Пример `requirements.txt`")
        st.code(
            """streamlit
pandas
numpy
matplotlib
plotly""",
            language="text",
        )

    with tab3:
        st.markdown("### Типичная структура Streamlit-проекта")
        st.code(
            '''my_streamlit_project/
├── app.py
├── requirements.txt
├── data/
├── images/
└── pages/''',
            language="text",
        )
        st.markdown(
            """
            Обычно главный файл приложения содержит навигацию и основные разделы,
            а вспомогательные страницы и ресурсы раскладываются по папкам.
            """
        )

elif slide == "Текст (Markdown, LaTeX)":
    hero("Работа с текстом", "Markdown и LaTeX в Streamlit")

    tab1, tab2, tab3 = st.tabs(["Markdown", "LaTeX", "Вместе в одном приложении"])

    with tab1:
        st.markdown("### Markdown")
        st.markdown(
            "Markdown в Streamlit используется для заголовков, списков, выделения текста, ссылок, заметок и пояснений."
        )
        code_md = '''st.markdown("""
# Заголовок
## Подзаголовок
- пункт 1
- пункт 2
**жирный текст**, *курсив*, `код`
[Ссылка](https://streamlit.io)
""")'''
        st.code(code_md, language="python")

        st.markdown("### Пример отображения")
        st.markdown(
            """
# Заголовок
## Подзаголовок
- пункт 1
- пункт 2
**жирный текст**, *курсив*, `код`
[Ссылка](https://streamlit.io)
"""
        )

    with tab2:
        st.markdown("### LaTeX")
        st.markdown(
            "LaTeX позволяет красиво выводить математические формулы, что особенно удобно для технических и научных приложений."
        )
        code_latex = r'''st.latex(r"""
J(\theta) = \frac{1}{m}\sum_{i=1}^{m}
\left(h_\theta(x^{(i)}) - y^{(i)}\right)^2
""")'''
        st.code(code_latex, language="python")
        st.latex(r"""
        J(\theta) = \frac{1}{m}\sum_{i=1}^{m}
        \left(h_\theta(x^{(i)}) - y^{(i)}\right)^2
        """)

        st.markdown("### Ещё пример")
        st.latex(r"x_{k+1} = x_k - \alpha \nabla f(x_k)")

    with tab3:
        st.markdown("### Markdown и LaTeX вместе")
        st.markdown(
            "Хороший стиль для научного приложения: сначала кратко объяснить идею текстом, а затем показать формулу."
        )
        st.markdown("**Пример:** метод градиентного спуска обновляет точку в направлении, противоположном градиенту функции.")
        st.latex(r"x_{k+1} = x_k - \alpha \nabla f(x_k)")
        st.info("Такой формат особенно удобен для презентаций, учебных примеров и расчётных интерфейсов.")

# ------------------- 2. ТАБЛИЦЫ: ОСНОВЫ -------------------
elif slide == "Таблицы: основы":
    st.title("📊 Таблицы в Streamlit")

    df = pd.DataFrame({
        'Имя': ['Анна', 'Борис', 'Виктор', 'Галина', 'Дмитрий'],
        'Возраст': [25, 32, 28, 35, 41],
        'Зарплата': [65000, 89000, 72000, 95000, 120000],
        'Город': ['Москва', 'СПб', 'Казань', 'Екб', 'Новосиб']
    })

    tab1, tab2, tab3 = st.tabs(["📄 st.table", "⚡ st.dataframe", "✏️ st.data_editor"])

    with tab1:
        st.markdown("**Статическая таблица** - только для отображения")
        st.code("st.table(df)", language="python")
        st.table(df.head(3))

    with tab2:
        st.markdown("**Интерактивная таблица** - можно сортировать и искать")
        st.code("st.dataframe(df, use_container_width=True)", language="python")
        st.dataframe(df, use_container_width=True, hide_index=True)

    with tab3:
        st.markdown("**Редактируемая таблица** - можно изменять данные")
        st.code("edited_df = st.data_editor(df)", language="python")
        edited_df = st.data_editor(df, use_container_width=True, hide_index=True)
        if edited_df is not None:
            st.success("Данные обновлены!")

# ------------------- 3. ТАБЛИЦЫ: ИНТЕРАКТИВ -------------------
elif slide == "Таблицы: интерактив":
    st.title("✨ Интерактивные возможности таблиц")

    np.random.seed(42)
    n_rows = st.slider("Количество строк", 5, 20, 10)

    df_large = pd.DataFrame({
        'Дата': pd.date_range('2024-01-01', periods=n_rows, freq='D'),
        'Продажи': np.random.randint(100, 1000, n_rows),
        'Прибыль': np.random.randint(10, 200, n_rows),
        'Регион': np.random.choice(['Москва', 'СПб', 'Казань', 'Сочи'], n_rows),
        'Менеджер': np.random.choice(['Иванов', 'Петров', 'Сидоров'], n_rows)
    })

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Фильтрация данных")
        min_sales = st.slider("Мин. продажи", 0, 1000, 200)
        filtered_df = df_large[df_large['Продажи'] > min_sales]
        st.dataframe(filtered_df, use_container_width=True)

    with col2:
        st.subheader("Статистика по данным")
        st.write(f"Всего записей: {len(df_large)}")
        st.write(f"Средние продажи: {df_large['Продажи'].mean():.0f}")
        st.write(f"Макс. продажи: {df_large['Продажи'].max()}")
        st.write(f"Мин. продажи: {df_large['Продажи'].min()}")

        st.subheader("Распределение по регионам")
        region_stats = df_large['Регион'].value_counts()
        st.dataframe(region_stats)

# ------------------- 4. MATPLOTLIB -------------------
elif slide == "Научная графика: Matplotlib":
    st.title("📈 Классическая графика с Matplotlib")

    st.sidebar.header("Настройки графика")
    func = st.sidebar.selectbox("Функция", ["sin(x)", "cos(x)", "sin(x)*cos(x)"])
    freq = st.sidebar.slider("Частота", 0.5, 3.0, 1.0)
    grid = st.sidebar.checkbox("Сетка", True)

    x = np.linspace(0, 4*np.pi, 500)
    if func == "sin(x)":
        y = np.sin(freq * x)
    elif func == "cos(x)":
        y = np.cos(freq * x)
    else:
        y = np.sin(freq * x) * np.cos(freq * x)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))

    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.set_title(f"{func}, частота={freq}")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y")
    if grid:
        ax1.grid(True, alpha=0.3)

    ax2.hist(y, bins=30, color='skyblue', edgecolor='black')
    ax2.set_title("Распределение значений")
    ax2.set_xlabel("Значение")
    ax2.set_ylabel("Частота")

    st.pyplot(fig)

    with st.expander("Показать код"):
        st.code("""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_title("График sin(x)")
st.pyplot(fig)
        """, language="python")

# ------------------- 5. PLOTLY -------------------
elif slide == "Научная графика: Plotly":
    st.title("✨ Интерактивная графика с Plotly")

    st.sidebar.header("Выбор датасета")
    dataset = st.sidebar.selectbox(
        "Датасет",
        ["Синусоида", "Ирисы Фишера", "Чаевые в ресторане"]
    )

    if dataset == "Синусоида":
        x = np.linspace(0, 4*np.pi, 200)
        y = np.sin(x)
        df = pd.DataFrame({'x': x, 'sin(x)': y})
        fig = px.line(df, x='x', y='sin(x)', title='Интерактивный график sin(x)')

    elif dataset == "Ирисы Фишера":
        df = px.data.iris()
        fig = px.scatter(
            df,
            x='sepal_width',
            y='sepal_length',
            color='species',
            size='petal_length',
            hover_data=['petal_width'],
            title='Датасет Iris'
        )

    else:
        df = px.data.tips()
        fig = px.scatter(
            df,
            x='total_bill',
            y='tip',
            color='sex',
            facet_col='smoker',
            title='Зависимость чаевых от суммы счета'
        )

    fig.update_layout(height=500)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    **Преимущества Plotly:**
    - 🔍 Масштабирование и панорамирование
    - 📊 Всплывающие подсказки
    - 💾 Возможность сохранить как PNG
    """)

# ------------------- 6. КОМПОНОВКА СТРАНИЦЫ -------------------
elif slide == "Компоновка страницы":
    st.title("🎓 Streamlit: компоновка и многостраничность")
    st.header("📐 Компоновка страницы")
    st.markdown("Элементы компоновки помогают организовать контент, группировать элементы и создавать интерактивные интерфейсы.")

    layout_tab = st.tabs(["Колонки", "Контейнеры", "Виджеты", "Графики", "Вкладки"])

    with layout_tab[0]:
        st.subheader("Колонки (st.columns)")
        st.write("Позволяют размещать элементы рядом. Ширину можно задавать пропорционально.")

        st.write("**Равные колонки**")
        col1, col2 = st.columns(2)
        col1.metric("Температура", "24°C", "+2°C")
        col2.metric("Влажность", "65%", "-5%")
        st.code("""
col1, col2 = st.columns(2)
col1.metric("Температура", "24°C", "+2°C")
col2.metric("Влажность", "65%", "-5%")
        """, language="python")

        st.write("**Колонки разной ширины (3:1)**")
        col_main, col_side = st.columns([3, 1])
        with col_main:
            st.line_chart(np.random.randn(20))
        with col_side:
            st.selectbox("Фильтр", ["A", "B", "C"], key="layout_filter")
        st.code("""
col_main, col_side = st.columns([3, 1])
with col_main:
    st.line_chart(...)
with col_side:
    st.selectbox(...)
        """, language="python")

        st.write("**Параметры gap и border**")
        left, center, right = st.columns(3, gap="large", border=True)
        left.button("Кнопка 1", use_container_width=True, key="layout_btn1")
        center.button("Кнопка 2", use_container_width=True, key="layout_btn2")
        right.button("Кнопка 3", use_container_width=True, key="layout_btn3")
        st.code("""
left, center, right = st.columns(3, gap="large", border=True)
left.button("Кнопка 1", use_container_width=True)
...
        """, language="python")

        st.info("Колонки можно комбинировать с `st.sidebar` или `st.expander` для создания сложных макетов.")

    with layout_tab[1]:
        st.subheader("Контейнеры (st.container)")
        st.write("Контейнеры группируют логически связанные элементы, упрощают код и позволяют применять стили или условное отображение.")

        st.write("**Группировка элементов**")
        with st.container(border=True):
            st.markdown("#### Карточка метрик")
            a, b, c = st.columns(3)
            a.metric("Заказы", "125", "+5")
            b.metric("Выручка", "₽1.2M", "-3%")
            c.metric("Клиенты", "342", "+5%")
        st.code("""
with st.container(border=True):
    st.markdown("#### Карточка метрик")
    a, b, c = st.columns(3)
    a.metric(...)
    ...
        """, language="python")

        st.write("**Вложенные контейнеры**")
        with st.container():
            st.write("Это внешний контейнер")
            with st.container():
                st.write("Это вложенный контейнер")
                st.button("вложение", key="nested_btn")
        st.code("""
with st.container():
    st.write("Это внешний контейнер")
    with st.container():
        st.write("Это вложенный контейнер")
        st.button("Кнопка во вложенном")
        """, language="python")

        st.write("**Условное отображение**")
        show_extra = st.checkbox("Показать дополнительный блок")
        if show_extra:
            with st.container(border=True):
                st.write("Этот блок виден только при установленном флажке.")
        st.code("""
show_extra = st.checkbox("Показать дополнительный блок")
if show_extra:
    with st.container(border=True):
        st.write("Этот блок виден только при установленном флажке.")
        """, language="python")

    with layout_tab[2]:
        st.subheader("Виджеты (интерактивные элементы)")
        st.write("Позволяют пользователю взаимодействовать с приложением.")

        st.write("**Кнопка (st.button)**")
        if st.button("Нажми меня", key="layout_press"):
            st.success("Кнопка нажата!")
        st.code("""
if st.button("Нажми меня"):
    st.success("Кнопка нажата!")
        """, language="python")

        st.write("**Выбор одного варианта (st.radio) и нескольких (st.multiselect)**")
        choice = st.radio("Выберите цвет", ["Красный", "Зелёный", "Синий"], key="layout_radio")
        st.write(f"Выбрано: {choice}")

        options = st.multiselect("Выберите фрукты", ["Яблоко", "Банан", "Апельсин"], default=["Яблоко"], key="layout_fruits")
        st.write(f"Выбрано: {options}")

        st.code("""
choice = st.radio("Выберите цвет", ["Красный", "Зелёный", "Синий"])
options = st.multiselect("Выберите фрукты", ["Яблоко", "Банан", "Апельсин"])
        """, language="python")

        st.write("**Текстовый ввод (st.text_input, st.text_area)**")
        name = st.text_input("Ваше имя", key="layout_name")
        st.write(f"Привет, {name}!")

        message = st.text_area("Сообщение", key="layout_message")
        st.write(f"Длина сообщения: {len(message)} символов")
        st.code("""
name = st.text_input("Ваше имя")
message = st.text_area("Сообщение")
        """, language="python")

        st.write("**Дата и время (st.date_input, st.time_input)**")
        date = st.date_input("Выберите дату", key="layout_date")
        time = st.time_input("Выберите время", key="layout_time")
        st.write(f"Выбрано: {date} {time}")
        st.code("""
date = st.date_input("Выберите дату")
time = st.time_input("Выберите время")
        """, language="python")

    with layout_tab[3]:
        st.subheader("Графики")
        st.write("Streamlit поддерживает различные способы визуализации: встроенные графики и интеграцию с Plotly.")

        st.write("**Встроенные графики (st.line_chart, st.bar_chart)**")
        chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
        st.line_chart(chart_data)
        st.code("""
chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["A", "B", "C"])
st.line_chart(chart_data)
        """, language="python")

    with layout_tab[4]:
        st.subheader("Вкладки (st.tabs)")
        st.write("Вкладки позволяют переключаться между разными представлениями внутри одной страницы.")

        tab_a, tab_b, tab_c = st.tabs(["Кошка", "Собака", "Сова"])
        with tab_a:
            st.write("### Домашняя кошка")
            st.image("https://static.streamlit.io/examples/cat.jpg", width=300, caption="Пушистый друг")
            st.markdown("""
            **Интересные факты о кошках:**
            - Отличный слух: слышат ультразвук.
            - Спят около 16 часов в день.
            - Мурлыканье помогает снижать стресс.
            """)
            if st.button("Нравится котик", key="cat_like"):
                st.balloons()

        with tab_b:
            st.write("### Верный друг - собака")
            st.image("https://static.streamlit.io/examples/dog.jpg", width=300, caption="Лучший друг человека")
            st.markdown("""
            **Интересные факты о собаках:**
            - Понимают до 250 слов и жестов.
            - Чуют запах в 10 000 раз лучше человека.
            - Хвост виляет не только от радости.
            """)
            if st.button("Нравится собака", key="dog_like"):
                st.balloons()

        with tab_c:
            st.write("### Ночной охотник - сова")
            st.image("https://static.streamlit.io/examples/owl.jpg", width=300, caption="Таинственная птица")
            st.markdown("""
            **Интересные факты о совах:**
            - Глаза неподвижны, но голова поворачивается на 270 градусов.
            - Бесшумный полёт благодаря особому строению перьев.
            - Могут охотиться в полной темноте.
            """)
            if st.button("Нравится сова", key="owl_like"):
                st.balloons()

# ------------------- 7. МНОГОСТРАНИЧНОСТЬ -------------------
elif slide == "Многостраничность":
    st.title("🎓 Streamlit: компоновка и многостраничность")
    st.header("📁 Многостраничные приложения")
    st.markdown("Streamlit поддерживает создание приложений из нескольких страниц.")

    multipage_tab = st.tabs(["Основы", "Порядок и эмодзи", "Обмен состоянием"])

    with multipage_tab[0]:
        st.subheader("Как это работает")
        st.markdown("""
        - Главная страница — файл, переданный в `streamlit run`.
        - Дополнительные страницы размещаются в папке **`pages/`** рядом с главным файлом.
        - Каждый `.py` файл в `pages/` автоматически становится отдельной страницей.
        - Навигация появляется в боковой панели автоматически.
        """)

        st.markdown("**Пример структуры:**")
        st.code("""
my_app/
    main.py
    pages/
        analiz.py
        grafik.py
        """, language="markdown")

        st.markdown("**Пример содержимого `pages/analiz.py`:**")
        st.code("""
import streamlit as st
st.set_page_config(page_title="Анализ", page_icon="📊")
st.title("Аналитический дашборд")
# код страницы 
        """, language="python")

        st.markdown("---")
        st.markdown("### Демонстрация: имитация переключения страниц")
        st.markdown("Нажмите кнопки, чтобы переключаться между условными страницами. Состояние сохраняется через `st.session_state`.")

        if "page" not in st.session_state:
            st.session_state.page = "Главная"

        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("🏠 Главная", use_container_width=True):
                st.session_state.page = "Главная"
        with col2:
            if st.button("📊 Анализ", use_container_width=True):
                st.session_state.page = "Анализ"
        with col3:
            if st.button("📈 Графики", use_container_width=True):
                st.session_state.page = "Графики"

        if st.session_state.page == "Главная":
            st.info("Вы на главной странице. Здесь может быть общая информация.")
        elif st.session_state.page == "Анализ":
            st.success("Страница анализа данных. Пример метрики:")
            st.metric("Продажи", "1 250", "+5%")
        elif st.session_state.page == "Графики":
            st.warning("Страница графиков.")
            chart_data = pd.DataFrame(np.random.randn(20), columns=["Значение"])
            st.line_chart(chart_data)

        st.caption("Это имитация. В реальном приложении каждая страница была бы в отдельном файле.")

        st.success("✅ Самый быстрый способ создать многостраничное приложение — использовать папку `pages/`.")

    with multipage_tab[1]:
        st.subheader("Управление порядком страниц и иконки")
        st.markdown("""
        По умолчанию страницы сортируются по имени файла. Чтобы задать порядок, используйте числовые префиксы.
        Можно добавлять эмодзи в имена файлов — они отобразятся в меню.
        """)

        st.code("""
# Файлы в папке pages/
01_🏠_Home.py
02_📊_Analiz.py
03_📈_Grafik.py
        """, language="markdown")

        st.markdown("Streamlit отобразит пункты меню в указанном порядке с иконками.")

        st.markdown("**Демонстрация меню с эмодзи (выберите пункт):**")
        menu_item = st.radio(
            "Навигация (пример)",
            ["🏠 Главная", "📊 Анализ", "📈 Графики"],
            label_visibility="collapsed"
        )
        if menu_item == "🏠 Главная":
            st.write("Выбрана главная страница.")
        elif menu_item == "📊 Анализ":
            st.write("Выбрана страница анализа.")
        else:
            st.write("Выбрана страница графиков.")

    with multipage_tab[2]:
        st.subheader("Обмен данными между страницами")
        st.markdown("""
        Для передачи данных между страницами используется `st.session_state`.
        Например, можно сохранить ввод на главной странице и отобразить его на другой.
        """)

        st.code("""
# На главной странице
st.text_input("Ваше имя", key="username")

# На другой странице
st.write(f"Привет, {st.session_state.username}!")
        """, language="python")

        st.info("Значения в `st.session_state` сохраняются при переключении страниц.")

        st.markdown("### Демонстрация передачи данных")
        if "shared_text" not in st.session_state:
            st.session_state.shared_text = ""
        if "shared_input" not in st.session_state:
            st.session_state.shared_input = ""

        page_choice = st.radio("Выберите страницу:", ["Страница 1 (ввод)", "Страница 2 (вывод)"], key="page_choice_shared")

        if page_choice == "Страница 1 (ввод)":
            st.text_input("Введите текст для сохранения", key="shared_input")
            st.session_state.shared_text = st.session_state.shared_input
            st.write("Текст сохранён. Переключитесь на страницу 2, чтобы увидеть его.")
        else:
            st.write(f"Сохранённый текст: **{st.session_state.shared_text}**")
            if st.button("Очистить", key="clear_shared"):
                st.session_state.shared_text = ""
                st.rerun()

# ------------------- 8. GUI ЭЛЕМЕНТЫ -------------------
elif slide == "GUI элементы":
    st.title("🎛️ Элементы графического интерфейса")

    st.markdown("""
    Streamlit предоставляет набор встроенных **виджетов** для взаимодействия пользователя с приложением.

    ⚡ Особенность:
    - при изменении любого виджета приложение **перезапускается**
    - интерфейс становится **реактивным**
    """)

    st.subheader("📌 Основные категории виджетов")

    st.subheader("🔘 Кнопки и переключатели (демонстрация)")

    st.markdown("""
    Ниже показано, как работают основные элементы управления.
    Каждый из них возвращает значение, которое можно использовать в логике программы.
    """)

    st.markdown("### ▶️ st.button() — обычная кнопка")

    code_button = '''
    if st.button("Нажми меня"):
        st.write("Кнопка была нажата")
    '''
    st.code(code_button, language="python")

    if st.button("Нажми меня", key="gui_press"):
        st.success("Кнопка была нажата!")

    st.markdown("### ☑️ st.checkbox() — флажок (True / False)")

    code_checkbox = '''
    flag = st.checkbox("Показать текст")
    if flag:
        st.write("Текст отображается")
    '''
    st.code(code_checkbox, language="python")

    flag = st.checkbox("Показать текст", key="gui_flag")

    if flag:
        st.info("Текст отображается")

    st.markdown("### 🔘 st.radio() — выбор одного варианта")

    code_radio = '''
    choice = st.radio("Выбери вариант", ["A", "B", "C"])
    st.write(choice)
    '''
    st.code(code_radio, language="python")

    choice = st.radio("Выбери вариант", ["A", "B", "C"], key="gui_choice")
    st.write("Вы выбрали:", choice)

    st.markdown("### ⬇️ st.download_button() — скачать файл")

    code_download = '''
    st.download_button(
        label="Скачать текст",
        data="Пример файла",
        file_name="example.txt"
    )
    '''
    st.code(code_download, language="python")

    st.download_button(
        label="Скачать текст",
        data="Пример файла",
        file_name="example.txt"
    )

    st.subheader("💻 Пример использования")

    code = '''
name = st.text_input("Ваше имя")
age = st.slider("Возраст", 0, 100, 25)
hobby = st.selectbox("Хобби", ["Спорт", "Музыка", "Программирование"])

if st.button("Приветствовать"):
    st.write(f"Привет, {name}! Тебе {age} лет, хобби — {hobby}.")
'''
    st.code(code, language="python")

    st.subheader("▶️ Демонстрация")

    name = st.text_input("Ваше имя", key="gui_name")
    age = st.slider("Возраст", 0, 100, 25, key="gui_age")
    hobby = st.selectbox("Хобби", ["Спорт", "Музыка", "Программирование"], key="gui_hobby")

    if st.button("Приветствовать", key="gui_greet"):
        st.success(f"Привет, {name}! Тебе {age} лет, хобби — {hobby}")

    st.subheader("⚠️ Особенности")

    st.markdown("""
    - Виджеты возвращают значения → их можно сохранять в переменные  
    - Можно использовать `st.sidebar`  
    - Для сложных форм используется `st.form`
    """)

    code_form = """
    code_form = '''
    slide = st.sidebar.radio(
    "📚 Содержание",
    [
        "Общая характеристика",
        "Установка",
        "Текст (Markdown, LaTeX)",
        "Таблицы",
        "Научная графика",
        "GUI элементы",
        "Параметрический расчет",
        "Компоновка страницы",
        "Многостраничность"
    ]
)'''
st.code(code_form, language="python")
"""
    st.code(code_form, language="python")

    st.subheader("📦 Пример формы")

    code_form = '''
with st.form("my_form"):
    x = st.number_input("Введите x", step=1, value=1)
    submit = st.form_submit_button("Рассчитать")

    if submit:
        st.write(x**2)
'''
    st.code(code_form, language="python")

    with st.form("form_demo"):
        x = st.number_input("Введите x", step=1, value=1)
        submit = st.form_submit_button("Рассчитать")

        if submit:
            st.write("x² =", x**2)

    code_form2 = '''
tabs = st.tabs([
        "sin",
        "Разные функции",
        "Полином",
        "Таблица",
        "Метод Ньютона",
        "Форма",
        "CSV",
        "Session state"
    ])
    '''
    st.code(code_form2, language="python")

# ------------------- 9. ПАРАМЕТРИЧЕСКИЙ РАСЧЕТ -------------------
elif slide == "Параметрический расчет":
    st.title("🧮 Расчетная программа с параметрическим вводом")

    st.markdown("""
    Параметрический ввод — это способ, при котором пользователь задаёт параметры,
    а результат вычислений обновляется автоматически.
    """)

    tabs = st.tabs([
        "sin",
        "Разные функции",
        "Полином",
        "Таблица",
        "CSV"
    ])

    with tabs[0]:
        st.subheader("📈 Базовый пример")

        code = '''
a = st.slider("Амплитуда", 0.1, 5.0, 1.0)
b = st.slider("Частота", 0.1, 5.0, 1.0)

x = np.linspace(0, 10, 100)
y = a * np.sin(b * x)
'''
        st.code(code, language="python")

        a = st.slider("Амплитуда (a)", 0.1, 5.0, 1.0, key="param_a")
        b = st.slider("Частота (b)", 0.1, 5.0, 1.0, key="param_b")

        x = np.linspace(0, 10, 200)
        y = a * np.sin(b * x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.grid()
        st.pyplot(fig)

    with tabs[1]:
        st.subheader("🔀 Разнообразие параметров")

        code = '''
func = st.selectbox("Функция", ["sin", "cos", "exp"])
a = st.slider("Амплитуда", 0.1, 5.0)

if func == "sin":
    y = a * np.sin(x)
elif func == "cos":
    y = a * np.cos(x)
else:
    y = a * np.exp(-x)
'''
        st.code(code, language="python")

        func = st.selectbox("Функция", ["sin", "cos", "exp"], key="param_func")
        a = st.slider("Амплитуда", 0.1, 5.0, key="param_amp2")

        x = np.linspace(0, 10, 200)

        if func == "sin":
            y = a * np.sin(x)
        elif func == "cos":
            y = a * np.cos(x)
        else:
            y = a * np.exp(-x)

        fig, ax = plt.subplots()
        ax.plot(x, y)
        st.pyplot(fig)

    with tabs[2]:
        st.subheader("📊 Полином")

        code = '''
    coeffs = []
    for i in range(4):
        coeffs.append(st.slider(f"a{i}", -5.0, 5.0, 1.0))

    y = np.polyval(coeffs, x)
    '''
        st.code(code, language="python")

        x_range = np.linspace(-5, 5, 200)
        coeffs = []
        for i in range(4):
            val = st.slider(f"a{i}", -5.0, 5.0, 1.0, key=f"poly_a{i}")
            coeffs.append(val)

        st.session_state.poly_coeffs = coeffs

        y = np.polyval(coeffs, x_range)

        fig, ax = plt.subplots()
        ax.plot(x_range, y)
        st.pyplot(fig)

    with tabs[3]:
        st.subheader("📋 Таблица значений полинома (связана с вкладкой 'Полином')")

        if "poly_coeffs" not in st.session_state:
            st.session_state.poly_coeffs = [1.0, 1.0, 1.0, 1.0]

        coeffs = st.session_state.poly_coeffs

        st.markdown(f"**Текущие коэффициенты:** a₀ = {coeffs[0]}, a₁ = {coeffs[1]}, a₂ = {coeffs[2]}, a₃ = {coeffs[3]}")

        x_table = np.linspace(-5, 5, 21)
        y_table = np.polyval(coeffs, x_table)

        df = pd.DataFrame({"x": x_table, "y": y_table})
        st.dataframe(df, use_container_width=True)

        x_plot = np.linspace(-5, 5, 200)
        y_plot = np.polyval(coeffs, x_plot)
        fig, ax = plt.subplots()
        ax.plot(x_plot, y_plot)
        ax.axhline(0, color='gray', ls='--', lw=0.5)
        ax.axvline(0, color='gray', ls='--', lw=0.5)
        ax.grid(True)
        st.pyplot(fig)

    with tabs[4]:
        st.subheader("📥 Выгрузка данных полинома в CSV")
        st.markdown("""
        Здесь отображаются значения полинома из вкладки **Полином**.  
        Вы можете скачать их в формате CSV.
        """)

        if "poly_coeffs" in st.session_state:
            a0, a1, a2, a3 = st.session_state.poly_coeffs
            st.success(f"Текущие коэффициенты: a₀ = {a0:.2f}, a₁ = {a1:.2f}, a₂ = {a2:.2f}, a₃ = {a3:.2f}")
        else:
            a0, a1, a2, a3 = 0.0, 1.0, 0.0, 0.0
            st.info("Сначала задайте коэффициенты во вкладке **Полином** (сейчас используются значения по умолчанию).")

        x_vals = np.linspace(-5, 5, 21)
        y_vals = a0 + a1 * x_vals + a2 * x_vals ** 2 + a3 * x_vals ** 3

        df = pd.DataFrame({
            "x": x_vals,
            "y": y_vals
        })

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Скачать CSV",
            data=csv,
            file_name="polynomial_values.csv",
            mime="text/csv"
        )

st.divider()
