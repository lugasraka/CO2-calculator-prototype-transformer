# Product Vision & Roadmap

> **Vision:** Make embodied and lifecycle carbon a *quantifiable, comparable, and
> auditable* input to every transformer design, sourcing, and R&D decision — turning
> sustainability from an after-the-fact report into a live engineering condition.

---

## The problem

Transformer manufacturers face rising pressure — regulation (CBAM, CSRD), science-based
targets (SBTi), and customer demand — to cut carbon. But the data needed to act on it is
fragmented: carbon factors sit in LCA databases, material masses in PLM/BOM systems, and
cost in ERP. None of it is connected to the moment a design decision is actually made.

The result: carbon is measured *after* the product is designed, not *while* it is being
designed. Decisions that lock in most of a product's footprint — material choice, sourcing,
efficiency class — are made without a fast, credible CO₂ number in front of the engineer.

## The product

A decision-support platform that translates **material and design choices** into
**fleet-wide carbon outcomes**, so R&D and procurement can target the highest-impact
reductions with data instead of guesswork.

Today it is a Streamlit prototype with three modules mapped to lifecycle stages:

| Module | Lifecycle scope | Job-to-be-done |
|--------|-----------------|----------------|
| **1. TCO & Carbon ROI** | Use-phase (B1–B6) | Justify high-efficiency units via 15-yr total cost of ownership |
| **2. Circularity & EOL Planner** | End-of-life (C1–C4 + D) | Decide retrofill vs. decommission; maximise material recovery |
| **3. Portfolio CO₂ Simulator ★** | Cradle-to-gate (A1–A3) | Bottom-up embodied carbon from BOM → portfolio, scenario comparison |

**Target users:** R&D / design engineers, sustainability leads, procurement & supply-chain
teams, and PLM gate reviewers.

---

## Guiding principles

1. **Separate the model from the data.** Formulas live in code; coefficients, BOMs, and
   scenarios live in a sourced, versioned data store. Every roadmap phase plugs into the
   data layer without rewriting the engine or UI.
2. **Every number is defensible.** Each carbon factor carries provenance (source, version,
   validity dates) and an uncertainty range — a precondition for external assurance.
3. **Scoped honestly.** The tool states exactly which lifecycle stages it covers and which
   it doesn't. No hand-waving across system boundaries.
4. **From calculator to advisor.** The long-term goal is not just to *compute* CO₂ but to
   *recommend* the lowest-cost path to a target.

---

## Roadmap

### ✅ Phase 1 — Foundation & Trust  *(current)*
**Theme: make the numbers real and defensible.**

- ✅ Externalise all coefficients and BOM masses out of code into sourced CSVs (`data/`),
  accessed through `data_layer.py`.
- ✅ Provenance per factor — source, version, validity dates.
- ✅ Uncertainty ranges (low / expected / high) on carbon factors.
- ✅ Save, name, and compare scenarios; persist runs in SQLite (`scenario_store.py`).
- ✅ Export per-family results (CSV) for gate reviews.

### 🔜 Phase 2 — Real Data Integration  *(3–9 mo)*
**Theme: connect to live enterprise systems.**

- Ingest **actual BOM** from PLM/ERP per real product — not class averages.
- Live EPD feed (**EcoSpace™ / EcoSmart™**) replacing static factor tables, behind the
  same data-layer interface.
- **Full lifecycle unification:** merge Modules 1–3 under one cradle-to-grave engine
  (A1–C4 + Module D), with a lifecycle-stage dimension on every emission line.
- Supplier-specific carbon factors tied to a supplier master.
- Add A4–A5 (transport & installation) coverage.

### 🔮 Phase 3 — Decision Intelligence  *(9–18 mo)*
**Theme: from calculator to advisor.**

- **Optimisation:** "hit −30% CO₂ at minimum cost" — a solver selects material levers.
- **Marginal abatement cost curves** (CO₂ vs. €) linking Module 1 + Module 3.
- **SBTi trajectory tracking:** portfolio actuals vs. target glide path over time.
- Sensitivity / what-if analysis and Monte Carlo over the uncertainty ranges.

### 🌐 Phase 4 — Platform & Scale  *(18 mo+)*
**Theme: multi-user, governed, integrated.**

- Multi-tenant, role-based access (R&D, procurement, sustainability).
- **API** so PLM gates call the engine programmatically — CO₂ as a hard design condition.
- Audit trail and versioned assumptions for external assurance / compliance.
- Regional grid factors, multi-currency, regulatory reporting (CBAM, CSRD).

---

## What each phase means for the data model

The core trajectory: **from constants-in-code → a versioned, sourced, relational model.**

| Phase | Data-model evolution |
|-------|----------------------|
| **1 (done)** | Coefficients & BOM extracted to sourced CSVs with uncertainty + provenance; scenarios/runs persisted in `scenario` + `simulation_run` tables (SQLite). |
| **2** | `product` + `bom_line` tables fed by real PLM/ERP; factors gain supplier + lifecycle-stage dimensions; static CSVs swapped for live EPD feed. |
| **3** | Time-series `volume_forecast` (year × region); optimisation & MAC-curve views read cost + carbon jointly; scenario results become comparable over time. |
| **4** | Owner / tenant on every record; temporal `valid_from` / `valid_to` on all assumptions; full audit trail for assurance; regional & regulatory dimensions. |

**Current schema (Phase 1)** — see [`README.md`](README.md#data-model-phase-1) for the ER diagram:

- `MATERIAL_FACTOR` — sourced carbon-intensity factors (CSV, read-only)
- `BOM_LINE` — bill-of-material masses per transformer class (CSV, read-only)
- `SCENARIO` — a named set of design-lever choices + volume forecast (SQLite)
- `SIMULATION_RUN` — computed portfolio results for a scenario (SQLite)

**Key principle:** the single most important data-model improvement — already done in
Phase 1 — is *separating the data from the model*. Everything downstream (live feeds,
optimisation, assurance, SBTi tracking) depends on that separation being in place first.

---

## Scope boundaries (current)

- Module 3 covers **cradle-to-gate (A1–A3)** embodied emissions only — raw material
  extraction through factory gate.
- Use-phase energy losses (B1–B6) are addressed in Module 1.
- End-of-life (C1–C4) and recycling credits (Module D) are addressed in Module 2.
- Full cradle-to-grave integration (A1–C4 + Module D) is a **Phase 2** deliverable.

---

*Maintained by Raka Adrianto — Sustainability, Product, Data ·
[LinkedIn](https://www.linkedin.com/in/lugasraka/)*
