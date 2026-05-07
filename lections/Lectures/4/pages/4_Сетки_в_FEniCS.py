import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Структурированные сетки", 
    "Модуль mshr",     
    "Импорт сеток",         
    )
)
  
if menu == "Структурированные сетки":
    r"""
##### Структурированные сетки
**Базовые регулярные сетки**

1D, 2D, 3D

**Параллелепипед**
    """
    c1, c2, = st.columns([2,1])
    image = Image.open("pages/figs/gr7.png")
    c1.image(image) 

    r"""   
**Фрагмент кода**
    """
 
    code = """
import pyvista
mesh = BoxMesh(Point(0, 0, 0), Point(1, 1, 1), 4, 4, 4)
pyvista_mesh = pyvista.UnstructuredGrid(mesh)
pyvista.plot(pyvista_mesh, show_edges=True, show_axes=True)
    """

    st.code(code, language="python")      
    
if menu == "Модуль mshr":
    r"""
##### Модуль mshr
**CSG технология**
* сборка 2D геометрии: Polygon, Circle, Rectangle, Ellipse
* сборка 3D геометрии: Cylinder, Box, Cone, Sphere, Tetrahedron

**Пример**
    """
    c1, c2, = st.columns([2,1])    
    image = Image.open("pages/figs/gr8.png")
    c1.image(image) 

    r"""   
**Фрагмент кода**
    """
 
    code = """
from mshr import *
domain = Rectangle(Point(0., 0.), Point(2, 2)) - Circle(Point(0.0, 0.0), 1) 
mesh = generate_mesh(domain, 10)
plot(mesh)
    """

    st.code(code, language="python")     

    
if menu == "Импорт сеток":
    r"""
##### Импорт сеток
**Трансформация форматов сеток**
* gmsh де-факто является стандартным генератором в научных и инженерных вычислениях
* Прямое использование сетки Gmsh (формат Gmsh 2) в FEniCS 
* Из других программ: сначала в формат gmsh, затем используется в FEniCS

**Подготовка сетки в netgen**
$~$
    """
    
    c1, c2, = st.columns([2,1])    
    image = Image.open("pages/figs/17.png")
    c1.image(image) 
    
    r"""
**Файл геометрии**
    """
    code = """    
algebraic3d

# Box
solid Box = orthobrick (0, 0, 0; 2, 2, 2);

# Cylinder
solid Cylinder = cylinder (0, 0, 0; 0, 0, 1; 1);


# Domain
solid Domain = Box and not Cylinder;

tlo Domain -col=[0,1,0] -transparent;
    """
    st.code(code, language="gmsh")  
    
    r"""
**Геометрии - генерация сетки - запись сетки в формате Gmsh 2**      
    """
 
    
                    
