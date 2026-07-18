from datetime import date

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import data_layer as dl
import scenario_store as store

# Configure the app's layout and title
st.set_page_config(page_title="Transformer Decarbonization Manager", layout="wide")

# Warn when sourced carbon factors are within this many days of their valid_to date.
FRESHNESS_WARN_DAYS = 180


def warn_factor_freshness() -> None:
    """Banner when sourced carbon factors approach or pass their validity date."""
    validity = dl.factor_validity()
    expiry = validity["earliest_expiry"]
    days_left = (expiry - date.today()).days
    materials = ", ".join(validity["expiring_materials"])
    if days_left < 0:
        st.error(
            f"⚠️ Carbon-intensity factors **expired {-days_left} days ago** "
            f"(valid to {expiry:%d %b %Y}: {materials}). Treat results as indicative "
            "until `data/material_factors.csv` is refreshed."
        )
    elif days_left <= FRESHNESS_WARN_DAYS:
        st.warning(
            f"⚠️ Carbon-intensity factors expire in **{days_left} days** "
            f"(valid to {expiry:%d %b %Y}: {materials}). Plan a data refresh before "
            "the next gate review."
        )


def saved_run_decision_metrics(run: pd.Series) -> dict:
    """Return the saved-run measures needed for a design-gate comparison."""
    results = store.get_run_results(int(run["run_id"]))

    def total_for(prefix: str) -> float:
        column = next((name for name in results.columns if name.startswith(prefix)), None)
        if column is None:
            return 0.0
        return float(pd.to_numeric(results[column], errors="coerce").fillna(0).sum())

    return {
        "portfolio_eco": float(run["total_eco"]),
        "green_premium_k_eur": total_for("Green premium"),
        "eco_low": total_for("Eco low"),
        "eco_high": total_for("Eco high"),
    }


st.sidebar.title("Decarbonization Workflow")
module = st.sidebar.radio(
    "Select Module:",
    [
        "1. TCO & Carbon ROI",
        "2. Circularity & EOL Planner",
        "3. Portfolio CO₂ Simulator ★",
        "4. GHG Scope 1/2/3 Report",
        "5. About & Source Code",
    ],
)

if module == "1. TCO & Carbon ROI":
    st.header("Total Cost of Ownership (TCO) & Carbon ROI Calculator")
    st.markdown(
        "Evaluate the lifetime **cost and carbon** payback of high-efficiency transformers. "
        "Covers **use-phase energy losses (B1–B6)** — the operational footprint outside Modules 2 & 3."
    )

    params = dl.energy_params()
    presets = dl.load_transformer_presets()
    std_p = presets[presets["design"] == "Standard"].iloc[0]
    eco_p = presets[presets["design"] == "Eco-Efficient"].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Standard {int(std_p.rating_kva)} kVA Transformer")
        std_capex = st.number_input(
            "Standard CAPEX (€)", value=float(std_p.capex_eur), format="%.0f"
        )
        std_no_load = st.number_input(
            "Standard No-Load Loss (W)", value=float(std_p.no_load_w), format="%.0f"
        )
        std_load = st.number_input(
            "Standard Load Loss (W)", value=float(std_p.load_w), format="%.0f"
        )
    with col2:
        st.subheader(f"Eco-Efficient {int(eco_p.rating_kva)} kVA Transformer")
        eco_capex = st.number_input(
            "Eco-Efficient CAPEX (€)", value=float(eco_p.capex_eur), format="%.0f"
        )
        eco_no_load = st.number_input(
            "Eco-Efficient No-Load Loss (W)",
            value=float(eco_p.no_load_w),
            format="%.0f",
        )
        eco_load = st.number_input(
            "Eco-Efficient Load Loss (W)", value=float(eco_p.load_w), format="%.0f"
        )

    st.markdown("---")
    st.markdown("#### Operating & Evaluation Assumptions")
    st.caption("Defaults sourced from `data/energy_params.csv` — override as needed.")
    a1, a2, a3 = st.columns(3)
    with a1:
        energy_price = st.number_input(
            "Energy price (€/kWh)",
            value=params["energy_price"],
            step=0.01,
            format="%.3f",
        )
        loading = (
            st.slider(
                "Average loading (%)", 0, 100, int(params["loading_factor"] * 100)
            )
            / 100
        )
    with a2:
        grid_ci = st.number_input(
            "Grid carbon intensity (kg CO₂e/kWh)",
            value=params["grid_carbon_intensity"],
            step=0.01,
            format="%.3f",
        )
        hours = st.number_input(
            "Operating hours (h/yr)",
            value=params["operating_hours"],
            step=100.0,
            format="%.0f",
        )
    with a3:
        eval_years = int(
            st.number_input(
                "Evaluation period (years)",
                min_value=1,
                value=int(params["eval_years"]),
                step=1,
            )
        )
        discount_rate = (
            st.number_input(
                "Discount rate (%)",
                value=params["discount_rate"] * 100,
                step=0.5,
                format="%.1f",
            )
            / 100
        )

    def evaluate(capex: float, no_load_w: float, load_w: float) -> dict:
        # Load losses scale with the square of loading; no-load losses are constant.
        annual_kwh = (no_load_w + load_w * loading**2) * hours / 1_000
        annual_cost = annual_kwh * energy_price
        annual_co2_t = annual_kwh * grid_ci / 1_000
        npv_energy = sum(
            annual_cost / (1 + discount_rate) ** y for y in range(1, eval_years + 1)
        )
        return {
            "capex": capex,
            "annual_kwh": annual_kwh,
            "annual_cost": annual_cost,
            "annual_co2_t": annual_co2_t,
            "npv_energy": npv_energy,
            "tco": capex + npv_energy,
            "lifetime_co2_t": annual_co2_t * eval_years,
        }

    std = evaluate(std_capex, std_no_load, std_load)
    eco = evaluate(eco_capex, eco_no_load, eco_load)

    cost_saving = std["tco"] - eco["tco"]
    co2_saving = std["lifetime_co2_t"] - eco["lifetime_co2_t"]
    extra_capex = eco["capex"] - std["capex"]
    annual_cost_saving = std["annual_cost"] - eco["annual_cost"]
    payback = (
        extra_capex / annual_cost_saving if annual_cost_saving > 0 else float("inf")
    )

    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric(
        f"Lifetime cost saving ({eval_years} yr)",
        f"€{cost_saving:,.0f}",
        delta=f"€{extra_capex:,.0f} extra CAPEX",
    )
    m2.metric(
        f"Lifetime CO₂ saving ({eval_years} yr)",
        f"{co2_saving:,.1f} t",
        delta="use-phase (B1–B6)",
    )
    m3.metric(
        "Payback period",
        "n/a" if payback == float("inf") else f"{payback:,.1f} yr",
        delta="on efficiency premium",
    )

    comp = pd.DataFrame(
        {
            "Metric": [
                "CAPEX (€)",
                "Annual loss energy (kWh)",
                "Annual energy cost (€)",
                "Annual CO₂ (t)",
                f"NPV energy cost @ {discount_rate:.0%} (€)",
                f"{eval_years}-yr TCO (€)",
                "Lifetime CO₂ (t)",
            ],
            "Standard": [
                std["capex"],
                std["annual_kwh"],
                std["annual_cost"],
                std["annual_co2_t"],
                std["npv_energy"],
                std["tco"],
                std["lifetime_co2_t"],
            ],
            "Eco-Efficient": [
                eco["capex"],
                eco["annual_kwh"],
                eco["annual_cost"],
                eco["annual_co2_t"],
                eco["npv_energy"],
                eco["tco"],
                eco["lifetime_co2_t"],
            ],
        }
    )
    comp["Standard"] = comp["Standard"].round(1)
    comp["Eco-Efficient"] = comp["Eco-Efficient"].round(1)
    st.dataframe(comp, use_container_width=True, hide_index=True)

    # Cumulative discounted cost-of-ownership crossover.
    years = list(range(0, eval_years + 1))

    def cumulative(capex: float, annual_cost: float) -> list:
        return [
            capex + sum(annual_cost / (1 + discount_rate) ** y for y in range(1, k + 1))
            for k in years
        ]

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=years,
            y=cumulative(std["capex"], std["annual_cost"]),
            name="Standard",
            mode="lines",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=years,
            y=cumulative(eco["capex"], eco["annual_cost"]),
            name="Eco-Efficient",
            mode="lines",
        )
    )
    fig.update_layout(
        title="Cumulative discounted cost of ownership",
        xaxis_title="Year",
        yaxis_title="Cumulative cost (€)",
    )
    st.plotly_chart(fig, use_container_width=True)

    if cost_saving > 0:
        st.success(
            f"**Result:** A €{extra_capex:,.0f} efficiency premium returns **€{cost_saving:,.0f}** over "
            f"{eval_years} years (payback ≈ {payback:,.1f} yr) and avoids **{co2_saving:,.1f} t CO₂e** "
            "of use-phase emissions."
        )
    else:
        st.warning(
            "Under these assumptions the standard design has the lower total cost of ownership."
        )

elif module == "2. Circularity & EOL Planner":
    st.header("♻️ Circularity & End-of-Life Management")
    st.markdown(
        "Covers lifecycle stages **C1–C4** — the end-of-life phase deferred by the Portfolio CO₂ Simulator (Module 3). "
        "Addresses mid-life asset intervention and secure decommissioning to maximise material recovery and minimise waste."
    )
    st.caption(
        "Lifecycle scope: C1 Deconstruction · C2 Transport · C3 Waste processing · C4 Disposal — plus Module D recycling credits"
    )
    warn_factor_freshness()
    st.divider()

    # ── REFERENCE DATA (BOM masses, baseline carbon intensity, recovery rates) ──
    BOM = dl.bom_by_family()
    baseline_ci = {c: dl.baseline_factor(c) for c in dl.COMPONENT_ORDER}
    rec_rates = dl.recovery_rates()

    family = st.selectbox("Transformer class", list(BOM.keys()))
    masses = dict(zip(dl.COMPONENT_ORDER, BOM[family]))

    intervention = st.radio(
        "Select asset lifecycle phase:",
        ["Mid-Life Extension (C0 intervention)", "End-of-Life Decommissioning (C1–C4)"],
    )

    if intervention == "Mid-Life Extension (C0 intervention)":
        # Retrofill defers manufacturing a replacement unit → avoids its full A1–A3 embodied carbon.
        embodied_unit = (
            sum(masses[c] * baseline_ci[c] for c in dl.COMPONENT_ORDER) / 1_000
        )  # tonnes CO₂e

        col_in, col_out = st.columns([1, 2])
        with col_in:
            installed_base = st.number_input(
                "Installed base of this class (units)", min_value=0, value=200, step=10
            )
            retrofill_pct = st.slider(
                "Share undergoing Retrofill instead of replacement (%)", 0, 100, 10
            )
        units_retrofilled = installed_base * retrofill_pct / 100
        fleet_avoided_kt = embodied_unit * units_retrofilled / 1_000

        with col_out:
            m1, m2, m3 = st.columns(3)
            m1.metric(
                "Avoided CO₂ / retrofill",
                f"{embodied_unit:,.1f} t",
                delta="deferred new unit (A1–A3)",
            )
            m2.metric(
                "Units retrofilled",
                f"{units_retrofilled:,.0f}",
                delta="+10–15 yrs asset life each",
            )
            m3.metric(
                "Fleet CO₂ avoided",
                f"{fleet_avoided_kt:,.2f} kt",
                delta="vs. full replacement",
            )
            st.success(
                "**Recommendation: Fluid Retrofill**\n\n"
                "Drain the aged mineral insulating oil and retrofill with re-refined mineral oil or "
                "natural ester fluid, restoring dielectric strength and moisture performance. "
                "This defers manufacturing of a replacement unit — avoiding its full A1–A3 embodied "
                "carbon — and extends the asset's functional life without hardware replacement.\n\n"
                f"**At portfolio scale:** retrofilling {retrofill_pct}% of the {installed_base:,} installed "
                f"**{family.strip()}** units defers **{fleet_avoided_kt:,.2f} kt CO₂e** of A1–A3 manufacturing "
                "emissions that a full-replacement strategy would otherwise incur."
            )
    else:
        st.markdown("**Annual decommissioning volume per class**")
        vcols = st.columns(len(BOM))
        volumes = {
            fam_name: col.number_input(
                fam_name.strip(), min_value=0, value=50, step=5, key=f"eol_vol_{i}"
            )
            for i, (col, fam_name) in enumerate(zip(vcols, BOM.keys()))
        }

        def _class_stats(mass_map: dict) -> tuple:
            total = sum(mass_map.values())
            recovered = sum(
                mass_map[c] * rec_rates.get(c, 0.0) for c in dl.COMPONENT_ORDER
            )
            credit_unit_t = (
                sum(
                    mass_map[c] * rec_rates.get(c, 0.0) * baseline_ci[c]
                    for c in dl.COMPONENT_ORDER
                )
                / 1_000
            )
            recyclability = recovered / total * 100 if total else 0
            return recyclability, credit_unit_t

        # ── PORTFOLIO VIEW (all classes) ──────────────────────────────────────
        portfolio_rows = []
        for fam_name, mass_list in BOM.items():
            mass_map = dict(zip(dl.COMPONENT_ORDER, mass_list))
            recyclability, credit_unit_t = _class_stats(mass_map)
            vol = volumes[fam_name]
            portfolio_rows.append(
                {
                    "Transformer class": fam_name.strip(),
                    "Units/yr": vol,
                    "Recyclability (%)": round(recyclability, 1),
                    "Module D credit/unit (t)": round(credit_unit_t, 2),
                    "Portfolio credit (kt/yr)": round(credit_unit_t * vol / 1_000, 3),
                }
            )
        portfolio_df = pd.DataFrame(portfolio_rows)
        total_portfolio_kt = portfolio_df["Portfolio credit (kt/yr)"].sum()
        total_units = portfolio_df["Units/yr"].sum()

        st.subheader("🌍 Portfolio Module D Credit — All Classes")
        p1, p2 = st.columns(2)
        p1.metric("Fleet decommissioning", f"{total_units:,.0f} units/yr")
        p2.metric(
            "Total Module D credit",
            f"{total_portfolio_kt:,.2f} kt/yr",
            delta="avoided virgin-material CO₂e",
        )
        st.dataframe(portfolio_df, use_container_width=True, hide_index=True)
        st.session_state["mod2_eol"] = {
            "total_portfolio_kt": float(total_portfolio_kt),
            "total_units": int(total_units),
            "volumes": {fam: float(volumes[fam]) for fam in BOM.keys()},
        }
        st.download_button(
            "⬇ Export portfolio credit (CSV)",
            portfolio_df.to_csv(index=False).encode("utf-8"),
            file_name="module_d_portfolio_credit.csv",
            mime="text/csv",
        )

        # ── COMPONENT DETAIL (selected class) ─────────────────────────────────
        st.subheader(f"🔍 Component Detail — {family.strip()}")
        rows = []
        for component in dl.COMPONENT_ORDER:
            mass = masses[component]
            rate = rec_rates.get(component, 0.0)
            recovered = mass * rate
            credit_unit_t = (
                recovered * baseline_ci[component] / 1_000
            )  # avoided virgin-material CO₂e
            rows.append(
                {
                    "Component": component.capitalize(),
                    "Mass (kg)": round(mass, 0),
                    "Recovery rate": f"{rate:.0%}",
                    "Recovered (kg)": round(recovered, 0),
                    "Module D credit/unit (t)": round(credit_unit_t, 2),
                    "Portfolio credit (kt/yr)": round(
                        credit_unit_t * volumes[family] / 1_000, 3
                    ),
                }
            )
        df = pd.DataFrame(rows)

        recyclability, credit_per_unit_t = _class_stats(masses)
        m1, m2, m3 = st.columns(3)
        m1.metric("Overall recyclability", f"{recyclability:,.1f}%", delta="by mass")
        m2.metric(
            "Module D credit / unit",
            f"{credit_per_unit_t:,.1f} t",
            delta="avoided virgin-material CO₂e",
        )
        m3.metric(
            "Class credit",
            f"{df['Portfolio credit (kt/yr)'].sum():,.2f} kt/yr",
            delta=f"{volumes[family]:,} units/yr",
        )

        st.dataframe(df, use_container_width=True, hide_index=True)
        st.download_button(
            "⬇ Export component detail (CSV)",
            df.to_csv(index=False).encode("utf-8"),
            file_name=f"module_d_detail_{family.strip().split()[0].lower()}.csv",
            mime="text/csv",
        )

        fig = px.bar(
            df,
            x="Component",
            y="Module D credit/unit (t)",
            title="Module D recovery credit by component (per unit)",
            labels={"Module D credit/unit (t)": "Avoided CO₂e (t/unit)"},
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(
            "**Recommendation: TX Life Replace Protocol**\n\n"
            "Deploy structured decommissioning manuals for safe disassembly. Key recovery streams:\n\n"
            "- 🔴 **Copper windings** → specialist smelters (high value, high embodied carbon avoided)\n"
            "- 🟡 **CRGO steel core** → steel recycling (reduces Scope 3 of next unit's BOM)\n"
            "- 🔵 **Insulation oil** → re-refining (circular loop; avoids incineration CO₂)\n"
            "- ⚠️ **Thermoset plastics / epoxy resins** → current waste challenge; Phase 2 design-for-disassembly target"
        )
        st.warning(
            "📋 **Module D credit (beyond system boundary):** Recovered copper and steel re-entering the supply chain "
            "displace virgin material, generating the carbon credit quantified above that offsets future A1–A3 "
            "emissions. Rates are representative EOL averages (`data/recovery_factors.csv`) pending treatment-partner data."
        )


elif module == "3. Portfolio CO₂ Simulator ★":
    st.title("🌍 Transformer Portfolio CO₂ Simulator")
    st.caption("Concept proposal | Lugas Raka Adrianto | June 2026")
    st.markdown(
        """
        A **granular bottom-up CO₂ impact calculator** for the transformer portfolio — translating BOM-level
        material design choices into fleet-wide carbon outcomes across product families and annual production volumes,
        powered by **live EPD data feeds**.
        """
    )
    st.caption(
        "ℹ️ An Environmental Product Declaration (EPD) is a standardized, independently verified report of a "
        "product's lifecycle environmental impacts, including embodied CO₂. Here a live EPD data feed represents "
        "the carbon-factor source that replaces the static CSV factor tables in Phase 2."
    )
    warn_factor_freshness()

    # ── SCOPE NOTE ───────────────────────────────────────────────────────────
    st.error(
        "⚠️  **Scope: Cradle-to-Gate (Stages A1–A3) — Scope 3 Upstream Embodied Emissions Only**\n\n"
        "This simulator covers **raw material extraction → processing → factory gate** (EN 15804 / ISO 14044 stages A1–A3). "
        "It quantifies the **embodied carbon of transformer materials** (CRGO steel, copper windings, insulation fluid, "
        "structural steel) as a function of BOM composition and material sourcing choices.\n\n"
        "**The following lifecycle stages are NOT included in this module:**\n"
        "- 🚚  **A4–A5** Transport to site & installation\n"
        "- ⚡  **B1–B6** Use-phase energy losses (40-year operational CO₂) → covered in **Module 1: TCO & Carbon ROI**\n"
        "- ♻️  **C1–C4** End-of-life processing, dismantling & recycling credits → covered in **Module 2: Circularity & EOL Planner**\n\n"
        "📋  **Full cradle-to-grave lifecycle assessment (A1–C4 + Module D) is under development "
        "and planned for Phase 2 integration with a live full-lifecycle EPD data feed.**"
    )
    st.divider()

    # ── METHODOLOGY & DATA ARCHITECTURE ──────────────────────────────────────
    with st.expander(
        "📐  Methodology & Data Architecture — How the simulator works", expanded=True
    ):
        st.markdown("### Calculation Methodology")
        st.markdown(
            """
            The simulator applies a **bottom-up Product Carbon Footprint (PCF)** approach, aligned with
            **ISO 14040 / 14044** (Life Cycle Assessment) and the **GHG Protocol Product Standard**:

            | Step | Formula | Unit |
            |---|---|---|
            | **1. Component CO₂** | mass_i [kg] × CI_i [kg CO₂e/kg] | kg CO₂e per BOM line |
            | **2. Unit CO₂** | Σ component CO₂ across all BOM lines | t CO₂e per transformer |
            | **3. Portfolio CO₂** | Unit CO₂ × annual volume [units/yr] | kt CO₂e / year |
            | **4. Lever attribution** | Δ CO₂ when CI_i changes (Baseline → Eco-Efficient); all other lines held constant | kt CO₂e / year saved per lever |
            | **5. Uncertainty bounds** | Σ mass_i × CI_i,low and Σ mass_i × CI_i,high (all factors simultaneously at their low / high ends) | kt CO₂e range |
            | **6. Abatement cost** | (mass_i × costΔ_i × volume) ÷ Δ CO₂ per lever | € per t CO₂e avoided |

            Where **CI** (carbon intensity) is the emission factor for a given material and sourcing scenario,
            expressed in **kg CO₂e per kg** of material delivered to the factory gate (cradle-to-gate).
            """
        )

        st.markdown("---")
        st.markdown("### System Boundary — Lifecycle Stages Covered")

        # System boundary: 4 stages with arrows
        IN = "background-color:#00CC9622; border:2px solid #00CC96; border-radius:8px; padding:12px; text-align:center;"
        OUT = "background-color:#33333388; border:2px dashed #666; border-radius:8px; padding:12px; text-align:center; color:#aaa;"
        ARR = "<div style='text-align:center;font-size:22px;padding-top:22px;color:#555;'>▶</div>"

        sb = st.columns([2, 0.3, 2, 0.3, 2, 0.3, 2])
        with sb[0]:
            st.markdown(
                f"<div style='{IN}'><b style='color:#00CC96'>✅ A1 – A3</b><br><br>"
                "<b>Raw Materials &amp;<br>Manufacturing</b><br><br>"
                "<small>Steel, copper, oil,<br>insulation, structure</small><br><br>"
                "<small><b>← THIS MODULE</b></small></div>",
                unsafe_allow_html=True,
            )
        with sb[1]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[2]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 A4 – A5</b><br><br>"
                "<b>Transport &amp;<br>Installation</b><br><br>"
                "<small>Logistics CO₂,<br>site works</small><br><br>"
                "<small>Phase 2</small></div>",
                unsafe_allow_html=True,
            )
        with sb[3]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[4]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 B1 – B6</b><br><br>"
                "<b>Use Phase</b><br>(40 years)<br><br>"
                "<small>No-load &amp; load<br>energy losses</small><br><br>"
                "<small>→ Module 1</small></div>",
                unsafe_allow_html=True,
            )
        with sb[5]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[6]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 C1 – C4 + D</b><br><br>"
                "<b>End of Life &amp;<br>Recycling</b><br><br>"
                "<small>Disassembly, Cu &amp;<br>oil recovery credits</small><br><br>"
                "<small>→ Module 4 / Phase 2</small></div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Data Architecture — Pipeline")

        # 4-tier pipeline: Sources → Engine → Outputs → Decisions
        TIER = (
            "border:1px solid #444; border-radius:10px; padding:14px; min-height:200px;"
        )
        ARR2 = "<div style='text-align:center;font-size:28px;padding-top:70px;color:#00CC96;'>▶</div>"

        da = st.columns([2.5, 0.3, 2.5, 0.3, 2.5, 0.3, 2.5])
        with da[0]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#00CC96'>📂 DATA SOURCES</b><br><br>"
                "🔹 <b>EPDs</b> — live EPD data platform<br>"
                "🔹 <b>BOM data</b> — PLM / PDM system<br>"
                "🔹 <b>Material CI factors</b> — Ecoinvent 3.x + supplier declarations<br>"
                "🔹 <b>Volume forecast</b> — Product Management<br>"
                "🔹 <b>Supplier ratings</b> — third-party sustainability ratings"
                "</div>",
                unsafe_allow_html=True,
            )
        with da[1]:
            st.markdown(ARR2, unsafe_allow_html=True)
        with da[2]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#636EFA'>⚙️ CALCULATION ENGINE</b><br><br>"
                "🔹 mass_i × CI_i per BOM line<br>"
                "🔹 Σ → CO₂ per transformer unit<br>"
                "🔹 × Volume → portfolio kt CO₂e/yr<br>"
                "🔹 Scenario Δ: Baseline vs. Eco-Efficient<br>"
                "🔹 Lever attribution (core / fluid / Cu)"
                "</div>",
                unsafe_allow_html=True,
            )
        with da[3]:
            st.markdown(ARR2, unsafe_allow_html=True)
        with da[4]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#FFA15A'>📊 OUTPUTS</b><br><br>"
                "🔹 Portfolio CO₂ KPIs (kt CO₂e/yr)<br>"
                "🔹 Reduction % vs. baseline<br>"
                "🔹 Waterfall: lever attribution<br>"
                "🔹 Cu procurement volume (t/yr)<br>"
                "🔹 kg CO₂e / kVA per product class"
                "</div>",
                unsafe_allow_html=True,
            )
        with da[5]:
            st.markdown(ARR2, unsafe_allow_html=True)
        with da[6]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#EF553B'>🎯 DECISIONS ENABLED</b><br><br>"
                "🔹 R&D: prioritise highest-impact BOM positions<br>"
                "🔹 Supply chain: size low-carbon material programmes<br>"
                "🔹 PLM gate: CO₂ as a hard design condition<br>"
                "🔹 SBTi: track Scope 3 upstream trajectory"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "📌 **Data note:** Carbon intensity values are sourced from Ecoinvent 3.x background database and "
            "manufacturer product declarations and published LCA studies. "
            "BOM mass estimates are representative averages per transformer class — to be replaced with actual PLM/BOM data in production deployment."
        )

        st.markdown("---")
        st.markdown("### Material Carbon Intensity Reference — Key Inputs")
        st.caption(
            "Source: Ecoinvent 3.x + manufacturer product declarations + supplier primary data"
        )

        st.dataframe(dl.reference_table(), use_container_width=True, hide_index=True)
        st.caption(
            "Supply chain context: third-party supplier sustainability ratings and a supplier development "
            "programme target the highest-carbon-intensity materials first."
        )

    st.divider()

    # ── ARCHITECTURE OVERVIEW ────────────────────────────────────────────────
    st.markdown("### What this simulator covers (A1–A3 scope)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            """
            ### 📥 INPUT
            - **EPDs** from a live EPD data platform
            - **Detailed BOM** per transformer class  
              *(CRGO steel, Cu windings, oil, insulation, structural steel)*
            - **Component-level CO₂ data**  
              *(kg CO₂e/kg per material + sourcing scenario)*
            - **Volume forecast** per product family / kVA class
            """
        )
    with col_b:
        st.markdown(
            """
            ### 📊 OUTPUT
            - Precise **bottom-up CO₂ calculation** per unit + portfolio total
            - Immediate **portfolio-wide impact** comparison  
              *(Baseline vs. Eco-Efficient design scenarios)*
            - **Lever attribution**: which design choice drives how much reduction
            - **Data-driven** decision support for R&D gate reviews & supplier programmes
            """
        )
    with col_c:
        st.markdown(
            """
            ### 🎯 IMPACT (PROPOSED)
            - **All transformer product families** mapped to embodied CO₂ intensity
            - **Highest-reduction BOM positions** identified for prioritised R&D focus
            - **Supply chain targets** quantified: low-carbon copper + green steel programme sizing
            - **Gate-ready KPIs**: kg CO₂e/kVA per product class, tracked vs. SBTi Scope 3 trajectory
            """
        )
    st.divider()

    # ── MATERIAL CARBON INTENSITY DATABASE (loaded from data/ — see data_layer.py) ──
    CORE_OPTS = dl.factor_details("core")
    FLUID_OPTS = dl.factor_details("fluid")
    COPPER_OPTS = dl.factor_details("copper")
    BASE = {c: dl.baseline_details(c) for c in ("core", "fluid", "copper")}
    INSUL_BASE = dl.baseline_details("insulation")  # kraft paper / pressboard (fixed)
    STRUCT_BASE = dl.baseline_details("structural")  # standard structural steel (fixed)

    # Representative average BOM per transformer class [core_kg, cu_kg, oil_kg, insul_kg, struct_kg]
    BOM = dl.bom_by_family()
    KVA = dl.kva_by_family()

    # ── STEP 1 — VOLUME FORECAST ─────────────────────────────────────────────
    st.subheader("Step 1 — Portfolio Volume Forecast")
    st.caption("Enter your annual production/sales forecast per transformer class.")
    c1, c2, c3 = st.columns(3)
    vol_dist = c1.number_input(
        "Distribution transformers (units / year)", value=500, step=10
    )
    vol_med = c2.number_input(
        "Medium Power transformers (units / year)", value=120, step=5
    )
    vol_large = c3.number_input(
        "Large Power transformers (units / year)", value=25, step=1
    )
    volumes = [vol_dist, vol_med, vol_large]

    # ── STEP 2 — DESIGN SCENARIO ─────────────────────────────────────────────
    st.subheader("Step 2 — Configure Design Scenario")
    st.caption(
        "Scenario A is fixed as today's standard BOM. Configure Scenario B (Eco-Efficient interventions)."
    )

    col_base, col_eco = st.columns(2)
    with col_base:
        st.markdown("**Scenario A — Baseline (Current BOM)**")
        st.info(
            "Core: CRGO Steel — Standard  \n"
            "Fluid: Virgin Mineral Oil  \n"
            "Copper: Standard sourcing"
        )
    with col_eco:
        st.markdown("**Scenario B — Eco-Efficient Design Interventions**")
        core_choice = st.selectbox(
            "Magnetic Core Material", list(CORE_OPTS.keys()), index=1
        )
        fluid_choice = st.selectbox(
            "Insulation Fluid", list(FLUID_OPTS.keys()), index=1
        )
        copper_choice = st.selectbox(
            "Copper Winding Sourcing", list(COPPER_OPTS.keys()), index=1
        )

    # ── STEP 3 — RUN SIMULATION ───────────────────────────────────────────────
    st.divider()
    if st.button(
        "▶  Run Portfolio CO₂ Simulation", type="primary", use_container_width=True
    ):
        core_d = CORE_OPTS[core_choice]
        fluid_d = FLUID_OPTS[fluid_choice]
        copper_d = COPPER_OPTS[copper_choice]
        core_b = BASE["core"]
        fluid_b = BASE["fluid"]
        copper_b = BASE["copper"]

        rows = []
        lever_cost = {"core": 0.0, "fluid": 0.0, "copper": 0.0}  # €/yr
        for (family, masses), vol in zip(BOM.items(), volumes):
            core_m, cu_m, oil_m, insul_m, struct_m = masses

            # CO₂ per unit (tonnes), expected factors
            base_unit = (
                core_m * core_b["ci"]
                + cu_m * copper_b["ci"]
                + oil_m * fluid_b["ci"]
                + insul_m * INSUL_BASE["ci"]
                + struct_m * STRUCT_BASE["ci"]
            ) / 1_000

            eco_unit = (
                core_m * core_d["ci"]
                + cu_m * copper_d["ci"]
                + oil_m * fluid_d["ci"]
                + insul_m * INSUL_BASE["ci"]
                + struct_m * STRUCT_BASE["ci"]
            ) / 1_000

            # Uncertainty bounds: all factors simultaneously at their low / high ends
            base_low = (
                core_m * core_b["low"]
                + cu_m * copper_b["low"]
                + oil_m * fluid_b["low"]
                + insul_m * INSUL_BASE["low"]
                + struct_m * STRUCT_BASE["low"]
            ) / 1_000
            base_high = (
                core_m * core_b["high"]
                + cu_m * copper_b["high"]
                + oil_m * fluid_b["high"]
                + insul_m * INSUL_BASE["high"]
                + struct_m * STRUCT_BASE["high"]
            ) / 1_000
            eco_low = (
                core_m * core_d["low"]
                + cu_m * copper_d["low"]
                + oil_m * fluid_d["low"]
                + insul_m * INSUL_BASE["low"]
                + struct_m * STRUCT_BASE["low"]
            ) / 1_000
            eco_high = (
                core_m * core_d["high"]
                + cu_m * copper_d["high"]
                + oil_m * fluid_d["high"]
                + insul_m * INSUL_BASE["high"]
                + struct_m * STRUCT_BASE["high"]
            ) / 1_000

            # Lever contributions per unit (tonnes)
            delta_core = (core_m * (core_b["ci"] - core_d["ci"])) / 1_000
            delta_fluid = (oil_m * (fluid_b["ci"] - fluid_d["ci"])) / 1_000
            delta_copper = (cu_m * (copper_b["ci"] - copper_d["ci"])) / 1_000

            # Material cost uplift of the eco design (€/unit and €/yr per lever)
            premium_unit = (
                core_m * core_d["cost_delta"]
                + cu_m * copper_d["cost_delta"]
                + oil_m * fluid_d["cost_delta"]
            )
            lever_cost["core"] += core_m * core_d["cost_delta"] * vol
            lever_cost["fluid"] += oil_m * fluid_d["cost_delta"] * vol
            lever_cost["copper"] += cu_m * copper_d["cost_delta"] * vol

            kva = KVA[family]

            rows.append(
                {
                    "Product Family": family,
                    "Units/yr": vol,
                    "Baseline CO₂/unit (t)": round(base_unit, 1),
                    "Eco-Efficient CO₂/unit (t)": round(eco_unit, 1),
                    "Reduction/unit (t)": round(base_unit - eco_unit, 1),
                    "Baseline kg CO₂e/kVA": round(base_unit * 1_000 / kva, 2),
                    "Eco kg CO₂e/kVA": round(eco_unit * 1_000 / kva, 2),
                    "Portfolio Baseline (kt/yr)": round(base_unit * vol / 1_000, 2),
                    "Portfolio Eco-Efficient (kt/yr)": round(eco_unit * vol / 1_000, 2),
                    "Portfolio Saving (kt/yr)": round(
                        (base_unit - eco_unit) * vol / 1_000, 2
                    ),
                    "Baseline low (kt/yr)": round(base_low * vol / 1_000, 2),
                    "Baseline high (kt/yr)": round(base_high * vol / 1_000, 2),
                    "Eco low (kt/yr)": round(eco_low * vol / 1_000, 2),
                    "Eco high (kt/yr)": round(eco_high * vol / 1_000, 2),
                    "Green premium (k€/yr)": round(premium_unit * vol / 1_000, 1),
                    "Δ Core (kt/yr)": round(delta_core * vol / 1_000, 3),
                    "Δ Fluid (kt/yr)": round(delta_fluid * vol / 1_000, 3),
                    "Δ Copper (kt/yr)": round(delta_copper * vol / 1_000, 3),
                }
            )

        df = pd.DataFrame(rows)
        total_base = df["Portfolio Baseline (kt/yr)"].sum()
        total_eco = df["Portfolio Eco-Efficient (kt/yr)"].sum()
        total_saving = total_base - total_eco
        pct_saving = total_saving / total_base * 100
        premium_eur = float(df["Green premium (k€/yr)"].sum() * 1_000)
        blended = premium_eur / (total_saving * 1_000) if total_saving > 0 else None

        st.session_state["sim"] = {
            "df": df,
            "kpis": {
                "total_base": float(total_base),
                "total_eco": float(total_eco),
                "total_saving": float(total_saving),
                "pct_saving": float(pct_saving),
            },
            "choices": {
                "core": core_choice,
                "fluid": fluid_choice,
                "copper": copper_choice,
            },
            "volumes": {"dist": vol_dist, "med": vol_med, "large": vol_large},
            "uncertainty": {
                "base_low": float(df["Baseline low (kt/yr)"].sum()),
                "base_high": float(df["Baseline high (kt/yr)"].sum()),
                "eco_low": float(df["Eco low (kt/yr)"].sum()),
                "eco_high": float(df["Eco high (kt/yr)"].sum()),
            },
            "cost": {
                "premium_eur": premium_eur,
                "blended_eur_per_t": blended,
                "lever_costs": lever_cost,
            },
        }

    # ── DISPLAY RESULTS (persisted across reruns via session_state) ──────────
    sim = st.session_state.get("sim")
    if sim:
        df = sim["df"]
        total_base = sim["kpis"]["total_base"]
        total_eco = sim["kpis"]["total_eco"]
        total_saving = sim["kpis"]["total_saving"]
        pct_saving = sim["kpis"]["pct_saving"]

        # ── PORTFOLIO KPI METRICS ─────────────────────────────────────────
        st.subheader("📊 Portfolio-Level CO₂ Output")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Baseline Portfolio", f"{total_base:.1f} kt CO₂e/yr")
        m2.metric(
            "Eco-Efficient Portfolio",
            f"{total_eco:.1f} kt CO₂e/yr",
            delta=f"-{total_saving:.1f} kt",
        )
        m3.metric("Total Reduction", f"{total_saving:.1f} kt CO₂e/yr")
        m4.metric("% Reduction", f"{pct_saving:.1f}%", delta=f"vs. baseline")

        unc = sim["uncertainty"]
        cost = sim["cost"]
        blended = cost["blended_eur_per_t"]
        n1, n2, n3, n4 = st.columns(4)
        n1.metric(
            "Annual green premium",
            f"€{cost['premium_eur']:,.0f}/yr",
            delta="material cost uplift vs. baseline",
            delta_color="off",
        )
        n2.metric(
            "Blended abatement cost",
            f"€{blended:,.0f}/t CO₂e" if blended is not None else "n/a",
            delta="portfolio average",
            delta_color="off",
        )
        n3.metric(
            "Baseline uncertainty",
            f"{unc['base_low']:.1f}–{unc['base_high']:.1f} kt",
            delta="factor low–high",
            delta_color="off",
        )
        n4.metric(
            "Eco-Efficient uncertainty",
            f"{unc['eco_low']:.1f}–{unc['eco_high']:.1f} kt",
            delta="factor low–high",
            delta_color="off",
        )
        st.caption(
            "Uncertainty bounds: all material carbon factors simultaneously at the low vs. high "
            "end of their sourced ranges (`uncertainty_low` / `uncertainty_high` in "
            "`data/material_factors.csv`). Cost figures use representative `cost_delta_eur_per_kg` "
            "values pending procurement quotes."
        )

        # ── PRODUCT-FAMILY TABLE ──────────────────────────────────────────
        st.markdown("**Bottom-up CO₂ by product family**")
        display_cols = [
            "Product Family",
            "Units/yr",
            "Baseline CO₂/unit (t)",
            "Eco-Efficient CO₂/unit (t)",
            "Reduction/unit (t)",
            "Baseline kg CO₂e/kVA",
            "Eco kg CO₂e/kVA",
            "Portfolio Saving (kt/yr)",
        ]
        st.dataframe(
            df[display_cols].set_index("Product Family"), use_container_width=True
        )

        # ── WATERFALL: LEVER ATTRIBUTION ─────────────────────────────────
        st.markdown(
            "**Design lever attribution — where does the reduction come from?**"
        )
        delta_core_total = df["Δ Core (kt/yr)"].sum()
        delta_fluid_total = df["Δ Fluid (kt/yr)"].sum()
        delta_copper_total = df["Δ Copper (kt/yr)"].sum()

        fig_wf = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=["absolute", "relative", "relative", "relative", "total"],
                x=[
                    "Baseline Portfolio",
                    "Core Material Lever",
                    "Fluid Lever",
                    "Copper Sourcing Lever",
                    "Eco-Efficient Portfolio",
                ],
                y=[
                    total_base,
                    -delta_core_total,
                    -delta_fluid_total,
                    -delta_copper_total,
                    0,
                ],
                text=[
                    f"{total_base:.1f} kt",
                    f"-{delta_core_total:.2f} kt",
                    f"-{delta_fluid_total:.2f} kt",
                    f"-{delta_copper_total:.2f} kt",
                    f"{total_eco:.1f} kt",
                ],
                textposition="outside",
                connector={"line": {"color": "rgb(63, 63, 63)"}},
                increasing={"marker": {"color": "#EF553B"}},
                decreasing={"marker": {"color": "#00CC96"}},
                totals={"marker": {"color": "#636EFA"}},
            )
        )
        fig_wf.update_layout(
            title="Portfolio CO₂ Reduction Waterfall — kt CO₂e/yr",
            yaxis_title="kt CO₂e / year",
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            height=420,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

        # ── STACKED BAR: BASELINE vs ECO-EFFICIENT BY PRODUCT FAMILY ────────
        st.markdown("**Baseline vs. Eco-Efficient CO₂ by product family**")
        fig_bar = go.Figure()
        fig_bar.add_trace(
            go.Bar(
                name="Baseline",
                x=df["Product Family"],
                y=df["Portfolio Baseline (kt/yr)"],
                marker_color="#EF553B",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=(
                        df["Baseline high (kt/yr)"] - df["Portfolio Baseline (kt/yr)"]
                    ).tolist(),
                    arrayminus=(
                        df["Portfolio Baseline (kt/yr)"] - df["Baseline low (kt/yr)"]
                    ).tolist(),
                ),
            )
        )
        fig_bar.add_trace(
            go.Bar(
                name="Eco-Efficient",
                x=df["Product Family"],
                y=df["Portfolio Eco-Efficient (kt/yr)"],
                marker_color="#00CC96",
                error_y=dict(
                    type="data",
                    symmetric=False,
                    array=(
                        df["Eco high (kt/yr)"] - df["Portfolio Eco-Efficient (kt/yr)"]
                    ).tolist(),
                    arrayminus=(
                        df["Portfolio Eco-Efficient (kt/yr)"] - df["Eco low (kt/yr)"]
                    ).tolist(),
                ),
            )
        )
        fig_bar.update_layout(
            barmode="group",
            yaxis_title="kt CO₂e / year",
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            legend=dict(orientation="h", yanchor="bottom", y=1.02),
            height=350,
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        st.caption(
            "Error bars: factor-uncertainty bounds (all factors simultaneously at low / high ends)."
        )

        # ── ABATEMENT COST RANKING ────────────────────────────────────────
        st.markdown(
            "**Abatement cost ranking — what does each tonne of CO₂ saved cost?**"
        )
        lever_meta = [
            ("Core material", delta_core_total, cost["lever_costs"]["core"]),
            ("Insulation fluid", delta_fluid_total, cost["lever_costs"]["fluid"]),
            ("Copper sourcing", delta_copper_total, cost["lever_costs"]["copper"]),
        ]
        ab_rows = []
        for name, delta_kt, cost_eur in lever_meta:
            eur_per_t = cost_eur / (delta_kt * 1_000) if delta_kt > 0 else None
            ab_rows.append(
                {
                    "Design lever": name,
                    "CO₂ saving (kt/yr)": round(delta_kt, 3),
                    "Extra material cost (k€/yr)": round(cost_eur / 1_000, 1),
                    "Abatement cost (€/t CO₂e)": (
                        f"€{eur_per_t:,.0f}"
                        if eur_per_t is not None
                        else "n/a — raises embodied CO₂"
                    ),
                }
            )
        ab_df = pd.DataFrame(ab_rows).sort_values("CO₂ saving (kt/yr)", ascending=False)
        st.dataframe(ab_df, use_container_width=True, hide_index=True)
        st.caption(
            "Levers ranked by CO₂ saving; the €/t column exposes the cheapest reduction first — "
            "the seed of the Phase 3 marginal-abatement-cost curve. Cost deltas are representative "
            "values (`cost_delta_eur_per_kg` in `data/material_factors.csv`)."
        )

        # ── IMPACT SUMMARY ────────────────────────────────────────────────
        st.divider()
        st.subheader("🎯 Impact Summary — What This Simulation Enables")
        ic1, ic2, ic3 = st.columns(3)
        with ic1:
            st.success(
                f"**Design prioritisation**\n\n"
                f"Core lever saves **{delta_core_total:.2f} kt/yr** — "
                f"Fluid lever saves **{delta_fluid_total:.2f} kt/yr** — "
                f"Copper lever saves **{delta_copper_total:.2f} kt/yr**.\n\n"
                f"Directs R&D investment to highest-impact BOM positions first."
            )
        with ic2:
            st.info(
                f"**Supply chain programme sizing**\n\n"
                f"Low-carbon copper procurement required: "
                f"**{df['Units/yr'].dot(pd.Series([m[1] for m in BOM.values()])) / 1_000:.0f} tonnes Cu/yr** "
                f"across the portfolio.\n\n"
                f"Quantifies the supplier development programme before contracts are written."
            )
        with ic3:
            intensity = " · ".join(
                f"{r['Product Family'].strip().split('  ')[0]} "
                f"{r['Eco kg CO₂e/kVA']:g} kg/kVA"
                for _, r in df.iterrows()
            )
            st.warning(
                f"**Gate-ready KPI for PLM reviews**\n\n"
                f"Eco-Efficient target: **{pct_saving:.1f}% lifecycle CO₂ reduction** vs. baseline — "
                f"**{intensity}** by product class.\n\n"
                f"Expressed as a gate condition at PLM design review — not a sustainability aspiration."
            )
        st.caption(
            "📌 Scope reminder: this simulation covers cradle-to-gate embodied carbon (A1–A3) only — "
            "Scope 3 upstream emissions from raw material extraction through factory gate. "
            "Use-phase energy losses (B1–B6) → Module 1 | End-of-life (C1–C4) → Module 2 | "
            "Full cradle-to-grave integration: Phase 2 roadmap item."
        )

        # ── SAVE & EXPORT THIS RUN ────────────────────────────────────────
        st.divider()
        st.subheader("💾 Save & Export Scenario")
        sc, ec = st.columns([2, 1])
        with sc:
            with st.form("save_run_form", clear_on_submit=True):
                default_name = (
                    f"{sim['choices']['core'].split(' —')[0]} + "
                    f"{sim['choices']['copper'].split(' (')[0]}"
                )
                run_name = st.text_input("Scenario name", value=default_name)
                if st.form_submit_button("💾 Save this run", use_container_width=True):
                    run_id = store.save_run(
                        name=run_name.strip() or "Untitled scenario",
                        choices=sim["choices"],
                        volumes=sim["volumes"],
                        kpis=sim["kpis"],
                        results=df,
                    )
                    st.success(f"Saved as run #{run_id} — “{run_name}”.")
        with ec:
            st.download_button(
                "⬇ Export results (CSV)",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="portfolio_co2_results.csv",
                mime="text/csv",
                use_container_width=True,
            )
            st.caption("Gate-review-ready per-family CO₂ breakdown.")

    # ── SAVED SCENARIOS — COMPARE (persists across sessions in data/runs.db) ──
    st.divider()
    st.subheader("🗂️ Saved Scenarios — Compare")
    saved = store.list_runs()
    if saved.empty:
        st.caption(
            "No saved runs yet. Run a simulation above and click **Save this run**."
        )
    else:
        saved = saved.copy()
        st.markdown("### Design-Gate Comparison")
        saved["gate_label"] = saved.apply(
            lambda row: f"#{row.run_id} - {row['name']} ({row.created_at[:10]})",
            axis=1,
        )
        gate_label_to_id = dict(zip(saved["gate_label"], saved["run_id"]))
        baseline_label = st.selectbox(
            "Baseline design",
            options=list(gate_label_to_id.keys()),
            key="design_gate_baseline",
        )
        alternative_options = [
            label for label in gate_label_to_id if label != baseline_label
        ]
        alternative_labels = st.multiselect(
            "Alternatives for this gate",
            options=alternative_options,
            max_selections=3,
            key="design_gate_alternatives",
        )

        if not alternative_labels:
            st.caption("Select one to three alternatives to make a design-gate comparison.")
        else:
            baseline = saved[
                saved["run_id"] == gate_label_to_id[baseline_label]
            ].iloc[0]
            baseline_metrics = saved_run_decision_metrics(baseline)
            comparison_rows = [
                {
                    "Scenario": baseline["name"],
                    "Role": "Baseline",
                    "Portfolio carbon (kt/yr)": baseline_metrics["portfolio_eco"],
                    "Carbon change (kt/yr)": 0.0,
                    "Carbon reduction": 0.0,
                    "Material cost delta (kEUR/yr)": 0.0,
                    "Abatement cost (EUR/tCO2e)": None,
                    "Uncertainty (kt/yr)": (
                        f"{baseline_metrics['eco_low']:.2f}-{baseline_metrics['eco_high']:.2f}"
                    ),
                    "run_id": int(baseline["run_id"]),
                }
            ]

            for label in alternative_labels:
                candidate = saved[
                    saved["run_id"] == gate_label_to_id[label]
                ].iloc[0]
                candidate_metrics = saved_run_decision_metrics(candidate)
                carbon_reduction = (
                    baseline_metrics["portfolio_eco"]
                    - candidate_metrics["portfolio_eco"]
                )
                cost_delta = (
                    candidate_metrics["green_premium_k_eur"]
                    - baseline_metrics["green_premium_k_eur"]
                )
                comparison_rows.append(
                    {
                        "Scenario": candidate["name"],
                        "Role": "Alternative",
                        "Portfolio carbon (kt/yr)": candidate_metrics["portfolio_eco"],
                        "Carbon change (kt/yr)": -carbon_reduction,
                        "Carbon reduction": carbon_reduction / baseline_metrics["portfolio_eco"] * 100,
                        "Material cost delta (kEUR/yr)": cost_delta,
                        "Abatement cost (EUR/tCO2e)": (
                            cost_delta / carbon_reduction
                            if carbon_reduction > 0
                            else None
                        ),
                        "Uncertainty (kt/yr)": (
                            f"{candidate_metrics['eco_low']:.2f}-{candidate_metrics['eco_high']:.2f}"
                        ),
                        "run_id": int(candidate["run_id"]),
                    }
                )

            comparison = pd.DataFrame(comparison_rows)
            recommendation = comparison[
                (comparison["Role"] == "Alternative")
                & (comparison["Carbon change (kt/yr)"] < 0)
            ].sort_values(
                ["Portfolio carbon (kt/yr)", "Material cost delta (kEUR/yr)"],
                ascending=[True, True],
            )

            if recommendation.empty:
                st.warning("None of the selected alternatives lowers portfolio embodied carbon.")
            else:
                winner = recommendation.iloc[0]
                st.success(
                    f"Recommended: {winner['Scenario']} - lowest portfolio embodied carbon "
                    f"at {winner['Portfolio carbon (kt/yr)']:.2f} ktCO2e/yr."
                )
                st.caption(
                    "Carbon-first rule: alternatives are ranked by lower portfolio carbon; "
                    "annual material-cost delta breaks a carbon tie."
                )

            display_comparison = comparison.drop(columns="run_id").copy()
            for column in [
                "Portfolio carbon (kt/yr)",
                "Carbon change (kt/yr)",
                "Carbon reduction",
                "Material cost delta (kEUR/yr)",
                "Abatement cost (EUR/tCO2e)",
            ]:
                display_comparison[column] = display_comparison[column].map(
                    lambda value: round(value, 2) if pd.notna(value) else "n/a"
                )
            st.dataframe(display_comparison, use_container_width=True, hide_index=True)
            st.download_button(
                "Export design-gate comparison (CSV)",
                data=display_comparison.to_csv(index=False).encode("utf-8"),
                file_name="design_gate_comparison.csv",
                mime="text/csv",
                use_container_width=False,
            )

        saved["label"] = saved.apply(
            lambda r: f"#{r.run_id} · {r['name']} ({r.created_at[:10]})", axis=1
        )
        label_to_id = dict(zip(saved["label"], saved["run_id"]))
        picked = st.multiselect(
            "Select saved runs to compare",
            options=list(label_to_id.keys()),
            default=list(label_to_id.keys())[: min(3, len(label_to_id))],
        )
        if picked:
            ids = [label_to_id[p] for p in picked]
            comp = saved[saved["run_id"].isin(ids)].set_index("label")
            kpi_view = comp[
                [
                    "core_choice",
                    "fluid_choice",
                    "copper_choice",
                    "total_base",
                    "total_eco",
                    "total_saving",
                    "pct_saving",
                ]
            ].rename(
                columns={
                    "core_choice": "Core",
                    "fluid_choice": "Fluid",
                    "copper_choice": "Copper",
                    "total_base": "Baseline (kt/yr)",
                    "total_eco": "Eco-Efficient (kt/yr)",
                    "total_saving": "Saving (kt/yr)",
                    "pct_saving": "% Reduction",
                }
            )
            st.dataframe(kpi_view, use_container_width=True)

            fig_cmp = go.Figure()
            fig_cmp.add_trace(
                go.Bar(
                    name="Saving (kt/yr)",
                    x=comp.index,
                    y=comp["total_saving"],
                    marker_color="#00CC96",
                )
            )
            fig_cmp.update_layout(
                title="Portfolio CO₂ Saving by Saved Scenario — kt CO₂e/yr",
                yaxis_title="kt CO₂e / year",
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font_color="white",
                height=340,
            )
            st.plotly_chart(fig_cmp, use_container_width=True)

            del_col1, del_col2 = st.columns([2, 1])
            with del_col1:
                to_delete = st.selectbox("Delete a saved run", options=["—"] + picked)
            with del_col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🗑️ Delete", use_container_width=True) and to_delete != "—":
                    store.delete_run(label_to_id[to_delete])
                    st.rerun()

elif module == "4. GHG Scope 1/2/3 Report":
    st.header("📋 GHG Scope 1 / 2 / 3 Emissions Report")
    st.markdown(
        """
        A **reporting re-categorization** of the manufacturer's annual transformer-related emissions
        according to the **GHG Protocol Corporate Standard** — the reporting framework behind **CSRD**
        and **SBTi** disclosure. This module rebuckets outputs from Modules 1–3 into Scope 1, 2 and 3
        categories; it does **not** introduce a new life-cycle model.
        """
    )
    st.caption(
        "Reporting entity: transformer manufacturer for a year of production. "
        "Reporting basis: annual year-of-sale (units sold × annual emissions), per SBTi/CSRD convention."
    )
    warn_factor_freshness()
    st.divider()

    st.error(
        "⚠️  **Scope aggregation — honest data-gap callouts**\n\n"
        "- **Scope 1 & 2** use **indicative factory-energy estimates** (`data/factory_energy.csv`) "
        "per product family. Metered MES/EMS factory data is a **Phase 2** deliverable.\n"
        "- **Scope 3.1 (Purchased goods, A1–A3)** pulls the latest run from **Module 3**. "
        "Run Module 3 first for accurate figures.\n"
        "- **Scope 3.11 (Use of sold products, B1–B6)** re-derives Module 1 loss intensity from "
        "sourced defaults, scaled across families by kVA — visit Module 1 to override.\n"
        "- **Scope 3.12 (EOL of sold products)** reflects the **Module D recovery credit** only "
        "(beyond-boundary); gross C1–C4 emissions await Phase 2 partner process data.\n"
        "- **Out of scope today:** fugitive SF₆ emissions (Scope 1), A4–A5 transport (Scope 3 Cat 4), "
        "business travel, employee commuting, investments."
    )
    st.divider()

    params = dl.energy_params()
    presets = dl.load_transformer_presets()
    std_p = presets[presets["design"] == "Standard"].iloc[0]
    eco_p = presets[presets["design"] == "Eco-Efficient"].iloc[0]

    factory_energy = dl.factory_energy_by_family()
    KVA = dl.kva_by_family()
    family_list = list(factory_energy.keys())

    sim = st.session_state.get("sim")
    mod2_eol = st.session_state.get("mod2_eol")
    if sim is None:
        st.info(
            "ℹ️ No Module 3 simulation found in this session. Using default volumes; "
            "Scope 3.1 rows will show '—' until you run Module 3."
        )

    st.subheader("Step 1 — Production Volumes (annual)")
    st.caption(
        "Reused from the latest Module 3 run if available; editable here otherwise."
    )
    default_vols = (
        sim["volumes"]
        if sim is not None
        else {
            "Distribution  (avg 1,000 kVA)": 500,
            "Medium Power  (avg 25 MVA)": 120,
            "Large Power   (avg 250 MVA)": 25,
        }
    )
    vol_inputs = {}
    vcols = st.columns(len(family_list))
    for col, fam in zip(vcols, family_list):
        default_v = default_vols.get(fam, 100)
        vol_inputs[fam] = col.number_input(
            f"{fam.strip()} (units/yr)",
            min_value=0,
            value=int(default_v),
            step=10,
            key=f"m4_vol_{fam}",
        )

    st.subheader("Step 2 — Scope 1 & 2 Factory Energy per Unit")
    st.caption(
        "Defaults from `data/factory_energy.csv`; grid factor from `data/energy_params.csv`."
    )
    fe_rows = []
    fe_cols = st.columns(len(family_list))
    editable_fe = {}
    for col, fam in zip(fe_cols, family_list):
        with col:
            st.markdown(f"**{fam.strip()}**")
            gas_kwh = st.number_input(
                "Natural gas (kWh/unit)",
                min_value=0.0,
                value=float(factory_energy[fam]["gas_kwh_per_unit"]),
                step=100.0,
                format="%.0f",
                key=f"m4_gas_{fam}",
            )
            elec_kwh = st.number_input(
                "Electricity (kWh/unit)",
                min_value=0.0,
                value=float(factory_energy[fam]["electricity_kwh_per_unit"]),
                step=100.0,
                format="%.0f",
                key=f"m4_elec_{fam}",
            )
        editable_fe[fam] = {
            "gas_kwh_per_unit": gas_kwh,
            "electricity_kwh_per_unit": elec_kwh,
        }

    ef_cols = st.columns(2)
    gas_factor = ef_cols[0].number_input(
        "Natural gas emission factor (kg CO₂e/kWh)",
        min_value=0.0,
        value=float(params["natural_gas_emission_factor"]),
        step=0.01,
        format="%.3f",
    )
    elec_factor = ef_cols[1].number_input(
        "Factory electricity emission factor (kg CO₂e/kWh)",
        min_value=0.0,
        value=float(params["factory_electricity_factor"]),
        step=0.01,
        format="%.3f",
    )

    st.subheader("Step 3 — Use-phase Loss Intensity (Scope 3.11)")
    st.caption(
        "Re-derived from Module 1 sourced presets; select which design represents the sold fleet."
    )
    design_choice = st.radio(
        "Sold-fleet loss design:",
        ["Standard", "Eco-Efficient"],
        index=0,
        horizontal=True,
    )
    chosen_preset = std_p if design_choice == "Standard" else eco_p
    loading_default = params["loading_factor"]
    hours_default = params["operating_hours"]
    grid_ci_default = params["grid_carbon_intensity"]
    l1, l2, l3 = st.columns(3)
    loading_m4 = (
        l1.slider("Average loading (%)", 0, 100, int(loading_default * 100)) / 100
    )
    hours_m4 = l2.number_input(
        "Operating hours (h/yr)", value=float(hours_default), step=100.0, format="%.0f"
    )
    grid_ci_m4 = l3.number_input(
        "Grid carbon intensity (kg CO₂e/kWh)",
        value=float(grid_ci_default),
        step=0.01,
        format="%.3f",
    )

    st.subheader("Step 4 — Scope 3.1 Scenario Selection")
    s31_choice = "Baseline"
    if sim is not None:
        s31_choice = st.radio(
            "Module 3 portfolio scenario to report under Scope 3.1:",
            ["Baseline", "Eco-Efficient"],
            index=0,
            horizontal=True,
        )
    else:
        st.caption(
            "Run Module 3 to enable Baseline vs. Eco-Efficient selection for Scope 3.1."
        )

    st.divider()

    scope1_t = sum(
        vol_inputs[fam] * editable_fe[fam]["gas_kwh_per_unit"] * gas_factor / 1_000
        for fam in family_list
    )
    scope2_t = sum(
        vol_inputs[fam]
        * editable_fe[fam]["electricity_kwh_per_unit"]
        * elec_factor
        / 1_000
        for fam in family_list
    )

    unit_loss_kwh = (
        (float(chosen_preset.no_load_w) + float(chosen_preset.load_w) * loading_m4**2)
        * hours_m4
        / 1_000
    )
    unit_loss_co2_t = unit_loss_kwh * grid_ci_m4 / 1_000
    ref_kva = float(std_p.rating_kva)
    scope3_11_t = 0.0
    for fam in family_list:
        kva_fam = KVA.get(fam, ref_kva)
        scale = kva_fam / ref_kva if ref_kva > 0 else 1.0
        scope3_11_t += vol_inputs[fam] * unit_loss_co2_t * scale

    scope3_1_available = sim is not None
    scope3_1_t = 0.0
    scope3_1_kt_row = None
    if scope3_1_available:
        df_sim = sim["df"]
        if s31_choice == "Baseline":
            scope3_1_kt_row = df_sim["Portfolio Baseline (kt/yr)"].sum()
        else:
            scope3_1_kt_row = df_sim["Portfolio Eco-Efficient (kt/yr)"].sum()
        scope3_1_t = float(scope3_1_kt_row) * 1_000

    scope3_12_available = mod2_eol is not None
    scope3_12_t = 0.0
    if scope3_12_available:
        scope3_12_t = (
            float(mod2_eol["total_portfolio_kt"]) * 1_000
        )  # credit (negative sign applied in display)

    total_pos_t = scope1_t + scope2_t + scope3_1_t + scope3_11_t
    if total_pos_t > 0:
        pct1 = scope1_t / total_pos_t * 100
        pct2 = scope2_t / total_pos_t * 100
        pct31 = scope3_1_t / total_pos_t * 100 if scope3_1_available else 0.0
        pct311 = scope3_11_t / total_pos_t * 100
    else:
        pct1 = pct2 = pct31 = pct311 = 0.0

    s1, s2, s3 = st.columns(3)
    s1.metric(
        "Scope 1 — Direct factory fuel",
        f"{scope1_t:,.0f} t CO₂e/yr",
        delta=f"{pct1:.1f}%",
    )
    s2.metric(
        "Scope 2 — Purchased electricity",
        f"{scope2_t:,.0f} t CO₂e/yr",
        delta=f"{pct2:.1f}%",
    )
    s3.metric(
        "Scope 3 — Value chain (gross)",
        f"{(scope3_1_t + scope3_11_t):,.0f} t CO₂e/yr"
        + (f" − {abs(scope3_12_t):,.0f} t D-credit" if scope3_12_available else ""),
        delta=f"{pct31 + pct311:.1f}%",
    )

    st.divider()
    st.subheader("📊 Detailed Scope Breakdown")

    report_rows = [
        {
            "Scope": "1 — Direct",
            "GHG Category": "Stationary combustion (annealing/drying ovens)",
            "Lifecycle stage": "A3 (in-factory)",
            "Source module": "NEW — `factory_energy.csv`",
            "Value (t CO₂e/yr)": round(scope1_t, 1),
            "Share": f"{pct1:.1f}%" if total_pos_t > 0 else "—",
            "Data status": "Phase 1 indicative estimate",
        },
        {
            "Scope": "2 — Purchased energy",
            "GHG Category": "Purchased electricity (location-based)",
            "Lifecycle stage": "A3 (in-factory)",
            "Source module": "NEW — `factory_energy.csv`",
            "Value (t CO₂e/yr)": round(scope2_t, 1),
            "Share": f"{pct2:.1f}%" if total_pos_t > 0 else "—",
            "Data status": "Phase 1 indicative estimate",
        },
        {
            "Scope": "3.1 — Purchased goods",
            "GHG Category": "Embodied carbon of BOM (cradle-to-gate)",
            "Lifecycle stage": "A1–A3",
            "Source module": "Module 3 (Portfolio CO₂ Simulator)",
            "Value (t CO₂e/yr)": round(scope3_1_t, 1) if scope3_1_available else "—",
            "Share": f"{pct31:.1f}%" if scope3_1_available and total_pos_t > 0 else "—",
            "Data status": "Available" if scope3_1_available else "Run Module 3 first",
        },
        {
            "Scope": "3.11 — Use of sold products",
            "GHG Category": "Operational energy losses (no-load + load)",
            "Lifecycle stage": "B1–B6",
            "Source module": "Module 1 (TCO & Carbon ROI) — re-derived here from sourced defaults",
            "Value (t CO₂e/yr)": round(scope3_11_t, 1),
            "Share": f"{pct311:.1f}%" if total_pos_t > 0 else "—",
            "Data status": "Approximation: 1600 kVA loss intensity scaled by kVA/class",
        },
        {
            "Scope": "3.12 — EOL of sold products",
            "GHG Category": "Module D beyond-boundary recovery credit (net negative)",
            "Lifecycle stage": "C1–C4 + D (Module D credit only)",
            "Source module": "Module 2 (Circularity & EOL Planner) — decommissioning branch",
            "Value (t CO₂e/yr)": -round(abs(scope3_12_t), 1)
            if scope3_12_available
            else "—",
            "Share": "n/a (beyond-boundary credit)",
            "Data status": "Available"
            if scope3_12_available
            else "Run Module 2 (decom.) first — gross C1–C4 awaits Phase 2",
        },
    ]
    report_df = pd.DataFrame(report_rows)
    st.dataframe(report_df, use_container_width=True, hide_index=True)

    net_total = (
        scope1_t
        + scope2_t
        + scope3_1_t
        + scope3_11_t
        - (abs(scope3_12_t) if scope3_12_available else 0.0)
    )
    st.caption(
        f"**Net total (gross scopes + Module D credit):** {net_total:,.0f} t CO₂e/yr. "
        "Module D credit is beyond-boundary per EN 15804 — shown for transparency, not netted by default in CSRD disclosure."
    )

    st.markdown("**Scope distribution (gross)**")
    chart_rows = [
        {"Scope": "1 — Direct", "t CO₂e/yr": scope1_t},
        {"Scope": "2 — Purchased energy", "t CO₂e/yr": scope2_t},
        {
            "Scope": "3.1 — Purchased goods",
            "t CO₂e/yr": scope3_1_t if scope3_1_available else 0.0,
        },
        {"Scope": "3.11 — Use of sold products", "t CO₂e/yr": scope3_11_t},
    ]
    chart_df = pd.DataFrame(chart_rows)
    fig_scope = px.bar(
        chart_df,
        x="Scope",
        y="t CO₂e/yr",
        color="Scope",
        title="Annual GHG emissions by scope (gross, t CO₂e/yr)",
    )
    fig_scope.update_layout(
        plot_bgcolor="#0e1117",
        paper_bgcolor="#0e1117",
        font_color="white",
        showlegend=False,
        height=380,
    )
    st.plotly_chart(fig_scope, use_container_width=True)

    st.markdown("**Scope hotspot view — gross shares (100% normalized)**")
    if not scope3_1_available:
        st.info(
            "ℹ️ Run Module 3 (Portfolio CO₂ Simulator) first to populate Scope 3.1 — "
            "the 100% normalized view needs it to avoid misreading shares. "
            "Scopes 1, 2, and 3.11 are always computed from sourced defaults."
        )
    else:
        total_gross_t = scope1_t + scope2_t + scope3_1_t + scope3_11_t
        if total_gross_t <= 0:
            st.caption("Total gross emissions are zero — nothing to normalize.")
        else:
            share_rows = [
                {
                    "Scope": "1 — Direct",
                    "Share (%)": scope1_t / total_gross_t * 100,
                    "Abs (t CO₂e/yr)": scope1_t,
                },
                {
                    "Scope": "2 — Purchased energy",
                    "Share (%)": scope2_t / total_gross_t * 100,
                    "Abs (t CO₂e/yr)": scope2_t,
                },
                {
                    "Scope": "3.1 — Purchased goods",
                    "Share (%)": scope3_1_t / total_gross_t * 100,
                    "Abs (t CO₂e/yr)": scope3_1_t,
                },
                {
                    "Scope": "3.11 — Use of sold products",
                    "Share (%)": scope3_11_t / total_gross_t * 100,
                    "Abs (t CO₂e/yr)": scope3_11_t,
                },
            ]
            share_df = pd.DataFrame(share_rows)
            fig_stack = go.Figure()
            for _, r in share_df.iterrows():
                fig_stack.add_trace(
                    go.Bar(
                        name=r["Scope"],
                        x=["Portfolio scope mix"],
                        y=[r["Share (%)"]],
                        text=[
                            f"{r['Share (%)']:.1f}%<br>({r['Abs (t CO₂e/yr)']:,.0f} t/yr)"
                        ],
                        textposition="inside",
                        hovertemplate=(
                            f"{r['Scope']}<br>"
                            f"Share: {r['Share (%)']:.1f}%<br>"
                            f"Absolute: {r['Abs (t CO₂e/yr)']:,.0f} t CO₂e/yr"
                            "<extra></extra>"
                        ),
                    )
                )
            fig_stack.update_layout(
                barmode="stack",
                title="Scope hotspot view — gross GHG emissions by share (%)",
                yaxis_title="Share of gross emissions (%)",
                yaxis=dict(range=[0, 100], ticksuffix="%"),
                plot_bgcolor="#0e1117",
                paper_bgcolor="#0e1117",
                font_color="white",
                legend=dict(orientation="h", yanchor="bottom", y=1.02),
                height=420,
                showlegend=True,
            )
            st.plotly_chart(fig_stack, use_container_width=True)
            st.caption(
                "Bar sums to 100% of gross Scope 1 + 2 + 3.1 + 3.11. Module D "
                "(Scope 3.12) is a beyond-boundary credit per EN 15804 and is not "
                "netted into this view. The largest segment is the scope hotspot."
            )

    st.download_button(
        "⬇ Export GHG Scope 1/2/3 Report (CSV)",
        report_df.to_csv(index=False).encode("utf-8"),
        file_name="ghg_scope_1_2_3_report.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.divider()
    st.subheader("📋 What is NOT in this report (honest-scope disclosure)")
    st.warning(
        "- **Scope 1 — fugitive SF₆ emissions:** not modelled — Phase 2 (gas-insulated switchgear leakage data).\n"
        "- **Scope 3.4 — upstream transport (A4–A5):** not in any module — Phase 2.\n"
        "- **Scope 3.12 gross C1–C4:** Module 2 only quantifies the Module D recovery credit; gross "
        "end-of-life emissions (deconstruction, transport, processing, disposal) await Phase 2 partner "
        "process data.\n"
        "- **Other Scope 3 categories:** business travel (Cat 6), employee commuting (Cat 7), upstream/downstream leases, "
        "investments (Cat 15) — outside this tool's boundary; use corporate carbon platforms.\n"
        "- **Module D netting:** shown for transparency. Standard CSRD practice reports it separately as beyond-boundary credit, "
        "not netted against gross Scope 3 totals."
    )

elif module == "5. About & Source Code":
    st.header("About & Source Code")
    st.markdown(
        """
        This app is an open-source concept prototype demonstrating a bottom-up CO₂ management
        workflow for transformer portfolios — covering use-phase TCO & carbon, circularity
        planning, and embodied carbon simulation across lifecycle stages A1–A3, B1–B6 and
        C1–C4 + Module D.
        """
    )
    st.divider()

    col_gh, col_demo = st.columns(2)
    with col_gh:
        st.markdown(
            """
            ### Source Code
            All source code, `requirements.txt`, and documentation are available on GitHub.

            [![GitHub](https://img.shields.io/badge/GitHub-lugasraka%2FCO2--calculator--prototype--transformer-181717?logo=github&logoColor=white)](https://github.com/lugasraka/CO2-calculator-prototype-transformer)

            **[github.com/lugasraka/CO2-calculator-prototype-transformer](https://github.com/lugasraka/CO2-calculator-prototype-transformer)**
            """
        )
    with col_demo:
        st.markdown(
            """
            ### Live Demo
            The app is deployed on Streamlit Community Cloud.

            [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://co2-calculator-prototype-transformer.streamlit.app/)

            **[co2-calculator-prototype-transformer.streamlit.app](https://co2-calculator-prototype-transformer.streamlit.app/)**
            """
        )

    st.divider()
    st.markdown("### Product Vision")
    st.markdown(
        """
        > Make embodied and lifecycle carbon a *quantifiable, comparable, and auditable* input
        > to every transformer design, sourcing, and R&D decision — turning sustainability
        > from an after-the-fact report into a live engineering condition.

        Today carbon is measured **after** the product is designed, not **while** it is being
        designed. This tool puts a fast, credible CO₂ number in front of the engineer at the
        moment the decision is made.
        """
    )
    st.divider()

    st.markdown("### Modules")
    st.markdown(
        """
        | Module | Lifecycle Scope | Description |
        |--------|-----------------|-------------|
        | **1. TCO & Carbon ROI** | B1–B6 (use phase) | Lifetime cost & carbon of standard vs. high-efficiency designs — NPV TCO, lifetime CO₂ savings, and payback |
        | **2. Circularity & EOL Planner** | C1–C4 + Module D | Retrofill vs. decommissioning trade-offs and Module D recovery credits from sourced recovery rates |
        | **3. Portfolio CO₂ Simulator ★** | A1–A3 (cradle-to-gate) | Bottom-up embodied carbon from BOM → portfolio, with factor-uncertainty bounds, kg CO₂e/kVA gate KPIs, and per-lever abatement cost (€/t CO₂e) |
        | **4. GHG Scope 1/2/3 Report** | Corporate (Scope 1 + 2 + 3.1/3.11/3.12) | Rebuckets Modules 1–3 outputs into GHG-Protocol scopes for CSRD/SBTi-style annual corporate reporting; Scope 1 & 2 use indicative factory-energy estimates (`data/factory_energy.csv`) until Phase 2 metered data |
        """
    )
    st.divider()

    st.markdown("### Roadmap at a Glance")
    st.markdown(
        """
        | Phase | Theme | Status | Key items |
        |-------|-------|--------|-----------|
        | **1 — Foundation & Trust** | Make the numbers real and defensible | ✅ Done | Sourced CSV data layer, provenance + uncertainty, scenario save/compare/export, gate KPIs, €/t abatement ranking |
        | **2 — Real Data Integration** | Connect to live enterprise systems | 🔜 3–9 mo | Partner factor/EPD feeds (not a self-built database), real PLM/ERP BOM ingestion, full cradle-to-grave unification |
        | **3 — Decision Intelligence** | From calculator to advisor | 🔮 9–18 mo | MAC curves as signature output, cost-optimal CO₂ targeting, gate-KPI artifacts, Monte Carlo sensitivity |
        | **4 — Platform & Scale** | Multi-user, governed, integrated | 🌐 18 mo+ | Open PLM-gate API (OpenEPD/ILCD-aligned), multi-tenant, third-party methodology validation |
        """
    )
    with st.expander("Full roadmap detail (Phase 1–4)"):
        st.markdown(
            """
            **✅ Phase 1 — Foundation & Trust (current):** sourced CSV data layer (`data/` via
            `data_layer.py`) with provenance, uncertainty ranges and validity dates; scenario
            save/compare/export (SQLite); uncertainty bounds, kg CO₂e/kVA gate KPI, per-lever
            €/t abatement cost, and a data-freshness banner in outputs.

            **🔜 Phase 2 — Real Data Integration (3–9 mo):** partner factor/EPD feeds behind the
            same data-layer interface (evaluate sustamize's factor API, One Click LCA's
            ILCD+EPD / OpenEPD outputs); actual BOM from PLM/ERP via standard import formats;
            full cradle-to-grave unification (A1–C4 + Module D); supplier-specific factors;
            A4–A5 coverage.

            **🔮 Phase 3 — Decision Intelligence (9–18 mo):** per-lever €/t ranking extended to
            full marginal abatement cost curves (linking Modules 1 + 3); cost-optimal lever
            selection ("hit −30% CO₂ at minimum cost"); exportable gate-KPI artifacts;
            Monte Carlo over uncertainty ranges; SBTi targets as constraints only.

            **🌐 Phase 4 — Platform & Scale (18 mo+):** multi-tenant role-based access; narrow
            open gate API with OpenEPD/ILCD-aligned exports; third-party methodology validation
            (GUTcert / DEKRA pattern); regional grid factors, multi-currency; CBAM/CSRD inputs
            to dedicated reporting tools rather than a competing engine.

            See `ROADMAP.md` for the full vision and data-model evolution.
            """
        )
    st.divider()

    st.markdown("### Competitive Position (July 2026)")
    st.markdown(
        """
        A landscape scan of five adjacent vendors (Makersite, sustamize, carbmee,
        Sphera/GaBi, One Click LCA):

        - **Commoditized:** BOM-based A1–A3 PCF — all five ship it. Not our moat.
        - **Uncontested (ours):** use-phase loss economics (B1–B6 → TCO/payback), gate-ready
          kg CO₂e/kVA, per-lever €/t abatement ranking, quantified factor uncertainty — plus
          open-source, engineer-first adoption that quote-only enterprise vendors can't match.
        - **Strategy:** partner for data (sustamize, One Click LCA), interoperate with
          PCF-exchange networks, out-run everyone on the decision layer.
        """
    )
    with st.expander("Full competitive landscape scan"):
        st.markdown(
            """
            Detailed per-competitor analyses and the synthesis live in the repo under
            `competitors/`:

            - `summarize-competitor.md` — capability matrix, positioning map, threat ranking & watch triggers
            - `competitor-makersite.md` — **primary threat (High, directional):** ships the
              cost+carbon-in-PLM thesis horizontally; owns PCF-exchange rails (SiGREEN → Mattermaps)
            - `competitor-sustamize.md` · `competitor-carbmee.md` ·
              `competitor-sphera-gabi.md` · `competitor-one-click-lca.md`

            Beachheads in our vertical already exist — Schneider Electric (Makersite,
            One Click LCA) and Siemens Energy (carbmee) — but no transformer-specific
            product yet.
            """
        )
    st.divider()

    st.markdown("### Glossary")
    st.markdown(
        """
        - **EPD (Environmental Product Declaration)** — standardized, independently verified
          report of a product's lifecycle environmental impacts, including embodied CO₂.
        - **CBAM (Carbon Border Adjustment Mechanism)** — EU carbon levy on imported goods,
          driving demand for verified product carbon footprints.
        - **CSRD (Corporate Sustainability Reporting Directive)** — EU directive mandating
          audited sustainability disclosure, including Scope 3 emissions.
        - **SBTi (Science Based Targets initiative)** — framework for corporate emission-reduction
          targets aligned with climate science.
        - **Module D** — EN 15804 lifecycle stage crediting benefits beyond the system boundary
          (e.g. recycling credits from recovered copper and steel).
        - **kg CO₂e/kVA** — embodied carbon normalized by transformer rating; the gate-ready KPI
          enabling cross-class comparison at PLM design reviews.
        """
    )
    st.divider()
    st.markdown("### Author")
    st.markdown(
        "Raka Adrianto · Sustainability, Product, Data · "
        "[LinkedIn](https://www.linkedin.com/in/lugasraka/)"
    )
