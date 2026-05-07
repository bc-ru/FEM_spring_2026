import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Область", 
    "Краевая задача", 
    "Функциональное выделение частей",
    "Явное выделение частей"
    )
)
  
if menu == "Область":
    r"""
##### Область
$~$
    """
    image = Image.open("pages/figs/1.png")
    st.image(image)
    r"""
* Две подобласти

  $\Omega = \Omega_1 \cup \Omega_2 \cup \gamma$
* Две части границы

  $\partial \Omega = \Gamma_1 \cup \Gamma_2$

    """    
    
if menu == "Краевая задача":
    r"""
##### Краевая задача

**Уравнение**

$\begin{aligned}
{-} \frac{\partial } {\partial x_1} \Big (k(\bm x) \frac{\partial u} {\partial x_1} \Big ) - \frac{\partial } {\partial x_2} \Big (k(\bm x) \frac{\partial u} {\partial x_2} \Big )  
 = 0, \quad \bm x = (x_1,x_2) \in \Omega
\end{aligned}$

**Неоднородная среда**

* $k(\bm x) = k_1, \quad  \bm x \in \Omega_1$
* $k(\bm x) = k_2, \quad  \bm x \in \Omega_2$

**Смешанные граничные условия**

Условия Дирихле

$\begin{aligned}
u(\bm x) = 0, \quad \bm x \in \Gamma_1
\end{aligned}$

Условия Неймана

$\begin{aligned}
\frac{\partial u}{\partial \nu} (\bm x) = 0, \quad \bm x \in \Gamma_2
\end{aligned}$

    """
    
if menu == "Функциональное выделение частей":

    r"""
##### Функциональное выделение частей
$~$
    """

    image = Image.open("pages/figs/2.png")
    st.image(image)    
    r"""
**Маркирование**
* части всей области $\Omega$
* части границы $\partial \Omega$

**Часть области**

Интерфейсная граница

$\gamma: \quad (x_1-a)^2 + (x_2-b)^2 = r^2$

Подобласти
* $\Omega_1: \quad (x_1-a)^2 + (x_2-b)^2 < r^2, \quad \bm x \in \Omega$
* $\Omega_2: \quad (x_1-a)^2 + (x_2-b)^2 > r^2, \quad \bm x \in \Omega$

**Часть границы**
* $\Gamma_1: \quad  x_1 = 0, \quad \bm x \in \partial \Omega$
* $\Gamma_2: \quad  x_1 > 0, \quad \bm x \in \partial \Omega$ 

   """
    
if menu == "Явное выделение частей":
    r"""
##### Явное выделение частей
$~$
    """
    image = Image.open("pages/figs/1.png")
    st.image(image)
    r"""
**Границы**
  
  $\Gamma_1, \Gamma_2, \gamma$

**Области**
* $\Omega_1: \quad \partial \Omega_1 = \gamma$

* $\Omega_2: \quad \partial \Omega_2 = \Gamma_1 \cup \Gamma_2 \cup \gamma$

    """
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    