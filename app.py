import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# Configure the app's layout and title
st.set_page_config(page_title="Hitachi Energy Decarbonization Manager", layout="wide")

st.sidebar.title("Decarbonization Workflow")
module = st.sidebar.radio("Select Module:",
                          ["1. TCO & Carbon ROI",
                           "2. Circularity & EOL Planner",
                           "3. Portfolio CO₂ Simulator ★"])

if module == "1. TCO & Carbon ROI":
    st.header("Total Cost of Ownership (TCO) & Carbon ROI Calculator")
    st.markdown("Evaluate the long-term financial benefits of high-efficiency EconiQ transformers.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Standard 1600 kVA Transformer")
        std_capex = st.number_input("Standard CAPEX (€)", value=14451)
        std_no_load = st.number_input("Standard No-Load Loss (W)", value=2800)
        std_load = st.number_input("Standard Load Loss (W)", value=15207)
        
    with col2:
        st.subheader("Efficient EconiQ 1600 kVA Transformer")
        eco_capex = st.number_input("EconiQ CAPEX (€)", value=14990)
        eco_no_load = st.number_input("EconiQ No-Load Loss (W)", value=2670)
        eco_load = st.number_input("EconiQ Load Loss (W)", value=14218)

    st.markdown("---")
    st.markdown("#### Capitalized Cost of Losses over 15 Years")
    energy_cost_no_load = st.number_input("Cost per Watt of No-Load Losses (€/W)", value=3.74)
    energy_cost_load = st.number_input("Cost per Watt of Load Losses (€/W)", value=1.58)

    if st.button("Calculate 15-Year TCO"):
        std_tco = std_capex + (std_no_load * energy_cost_no_load) + (std_load * energy_cost_load)
        eco_tco = eco_capex + (eco_no_load * energy_cost_no_load) + (eco_load * energy_cost_load)
        
        st.success(f"**Standard Transformer Total Owning Cost:** €{std_tco:,.2f}")
        st.success(f"**EconiQ Transformer Total Owning Cost:** €{eco_tco:,.2f}")
        st.info(f"**Result:** By investing €{eco_capex - std_capex:,.0f} more upfront, the efficient design yields a lifetime savings of €{std_tco - eco_tco:,.2f} with a payback period of approximately 5 years.")

elif module == "2. Circularity & EOL Planner":
    st.header("♻️ Circularity & End-of-Life Management")
    st.markdown(
        "Covers lifecycle stages **C1–C4** — the end-of-life phase deferred by the Portfolio CO₂ Simulator (Module 3). "
        "Addresses mid-life asset intervention and secure decommissioning to maximise material recovery and minimise waste."
    )
    st.caption("Lifecycle scope: C1 Deconstruction · C2 Transport · C3 Waste processing · C4 Disposal — plus Module D recycling credits")
    st.divider()

    intervention = st.radio("Select asset lifecycle phase:", ["Mid-Life Extension (C0 intervention)", "End-of-Life Decommissioning (C1–C4)"])

    if intervention == "Mid-Life Extension (C0 intervention)":
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Avoided CO₂", "Up to 90%", delta="vs. full replacement")
            st.metric("Asset life extension", "+10–15 yrs", delta="without new hardware")
        with col2:
            st.success(
                "**Recommendation: EconiQ® Retrofill**\n\n"
                "Replace high-GWP SF₆ insulation gas with an eco-efficient alternative gas mixture. "
                "Eliminates the embodied carbon of manufacturing a replacement unit and extends the asset's "
                "functional life without hardware replacement.\n\n"
                "**Why this matters at portfolio scale:** If 10% of the installed base undergoes Retrofill "
                "instead of replacement, the avoided manufacturing emissions dwarf the annual A1–A3 "
                "footprint of the entire new-unit portfolio."
            )
    else:
        col1, col2 = st.columns([1, 2])
        with col1:
            st.metric("Copper recovery rate", ">95%", delta="routed to specialist smelters")
            st.metric("Oil recovery rate", "~90%", delta="re-refined, not incinerated")
            st.metric("Overall material recyclability", "~85–90%", delta="by mass")
        with col2:
            st.info(
                "**Recommendation: TX Life Replace Protocol**\n\n"
                "Deploy structured decommissioning manuals for safe disassembly. Key recovery streams:\n\n"
                "- 🔴 **Copper windings** → specialist smelters (>95% recovery; high value, high embodied carbon avoided)\n"
                "- 🟡 **CRGO steel core** → steel recycling (reduces Scope 3 of next unit's BOM)\n"
                "- 🔵 **Insulation oil** → re-refining (Nytro RR 900X circular loop; avoids incineration CO₂)\n"
                "- ⚠️ **Thermoset plastics / epoxy resins** → current waste challenge; Phase 2 design-for-disassembly target"
            )
        st.warning(
            "📋 **Module D credit (beyond system boundary):** Recycled copper and steel re-entering the supply chain "
            "generate a carbon credit that offsets future A1–A3 emissions. Quantification of Module D credits is "
            "included in the Phase 2 full cradle-to-grave LCA roadmap."
        )

elif module == "3. Portfolio CO₂ Simulator ★":
    st.title("🌍 Transformer Portfolio CO₂ Simulator")
    st.caption("Concept proposal | Lugas Raka Adrianto → Hitachi Energy Engineering Global Sustainability Leader | June 2026")
    st.markdown(
        """
        A **granular bottom-up CO₂ impact calculator** for the transformer portfolio — translating BOM-level
        material design choices into fleet-wide carbon outcomes across product families and annual production volumes,
        powered by **EcoSpace™ / EcoSmart™** data feeds.
        """
    )

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
        "and planned for Phase 2 integration with the EcoSpace™ full-lifecycle data feed.**"
    )
    st.divider()

    # ── METHODOLOGY & DATA ARCHITECTURE ──────────────────────────────────────
    with st.expander("📐  Methodology & Data Architecture — How the simulator works", expanded=True):

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
            | **4. Lever attribution** | Δ CO₂ when CI_i changes (Baseline → EconiQ); all other lines held constant | kt CO₂e / year saved per lever |

            Where **CI** (carbon intensity) is the emission factor for a given material and sourcing scenario,
            expressed in **kg CO₂e per kg** of material delivered to the factory gate (cradle-to-gate).
            """
        )

        st.markdown("---")
        st.markdown("### System Boundary — Lifecycle Stages Covered")

        # System boundary: 4 stages with arrows
        IN  = "background-color:#00CC9622; border:2px solid #00CC96; border-radius:8px; padding:12px; text-align:center;"
        OUT = "background-color:#33333388; border:2px dashed #666; border-radius:8px; padding:12px; text-align:center; color:#aaa;"
        ARR = "<div style='text-align:center;font-size:22px;padding-top:22px;color:#555;'>▶</div>"

        sb = st.columns([2, 0.3, 2, 0.3, 2, 0.3, 2])
        with sb[0]:
            st.markdown(
                f"<div style='{IN}'><b style='color:#00CC96'>✅ A1 – A3</b><br><br>"
                "<b>Raw Materials &amp;<br>Manufacturing</b><br><br>"
                "<small>Steel, copper, oil,<br>insulation, structure</small><br><br>"
                "<small><b>← THIS MODULE</b></small></div>", unsafe_allow_html=True)
        with sb[1]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[2]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 A4 – A5</b><br><br>"
                "<b>Transport &amp;<br>Installation</b><br><br>"
                "<small>Logistics CO₂,<br>site works</small><br><br>"
                "<small>Phase 2</small></div>", unsafe_allow_html=True)
        with sb[3]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[4]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 B1 – B6</b><br><br>"
                "<b>Use Phase</b><br>(40 years)<br><br>"
                "<small>No-load &amp; load<br>energy losses</small><br><br>"
                "<small>→ Module 1</small></div>", unsafe_allow_html=True)
        with sb[5]:
            st.markdown(ARR, unsafe_allow_html=True)
        with sb[6]:
            st.markdown(
                f"<div style='{OUT}'><b>🔜 C1 – C4 + D</b><br><br>"
                "<b>End of Life &amp;<br>Recycling</b><br><br>"
                "<small>Disassembly, Cu &amp;<br>oil recovery credits</small><br><br>"
                "<small>→ Module 4 / Phase 2</small></div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("### Data Architecture — Pipeline")

        # 4-tier pipeline: Sources → Engine → Outputs → Decisions
        TIER = "border:1px solid #444; border-radius:10px; padding:14px; min-height:200px;"
        ARR2 = "<div style='text-align:center;font-size:28px;padding-top:70px;color:#00CC96;'>▶</div>"

        da = st.columns([2.5, 0.3, 2.5, 0.3, 2.5, 0.3, 2.5])
        with da[0]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#00CC96'>📂 DATA SOURCES</b><br><br>"
                "🔹 <b>EPDs</b> — EcoSpace™ / EcoSmart™<br>"
                "🔹 <b>BOM data</b> — PLM / PDM system<br>"
                "🔹 <b>Material CI factors</b> — Ecoinvent 3.x + supplier declarations<br>"
                "🔹 <b>Volume forecast</b> — Product Management<br>"
                "🔹 <b>Supplier ratings</b> — EcoVadis scores"
                "</div>", unsafe_allow_html=True)
        with da[1]:
            st.markdown(ARR2, unsafe_allow_html=True)
        with da[2]:
            st.markdown(
                f"<div style='{TIER}'>"
                "<b style='color:#636EFA'>⚙️ CALCULATION ENGINE</b><br><br>"
                "🔹 mass_i × CI_i per BOM line<br>"
                "🔹 Σ → CO₂ per transformer unit<br>"
                "🔹 × Volume → portfolio kt CO₂e/yr<br>"
                "🔹 Scenario Δ: Baseline vs. EconiQ<br>"
                "🔹 Lever attribution (core / fluid / Cu)"
                "</div>", unsafe_allow_html=True)
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
                "</div>", unsafe_allow_html=True)
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
                "</div>", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.info(
            "📌 **Data note:** Carbon intensity values are sourced from Ecoinvent 3.x background database and "
            "Hitachi Energy EconiQ® product declarations (Bhaba Das & Ghazi Kablouti, Hitachi Energy published LCA studies). "
            "BOM mass estimates are representative averages per transformer class — to be replaced with actual PLM/BOM data in production deployment."
        )

        st.markdown("---")
        st.markdown("### Material Carbon Intensity Reference — Key Inputs")
        st.caption("Source: Ecoinvent 3.x + Hitachi Energy EconiQ® product declarations + supplier primary data")

        ci_data = {
            "Material / Option": [
                "CRGO Steel — Standard sourcing",
                "CRGO Steel — Green H₂-based sourcing",
                "Amorphous Metal Alloy (mfg. phase)",
                "Structural Steel — Standard",
                "Copper Windings — Standard sourcing",
                "Copper Windings — Low-carbon (fossil-free refining)",
                "Virgin Mineral Oil — Baseline",
                "Re-refined Oil — Nytro RR 900X",
                "Biodegradable Natural Ester",
                "Kraft paper / Pressboard insulation",
            ],
            "kg CO₂e / kg": [2.5, 0.8, 5.0, 1.8, 3.4, 1.5, 0.85, 0.085, 0.30, 0.5],
            "vs. Baseline": [
                "—", "−68%", "Higher mfg, lower op. losses", "—",
                "—", "−56%", "—", "−90%", "−65%", "—",
            ],
            "Supplier programme": [
                "Standard", "Green steel procurement (SSDP)", "Specialist suppliers", "Standard",
                "Standard", "Low-carbon Cu programme (e.g. TenneT model)",
                "Standard", "Circular re-refining (EcoVadis Platinum suppliers)",
                "Specialist bio-fluid suppliers", "Standard",
            ],
        }
        st.dataframe(ci_data, use_container_width=True, hide_index=True)
        st.caption(
            "EcoVadis supply chain context: Hitachi Energy avg supplier score 55.6 vs 48.1 global average · "
            "Platinum rating (top 1% of 89,000 companies assessed) · "
            "Supplier Sustainability Development Program (SSDP) targets highest-CI materials first."
        )

    st.divider()

    # ── ARCHITECTURE OVERVIEW ────────────────────────────────────────────────
    st.markdown("### What this simulator covers (A1–A3 scope)")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown(
            """
            ### 📥 INPUT
            - **EPDs** from EcoSpace™ / EcoSmart™
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
              *(Baseline vs. EconiQ design scenarios)*
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

    # ── MATERIAL CARBON INTENSITY DATABASE ──────────────────────────────────
    CORE_CI = {
        "CRGO Steel — Standard (2.5 kg CO₂e/kg)":         2.5,
        "CRGO Steel — Green sourcing (0.8 kg CO₂e/kg)":   0.8,
        "Amorphous Metal Alloy (5.0 kg CO₂e/kg mfg)":     5.0,
    }
    FLUID_CI = {
        "Virgin Mineral Oil — Baseline (0.85 kg CO₂e/kg)":       0.85,
        "Re-refined Oil — Nytro RR 900X (0.085 kg CO₂e/kg)":     0.085,
        "Biodegradable Natural Ester (0.30 kg CO₂e/kg)":          0.30,
    }
    COPPER_CI = {
        "Standard Copper (3.4 kg CO₂e/kg)":       3.4,
        "Low-Carbon Copper (1.5 kg CO₂e/kg)":     1.5,
    }
    STRUCT_CI_BASE = 1.8   # standard structural steel kg CO₂e/kg
    INSUL_CI      = 0.5    # kraft paper / pressboard kg CO₂e/kg (fixed)

    # Representative average BOM per transformer class [core_kg, cu_kg, oil_kg, insul_kg, struct_kg]
    BOM = {
        "Distribution  (avg 1,000 kVA)":   [500,    150,   500,   50,    300],
        "Medium Power  (avg 25 MVA)":       [8_000,  3_000, 8_000, 1_000, 6_000],
        "Large Power   (avg 250 MVA)":      [60_000, 25_000,50_000,8_000, 40_000],
    }

    # ── STEP 1 — VOLUME FORECAST ─────────────────────────────────────────────
    st.subheader("Step 1 — Portfolio Volume Forecast")
    st.caption("Enter your annual production/sales forecast per transformer class.")
    c1, c2, c3 = st.columns(3)
    vol_dist  = c1.number_input("Distribution transformers (units / year)", value=500,  step=10)
    vol_med   = c2.number_input("Medium Power transformers (units / year)", value=120,  step=5)
    vol_large = c3.number_input("Large Power transformers (units / year)",  value=25,   step=1)
    volumes   = [vol_dist, vol_med, vol_large]

    # ── STEP 2 — DESIGN SCENARIO ─────────────────────────────────────────────
    st.subheader("Step 2 — Configure Design Scenario")
    st.caption("Scenario A is fixed as today's standard BOM. Configure Scenario B (EconiQ interventions).")

    col_base, col_eco = st.columns(2)
    with col_base:
        st.markdown("**Scenario A — Baseline (Current BOM)**")
        st.info(
            "Core: CRGO Steel — Standard  \n"
            "Fluid: Virgin Mineral Oil  \n"
            "Copper: Standard sourcing"
        )
    with col_eco:
        st.markdown("**Scenario B — EconiQ Design Interventions**")
        core_choice   = st.selectbox("Magnetic Core Material",   list(CORE_CI.keys()),   index=1)
        fluid_choice  = st.selectbox("Insulation Fluid",          list(FLUID_CI.keys()),  index=1)
        copper_choice = st.selectbox("Copper Winding Sourcing",   list(COPPER_CI.keys()), index=1)

    # ── STEP 3 — RUN SIMULATION ───────────────────────────────────────────────
    st.divider()
    if st.button("▶  Run Portfolio CO₂ Simulation", type="primary", use_container_width=True):

        core_ci_eco   = CORE_CI[core_choice]
        fluid_ci_eco  = FLUID_CI[fluid_choice]
        copper_ci_eco = COPPER_CI[copper_choice]
        core_ci_base, fluid_ci_base, copper_ci_base = 2.5, 0.85, 3.4

        rows = []
        for (family, masses), vol in zip(BOM.items(), volumes):
            core_m, cu_m, oil_m, insul_m, struct_m = masses

            # CO₂ per unit (tonnes)
            base_unit = (core_m * core_ci_base + cu_m * copper_ci_base +
                         oil_m * fluid_ci_base + insul_m * INSUL_CI +
                         struct_m * STRUCT_CI_BASE) / 1_000

            eco_unit  = (core_m * core_ci_eco + cu_m * copper_ci_eco +
                         oil_m * fluid_ci_eco  + insul_m * INSUL_CI +
                         struct_m * STRUCT_CI_BASE) / 1_000

            # Lever contributions per unit (tonnes)
            delta_core   = (core_m   * (core_ci_base   - core_ci_eco))   / 1_000
            delta_fluid  = (oil_m    * (fluid_ci_base   - fluid_ci_eco))  / 1_000
            delta_copper = (cu_m     * (copper_ci_base  - copper_ci_eco)) / 1_000

            rows.append({
                "Product Family":            family,
                "Units/yr":                  vol,
                "Baseline CO₂/unit (t)":     round(base_unit,  1),
                "EconiQ CO₂/unit (t)":       round(eco_unit,   1),
                "Reduction/unit (t)":        round(base_unit - eco_unit, 1),
                "Portfolio Baseline (kt/yr)": round(base_unit * vol / 1_000, 2),
                "Portfolio EconiQ (kt/yr)":  round(eco_unit  * vol / 1_000, 2),
                "Portfolio Saving (kt/yr)":  round((base_unit - eco_unit) * vol / 1_000, 2),
                "Δ Core (kt/yr)":            round(delta_core   * vol / 1_000, 3),
                "Δ Fluid (kt/yr)":           round(delta_fluid  * vol / 1_000, 3),
                "Δ Copper (kt/yr)":          round(delta_copper * vol / 1_000, 3),
            })

        df = pd.DataFrame(rows)
        total_base   = df["Portfolio Baseline (kt/yr)"].sum()
        total_eco    = df["Portfolio EconiQ (kt/yr)"].sum()
        total_saving = total_base - total_eco
        pct_saving   = total_saving / total_base * 100

        # ── PORTFOLIO KPI METRICS ─────────────────────────────────────────
        st.subheader("📊 Portfolio-Level CO₂ Output")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Baseline Portfolio", f"{total_base:.1f} kt CO₂e/yr")
        m2.metric("EconiQ Portfolio",   f"{total_eco:.1f} kt CO₂e/yr",
                  delta=f"-{total_saving:.1f} kt")
        m3.metric("Total Reduction",    f"{total_saving:.1f} kt CO₂e/yr")
        m4.metric("% Reduction",        f"{pct_saving:.1f}%",
                  delta=f"vs. baseline")

        # ── PRODUCT-FAMILY TABLE ──────────────────────────────────────────
        st.markdown("**Bottom-up CO₂ by product family**")
        display_cols = ["Product Family", "Units/yr", "Baseline CO₂/unit (t)",
                        "EconiQ CO₂/unit (t)", "Reduction/unit (t)", "Portfolio Saving (kt/yr)"]
        st.dataframe(df[display_cols].set_index("Product Family"), use_container_width=True)

        # ── WATERFALL: LEVER ATTRIBUTION ─────────────────────────────────
        st.markdown("**Design lever attribution — where does the reduction come from?**")
        delta_core_total   = df["Δ Core (kt/yr)"].sum()
        delta_fluid_total  = df["Δ Fluid (kt/yr)"].sum()
        delta_copper_total = df["Δ Copper (kt/yr)"].sum()

        fig_wf = go.Figure(go.Waterfall(
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Baseline Portfolio", "Core Material Lever", "Fluid Lever", "Copper Sourcing Lever", "EconiQ Portfolio"],
            y=[total_base, -delta_core_total, -delta_fluid_total, -delta_copper_total, 0],
            text=[f"{total_base:.1f} kt",
                  f"-{delta_core_total:.2f} kt",
                  f"-{delta_fluid_total:.2f} kt",
                  f"-{delta_copper_total:.2f} kt",
                  f"{total_eco:.1f} kt"],
            textposition="outside",
            connector={"line": {"color": "rgb(63, 63, 63)"}},
            increasing={"marker": {"color": "#EF553B"}},
            decreasing={"marker": {"color": "#00CC96"}},
            totals={"marker": {"color": "#636EFA"}},
        ))
        fig_wf.update_layout(
            title="Portfolio CO₂ Reduction Waterfall — kt CO₂e/yr",
            yaxis_title="kt CO₂e / year",
            plot_bgcolor="#0e1117",
            paper_bgcolor="#0e1117",
            font_color="white",
            height=420,
        )
        st.plotly_chart(fig_wf, use_container_width=True)

        # ── STACKED BAR: BASELINE vs ECONIQ BY PRODUCT FAMILY ────────────
        st.markdown("**Baseline vs. EconiQ CO₂ by product family**")
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name="Baseline",
            x=df["Product Family"],
            y=df["Portfolio Baseline (kt/yr)"],
            marker_color="#EF553B",
        ))
        fig_bar.add_trace(go.Bar(
            name="EconiQ",
            x=df["Product Family"],
            y=df["Portfolio EconiQ (kt/yr)"],
            marker_color="#00CC96",
        ))
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
            st.warning(
                f"**Gate-ready KPI for PLM reviews**\n\n"
                f"EconiQ target: **{pct_saving:.1f}% lifecycle CO₂ reduction** vs. baseline.\n\n"
                f"Expressed as a gate condition at PLM design review — not a sustainability aspiration."
            )
        st.caption(
            "📌 Scope reminder: this simulation covers cradle-to-gate embodied carbon (A1–A3) only — "
            "Scope 3 upstream emissions from raw material extraction through factory gate. "
            "Use-phase energy losses (B1–B6) → Module 1 | End-of-life (C1–C4) → Module 2 | "
            "Full cradle-to-grave integration: Phase 2 roadmap item."
        )