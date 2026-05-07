import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Сборка снизу-вверх", 
    "1D модели", 
    "2D модель",
    "Геометрия (gmsh)",    
    "Недостатки, достоинства",
    )
)
  
if menu == "Сборка снизу-вверх":
    r"""
##### Сборка снизу-вверх

**Геометрические примитивы (0D, 1D, 2D, 3D)**

$~\bullet~$ 0D: $\quad$ точки

$\to$ 1D: $\quad$ 0D $\sim$ 0D - кривая с начальной и конечной точкой

$\bigcirc$ 1D: $\quad$ $\cup \to$ 1D - замкнутая кривая 

$\blacksquare~$ 2D: $\quad$  $\bigcirc$ 1D $\cup$  ($~\cup$ $\bigcirc$ 1D) - плоская область
(внешняя и внутренние границы)

$~~~~\,$ 3D: $\quad$ плоские, криволинейные поверхности, замкнутая поверхность, трехмерный объем

    """ 
    
if menu == "1D модели":
    r"""
##### 1D модели

**Отрезок**
    """
    image = Image.open("pages/figs/3.png")
    st.image(image)   

    r"""
**Кривая (2D, 3D)**
    """
    image = Image.open("pages/figs/4.png")
    st.image(image)    

    r"""
**Граф (2D, 3D)**
    """
    image = Image.open("pages/figs/5.png")
    st.image(image)   
    
if menu == "2D модель":

    r"""
##### 2D модель
**Элементы геометрической модели**
$~$ 
    """

    image = Image.open("pages/figs/6.png")
    st.image(image)    
    r"""
**Файл геометрии (gmsh)**   
    """

    code = """
// шаг сетки
h = 0.5;
hh = h /5;

// точки для прямоугольника
Point(1) = {0,0,0,h};
Point(2) = {0,4,0,h};
Point(3) = {8,4,0,h};
Point(4) = {8,0,0,h};

// точки для круга
Point(5) = {2,2,0,hh};
Point(6) = {1,2,0,hh};
Point(7) = {2,3,0,hh};
Point(8) = {3,2,0,hh};
Point(9) = {2,1,0,hh};

// линии на границе прямоугольнике
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// линии на окружности
Circle(5) = {6,5,7};
Circle(6) = {7,5,8};
Circle(7) = {8,5,9};
Circle(8) = {9,5,6};

// граница прямоугольника
Line Loop(11) = {1,2,3,4};

// окружность
Line Loop(12) = {5,6,7,8};

// прямоугольник с вырезом
Plane Surface(21) = {11,12};

// круг
Plane Surface(22) = {12};

// выделение частей границы
Physical Line(1) = {1};
Physical Line(2) = {2,3,4};

// выделение частей области
Physical Surface(1) = {21};
Physical Surface(2) = {22};
    """
    st.code(code, language="gmsh")  
    
if menu == "Геометрия (gmsh)":    
    r"""
##### Геометрия (gmsh)
**Части границы**
$~$ 
    """
    c1, c2 = st.columns(2)
    image = Image.open("pages/figs/7.png")
    c1.image(image)      
    image = Image.open("pages/figs/8.png")
    c2.image(image)      
    r"""
**Части области**
$~$ 
    """
    c1, c2 = st.columns(2)
    image = Image.open("pages/figs/9.png")
    c1.image(image)      
    image = Image.open("pages/figs/10.png")
    c2.image(image)      
     
if menu == "Недостатки, достоинства":
    r"""
##### Недостатки, достоинства

$\bm - ~~$  сложность 

$\bm + ~~$ детальность и контроль качества геометрической модели (сетки)

$\bm + ~~$ проработка всех частей области и границы расчетной области    

    """
    
    