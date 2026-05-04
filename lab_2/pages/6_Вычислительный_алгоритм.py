import streamlit as st

from ui_helpers import code_block

st.title("6. Вычислительный алгоритм")

st.subheader("1. Генерация геометрии в Gmsh")
code_block(
    "Физические метки границ и области",
    """
Point(1) = {-R, 0, 0, h_outer};
Point(2) = { 0, R, 0, h_outer};
Point(3) = { R, 0, 0, h_outer};
...
Physical Curve(1) = {4,5};   // sphere
Physical Curve(2) = {1,2};   // outer
Physical Curve(3) = {6};     // axis left
Physical Curve(4) = {3};     // axis right
Physical Surface(10) = {10}; // domain
    """,
    language="c",
)

st.subheader("2. Конвертация .msh → XDMF")
code_block(
    "Склейка блоков ячеек и меток из Gmsh 4.x",
    """
for cell_block, data_block in zip(mesh.cells, mesh.cell_data[data_name]):
    if cell_block.type == cell_type:
        cells.append(cell_block.data)
        cell_data.append(np.asarray(data_block, dtype=np.int32))

cells = np.vstack(cells)
cell_data = np.concatenate(cell_data)
    """,
)

st.subheader("3. Конечно-элементная постановка в FEniCS")
code_block(
    "Билинейная форма и граничные условия",
    """
V = FunctionSpace(mesh, "CG", p)
r = SpatialCoordinate(mesh)[1]

bcs = [
    DirichletBC(V, Constant(0.0), facets, PHYS_SPHERE),
    DirichletBC(V, psi_outer, facets, PHYS_OUTER),
    DirichletBC(V, Constant(0.0), facets, PHYS_AXIS_LEFT),
    DirichletBC(V, Constant(0.0), facets, PHYS_AXIS_RIGHT),
]

a_form = (dot(grad(psi), grad(v)) / r) * dx
solve(a_form == L_form, psi_h, bcs)
    """,
)

st.subheader("4. Постпроцессинг")
code_block(
    "Вычисление касательной скорости на поверхности шара",
    """
u_r_h = project(psi_h.dx(0) / r_safe, Q)
u_z_h = project(-psi_h.dx(1) / r_safe, Q)

tau_z = -r / rho
tau_r = z / rho
u_tau_h = tau_z * uz + tau_r * ur
u_tau_exact = 3.0 * u_inf / (2.0 * (1.0 - a**3 / R**3)) * np.sin(theta)
    """,
)

st.subheader("5. Batch-расчёты")
code_block(
    "Цикл по сеткам, степеням p и значениям R",
    """
MESHES = {"coarse": 0.5, "medium": 0.25, "fine": 0.125}
P_VALUES = [1, 2, 3]
R_VALUES = [3.0, 5.0, 10.0]

for mesh_name, h in MESHES.items():
    generate_geo(A, 5.0, h, geo_path)
    ...
    for p in P_VALUES:
        run_case(..., p=p)
    """,
)

st.divider()

st.subheader("Используемые имена переменных")
code_block("Dockerfile",
        """
    FROM ghcr.io/scientificcomputing/fenics:2025-10-09

    WORKDIR /tmp

    RUN export DEBIAN_FRONTEND=noninteractive && \
        apt-get -qq update && \
        apt-get -yq --with-new-pkgs -o Dpkg::Options::="--force-confold" upgrade && \
        apt-get -y install \
        libglu1 \
        libxcursor-dev \
        libxft2 \
        libxinerama1 \
        libfltk1.3-dev \
        libfreetype6-dev \
        libgl1-mesa-dev \
        libocct-foundation-dev \
        libocct-data-exchange-dev && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

    COPY gmsh-4.15.2-Linux64/ /opt/gmsh/

    RUN ln -s /opt/gmsh/bin/gmsh /usr/local/bin/gmsh && \
        chmod +x /opt/gmsh/bin/gmsh


    RUN python3 -m pip install --no-cache-dir \
        meshio \
        streamlit \
        numpy \
        matplotlib \
        pandas \
        h5py

    WORKDIR /workspace
        """,
)
