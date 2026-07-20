"""Monte Carlo uncertainty propagation over portfolio CO₂ calculations.

Replaces the deterministic point-estimate uncertainty bounds (all factors
simultaneously at low or high) with probabilistic confidence intervals.
Each material's carbon intensity is sampled from a triangular distribution
parameterised by the sourced ``uncertainty_low``, ``kg_co2e_per_kg`` (mode)
and ``uncertainty_high`` values in ``data/material_factors.csv``.

The engine is pure NumPy — no Streamlit dependency — so it can be unit-tested
and reused by the design advisor in future phases.
"""

from typing import Sequence

import numpy as np

ChoiceDetails = dict[str, float]
MaterialOptions = dict[str, ChoiceDetails]

DEFAULT_ITERATIONS = 10_000
PERCENTILES = (10, 50, 90)


def _sample_ci(
    low: float, mode: float, high: float, n: int, rng: np.random.Generator
) -> np.ndarray:
    if low == high:
        return np.full(n, mode)
    return rng.triangular(low, mode, high, size=n)


def run_monte_carlo(
    *,
    choices: dict[str, str],
    option_details: dict[str, MaterialOptions],
    volumes: Sequence[float],
    bom: dict[str, list[float]],
    kva_by_family: dict[str, float],
    baseline: dict[str, ChoiceDetails],
    insulation_baseline: ChoiceDetails,
    structural_baseline: ChoiceDetails,
    n_iterations: int = DEFAULT_ITERATIONS,
    seed: int | None = None,
) -> dict:
    rng = np.random.default_rng(seed)

    core_detail = option_details["core"][choices["core"]]
    fluid_detail = option_details["fluid"][choices["fluid"]]
    copper_detail = option_details["copper"][choices["copper"]]
    core_base = baseline["core"]
    fluid_base = baseline["fluid"]
    copper_base = baseline["copper"]

    n = n_iterations

    core_base_s = _sample_ci(
        core_base["low"], core_base["ci"], core_base["high"], n, rng
    )
    copper_base_s = _sample_ci(
        copper_base["low"], copper_base["ci"], copper_base["high"], n, rng
    )
    fluid_base_s = _sample_ci(
        fluid_base["low"], fluid_base["ci"], fluid_base["high"], n, rng
    )
    insul_base_s = _sample_ci(
        insulation_baseline["low"],
        insulation_baseline["ci"],
        insulation_baseline["high"],
        n,
        rng,
    )
    struct_base_s = _sample_ci(
        structural_baseline["low"],
        structural_baseline["ci"],
        structural_baseline["high"],
        n,
        rng,
    )

    core_des_s = _sample_ci(
        core_detail["low"], core_detail["ci"], core_detail["high"], n, rng
    )
    copper_des_s = _sample_ci(
        copper_detail["low"], copper_detail["ci"], copper_detail["high"], n, rng
    )
    fluid_des_s = _sample_ci(
        fluid_detail["low"], fluid_detail["ci"], fluid_detail["high"], n, rng
    )

    portfolio_base = np.zeros(n)
    portfolio_eco = np.zeros(n)
    lever_core = np.zeros(n)
    lever_fluid = np.zeros(n)
    lever_copper = np.zeros(n)

    family_base = {}
    family_eco = {}

    for (family, masses), volume in zip(bom.items(), volumes):
        core_m, copper_m, fluid_m, insul_m, struct_m = masses

        base_unit = (
            core_m * core_base_s
            + copper_m * copper_base_s
            + fluid_m * fluid_base_s
            + insul_m * insul_base_s
            + struct_m * struct_base_s
        ) / 1_000

        eco_unit = (
            core_m * core_des_s
            + copper_m * copper_des_s
            + fluid_m * fluid_des_s
            + insul_m * insul_base_s
            + struct_m * struct_base_s
        ) / 1_000

        base_kt = base_unit * volume / 1_000
        eco_kt = eco_unit * volume / 1_000

        portfolio_base += base_kt
        portfolio_eco += eco_kt

        family_base[family] = base_kt
        family_eco[family] = eco_kt

        lever_core += core_m * (core_base_s - core_des_s) / 1_000 * volume / 1_000
        lever_fluid += fluid_m * (fluid_base_s - fluid_des_s) / 1_000 * volume / 1_000
        lever_copper += (
            copper_m * (copper_base_s - copper_des_s) / 1_000 * volume / 1_000
        )

    portfolio_saving = portfolio_base - portfolio_eco
    reduction_pct = np.where(
        portfolio_base > 0, portfolio_saving / portfolio_base * 100, 0.0
    )

    def _pct(arr: np.ndarray) -> dict:
        vals = np.percentile(arr, PERCENTILES)
        return {"p10": float(vals[0]), "p50": float(vals[1]), "p90": float(vals[2])}

    families_out = {}
    for family in bom:
        families_out[family] = {
            "baseline": _pct(family_base[family]),
            "eco": _pct(family_eco[family]),
            "saving": _pct(family_base[family] - family_eco[family]),
        }

    return {
        "portfolio": {
            "baseline": _pct(portfolio_base),
            "eco": _pct(portfolio_eco),
            "saving": _pct(portfolio_saving),
            "reduction_pct": _pct(reduction_pct),
        },
        "families": families_out,
        "levers": {
            "core": _pct(lever_core),
            "fluid": _pct(lever_fluid),
            "copper": _pct(lever_copper),
        },
        "distributions": {
            "portfolio_base": portfolio_base,
            "portfolio_eco": portfolio_eco,
            "portfolio_saving": portfolio_saving,
            "reduction_pct": reduction_pct,
            "lever_core": lever_core,
            "lever_fluid": lever_fluid,
            "lever_copper": lever_copper,
        },
        "n_iterations": n_iterations,
    }
