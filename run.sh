#!/usr/bin/env bash
set -e

docker run --rm -it \
  -p 127.0.0.1:8501:8501 \
  -v "$(pwd)":/workspace \
  -w /workspace \
  ghcr.io/bc-ru/fenics-gmsh-env:stable