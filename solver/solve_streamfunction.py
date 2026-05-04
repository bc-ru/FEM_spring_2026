from fenics import *
from pathlib import Path


PHYS_SPHERE = 1
PHYS_OUTER = 2
PHYS_AXIS_LEFT = 3
PHYS_AXIS_RIGHT = 4


def load_mesh():
    mesh = Mesh()

    with XDMFFile("meshes/sphere_domain.xdmf") as infile:
        infile.read(mesh)

    mvc = MeshValueCollection("size_t", mesh, 1)
    with XDMFFile("meshes/sphere_facets.xdmf") as infile:
        infile.read(mvc, "name_to_read")

    facets = cpp.mesh.MeshFunctionSizet(mesh, mvc)
    return mesh, facets


def exact_solution_expression(a: float, R: float, u_inf: float, degree: int = 4):
    return Expression(
        "0.5*u_inf*x[1]*x[1]"
        "*(1.0 - pow(a, 3)/pow(x[0]*x[0] + x[1]*x[1], 1.5))"
        "/(1.0 - pow(a, 3)/pow(R, 3))",
        degree=degree,
        a=a,
        R=R,
        u_inf=u_inf,
    )


def solve_problem(a=1.0, R=5.0, u_inf=1.0, p=2):
    mesh, facets = load_mesh()

    V = FunctionSpace(mesh, "CG", p)

    x = SpatialCoordinate(mesh)
    r = x[1]

    psi_outer = Expression(
        "0.5*u_inf*x[1]*x[1]",
        degree=max(2, p + 1),
        u_inf=u_inf,
    )

    bcs = [
        DirichletBC(V, Constant(0.0), facets, PHYS_SPHERE),
        DirichletBC(V, psi_outer, facets, PHYS_OUTER),
        DirichletBC(V, Constant(0.0), facets, PHYS_AXIS_LEFT),
        DirichletBC(V, Constant(0.0), facets, PHYS_AXIS_RIGHT),
    ]

    psi = TrialFunction(V)
    v = TestFunction(V)

    a_form = (dot(grad(psi), grad(v)) / r) * dx
    L_form = Constant(0.0) * v * dx

    psi_h = Function(V)
    solve(
        a_form == L_form,
        psi_h,
        bcs,
        solver_parameters={"linear_solver": "mumps"},
    )

    psi_exact = interpolate(
        exact_solution_expression(a=a, R=R, u_inf=u_inf, degree=max(4, p + 2)),
        V,
    )

    err_L2 = errornorm(psi_exact, psi_h, norm_type="L2")
    err_H1 = errornorm(psi_exact, psi_h, norm_type="H1")

    return mesh, facets, psi_h, psi_exact, err_L2, err_H1


if __name__ == "__main__":
    Path("results").mkdir(exist_ok=True)

    mesh, facets, psi_h, psi_exact, err_L2, err_H1 = solve_problem(
        a=1.0,
        R=5.0,
        u_inf=1.0,
        p=2,
    )

    File("results/psi_h.pvd") << psi_h
    File("results/psi_exact.pvd") << psi_exact

    print("Число ячеек:", mesh.num_cells())
    print("Число узлов:", mesh.num_vertices())
    print("Ошибка L2:", err_L2)
    print("Ошибка H1:", err_H1)