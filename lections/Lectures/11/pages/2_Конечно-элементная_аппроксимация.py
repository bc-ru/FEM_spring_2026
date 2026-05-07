import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Краевая задача", 
    "Аппроксимация расчетной области", 
    "Лагранжевые конечные элементы",
    "Интегральное тождество",
    "Вариационная задача",
    )
)
  
if menu == "Краевая задача":
    r"""
##### Краевая задача

**Уравнение**

$\begin{aligned} 
\mathcal{L} u \equiv - 
 \operatorname{div} \big (k(\bm x) \operatorname{grad} u) + c(\bm x) u = f(\bm x) ,
 \quad \bm x = (x_1, x_2) \in \Omega
\end{aligned}$

с переменными коэффициентами

$\begin{aligned}
  k(\bm x) \geq \kappa > 0,
  \quad c(\bm x) \geq 0
\end{aligned}$

**Смешанные граничные условия**

Граница 

$\begin{aligned}
  \partial \Omega = \Gamma_D \cup \Gamma_N
\end{aligned}$

Условия Дирихле

$\begin{aligned}
  u(\bm x) = \mu(\bm x), 
  \quad \bm x \in \Gamma_D
\end{aligned}$

Условия Неймана

$\begin{aligned}
  k(\bm x) \frac{\partial u}{\partial n} =q(\bm x),
  \quad \bm x \in \Gamma_N
\end{aligned}$

    """    
    
if menu == "Аппроксимация расчетной области":
    r"""
##### Аппроксимация расчетной области

Расчетная область 

$\begin{aligned}
 \Omega, 
 \quad \partial \Omega
\end{aligned}$ 

Сетка  

$\begin{aligned}
   \overline{\omega} = \omega \cup \partial\omega = \{\bm x~ |~ \bm x = \bar{\bm x}_\alpha , \ \bar{\bm x}_\alpha \in \Omega \cup \partial \Omega, \ \alpha  = 0,1,\ldots,m\}
\end{aligned}$

* $\omega$ - множество внутренних узлов ($\bar{\bm x}_\alpha \in \Omega$) 
* $\partial\omega$ - множество граничных узлов ($\bar{\bm x}_\alpha \in \partial\Omega$)

Ячейки

$\begin{aligned}
 \Omega \approx \bigcup_{\beta}^{m} \Omega_\beta
\end{aligned}$
 
    """  
    
    c1, c2 = st.columns([2,1])
    c1.write("$~$")
    image = Image.open("pages/figs/1.png")    
    c1.image(image)   
    
if menu == "Лагранжевые конечные элементы":
    r"""
##### Лагранжевые конечные элементы

**Кусочно линейная аппроксимация**

$y(\bm x) = a_0 + a_1 x_1 + a_2 x_2$ - три узла аппроксимации

Узлы аппроксимации совпадают с узлами сетки 

    """ 
    
    c1, c2 = st.columns([2,1])
    c1.write("$~$")
    image = Image.open("pages/figs/2.png")    
    c1.image(image)   
    
    r"""
$~$

**Аппроксимация полиномом второго порядка**

$y(\bm x) = a_0 + a_1 x_1 + a_2 x_2 + a_3 x_1 x_1 + a_4 x_1 x_2 + a_5 x_2 x_2$ 

Узлы аппроксимации
 
 * три узла сетки
 * три узла на серединах ребер ячейки

    """ 
    
    c1, c2 = st.columns([2,1])
    c1.write("$~$")
    image = Image.open("pages/figs/3.png")    
    c1.image(image)  

if menu == "Интегральное тождество":
    r"""
##### Интегральное тождество

**Теорема о дивергенции**

$\begin{aligned}
 \int_\Omega \operatorname{div} \bm u \, dx = \int_{\partial \Omega}\bm u \cdot \bm n \, d s 
\end{aligned}$

$\bm n ~-~$ внешняя нормаль к $\partial \Omega$

**Пространства**

* $V$ - пространство достаточно гладких функций
* Подпространство $V_D = \{ v \ | \ v \in V, \quad v(\bm x) = \mu(\bm x),
  \quad \bm x \in \Gamma_D \}$ 
* Подпространство $V_0 = \{ v \ | \ v \in V, \quad v(\bm x) = 0,
  \quad \bm x \in \Gamma_D \}$ 

**Интегральное тождество**

$\begin{aligned}
(\mathcal{L} u - f, v) = 0 , 
\quad u \in V_D, \ v \in V_0
\end{aligned}$  

С учетом

$\begin{aligned}
& \operatorname{div} (\varphi \bm w) = \bm w \cdot \operatorname{grad} \varphi + \varphi \operatorname{div} \bm w \\
& \bm w = k(\bm x) \operatorname{grad}u, \quad \varphi = v
\end{aligned}$
  
для $u \in V_D$ и $v \in V_0$  
  
$\begin{aligned}
 (\mathcal{L} u, v) &= - \int_{\Omega} \operatorname{div} (k(\bm x) \operatorname{grad}u) v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx = \\
 &= - \int_{\Omega} \big (\operatorname{div} (k(\bm x) \operatorname{grad}u \, v ) - k(\bm x) \operatorname{grad} u \operatorname{grad} v \big ) \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx = \\
 & = - {\color {red}  \int_{\partial \Omega} k(\bm x) v \operatorname{grad} u \cdot \bm n \, ds} +  \int_{\Omega} k(\bm x) \operatorname{grad} u \operatorname{grad} v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx
\end{aligned}$

С учетом $v \in V_0$ и граничных условий Неймана

$\begin{aligned}
 \int_{\partial \Omega} k(\bm x) v \operatorname{grad} u \cdot \bm n \, ds = \int_{\Gamma_N} q(\bm x) v \, ds 
\end{aligned}$

Результат

$\begin{aligned}
\int_{\Omega} k(\bm x) \operatorname{grad} u \operatorname{grad} v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx = \int_{\Omega} f(\bm x) v \, d x + \int_{\Gamma_N} q(\bm x) v \, ds
\end{aligned}$

    """  
    
if menu == "Вариационная задача":
    r"""
##### Вариационная задача


Билинейная форма 

$\begin{aligned}
 a(u,v) = \int_{\Omega} k(\bm x) \operatorname{grad} u \operatorname{grad} v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx
\end{aligned}$

Линейная форма 

$\begin{aligned}
 l(v) = \int_{\Omega} f(\bm x) v \, d x + \int_{\Gamma_N} q(\bm x) v \, ds
\end{aligned}$

Вариационная задача: найти  $u \in V_D$ такую, что

$\begin{aligned}
 a(u,v) = l(v) ,
 \quad \forall v \in V_0
\end{aligned}$

    """   
