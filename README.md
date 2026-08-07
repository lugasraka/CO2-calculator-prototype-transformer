# Transformer Decarbonization Manager

**[Live demo](https://co2-calculator-prototype-transformer.streamlit.app/)**

A Streamlit prototype for evaluating CO₂ reduction across the transformer lifecycle, from embodied carbon in materials to end-of-life recovery.

See **[ROADMAP.md](ROADMAP.md)** for the product vision, phased roadmap, and data-model evolution.

## Modules

| Module | Description |
|--------|-------------|
| **1. TCO & Carbon ROI** | Compares total cost of ownership and use-phase carbon (B1–B6) for standard and high-efficiency designs. Models loss energy from loading, discounts it to an NPV TCO, and derives lifetime CO₂ savings and payback. |
| **2. Circularity & EOL Planner** | Quantifies the avoided replacement carbon of a mid-life retrofill and the Module D recovery credit from decommissioning, using sourced recovery rates for each material. |
| **3. Portfolio CO₂ Simulator** | Calculates embodied carbon (A1–A3) from BOM material choices, product families, and annual volumes. Its constraint-aware advisor evaluates every core/fluid/copper combination against a reduction target, annual premium cap, and approved-material rules. Engineers can apply a recommendation, simulate and save it, then compare designs with benchmarks, uncertainty ranges, cost trade-offs, and CSV exports. Monte Carlo analysis samples the factor ranges and reports P10/P50/P90 intervals for portfolio CO₂, reduction percentage, family results, and lever attribution. |
| **4. GHG Scope 1/2/3 Report** | Rebuckets Modules 1–3 into a corporate GHG Protocol view: Scope 1 factory fuel, Scope 2 factory electricity, and Scope 3 Categories 1, 11, and 12. It includes editable per-family factory-energy inputs (`data/factory_energy.csv`) and CSV export. Scope 1 and 2 use indicative estimates until Phase 2 adds metered data. |

## Competitive position

A 2026 landscape scan of five adjacent vendors (Makersite, sustamize, carbmee,
Sphera/GaBi, and One Click LCA; see **[competitors/summarize-competitor.md](competitors/summarize-competitor.md)**)
found BOM-based A1–A3 PCF to be commoditized. All five ship it. None ship use-phase
loss economics, gate-ready kg CO₂e/kVA KPIs, per-lever €/t abatement ranking, or
quantified factor uncertainty. This tool focuses on the gap between electrical
equipment and design-time decision support. The strategy is to partner for carbon and
EPD data, then build the decision layer on top of it.

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

The app separates the **model** (`design_engine.py`) from the **UI** (`app.py`) and
the **data** (sourced coefficients, BOM masses, and saved runs). Phase 1 puts every
coefficient and BOM mass behind the data layer, so later PLM/EPD feeds can replace the
CSV files without changing the UI or calculation engine.

```mermaid
flowchart TD
    subgraph UI["Streamlit UI - app.py"]
        M1["Module 1<br/>TCO & Carbon ROI"]
        M2["Module 2<br/>Circularity & EOL"]
        M3["Module 3<br/>Portfolio CO₂ Simulator"]
        M4["Module 4<br/>GHG Scope 1/2/3 Report"]
    end

    subgraph LOGIC["Calculation Engine"]
        CALC["design_engine.py<br/>Bottom-up CO₂ calc"]
        ADVISOR["Constraint-aware advisor<br/>Feasible-design search"]
        MC["monte_carlo.py<br/>Probabilistic uncertainty"]
    end

    subgraph DATA["Data Layer"]
        DL["data_layer.py<br/>(cached reads)"]
        SS["scenario_store.py<br/>(persistence)"]
    end

    subgraph STORE["Data Store"]
        MF["material_factors.csv<br/>coefficients + provenance"]
        BOM["bom.csv<br/>BOM masses"]
        RF["recovery_factors.csv<br/>EOL recovery rates"]
        EP["energy_params.csv +<br/>transformer_presets.csv"]
        FE["factory_energy.csv<br/>per-unit factory gas & electricity"]
        BM["benchmarks.csv<br/>EPDi per-family kg CO₂e/kVA"]
        DB["runs.db (SQLite)<br/>saved scenarios, runs, M2 EOL, prefs"]
    end

    subgraph FUTURE["Phase 2+ (planned)"]
        FEED["Partner factor / EPD feeds<br/>+ PLM/BOM feeds"]
    end

    M1 --> CALC
    M2 --> CALC
    M3 --> CALC
    M3 --> ADVISOR
    M3 --> MC
    ADVISOR --> CALC
    MC --> CALC
    M4 -->|aggregate M1-M3 outputs| CALC
    CALC --> DL
    M3 -->|save / design-gate compare / export| SS
    M4 -->|read latest saved run from runs.db| SS
    DL --> MF
    DL --> BOM
    DL --> RF
    DL --> EP
    DL --> FE
    DL --> BM
    SS --> DB
    FEED -.replaces CSVs.-> DL

    classDef future stroke-dasharray: 5 5;
    class FUTURE,FEED future;
```

**Flow:** Module 3 reads carbon-intensity factors and BOM masses through
`data_layer.py`, then uses `design_engine.py` for simulations and design advice. The
advisor evaluates each available material combination, filters on the three hard
constraints, and ranks feasible designs by annual green premium, with lower portfolio
carbon breaking a cost tie. Engineers can apply a recommendation and send it through
the existing simulation and save workflow. Named scenarios and results persist through
`scenario_store.py`.

`monte_carlo.py` samples sourced factor ranges with triangular distributions and
reports P10/P50/P90 intervals for portfolio CO₂, reduction percentage, family results,
and lever attribution. Module 2 uses the same BOM masses, baseline factors, and
material recovery rates to calculate end-of-life credits. Module 1 uses sourced energy
assumptions and transformer presets for use-phase cost and carbon. Module 4 reads the
latest saved Module 1–3 outputs from SQLite, rebuckets them into GHG Protocol
categories, and adds factory-energy inputs from `data/factory_energy.csv`.

An **Environmental Product Declaration (EPD)** is a standardized, independently
> verified report of a product's lifecycle environmental impacts, including embodied
> CO₂. In this tool a partner EPD data feed (e.g. machine-readable OpenEPD / ILCD)
> would replace the static CSV factor tables in Phase 2.

## Data model (Phase 1)

Reference data lives in sourced CSVs under `data/`; user-generated state lives in
`data/runs.db` (SQLite). `data_layer.py` and `scenario_store.py` provide the access
interfaces. Phase 2 partner feeds can replace the CSV sources without touching
`app.py`. Every factor carries provenance + `valid_from` / `valid_to`; a freshness
banner warns within 180 days of expiry.

| Entity | Where | Key | Notes |
|--------|-------|-----|-------|
| `MATERIAL_FACTOR` | `data/material_factors.csv` | `material_id` | per-material kg CO₂e/kg, uncertainty range, cost Δ, source, version, validity window |
| `BOM_LINE` | `data/bom.csv` | `(family, component)` | per-family BOM masses (core / copper / fluid / insulation / structural) |
| `RECOVERY_FACTOR` | `data/recovery_factors.csv` | `component` | EOL recovery rate, route, secondary-material note |
| `FACTORY_ENERGY` | `data/factory_energy.csv` | `family` | per-family gas + electricity per unit → Scope 1/2 |
| `BENCHMARK` | `data/benchmarks.csv` | `family` | EPDi industry average kg CO₂e/kVA, source ID, validity |
| `ENERGY_PARAMS` | `data/energy_params.csv` | `parameter` | key/value: grid intensity, energy price, hours, loading, discount rate, emission factors |
| `TRANSFORMER_PRESETS` | `data/transformer_presets.csv` | `(design, rating_kva)` | Standard vs. Eco-Efficient CAPEX and loss presets per rating |
| `SCENARIO` | `scenario` (SQLite) | `scenario_id` | name + 3 `MATERIAL_FACTOR.selector_label` choices (core/fluid/copper) + volume forecast |
| `SIMULATION_RUN` | `simulation_run` (SQLite) | `run_id` | `scenario_id` FK; portfolio totals + `results_json` (per-family table) |
| `MODULE2_EOL` | `module2_eol` (SQLite) | `eol_id` | Module 2 decommissioning output → consumed by Module 4 Scope 3.12 |
| `APP_PREFERENCE` | `app_preference` (SQLite) | `key` | generic k/v; today holds the design-gate cost-ceiling % |

```mermaid
erDiagram
    MATERIAL_FACTOR    }o--o{ SCENARIO         : "core/fluid/copper_choice → selector_label"
    SCENARIO           ||--|| SIMULATION_RUN   : "produces 1 run (results_json holds per-family table)"
    BOM_LINE           }o--o{ SIMULATION_RUN   : "aggregated per family into results_json"
    BENCHMARK          ||--o{ BOM_LINE         : "family = key"
    RECOVERY_FACTOR    ||--o{ BOM_LINE         : "component = key"
    FACTORY_ENERGY     ||--o{ BOM_LINE         : "family = key"
    MODULE2_EOL        }o--o{ FACTORY_ENERGY   : "per-family decommissioning volumes"
    APP_PREFERENCE     ||--o{ SCENARIO         : "key=cost_ceiling_pct, read by design-gate filter"
```

SQLite has no FK constraints here. Joins happen at read time in
`data_layer.py` / `scenario_store.py`. Only `SCENARIO → SIMULATION_RUN` is a real
DB-level FK (`scenario_id`). `BENCHMARK`, `RECOVERY_FACTOR` and `FACTORY_ENERGY`
stay as separate CSVs (not normalised into the BOM) so each has its own
provenance and validity window, and a Phase 2 partner-feed swap is a single
file. `MODULE2_EOL` lives in SQLite rather than session state, so Module 4's report
survives tab refresh, multi-tab, and mobile views. `APP_PREFERENCE` stores future
user settings such as regional grid factor and currency.

## Scope

- Module 3 covers **cradle-to-gate (A1–A3)** embodied emissions only, from raw material extraction through factory gate.
- Use-phase energy losses (B1–B6) are addressed in Module 1.
- End-of-life (C1–C4) and recycling credits (Module D) are addressed in Module 2.
- Module 4 rebuckets Modules 1–3 outputs into **GHG Protocol Scope 1/2/3** for corporate reporting (CSRD/SBTi alignment). Scope 1 and 2 use indicative factory-energy estimates; full metered factory data is a Phase 2 deliverable.
- Full cradle-to-grave integration (A1–C4 + Module D) is planned for Phase 2.

See **[ROADMAP.md](ROADMAP.md)** for how these boundaries expand across future phases.

## Author

- Raka Adrianto | Sustainability, Product, Data [LinkedIn](https://www.linkedin.com/in/lugasraka/)
