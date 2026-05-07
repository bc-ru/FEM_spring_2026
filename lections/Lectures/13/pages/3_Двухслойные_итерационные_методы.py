import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Стационарный итерационный метод", 
    "Оптимальные итерационные параметры",    
    "Метод минимальных невязок", 
    "Двухслойный итерационный метод",    
    "Трехслойный итерационный метод",       
    )
)
  
if menu == "Стационарный итерационный метод":
    r"""
##### Стационарный итерационный метод

Задача

$\begin{aligned}
 A y = g,
 \quad A = A^*  > 0 
\end{aligned}$

$\tau_{k+1} = \tau ~-~$ метод простой итерации 

$\quad ~$ (стационарный итерационный метод)

$\begin{aligned}
  B \frac {y^{k+1} - y^k}{\tau} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

**Основное утверждение**

Метод простой итерации сходится в $H_A$ при выполнении 

$\quad ~$ (неравенство А.А. Самарского)

$\begin{aligned}
  B > \frac{\tau}{2} A 
\end{aligned}$
    """

if menu == "Оптимальные итерационные параметры":
    r"""
##### Оптимальные итерационные параметры

$\begin{aligned}
  B \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

Пусть

$\begin{aligned}
 B = B^* > 0,
 \quad \gamma_1 B \le A \le \gamma_2 B ,
 \quad \gamma_1 > 0
\end{aligned}$

Оптимальное значение $\tau$ для стационарного итерационного метода

$\begin{aligned}
 \tau = \tau_0 = \frac {2}{\gamma_1 + \gamma_2}
\end{aligned}$

Число итераций

$\begin{aligned}
 K \ge K_0(\varepsilon) = \frac {\ln \varepsilon} {\ln \varrho_0},
 \quad \varrho_0 = \frac {1 -\xi}{1+\xi},
 \quad \xi = \frac {\gamma_1}{\gamma_2} 
\end{aligned}$

Чебышевский итерационный метод 

$\quad ~$ (метод Ричардсона) 

$\begin{aligned}
  \tau_k = \frac {\tau_0}{1 + \varrho_0 \mu_k},
  \quad k = 1,2,\ldots,K 
\end{aligned}$

$\mu_k ~-~$ корни полинома Чебышева
    """

if menu == "Метод минимальных невязок":
    r"""
##### Метод минимальных невязок

Явный ($B = I$) итерационный метод

$\begin{aligned}
  \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

$\tau_{k+1}$ из условия минимума невязки на новой итерации

Для погрешности $z^k = y^k - y$ и невязки $r^k = A y^k-A y = Az^k$ 

$\begin{aligned}
 z^{k+1} = z^k - \tau_{k+1} A z^k,
 \quad r^{k+1} = r^k - \tau_{k+1} A r^k  
\end{aligned}$

Для нормы невязки

$\begin{aligned}
 \|r^{k+1}\|^2 = \|r^k\|^2 - 2\tau_{k+1} (A r^k, r^k) + \tau_{k+1}^2 \|A r^k\|^2 
\end{aligned}$

Минимум правой части при

$\begin{aligned}
 \tau_{k+1} = \frac{ (A r^k, r^k)}{\|A r^k\|^2 } 
\end{aligned}$
    """

if menu == "Двухслойный итерационный метод":
    r"""
##### Двухслойный итерационный метод

$\begin{aligned}
  B \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

Итерационный процесс запишется следующим образом

$\begin{aligned}
 y^{k+1} = y^k  - \tau_{k+1} w^k ,
 \quad k = 0,1, \ldots 
\end{aligned}$

$r^k  = A y^k  - g ~-~$ невязка, $w^k   = B^{-1} r^k ~-~$  поправка

Минимум погрешности в $H_R$ при

$\begin{aligned}
   \tau_{k+1} = \frac {(Rw^k, z^k)}{(Rw^k,w^k)}
\end{aligned}$

Метод скорейшего спуска

$\begin{aligned}
 R =  A,
 \quad   \tau_{k+1} = \frac {(w^k, r^k)}{(Aw^k,w^k)}
\end{aligned}$

Метод минимальных поправок

$\begin{aligned}
 R =  A B^{-1} A, 
 \quad \tau_{k+1} = \frac {(Aw^k, w^k)}{(B^{-1}Aw^k,Aw^k)}
\end{aligned}$

    """
    
if menu == "Трехслойный итерационный метод":
    r"""
##### Трехслойный итерационный метод

Каноническая  форма

$\begin{aligned}
  By^{k+1} = \alpha_{k+1} (B - \tau_{k+1} A) y^k +
  (1 - \alpha_{k+1}) By^{k-1} + \alpha_{k+1} \tau_{k+1} g,
  \quad k = 1,2, \ldots 
\end{aligned}$

$\begin{aligned}
  By^{1} = (B - \tau_{1} A) y^0 + \tau_{1} g
\end{aligned}$

$\alpha_{k+1}$  и  $\tau_{k+1} ~-~$ итерационные параметры

В методе сопряженных градиентов 

$\begin{aligned}
 \tau_{k+1} = \frac {(w^k, r^k)}{(Aw^k,w^k)}.
 \quad k = 0,1, \ldots 
\end{aligned}$

$\begin{aligned}
 \alpha_1 = 1,
 \quad \alpha_{k+1} = \left (1 - \frac {\tau_{k+1}}{\tau_k}
 \frac {(w^k, r^k)}{(w^{k-1},r^{k-1})}
 \frac {1}{\alpha_k} \right )^{-1} ,
 \quad k = 1,2 \ldots 
\end{aligned}$
    """

    

    
