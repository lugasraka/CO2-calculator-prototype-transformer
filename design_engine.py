"""Deterministic portfolio calculation and constrained design recommendation.

The calculation engine is shared by Module 3's manual simulation and design
advisor so recommendations always use the same carbon, uncertainty, and cost
formulas as the displayed portfolio results.
"""

from itertools import product
from typing import Sequence

import pandas as pd


ChoiceDetails = dict[str, float]
MaterialOptions = dict[str, ChoiceDetails]


def calculate_portfolio_design(
    *,
    choices: dict[str, str],
    option_details: dict[str, MaterialOptions],
    volumes: Sequence[float],
    bom: dict[str, list[float]],
    kva_by_family: dict[str, float],
    baseline: dict[str, ChoiceDetails],
    insulation_baseline: ChoiceDetails,
    structural_baseline: ChoiceDetails,
) -> dict:
    """Calculate Module 3 outputs for one material-design combination."""
    core_detail = option_details["core"][choices["core"]]
    fluid_detail = option_details["fluid"][choices["fluid"]]
    copper_detail = option_details["copper"][choices["copper"]]
    core_baseline = baseline["core"]
    fluid_baseline = baseline["fluid"]
    copper_baseline = baseline["copper"]

    rows = []
    lever_costs = {"core": 0.0, "fluid": 0.0, "copper": 0.0}
    for (family, masses), volume in zip(bom.items(), volumes):
        core_mass, copper_mass, fluid_mass, insulation_mass, structural_mass = masses

        baseline_unit = (
            core_mass * core_baseline["ci"]
            + copper_mass * copper_baseline["ci"]
            + fluid_mass * fluid_baseline["ci"]
            + insulation_mass * insulation_baseline["ci"]
            + structural_mass * structural_baseline["ci"]
        ) / 1_000
        design_unit = (
            core_mass * core_detail["ci"]
            + copper_mass * copper_detail["ci"]
            + fluid_mass * fluid_detail["ci"]
            + insulation_mass * insulation_baseline["ci"]
            + structural_mass * structural_baseline["ci"]
        ) / 1_000

        baseline_low = (
            core_mass * core_baseline["low"]
            + copper_mass * copper_baseline["low"]
            + fluid_mass * fluid_baseline["low"]
            + insulation_mass * insulation_baseline["low"]
            + structural_mass * structural_baseline["low"]
        ) / 1_000
        baseline_high = (
            core_mass * core_baseline["high"]
            + copper_mass * copper_baseline["high"]
            + fluid_mass * fluid_baseline["high"]
            + insulation_mass * insulation_baseline["high"]
            + structural_mass * structural_baseline["high"]
        ) / 1_000
        design_low = (
            core_mass * core_detail["low"]
            + copper_mass * copper_detail["low"]
            + fluid_mass * fluid_detail["low"]
            + insulation_mass * insulation_baseline["low"]
            + structural_mass * structural_baseline["low"]
        ) / 1_000
        design_high = (
            core_mass * core_detail["high"]
            + copper_mass * copper_detail["high"]
            + fluid_mass * fluid_detail["high"]
            + insulation_mass * insulation_baseline["high"]
            + structural_mass * structural_baseline["high"]
        ) / 1_000

        core_reduction = core_mass * (core_baseline["ci"] - core_detail["ci"]) / 1_000
        fluid_reduction = (
            fluid_mass * (fluid_baseline["ci"] - fluid_detail["ci"]) / 1_000
        )
        copper_reduction = (
            copper_mass * (copper_baseline["ci"] - copper_detail["ci"]) / 1_000
        )

        premium_per_unit = (
            core_mass * core_detail["cost_delta"]
            + copper_mass * copper_detail["cost_delta"]
            + fluid_mass * fluid_detail["cost_delta"]
        )
        lever_costs["core"] += core_mass * core_detail["cost_delta"] * volume
        lever_costs["fluid"] += fluid_mass * fluid_detail["cost_delta"] * volume
        lever_costs["copper"] += (
            copper_mass * copper_detail["cost_delta"] * volume
        )

        kva = kva_by_family[family]
        rows.append(
            {
                "Product Family": family,
                "Units/yr": volume,
                "Baseline CO₂/unit (t)": round(baseline_unit, 1),
                "Eco-Efficient CO₂/unit (t)": round(design_unit, 1),
                "Reduction/unit (t)": round(baseline_unit - design_unit, 1),
                "Baseline kg CO₂e/kVA": round(baseline_unit * 1_000 / kva, 2),
                "Eco kg CO₂e/kVA": round(design_unit * 1_000 / kva, 2),
                "Portfolio Baseline (kt/yr)": round(
                    baseline_unit * volume / 1_000, 2
                ),
                "Portfolio Eco-Efficient (kt/yr)": round(
                    design_unit * volume / 1_000, 2
                ),
                "Portfolio Saving (kt/yr)": round(
                    (baseline_unit - design_unit) * volume / 1_000, 2
                ),
                "Baseline low (kt/yr)": round(
                    baseline_low * volume / 1_000, 2
                ),
                "Baseline high (kt/yr)": round(
                    baseline_high * volume / 1_000, 2
                ),
                "Eco low (kt/yr)": round(design_low * volume / 1_000, 2),
                "Eco high (kt/yr)": round(design_high * volume / 1_000, 2),
                "Green premium (k€/yr)": round(
                    premium_per_unit * volume / 1_000, 1
                ),
                "Δ Core (kt/yr)": round(
                    core_reduction * volume / 1_000, 3
                ),
                "Δ Fluid (kt/yr)": round(
                    fluid_reduction * volume / 1_000, 3
                ),
                "Δ Copper (kt/yr)": round(
                    copper_reduction * volume / 1_000, 3
                ),
            }
        )

    results = pd.DataFrame(rows)
    total_baseline = float(results["Portfolio Baseline (kt/yr)"].sum())
    total_design = float(results["Portfolio Eco-Efficient (kt/yr)"].sum())
    total_saving = total_baseline - total_design
    reduction_pct = (
        total_saving / total_baseline * 100 if total_baseline > 0 else 0.0
    )
    premium_eur = float(results["Green premium (k€/yr)"].sum() * 1_000)
    blended_cost = (
        premium_eur / (total_saving * 1_000) if total_saving > 0 else None
    )

    return {
        "df": results,
        "kpis": {
            "total_base": total_baseline,
            "total_eco": total_design,
            "total_saving": total_saving,
            "pct_saving": reduction_pct,
        },
        "uncertainty": {
            "base_low": float(results["Baseline low (kt/yr)"].sum()),
            "base_high": float(results["Baseline high (kt/yr)"].sum()),
            "eco_low": float(results["Eco low (kt/yr)"].sum()),
            "eco_high": float(results["Eco high (kt/yr)"].sum()),
        },
        "cost": {
            "premium_eur": premium_eur,
            "blended_eur_per_t": blended_cost,
            "lever_costs": lever_costs,
        },
    }


def evaluate_constrained_designs(
    *,
    option_details: dict[str, MaterialOptions],
    approved_materials: dict[str, set[str]],
    min_reduction_pct: float,
    max_premium_k_eur: float,
    volumes: Sequence[float],
    bom: dict[str, list[float]],
    kva_by_family: dict[str, float],
    baseline: dict[str, ChoiceDetails],
    insulation_baseline: ChoiceDetails,
    structural_baseline: ChoiceDetails,
) -> pd.DataFrame:
    """Evaluate and rank every material combination against hard constraints."""
    candidate_rows = []
    option_combinations = product(
        option_details["core"],
        option_details["fluid"],
        option_details["copper"],
    )

    for core_choice, fluid_choice, copper_choice in option_combinations:
        choices = {
            "core": core_choice,
            "fluid": fluid_choice,
            "copper": copper_choice,
        }
        simulation = calculate_portfolio_design(
            choices=choices,
            option_details=option_details,
            volumes=volumes,
            bom=bom,
            kva_by_family=kva_by_family,
            baseline=baseline,
            insulation_baseline=insulation_baseline,
            structural_baseline=structural_baseline,
        )
        kpis = simulation["kpis"]
        uncertainty = simulation["uncertainty"]
        premium_k_eur = simulation["cost"]["premium_eur"] / 1_000

        material_failures = [
            category
            for category, choice in choices.items()
            if choice not in approved_materials[category]
        ]
        passes_carbon = kpis["pct_saving"] >= min_reduction_pct
        passes_premium = premium_k_eur <= max_premium_k_eur
        passes_materials = not material_failures

        reasons = []
        if not passes_carbon:
            reasons.append(
                f"CO₂ reduction {kpis['pct_saving']:.1f}% < "
                f"{min_reduction_pct:.1f}% minimum"
            )
        if not passes_premium:
            reasons.append(
                f"premium {premium_k_eur:.1f} kEUR/yr > "
                f"{max_premium_k_eur:.1f} kEUR/yr cap"
            )
        for category in material_failures:
            reasons.append(f"{category} option is not approved")

        failed_constraints = (
            int(not passes_carbon)
            + int(not passes_premium)
            + len(material_failures)
        )
        candidate_rows.append(
            {
                "Core": core_choice,
                "Fluid": fluid_choice,
                "Copper": copper_choice,
                "Portfolio carbon (kt/yr)": kpis["total_eco"],
                "CO₂ reduction (%)": kpis["pct_saving"],
                "Annual green premium (kEUR/yr)": premium_k_eur,
                "Abatement cost (EUR/tCO₂e)": simulation["cost"][
                    "blended_eur_per_t"
                ],
                "Expected low (kt/yr)": uncertainty["eco_low"],
                "Expected high (kt/yr)": uncertainty["eco_high"],
                "Passes CO₂ target?": passes_carbon,
                "Passes premium cap?": passes_premium,
                "Uses approved materials?": passes_materials,
                "Feasible?": failed_constraints == 0,
                "Failed constraints": failed_constraints,
                "CO₂ target shortfall (pp)": max(
                    0.0, min_reduction_pct - kpis["pct_saving"]
                ),
                "Premium cap excess (kEUR/yr)": max(
                    0.0, premium_k_eur - max_premium_k_eur
                ),
                "Exclusion reasons": "; ".join(reasons) if reasons else "—",
            }
        )

    candidates = pd.DataFrame(candidate_rows)
    return candidates.sort_values(
        [
            "Feasible?",
            "Failed constraints",
            "Annual green premium (kEUR/yr)",
            "Portfolio carbon (kt/yr)",
        ],
        ascending=[False, True, True, True],
        ignore_index=True,
    )
