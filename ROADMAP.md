# Product Vision & Roadmap

> **Vision:** Give transformer design, sourcing, and R&D teams a carbon number they can
> compare and audit while decisions are still open.

---

## The problem

Transformer manufacturers face pressure from regulation (CBAM, CSRD), science-based
targets (SBTi), and customers to cut carbon. The data needed to act on it is fragmented:
carbon factors sit in LCA databases, material masses in PLM/BOM systems, and cost in ERP.
Those sources are rarely connected to the moment a design decision is made.

As a result, teams often measure carbon after the product is designed. Material choice,
sourcing, and efficiency class are decided without a fast, credible CO₂ number in front
of the engineer.

## The product

A decision-support platform that translates **material and design choices** into
**fleet-wide carbon outcomes**. R&D and procurement teams can compare reductions before
they commit to a design.

Today it is a Streamlit prototype with four modules mapped to lifecycle stages and
corporate reporting scopes:

| Module | Lifecycle scope | Job-to-be-done |
|--------|-----------------|----------------|
| **1. TCO & Carbon ROI** | Use-phase (B1–B6) | Justify high-efficiency units via lifetime TCO, use-phase carbon savings, and payback |
| **2. Circularity & EOL Planner** | End-of-life (C1–C4 + D) | Quantify retrofill vs. decommission trade-offs and the Module D recovery credit from sourced recovery rates |
| **3. Portfolio CO₂ Simulator** | Cradle-to-gate (A1–A3) | Calculates embodied carbon from BOM to portfolio, recommends feasible material combinations, compares saved design-gate runs, and reports Monte Carlo intervals (P10/P50/P90) |
| **4. GHG Scope 1/2/3 Report** | Corporate (Scope 1 + 2 + 3.1/3.11/3.12) | Rebuckets Modules 1–3 into GHG Protocol scopes for annual reporting. Scope 1 and 2 use indicative factory-energy estimates (`data/factory_energy.csv`) until Phase 2 adds metered data |

**Target users:** R&D / design engineers, sustainability leads, procurement & supply-chain
teams, and PLM gate reviewers.

---

## Guiding principles

1. **Separate the model from the data.** Formulas live in code; coefficients, BOMs, and
  scenarios live in a sourced, versioned data store. Later phases can replace the data
  source without rewriting the engine or UI.
2. **Show where each number comes from.** Each carbon factor carries provenance (source,
  version, validity dates) and an uncertainty range.
3. **State the boundary.** The tool names the lifecycle stages it covers and the stages
  it does not.
4. **Recommend a design.** The long-term goal is to find the lowest-cost path to a
  carbon target, not only calculate a footprint.
5. **Partner for data; build the decision layer.** BOM-based PCF factor data is
  commoditized (see [competitive scan](competitors/summarize-competitor.md)). The
  product's differentiation is what it calculates on top of the data: loss economics,
  gate KPIs, and abatement cost.

---

## Roadmap

### Phase 1 - Foundation & Trust (current)
**Theme: sourced inputs and traceable outputs.**

- Move all coefficients and BOM masses out of code into sourced CSVs (`data/`), read
  through `data_layer.py`.
- Provenance per factor: source, version, validity dates.
- Uncertainty ranges (low / expected / high) on carbon factors.
- Save, name, and compare scenarios; persist runs in SQLite (`scenario_store.py`).
- Design-Gate Comparison for engineers: compare one saved baseline with up to three
  alternatives; show carbon, cost, abatement cost, and uncertainty; export the
  comparison; and make a transparent carbon-first recommendation.
- **Cost-ceiling constraint in design-gate comparison:** an engineer sets a maximum material
  cost premium (%) vs. the baseline's green premium; alternatives above the ceiling are
  flagged and excluded from the recommendation (with the exclusion named in the success
  message). This gives procurement a cost boundary for carbon-first choices while the
  full Phase 3 design-selection work remains ahead.
- **Constraint-aware design advisor:** exhaustively evaluates every selectable
  core/fluid/copper combination against a minimum expected CO₂-reduction target, an
  absolute annual green-premium cap, and approved-material lists. It recommends the
  lowest-cost feasible design (lower carbon breaks a cost tie), explains every rejection,
  exports the candidate matrix, and can populate Scenario B for explicit simulation and
  saving. Loss-performance constraints remain pending until material choices have
  defensible no-load and load-loss mappings.
- Export per-family results (CSV) for gate reviews.
- Quantify Module 2 end-of-life outcomes: avoided-replacement carbon (retrofill) and
  the Module D recovery credit from a sourced `recovery_factors.csv`, with CSV export.
- Model Module 1 use-phase cost **and** carbon from first principles (loss energy ->
  NPV TCO + lifetime CO₂ + payback), with assumptions and design presets sourced from
  `energy_params.csv` / `transformer_presets.csv`.
- Surface uncertainty bounds in portfolio outputs (low-high factor ranges as KPI
  bands and chart error bars).
- Gate KPI per class (kg CO₂e/kVA), per-lever abatement cost (€/t CO₂e) from
  representative cost deltas, and a data-freshness banner driven by factor `valid_to` dates.
- **Industry benchmark column** in the per-family table: kg CO₂e/kVA results sit next
  to an EPDi average from `data/benchmarks.csv`, with sample size, source EPDs, and
  validity dates documented. Phase 2 replaces the static CSV with the EPDi data feed.
- **Monte Carlo uncertainty analysis:** propagates factor uncertainty through the
  portfolio model using probabilistic triangular sampling over sourced ranges
  (`uncertainty_low` → `kg_co2e_per_kg` → `uncertainty_high`). Produces P10/P50/P90
  confidence intervals for portfolio baseline, eco-efficient, saving, reduction %,
  per-family breakdowns, and per-lever attribution. Histograms show the full
  distribution with percentile markers. Iterations are configurable (1K–50K), with CSV
  export. The engine is pure NumPy (`monte_carlo.py`) and has no Streamlit dependency,
  so it can be unit-tested and reused by the design advisor in future phases.
- Module 4 GHG Scope 1/2/3 reporting view: rebuckets Modules 1–3 outputs into
  GHG-Protocol scopes (1, 2, 3.1, 3.11, 3.12), with editable per-family factory-energy
  inputs (`data/factory_energy.csv`) for indicative Scope 1 and 2 estimates until Phase 2
  adds metered factory data. **Module 4 now reads the latest saved Module 3 / Module 2
  run from `runs.db` instead of Streamlit session state.** Scope 3.1 and 3.12 survive
  tab refresh, multi-tab, and mobile views.

### Phase 2 - Real Data Integration (3–9 mo)
**Theme: connect to enterprise systems.**

- Ingest **actual BOM** from PLM/ERP for each product rather than class averages, using
  standard BOM import formats before bespoke connectors.
- **Partner factor/EPD feeds** replace the static CSVs behind the same data-layer
  interface. Evaluate sustamize's factor API and One Click LCA's machine-readable
  EPD outputs (ILCD+EPD / OpenEPD) rather than building a competing factor database.
  *(An Environmental Product Declaration (EPD) is a standardized, independently verified
  report of a product's lifecycle environmental impacts, including embodied CO₂.)*
- **Replace static `benchmarks.csv` with the EPDi / One Click LCA platform feed** to
  keep the per-family benchmark current without manual curation.
- **Full lifecycle engine:** merge Modules 1–3 under one cradle-to-grave engine
  (A1–C4 + Module D), with a lifecycle-stage dimension on every emission line.
- Supplier-specific carbon factors tied to a supplier master.
- Add A4–A5 (transport & installation) coverage.
- Replace indicative Module 4 factory-energy estimates with **metered factory gas &
  electricity** per plant and product line (MES/EMS integration); add Scope 1 fugitive
  SF₆ leakage; gross C1–C4 emissions from partner process data.

### Phase 3 - Decision Intelligence (9–18 mo)
**Theme: recommend designs under real constraints.**

- **Constraint-aware design selection:** extend the shipped minimum carbon-reduction,
  annual-premium, and approved-material constraints with loss-performance limits and
  approved-supplier rules. Loss limits require design-specific no-load and load-loss
  mappings; the current single Standard/Eco preset pair is not sufficient evidence.
- **Abatement economics:** extend the shipped per-lever €/t
  ranking into full **marginal abatement cost curves** (CO₂ vs. €) linking Module 1 +
  Module 3.
- **Optimisation:** "hit −30% CO₂ at minimum cost" with a solver that selects material
  levers.
- **Gate-KPI artifacts:** exportable kg CO₂e/kVA pass/fail objects for PLM design reviews.
- Extend Monte Carlo to correlate factor uncertainties (e.g. steel and copper from the
  same supplier programme) and propagate through marginal abatement cost curves.
- SBTi targets enter as *constraints* on portfolio scenarios. Corporate-target tooling
  remains with corporate-carbon platforms (carbmee, Makersite, Sphera).

### Phase 4 - Platform & Scale (18 mo+)
**Theme: multi-user, governed, integrated.**

- Multi-tenant, role-based access (R&D, procurement, sustainability).
- **Narrow, open gate API** so PLM gates can call the engine programmatically and treat
  CO₂ as a design condition; exports align with OpenEPD / ILCD machine-readable formats.
- Audit trail and versioned assumptions, plus **third-party methodology validation**
  (the GUTcert / DEKRA pattern competitors use) instead of self-asserted assurance.
- Regional grid factors, multi-currency.
- CBAM/CSRD: emit compliant *inputs* to dedicated reporting tools. Makersite, sustamize,
  and carbmee already cover that reporting layer.

---

## Competitive context (July 2026)

Full scan: **[competitors/summarize-competitor.md](competitors/summarize-competitor.md)**
(five vendors: Makersite, sustamize, carbmee, Sphera/GaBi, One Click LCA).

- **Commoditized:** BOM-based A1–A3 PCF is available from all five vendors.
- **Product focus:** use-phase loss economics (B1–B6 to TCO and payback), gate-ready
  kg CO₂e/kVA, per-lever €/t abatement ranking, quantified factor uncertainty, and
  transformer EOL decision logic. The open-source prototype is designed for engineers
  who need a result during design review.
- **Primary threat:** Makersite (High, directional) ships a horizontal cost-and-carbon
  in-PLM product and now owns PCF-exchange rails (SiGREEN to Mattermaps). Watch for a
  heavy-electrical-equipment template.
- **Existing vertical customers:** Schneider Electric uses Makersite and One Click LCA;
  Siemens Energy uses carbmee. None of the scanned products is transformer-specific.
- **Strategy:** partner for data (sustamize, One Click LCA), interoperate with PCF
  exchange networks, and invest in the decision layer.

---

## What each phase means for the data model

The data model moves from constants in code to a versioned, sourced, relational model.

| Phase | Data-model evolution |
|-------|----------------------|
| **1 (done)** | Coefficients, BOM, EOL recovery rates, energy/evaluation assumptions, and factory energy per unit live in sourced CSVs with uncertainty and provenance. Scenarios and runs persist in `scenario` and `simulation_run` tables (SQLite). Module 4 reads the factory-energy CSV for Scope 1 and 2 estimates. |
| **2** | `product` + `bom_line` tables fed by real PLM/ERP; factors gain supplier + lifecycle-stage dimensions; static CSVs swapped for partner factor/EPD feeds. |
| **3** | Time-series `volume_forecast` (year × region); optimisation & MAC-curve views read cost + carbon jointly; scenario results become comparable over time. |
| **4** | Owner / tenant on every record; temporal `valid_from` / `valid_to` on all assumptions; full audit trail for assurance; regional & regulatory dimensions. |

**Current schema (Phase 1)** is documented in the [README ER diagram](README.md#data-model-phase-1):

- `MATERIAL_FACTOR`: sourced carbon-intensity factors (CSV, read-only)
- `BOM_LINE`: bill-of-material masses per transformer class (CSV, read-only)
- `RECOVERY_FACTOR`: per-component end-of-life recovery rates and routes (CSV, read-only)
- `BENCHMARK`: per-family industry benchmark kg CO₂e/kVA from EPDi EPDs (CSV, read-only)
- `FACTORY_ENERGY`: per-family factory gas and electricity per unit (CSV, read-only)
- `SCENARIO`: a named set of design-lever choices and volume forecast (SQLite)
- `SIMULATION_RUN`: computed portfolio results for a scenario (SQLite)
- `MODULE2_EOL`: Module 2 decommissioning-branch output (SQLite, persisted so Module 4
  can read it after a tab refresh)
- `APP_PREFERENCE`: single-row app preferences keyed by string (SQLite; holds the
  last-used cost-ceiling %)

Phase 1 separates the data from the model. Live feeds, optimisation, assurance, and
SBTi tracking can build on that boundary.

---

## Scope boundaries (current)

- Module 3 covers **cradle-to-gate (A1–A3)** embodied emissions only, from raw material
  extraction through factory gate.
- Use-phase energy losses (B1–B6) are addressed in Module 1.
- End-of-life (C1–C4) and recycling credits (Module D) are addressed in Module 2.
- Module 4 rebuckets Modules 1–3 into GHG Protocol Scope 1/2/3 for corporate reporting.
  Scope 1 and 2 use indicative factory-energy estimates; full metered factory data is a
  **Phase 2** deliverable.
- Full cradle-to-grave integration (A1–C4 + Module D) is a **Phase 2** deliverable.

---

*Maintained by Raka Adrianto, Sustainability, Product, Data*
[LinkedIn](https://www.linkedin.com/in/lugasraka/)*
