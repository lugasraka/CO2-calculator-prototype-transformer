"""Phase 1 data-access layer.

Separates the CO₂ *model* (formulas in app.py) from the *data* (carbon-intensity
coefficients and bill-of-material masses). All reference data now lives in
sourced, versioned CSVs under ``data/`` instead of hardcoded Python dicts, so it
can be reviewed, cited and swapped for live PLM/EPD feeds in Phase 2.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA_DIR = Path(__file__).parent / "data"

# Canonical component order used throughout the CO₂ calculation engine.
COMPONENT_ORDER = ["core", "copper", "fluid", "insulation", "structural"]


@st.cache_data
def load_material_factors() -> pd.DataFrame:
    """Carbon-intensity factors per material option (kg CO₂e / kg)."""
    return pd.read_csv(
        DATA_DIR / "material_factors.csv",
        dtype={"source_version": "string"},
    )


@st.cache_data
def load_bom() -> pd.DataFrame:
    """Long-format bill-of-material masses per product family (kg)."""
    return pd.read_csv(DATA_DIR / "bom.csv")


@st.cache_data
def load_recovery_factors() -> pd.DataFrame:
    """End-of-life material recovery rates and routes per component."""
    return pd.read_csv(DATA_DIR / "recovery_factors.csv")


def recovery_rates() -> dict:
    """``{component: recovery_rate}`` for the Module 2 EOL calculator."""
    df = load_recovery_factors()
    return {row.component: float(row.recovery_rate) for row in df.itertuples()}


@st.cache_data
def load_energy_params() -> pd.DataFrame:
    """Operating & evaluation assumptions for the Module 1 TCO/carbon model."""
    return pd.read_csv(DATA_DIR / "energy_params.csv")


def energy_params() -> dict:
    """``{parameter: value}`` of the sourced energy/evaluation assumptions."""
    df = load_energy_params()
    return {row.parameter: float(row.value) for row in df.itertuples()}


@st.cache_data
def load_transformer_presets() -> pd.DataFrame:
    """Standard vs. Eco-Efficient transformer CAPEX and loss presets per rating."""
    return pd.read_csv(DATA_DIR / "transformer_presets.csv")


@st.cache_data
def load_factory_energy() -> pd.DataFrame:
    """Per-family factory gas & electricity consumption per manufactured unit.

    Drives the GHG-Protocol Scope 1 (fuel combustion) and Scope 2 (purchased
    electricity) estimates in Module 4. Values are representative Phase 1
    placeholders pending metered MES/EMS data in Phase 2.
    """
    return pd.read_csv(DATA_DIR / "factory_energy.csv")


def factory_energy_by_family() -> dict:
    """``{family: {gas_kwh_per_unit, electricity_kwh_per_unit}}`` for Module 4."""
    df = load_factory_energy()
    families = df["family"].drop_duplicates().tolist()
    return {
        fam: {
            "gas_kwh_per_unit": float(
                df.loc[df["family"] == fam, "natural_gas_kwh_per_unit"].iloc[0]
            ),
            "electricity_kwh_per_unit": float(
                df.loc[df["family"] == fam, "electricity_kwh_per_unit"].iloc[0]
            ),
        }
        for fam in families
    }


def _category(category: str, selectable_only: bool = False) -> pd.DataFrame:
    df = load_material_factors()
    df = df[df["category"] == category]
    if selectable_only:
        df = df[df["selectable"] == 1]
    return df


def factor_details(category: str) -> dict:
    """Ordered ``{selector_label: {ci, low, high, cost_delta}}`` for selectboxes.

    Each selectable Scenario-B option carries its expected carbon intensity, the
    sourced uncertainty bounds and the material cost delta vs. baseline (€/kg).
    """
    df = _category(category, selectable_only=True)
    return {
        row.selector_label: {
            "ci": float(row.kg_co2e_per_kg),
            "low": float(row.uncertainty_low),
            "high": float(row.uncertainty_high),
            "cost_delta": float(row.cost_delta_eur_per_kg),
        }
        for row in df.itertuples()
    }


def baseline_details(category: str) -> dict:
    """Factor detail (CI + uncertainty bounds) of the baseline material."""
    df = _category(category)
    row = df[df["is_baseline"] == 1].iloc[0]
    return {
        "ci": float(row["kg_co2e_per_kg"]),
        "low": float(row["uncertainty_low"]),
        "high": float(row["uncertainty_high"]),
        "cost_delta": 0.0,
    }


def baseline_factor(category: str) -> float:
    """kg CO₂e/kg of the baseline (current-BOM) material in a category."""
    return baseline_details(category)["ci"]


def _parse_kva(kva_class: str) -> float:
    """Numeric kVA rating from labels like ``1000 kVA`` or ``25 MVA``."""
    parts = str(kva_class).replace(",", "").split()
    value = float(parts[0])
    return value * 1_000 if any("MVA" in p.upper() for p in parts[1:]) else value


def kva_by_family() -> dict:
    """``{family: rated kVA}`` parsed from the BOM ``kva_class`` labels."""
    df = load_bom().drop_duplicates("family")
    return {row.family: _parse_kva(row.kva_class) for row in df.itertuples()}


def factor_validity() -> dict:
    """Earliest factor expiry date and the material(s) expiring then.

    Drives the data-freshness banner: sourced factors carry ``valid_to`` dates,
    and gate decisions shouldn't rest on factors past (or near) their validity.
    """
    df = load_material_factors()
    valid_to = pd.to_datetime(df["valid_to"])
    earliest = valid_to.min()
    return {
        "earliest_expiry": earliest.date(),
        "expiring_materials": df.loc[valid_to == earliest, "ref_name"].tolist(),
    }


def bom_by_family() -> dict:
    """``{family: [core, copper, fluid, insulation, structural]}`` masses in kg."""
    df = load_bom()
    families = df["family"].drop_duplicates().tolist()  # preserve file order
    out = {}
    for family in families:
        masses = df[df["family"] == family].set_index("component")["mass_kg"]
        out[family] = [float(masses[component]) for component in COMPONENT_ORDER]
    return out


def reference_table() -> pd.DataFrame:
    """Material carbon-intensity reference for the methodology panel.

    Regenerated from the same source of truth as the calculator, now carrying
    uncertainty ranges and data provenance (Phase 1 additions).
    """
    df = load_material_factors()
    return pd.DataFrame(
        {
            "Material / Option": df["ref_name"],
            "kg CO₂e / kg": df["kg_co2e_per_kg"],
            "Uncertainty (kg CO₂e/kg)": [
                f"{low:g}–{high:g}"
                for low, high in zip(df["uncertainty_low"], df["uncertainty_high"])
            ],
            "vs. Baseline": df["vs_baseline"],
            "Cost Δ vs. baseline (€/kg)": df["cost_delta_eur_per_kg"],
            "Supplier programme": df["supplier_programme"],
            "Source": df["source"] + " " + df["source_version"].fillna(""),
        }
    )
