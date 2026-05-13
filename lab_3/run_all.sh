#!/usr/bin/env bash

python3 geo/generate_geo.py \
  --L 4 --H 1 --l 1 --h 1 \
  --lc 0.08 \
  --out meshes/base/step_channel.geo

gmsh -2 meshes/base/step_channel.geo -format msh2 -o meshes/base/step_channel.msh

python3 solver/mesh_convert.py \
  meshes/base/step_channel.msh \
  meshes/base/step_channel

python3 solver/run_case.py \
  --mesh-prefix meshes/base/step_channel \
  --out results/base/p1_Gamma-2 \
  --L 4 --H 1 --l 1 --h 1 \
  --Gamma -2 \
  --degree 1 \
  --alpha 0.5

python3 experiments/run_base_meshes.py

python3 experiments/run_poly_degree.py

python3 experiments/run_gamma_sweep.py

python3 experiments/run_height_sweep.py
