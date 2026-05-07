import streamlit as st
from PIL import Image

menu = st.sidebar.radio('***',
    (
    "Влияние вязкости",    
    "Иллюстрации",  
    "Режимы обтекания",   
    )
)
if menu == "Влияние вязкости":

    r"""
    ##### Влияние вязкости
    
    **Вязкая жидкость**

    $\begin{aligned}
      \frac{\partial \bm u }{\partial t} + (\bm u \cdot \operatorname{grad} ) \bm u +  \operatorname{grad} p  + 
      \frac{1}{ \operatorname{Re}} \operatorname{div} \operatorname{grad} \bm u = 0
    \end{aligned}$ 

    **Идеальная жидкость**

    $\begin{aligned}
      \frac{\partial \bm u }{\partial t} + (\bm u \cdot \operatorname{grad} ) \bm u +  \operatorname{grad} p = 0
    \end{aligned}$ 

    **Число Рейнольдса**

    $\begin{aligned}
     \operatorname{Re} = \frac{\varrho u l}{\mu} 
    \end{aligned}$ 

    **Типы течений**

    + ползущее
    + ламинарное
    + переходное
    + турбулентное 
    
    """   
    
if menu == "Иллюстрации":

    r"""
    ##### Иллюстрации
	    
    **Экспериментальные данные**
	    
    М.Ван-Дайк. *Альбом течений жидкости и газа*. М.: Мир, 1986
	    
    $\operatorname{Re} = 26$	

    """
    

	
    image = Image.open("pages/data/1.jpg")    
    st.image(image)     
    

    r"""
    $~$

    **Расчетные данные**

    An album of computational fluid motion

    """   
    st.link_button(":globe_with_meridians: album-of-cfm.com",  "https://album-of-cfm.com/")
    	
    st.video("pages/data/Reynolds number and flow past a cylinder.mp4")
	
if menu == "Режимы обтекания":

    r"""
    ##### Режимы обтекания
	       
    $\operatorname{Re} = 0.01$	

    """   
	
    image = Image.open("pages/data/2.png")    
    st.image(image)  
    
    r"""
	       
    $\operatorname{Re} = 20$	

    """   
	
    image = Image.open("pages/data/3.png")    
    st.image(image)  

    r"""
	       
    $\operatorname{Re} = 100$	

    """   
	
    image = Image.open("pages/data/4.png")    
    st.image(image)  

    r"""
	       
    $\operatorname{Re} = 10 \, 000$	

    """   
	
    image = Image.open("pages/data/5.png")    
    st.image(image)  

    r"""
	       
    $\operatorname{Re} = 10 \, 000 \, 000$	

    """   
	
    image = Image.open("pages/data/6.png")    
    st.image(image)  

    r"""
	       
    $\operatorname{Re} = \infty$	

    """   
	
    image = Image.open("pages/data/7.png")    
    st.image(image)  


