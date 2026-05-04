#!/usr/bin/env bash
set -e

docker run --rm -it \
  -p 127.0.0.1:8501:8501 \
  -v "$(pwd)":/workspace \
  -w /workspace \
  cr.yandex/crpdtgu6t719a7cssr10/fenics-env:v0.1