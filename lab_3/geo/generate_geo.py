#!/usr/bin/env python3
"""Generate a Gmsh .geo file from a simple template."""
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--L", type=float, default=4.0)
    parser.add_argument("--H", type=float, default=1.0)
    parser.add_argument("--l", type=float, default=1.0)
    parser.add_argument("--h", type=float, default=1.0)
    parser.add_argument("--lc", type=float, default=0.08)
    parser.add_argument("--lc-step", type=float, default=None)
    parser.add_argument("--template", default="geo/step_channel.geo.tpl")
    parser.add_argument("--out", default="meshes/step_channel.geo")
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    template_path = root / args.template if not Path(args.template).is_absolute() else Path(args.template)
    out_path = root / args.out if not Path(args.out).is_absolute() else Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    lc_step = args.lc_step if args.lc_step is not None else args.lc / 2.0

    text = template_path.read_text(encoding="utf-8").format(
        L=args.L,
        H=args.H,
        l=args.l,
        h=args.h,
        lc=args.lc,
        lc_step=lc_step,
    )
    out_path.write_text(text, encoding="utf-8")
    print(out_path)


if __name__ == "__main__":
    main()
