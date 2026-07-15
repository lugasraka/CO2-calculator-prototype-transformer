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


def _category(category: str, selectable_only: bool = False) -> pd.DataFrame:
    df = load_material_factors()
    df = df[df["category"] == category]
    if selectable_only:
        df = df[df["selectable"] == 1]
    return df


def selector_options(category: str) -> dict:
    """Ordered ``{selector_label: kg_co2e_per_kg}`` for a Scenario-B selectbox."""
    df = _category(category, selectable_only=True)
    return {row.selector_label: float(row.kg_co2e_per_kg) for row in df.itertuples()}


def baseline_factor(category: str) -> float:
    """kg CO₂e/kg of the baseline (current-BOM) material in a category."""
    df = _category(category)
    return float(df[df["is_baseline"] == 1].iloc[0]["kg_co2e_per_kg"])


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
            "Supplier programme": df["supplier_programme"],
            "Source": df["source"] + " " + df["source_version"].fillna(""),
        }
    )
