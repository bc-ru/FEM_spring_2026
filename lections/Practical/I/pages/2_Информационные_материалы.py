import streamlit as st

menu = st.sidebar.radio('***',
    (
    "Папка в облаке",
    "Основная литература",
    "Дополнительная литература",
    )
)

if menu == "Папка в облаке":
    r"""
	##### Папка в облаке

	* Содержание
		- Books
		- Lectures
		- Practical
		- Projects
		- PyStr
	* Электронные книги
	* Конспекты лекций (streamlit)
	* Материалы к практическим занятиям
	* Материалы проектных групп
	* Программа PyStr

	"""

    st.link_button(":open_file_folder: Переход к папке", "https://disk.yandex.ru/d/MhX_qdTg_e0mZQ")


if menu == "Основная литература":
    r"""
	##### Основная литература

	- Р.З. Даутов, М.М. Карчевский. Введение в теорию метода конечных элементов. Казань, Казанский федеральный университет, 2011

	- Mats G. Larson, Fredrik Bengzon. The Finite Element Method: Theory, Implementation, and Applications. Springer, 2013


	- Hans Petter Langtangen, Anders Logg. Solving PDEs in Python: The FEniCS Tutorial I. Springer, 2016
	"""

if menu == "Дополнительная литература":

	r"""
	##### Дополнительная литература

	- В.Б. Андреев. Лекции по методу конечных элементов. М., МАКС Пресс, 2010

	- Вычислительные технологии. Профессиональный уровень. Под ред. П.Н. Вабищевича. М., ЛЕНАНД, 2016

	- Вычислительные технологии. Базовый уровень. Под ред. П.Н. Вабищевича. М., ЛЕНАНД, 2016

	- Pascal Jean Frey, Paul-Louis George. Mesh generation application to finite elements. ISTE Ltd and John Wiley, 2008

	- Robert Johansson. Numerical Python: Scientific Computing and Data Science Applications with Numpy, SciPy and Matplotlib. Apress, 2019

	- Hans Petter Langtangen, Kent-Andre Mardal. Introduction to Numerical Methods for Variational Problems. Springer, 2019

	- Mark S. Gockenbach. Understanding and Implementing the Finite Element Method. SIAM, 2006

	- Sujay Raghavendra. Beginner’s Guide to Streamlit with Python: Build Web-Based Data and Machine Learning Applications. Apress, 2023

	"""
