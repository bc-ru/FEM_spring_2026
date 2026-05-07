import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Аппроксимация области", 
    "2D триангуляция",     
    "3D триангуляция",         
    "Качество сетки", 
    "Хорошая сетка",
    )
)
  
if menu == "Аппроксимация области":
    r"""
##### Аппроксимация области
**Разбиение области на ячейки**

$\begin{aligned}
\Omega  \approx \bigcup_{\alpha=1}^{m} \Omega_\alpha
\end{aligned}$

**Пример (gmsh)**
    """
    st.write("")      
    image = Image.open("pages/figs/3.png")
    st.image(image)  
 
if menu == "2D триангуляция":
    r"""
##### 2D триангуляция
$~$
    """
    st.write("2D ячейки: треугольник, четырехугольник")      
    image = Image.open("pages/figs/1.png")
    st.image(image) 
    
    r"""
$~$
    """    
    st.write("Неконформная и конформная сетки")
    image = Image.open("pages/figs/4.png")
    st.image(image)     
      
    
if menu == "3D триангуляция":
    r"""
##### 3D триангуляция
$~$
    """
    st.write("3D ячейки: тетраэдр (черырехгранник), пятигранник, шестигранник")      
    image = Image.open("pages/figs/2.png")
    st.image(image)  
    
                    
if menu == "Качество сетки":
    r"""
##### Качество сетки 
**Теоретическая оценка**

Для погрешности аппроксимации $\delta u$ функции $u(x)$ линейными конечными элементами

$\begin{aligned}
\|\delta u\| \le \frac{c}{q} h \|u\|_*
\end{aligned}$

* $c = \textrm{const}$
* $h$ - диаметр ячейки (треугольника, тетраэдра)

**Ключевой параметр**

$\begin{aligned}
q = \frac{r}{h} 
\end{aligned}$

$r$ - радиус вписанной окружности (сферы)

$~$
    """
    st.write("")      
    image = Image.open("pages/figs/5.png")
    st.image(image)  
    
if menu == "Хорошая сетка":

    r"""
##### Хорошая сетка

Критерий

$\begin{aligned}
q = \frac{r}{h} \to \max = \frac{1}{\sqrt{3}}
\end{aligned}$

Равносторонний треугольник
* Стороны треугольника

$\begin{aligned}
\quad \ \frac{h_{min}}{h_{max}} \to \max = 1
\end{aligned}$

* Углы треугольника

$\begin{aligned}
\quad \ \min (\theta) \to \max = 60^0
\end{aligned}$

Идеал: триангуляция равносторонними треугольниками

    """

    
    
