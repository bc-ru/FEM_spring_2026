import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Конечный элемент", 
    "Ячейки", 
    "Основные конечные элементы",
    )
)
  
if menu == "Конечный элемент":
    r"""
##### Конечный элемент

**Аппроксимация области**

* ячейки

**Аппроксимация на ячейке**

* узлы аппроксимации

* аппроксимирующая функция (полином)

    """    
    
if menu == "Ячейки":
    r"""
##### Ячейки

**1D**

$~$
    """

    c1,c2 = st.columns([1,4])
    image = Image.open("pages/figs/1.png")
    c1.image(image)  

    r""" 
$~$   
    
**2D**

$~$
    """

    c1,cc1,c2,cc2 = st.columns([2,2,2,5])
    image = Image.open("pages/figs/2.png")
    c1.image(image)  
    image = Image.open("pages/figs/3.png")
    c2.image(image)  

    r""" 
$~$
       
**3D**

$~$
    """

    c1,cc1,c2,cc2 = st.columns([2,1.2,2.4,4])
    image = Image.open("pages/figs/4.png")
    c1.image(image)  
    image = Image.open("pages/figs/5.png")
    c2.image(image)  
    
if menu == "Основные конечные элементы":
    r"""
##### Основные конечные элементы

* Непрерывные лагранжевые элементы
* Разрывные лагранжевые элементы
* Векторные конечные элементы

    """   
            