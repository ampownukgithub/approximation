#!/usr/bin/env python3
"""Demonstrate solving a cubic equation using Cardano's method."""

from __future__ import annotations

import argparse
import cmath
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class CubicSolution:
    a: float
    b: float
    c: float
    d: float
    p: float
    q: float
    discriminant: float
    roots: tuple[complex, complex, complex]


def cbrt(z: complex) -> complex:
    if z == 0:
        return 0j
    return cmath.exp(cmath.log(z) / 3)


def solve_cubic(a: float, b: float, c: float, d: float) -> CubicSolution:
    if a == 0:
        raise ValueError("Coefficient 'a' must be non-zero for a cubic equation.")

    b_n = b / a
    c_n = c / a
    d_n = d / a

    p = c_n - (b_n**2) / 3
    q = (2 * b_n**3) / 27 - (b_n * c_n) / 3 + d_n

    discriminant = (q / 2) ** 2 + (p / 3) ** 3

    sqrt_disc = cmath.sqrt(discriminant)
    u = cbrt(-q / 2 + sqrt_disc)
    v = cbrt(-q / 2 - sqrt_disc)

    omega = complex(-0.5, math.sqrt(3) / 2)

    roots = (
        u + v - b_n / 3,
        u * omega + v * omega.conjugate() - b_n / 3,
        u * omega.conjugate() + v * omega - b_n / 3,
    )

    return CubicSolution(
        a=a,
        b=b,
        c=c,
        d=d,
        p=p,
        q=q,
        discriminant=float(discriminant.real),
        roots=roots,
    )


def format_complex(value: complex, precision: int = 6) -> str:
    real = round(value.real, precision)
    imag = round(value.imag, precision)
    if abs(imag) < 10 ** (-precision):
        return f"{real}"
    sign = "+" if imag >= 0 else "-"
    return f"{real} {sign} {abs(imag)}i"


def render_solution(solution: CubicSolution) -> str:
    lines = [
        "Cubic equation: ax^3 + bx^2 + cx + d = 0",
        f"a={solution.a}, b={solution.b}, c={solution.c}, d={solution.d}",
        "",
        "Normalize and depress the cubic: x = t - b/(3a)",
        f"p = {solution.p:.6f}",
        f"q = {solution.q:.6f}",
        f"discriminant = {solution.discriminant:.6f}",
        "",
        "Roots:",
    ]

    for idx, root in enumerate(solution.roots, start=1):
        lines.append(f"  x{idx} = {format_complex(root)}")

    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Demonstrate solving a cubic equation with Cardano's method.",
    )
    parser.add_argument("a", type=float, nargs="?", default=1.0, help="Coefficient a")
    parser.add_argument("b", type=float, nargs="?", default=-6.0, help="Coefficient b")
    parser.add_argument("c", type=float, nargs="?", default=11.0, help="Coefficient c")
    parser.add_argument("d", type=float, nargs="?", default=-6.0, help="Coefficient d")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    solution = solve_cubic(args.a, args.b, args.c, args.d)
    print(render_solution(solution))


if __name__ == "__main__":
    main()
