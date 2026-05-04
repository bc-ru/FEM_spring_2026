from pathlib import Path


def generate_geo(a, R, h, out_path: Path):
    template = Path("meshes/sphere_template.geo").read_text()

    header = f"""
a = {a};
R = {R};

h_outer = {h};
h_inner = {h * 0.3};
"""

    geo = header + "\n" + template

    out_path.write_text(geo)