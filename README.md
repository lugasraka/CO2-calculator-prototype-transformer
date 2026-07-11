# Transformer Decarbonization Manager

**[▶ Live Demo](https://co2-calculator-prototype-transformer.streamlit.app/)**

A Streamlit prototype for evaluating and simulating CO₂ reduction across the transformer lifecycle — from embodied carbon in materials through to end-of-life recovery.

> 📌 See **[ROADMAP.md](ROADMAP.md)** for the full product vision, phased roadmap, and data-model evolution.

## Modules

| Module | Description |
|--------|-------------|
| **1. TCO & Carbon ROI** | Compares total cost of ownership between standard and high-efficiency transformer designs over 15 years, including capitalised loss costs. |
| **2. Circularity & EOL Planner** | Covers end-of-life lifecycle stages (C1–C4): mid-life retrofill vs. structured decommissioning with material recovery rates. |
| **3. Portfolio CO₂ Simulator ★** | Bottom-up embodied carbon calculator (A1–A3 scope) — translates BOM material choices into fleet-wide CO₂ outcomes across product families and annual volumes. |

## Setup

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Architecture

The app separates the **model** (calculation logic in `app.py`) from the **data**
(sourced coefficients, BOM masses, and saved runs). This is the key Phase 1
design decision — every later phase (live PLM/EPD feeds, optimisation, assurance)
plugs into the data layer without touching the UI or the calculation engine.

```mermaid
flowchart TD
    subgraph UI["🖥️ Streamlit UI — app.py"]
        M1["Module 1<br/>TCO & Carbon ROI"]
        M2["Module 2<br/>Circularity & EOL"]
        M3["Module 3 ★<br/>Portfolio CO₂ Simulator"]
    end

    subgraph LOGIC["⚙️ Calculation Engine"]
        CALC["Bottom-up CO₂ calc<br/>(BOM mass × carbon intensity)"]
    end

    subgraph DATA["📦 Data Layer"]
        DL["data_layer.py<br/>(cached reads)"]
        SS["scenario_store.py<br/>(persistence)"]
    end

    subgraph STORE["🗄️ Data Store"]
        MF["material_factors.csv<br/>coefficients + provenance"]
        BOM["bom.csv<br/>BOM masses"]
        DB["runs.db (SQLite)<br/>saved scenarios & runs"]
    end

    subgraph FUTURE["🔮 Phase 2+ (planned)"]
        FEED["EcoSpace™ / EcoSmart™<br/>live EPD + PLM/BOM feeds"]
    end

    M3 --> CALC
    CALC --> DL
    M3 -->|save / compare / export| SS
    DL --> MF
    DL --> BOM
    SS --> DB
    FEED -.replaces CSVs.-> DL

    classDef future stroke-dasharray: 5 5;
    class FUTURE,FEED future;
```

**Flow:** Module 3 reads carbon-intensity factors and BOM masses through
`data_layer.py`, runs the bottom-up calculation, then persists named scenarios and
their results through `scenario_store.py`. In Phase 2 the static CSVs are swapped
for live EcoSpace™/EcoSmart™ feeds behind the same data-layer interface.

## Data model (Phase 1)

Reference data is separated from the calculation logic. Carbon-intensity
coefficients and bill-of-material masses live in sourced, versioned CSVs under
`data/`, loaded through `data_layer.py` — replacing the previously hardcoded
Python dicts. Each factor carries an uncertainty range and provenance
(source + version + validity dates), the groundwork for the Phase 2 live
PLM/EPD data feeds.

```mermaid
erDiagram
    MATERIAL_FACTOR {
        string material_id PK
        string category
        string selector_label
        float  kg_co2e_per_kg
        float  uncertainty_low
        float  uncertainty_high
        bool   is_baseline
        string source
        string source_version
        date   valid_from
        date   valid_to
    }
    BOM_LINE {
        string family
        string kva_class
        string component
        float  mass_kg
        string source
    }
    SCENARIO {
        int    scenario_id PK
        string name
        string core_choice
        string fluid_choice
        string copper_choice
        int    vol_dist
        int    vol_med
        int    vol_large
        string created_at
    }
    SIMULATION_RUN {
        int    run_id PK
        int    scenario_id FK
        float  total_base
        float  total_eco
        float  total_saving
        float  pct_saving
        json   results_json
        string created_at
    }

    SCENARIO ||--|| SIMULATION_RUN : "produces"
    MATERIAL_FACTOR }o--o{ SCENARIO : "chosen as core/fluid/copper lever"
    BOM_LINE }o--o{ SIMULATION_RUN : "aggregated per family"
```

- **`MATERIAL_FACTOR`** and **`BOM_LINE`** are the sourced reference data (CSV, read-only in the app).
- **`SCENARIO`** and **`SIMULATION_RUN`** are user-generated and persisted in `runs.db` (SQLite).
- Each scenario's lever choices reference a `MATERIAL_FACTOR`; each run aggregates `BOM_LINE` masses into portfolio CO₂ totals.

| File | Purpose |
|------|---------|
| `data/material_factors.csv` | Per-material CO₂ intensity (kg CO₂e/kg), uncertainty range, supplier programme, source & version |
| `data/bom.csv` | Long-format bill-of-material masses per transformer class |
| `data_layer.py` | Cached access layer exposing factors, BOM and the reference table to the app |
| `scenario_store.py` | SQLite-backed persistence for named scenarios and simulation runs (`data/runs.db`) |

Module 3 lets you **save named scenarios**, **export** per-family results to CSV,
and **compare** saved runs side by side. Saved runs persist locally in
`data/runs.db` (gitignored, regenerated at runtime).

## Scope

- Module 3 covers **cradle-to-gate (A1–A3)** embodied emissions only — raw material extraction through factory gate.
- Use-phase energy losses (B1–B6) are addressed in Module 1.
- End-of-life (C1–C4) and recycling credits (Module D) are addressed in Module 2.
- Full cradle-to-grave integration (A1–C4 + Module D) is planned for Phase 2.

See **[ROADMAP.md](ROADMAP.md)** for how these boundaries expand across future phases.

## Author 

- Raka Adrianto | Sustainability, Product, Data [LinkedIn](https://www.linkedin.com/in/lugasraka/)