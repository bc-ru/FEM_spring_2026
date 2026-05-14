# ЛР3: вихре-потенциальное течение в канале с уступом

Проект содержит стартовую реализацию лабораторной работы на `fenics-legacy` + `Gmsh`.

## 1. Что реализовано

Решается задача для функции тока

```math
-\Delta \psi = \omega(\psi)
```

с разделением области по знаку функции тока:

```math
\psi > 0 \quad \text{потенциальная область},
\qquad
\psi < 0 \quad \text{вихревая область}.
```

На каждой итерации решается линейная задача Пуассона:

```math
-\Delta \psi^{k+1} = \lambda^k F(\psi^k),
\qquad
\lambda^k = \frac{\Gamma}{\int_\Omega F(\psi^k)\,dx}.
```

Базовая модель: `F(ψ)=I(ψ<0)`. Исследовательская модель: `F(ψ)=(-ψ)^q I(ψ<0)`.

Скорость восстанавливается как

```math
v = (\partial_y \psi, -\partial_x \psi).
```

## 2. Структура

```text
geo/             параметризованный .geo шаблон и генератор
solver/          FEniCS legacy solver
experiments/     скрипты серий запусков
results/         результаты расчётов
app/             Streamlit-презентация
meshes/          сетки
```

## 3. Зависимости

Нужны:

- `fenics-legacy` / `dolfin`;
- `gmsh`;
- `meshio`;
- `numpy`, `pandas`;
- `streamlit` для презентации.

Пример установки внутри подходящего FEniCS-контейнера:

```bash
pip3 install meshio pandas streamlit
```

## 4. Быстрый запуск одного расчёта

Из корня проекта:

```bash
python3 geo/generate_geo.py \
  --L 4 --H 1 --l 1 --h 1 \
  --lc 0.08 \
  --out meshes/base/step_channel.geo

gmsh -2 meshes/base/step_channel.geo -format msh2 -o meshes/base/step_channel.msh

python3 solver/mesh_convert.py \
  meshes/base/step_channel.msh \
  meshes/base/step_channel

python3 solver/run_case.py \
  --mesh-prefix meshes/base/step_channel \
  --out results/base/p1_Gamma-2 \
  --L 4 --H 1 --l 1 --h 1 \
  --Gamma -2 \
  --degree 1 \
  --alpha 0.5 \
  --omega-model constant \
  --omega-power 0
```

Результаты появятся в:

```text
results/base/p1_Gamma-2/
├── psi.xdmf
├── velocity.xdmf
├── omega.xdmf
├── indicator.xdmf
├── metrics.csv
└── metrics.json
```

Файлы `.xdmf` можно открыть в ParaView.

## 5. Серии экспериментов

### Три сетки

```bash
python3 experiments/run_base_meshes.py
```

### Степени аппроксимации `p=1,2,3`

```bash
python3 experiments/run_poly_degree.py
```

### Разные значения циркуляции

```bash
python3 experiments/run_gamma_sweep.py
```

### Разные высоты уступа

```bash
python3 experiments/run_height_sweep.py
```

### Исследовательский трек: зависимость `ω(ψ)`

```bash
python3 experiments/run_omega_model_sweep.py
```

## 6. Streamlit

```bash
streamlit run app/presentation.py
```

## 7. Важное замечание по геометрии

Здесь используется геометрия типа backward-facing step:

```text
(-l,0) -> (0,0) -> (0,-h) -> (L,-h) -> (L,H) -> (-l,H)
```

Это согласуется с базовыми параметрами `L=4, H=1, l=1, h=1`, так как полная высота выходного сечения равна `H+h`.
Если в методичке используется другая ориентация уступа, нужно поправить только `geo/step_channel.geo.tpl` и граничные Physical Curve ID.

## 8. Численная устойчивость

Если расчёт падает с сообщением `Vortex area is zero`, попробуй увеличить начальное возмущение:

```bash
--initial-eps 0.1 --initial-vortex-x 3.0
```

Если итерации осциллируют, уменьши релаксацию:

```bash
--alpha 0.2
```

## 9. Обновлённая Streamlit-презентация

Презентация стала более подробной:

- интерактивная геометрическая схема с параметрами `L`, `H`, `l`, `h`;
- таблица граничных условий и Physical ID;
- предпросмотр `.msh` сеток из каталога `meshes/`;
- компактные таблицы метрик, чтобы они помещались на экран;
- фильтрация результатов по `case` и `degree`;
- графики по выбранным столбцам метрик;
- отображение PNG-картинок полей из `results/<case>/figs/`.

После каждого нового расчёта solver пытается сохранить презентационные PNG:

```text
results/<case>/figs/
├── mesh.png
├── psi.png
├── indicator.png
├── omega.png
└── velocity_magnitude.png
```

Если `matplotlib` не установлен, численный расчёт не прерывается, но PNG не создаются.
Установить зависимость можно так:

```bash
pip3 install matplotlib
```
