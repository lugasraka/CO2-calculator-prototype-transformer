# Copilot instructions

Streamlit prototype for evaluating CO₂ reduction across the transformer lifecycle. See `README.md` for the module overview and `ROADMAP.md` for the phased vision.

## Commands

```bash
pip install -r requirements.txt   # streamlit, pandas, plotly
streamlit run app.py              # run the app locally
```

There is no test, lint, or build tooling in this repo — don't invent any.

## Architecture

The core design decision (Phase 1) is separating the **model** (calculation logic) from the **data** (sourced coefficients + BOM masses + saved runs). Every planned later phase plugs into the data layer without touching the UI or calculation engine.

- **`app.py`** — the Streamlit UI and module orchestration. A sidebar `st.radio` selects one of five modules, dispatched by a top-level `if module == ... / elif` chain. Modules 1–4 are data-driven via `data_layer.py`; Module 5 is a static reference page. Module 3 delegates its shared portfolio calculation and candidate search to `design_engine.py`.
  - **Module 1 — TCO & Carbon ROI** (use-phase, B1–B6) — a first-principles cost + carbon calculator. Transformer CAPEX/loss presets come from `data/transformer_presets.csv` and operating assumptions from `data/energy_params.csv` (`dl.energy_params()`). It computes annual loss energy `(no_load_W + load_W × loading²) × hours / 1000`, discounts the energy cost over the evaluation horizon into an NPV TCO, and derives use-phase CO₂ (`kWh × grid_intensity`), the real payback (`ΔCAPEX / annual cost saving`), and a Plotly cumulative cost-of-ownership crossover. Reactive (no button).
  - **Module 2 — Circularity & EOL Planner** (end-of-life, C1–C4 + Module D) — a data-driven calculator. A `st.selectbox` picks a transformer class (BOM via `dl.bom_by_family()`); a nested `st.radio` toggles two paths. **Mid-Life Extension** computes the avoided A1–A3 embodied carbon of the replacement unit that a Retrofill defers (`Σ mass × baseline_ci / 1000`), scaled by installed base and retrofill share. **End-of-Life Decommissioning** takes per-class annual decommissioning volumes, then shows a **portfolio view** (Module D avoided-virgin-material credit aggregated across all classes) and a **component detail** for the selected class — per-component recovered mass (`mass × recovery_rate`), credit (`recovered × baseline_ci / 1000`), recyclability by mass — rendered as metrics, tables, a Plotly bar chart, and CSV `st.download_button` exports for both tables.
  - **Module 3 — Portfolio CO₂ Simulator ★** (embodied materials, A1–A3) — the flagship, data-driven workflow. **Step 1:** enter annual volumes per transformer class. **Step 2:** the constraint-aware advisor evaluates every selectable core/fluid/copper combination against minimum expected CO₂ reduction, maximum annual green premium, and approved-material rules, then recommends the lowest-cost feasible design. **Step 3:** Scenario A is the fixed current-BOM baseline; the user configures Scenario B via three `st.selectbox` levers or applies the recommendation. **Step 4:** running the sim executes the shared `design_engine.calculate_portfolio_design(...)` calculation per family, aggregates portfolio kt/yr totals plus per-lever deltas into a results DataFrame, and stores it in `st.session_state["sim"]`. Results render as Plotly charts + a table, and can be saved (`store.save_run`), exported to CSV (`st.download_button`), and compared against prior saved runs (`store.list_runs` / `delete_run`).
  - **Module 5 — About & Source Code.** Static reference page: project description, GitHub/live-demo links, a module summary table (module ↔ lifecycle scope), and author credit. Pure markdown — keep the module table here in sync with any module scope or naming changes.
- **`design_engine.py`** — pure deterministic Module 3 calculation and recommendation logic. `calculate_portfolio_design(...)` is the single formula path used by manual simulation and advice; `evaluate_constrained_designs(...)` exhaustively ranks current material combinations and records pass/fail reasons. Keep Streamlit UI calls out of this module.
- **`data_layer.py`** — cached (`@st.cache_data`) read access to the reference CSVs. The UI never reads CSVs directly; it calls helpers like `factor_details(category)` (CI + uncertainty bounds + cost delta per selectable option), `baseline_details(category)` / `baseline_factor(category)`, `bom_by_family()`, `kva_by_family()`, and `factor_validity()` (drives the data-freshness banner). This interface is what Phase 2 swaps to partner factor/EPD and PLM feeds.
- **`scenario_store.py`** — SQLite persistence (`data/runs.db`) for named scenarios and their simulation runs, so Module 3 results survive reruns and can be listed/compared/deleted. `init_db()` is called lazily by every public function.
- **`data/material_factors.csv`** — per-material carbon intensity (kg CO₂e/kg) with uncertainty range and provenance (source/version/validity).
- **`data/bom.csv`** — long-format bill-of-material masses per transformer class.
- **`data/recovery_factors.csv`** — per-component end-of-life recovery rate + route, consumed by Module 2 via `dl.load_recovery_factors()` / `dl.recovery_rates()`.
- **`data/energy_params.csv`** & **`data/transformer_presets.csv`** — Module 1 operating/evaluation assumptions and CAPEX/loss presets, via `dl.energy_params()` / `dl.load_transformer_presets()`.

Data flow for Module 3: `app.py` reads factors + BOM via `data_layer.py` → `design_engine.py` calculates or evaluates candidates → `app.py` presents/applies the result → `scenario_store.py` persists explicit saved runs.

## Conventions

- **Component order is canonical.** `data_layer.COMPONENT_ORDER = ["core", "copper", "fluid", "insulation", "structural"]`. `bom_by_family()` returns masses as a list in this exact order, and `design_engine.py` unpacks them positionally. Keep the order consistent across the CSV, the data layer, and the unpacking.
- **CO₂ math.** Per-unit emissions are `mass_kg × kg_co2e_per_kg`, divided by 1,000 for tonnes; portfolio totals multiply by annual volume and divide by another 1,000 for kt/yr.
- **Material factor rows** are filtered by `category`; `selectable == 1` marks user-choosable options and `is_baseline == 1` marks the current-BOM baseline. `material_factors.csv` is the single source of truth for both the calculator and the methodology reference table (`reference_table()`).
- **Module 3 state** lives under `st.session_state["sim"]` so results persist across Streamlit reruns. Persisted scenario choices are the `["core", "fluid", "copper"]` levers (`scenario_store.CHOICE_KEYS`); Scenario-A baseline is implicit.
- **`data/runs.db` is gitignored** and regenerated at runtime — never commit it.
- **Lifecycle scope labels** (A1–A3, B1–B6, C1–C4, Module D) are used deliberately and partition cleanly across modules: Module 1 = B1–B6 use-phase energy losses, Module 3 = A1–A3 embodied materials, Module 2 = C1–C4 end-of-life + Module D recycling credits. Preserve these boundaries when editing copy — each module cross-references the others by scope.
