import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Сборка из многомерных примитивов", 
    "Булевы операции", 
    "3D CSG моделирование",
    "Геометрия (netgen)",    
    "Недостатки, достоинства",
    )
)
  
if menu == "Сборка из многомерных примитивов":
    r"""
##### Сборка из многомерных примитивов
**CSG (Constructive Solid Geometry) технология**
* 2D геометрическая модель: сборка из двумерных примитивов
* 3D геометрическая модель: сборка из трехмерных примитивов

**Библиотека примитивов (mshr в FEniCS)** 
* 2D: Polygon, Circle, Rectangle, Ellipse
* 3D: Cylinder, Box, Cone, Sphere, Tetrahedron

    """ 
    
if menu == "Булевы операции":
    r"""
##### Булевы операции 

$\bm \cup~~$ *Объединение*

$~~~~~~$ слияние двух геометрических объектов в один

$\bm -~~$ *Разность*

$~~~~~~~$ вычитание одного геометрического объекта из другого	

$\bm \cap~~$ *Пересечение*

$~~~~~~$  общая часть обоих геометрических объектов
    """
    
if menu == "3D CSG моделирование":

    r"""
##### 3D CSG моделирование
**Геометрические примитивы**
$~$ 
    """
    c1, c2 = st.columns(2)
    c1.write("$D_1$")
    image = Image.open("pages/figs/11.png")    
    c1.image(image)    
    c2.write("$D_2$")      
    image = Image.open("pages/figs/12.png")
    c2.image(image)   
    r"""
$~$ 

**Булевы операции**   
    """
    c1, c2 = st.columns(2)
    c1.write("$D_1 - D_2$")
    image = Image.open("pages/figs/13.png")    
    c1.image(image)    
    c2.write("$(D_1-D_2) \cup D_2$")      
    image = Image.open("pages/figs/14.png")
    c2.image(image)   
    
    
if menu == "Геометрия (netgen)":    
    r"""
##### Геометрия (netgen)
**Файл геометрии**  

    """

    code = """
algebraic3d

# Box
solid Box = orthobrick (0, 0, 0; 8, 4, 2);

# Ball
solid Ball = sphere (2, 2, 2; 1);

# Domain
solid Domain = Box and not Ball;

# Color
# tlo Box - col=[0,0,1];
tlo Ball - col=[1,0,0];
tlo Domain -col=[0,1,0] -transparent;
    """

    st.code(code, language="gmsh")  
     
if menu == "Недостатки, достоинства":
    r"""
##### Недостатки, достоинства

$\bm + ~~$ простота 

$\bm - ~~$ нет детального контроля геометрической модели (сетки)

$\bm - ~~$ проработка только частей области 

    """
    
    