from dolfin import *
import matplotlib.pyplot as plt

# Параметры
n = 20
eps = Constant(0.01)

# Область и сетка
mesh = UnitSquareMesh(n, n)
plot(mesh, title="Сетка")
plt.savefig("gr1.png", format="png", dpi=300)
plt.clf()

# Функциональное пространство
V = FunctionSpace(mesh, "Lagrange", 2)

# Часть границы
class DirichletBoundary(SubDomain):
    def inside(self, x, on_boundary):
        return x[0] + x[1] > 1.0 - DOLFIN_EPS and on_boundary

# Краевые условия Дирихле
bc = DirichletBC(V, Constant(0.0), DirichletBoundary())

# Вариационная задача
u = TrialFunction(V)
v = TestFunction(V)
f = interpolate(Expression("x[0]", degree=2), V)
a = eps * inner(grad(u), grad(v)) * dx + u * v * dx
L = f * v * dx

# Численное решение
u_sol = Function(V)
solve(a == L, u_sol, bc,
      solver_parameters={'linear_solver': 'mumps'})

# Амплитуда решения
print("max|u(x)| = ", u_sol.vector().norm('linf'))

# График
plot(u_sol, title="Решение")
plt.savefig("gr2.png", format="png", dpi=300)
plt.clf()
