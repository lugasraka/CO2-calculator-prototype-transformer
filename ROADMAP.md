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

Today it is a Streamlit prototype with four modules mapped to lifecycle stages and corporate reporting scopes:

| Module | Lifecycle scope | Job-to-be-done |
|--------|-----------------|----------------|
| **1. TCO & Carbon ROI** | Use-phase (B1–B6) | Justify high-efficiency units via lifetime TCO, use-phase carbon savings, and payback |
| **2. Circularity & EOL Planner** | End-of-life (C1–C4 + D) | Quantify retrofill vs. decommission trade-offs and the Module D recovery credit from sourced recovery rates |
| **3. Portfolio CO₂ Simulator ★** | Cradle-to-gate (A1–A3) | Bottom-up embodied carbon from BOM → portfolio, scenario comparison |
| **4. GHG Scope 1/2/3 Report** | Corporate (Scope 1 + 2 + 3.1/3.11/3.12) | Rebuckets Modules 1–3 into GHG-Protocol scopes for CSRD/SBTi-style annual corporate reporting; Scope 1 & 2 use indicative factory-energy estimates (`data/factory_energy.csv`) until Phase 2 metered data |

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
5. **Partner for data; build the decision layer.** BOM-based PCF factor data is
   commoditized (see [competitive scan](competitors/summarize-competitor.md)). Our
   differentiation is what we compute *on top* of the data — loss economics, gate
   KPIs, abatement cost — not the data itself.

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
- ✅ Quantify Module 2 end-of-life outcomes — avoided-replacement carbon (retrofill) and
  the Module D recovery credit — from a sourced `recovery_factors.csv`, with CSV export.
- ✅ Model Module 1 use-phase cost **and** carbon from first principles (loss energy →
  NPV TCO + lifetime CO₂ + payback), with assumptions and design presets sourced from
  `energy_params.csv` / `transformer_presets.csv`.
- ✅ Surface uncertainty bounds in portfolio outputs (low–high factor ranges as KPI
  bands and chart error bars) — no more point-estimate-only results.
- ✅ Gate KPI per class (kg CO₂e/kVA), per-lever abatement cost (€/t CO₂e) from
  representative cost deltas, and a data-freshness banner driven by factor `valid_to` dates.
- ✅ Module 4 GHG Scope 1/2/3 reporting view — rebuckets Modules 1–3 outputs into
  GHG-Protocol scopes (1, 2, 3.1, 3.11, 3.12), with editable per-family factory-energy
  inputs (`data/factory_energy.csv`) for indicative Scope 1 & 2 estimates until Phase 2
  metered factory data.

### 🔜 Phase 2 — Real Data Integration  *(3–9 mo)*
**Theme: connect to live enterprise systems.**

- Ingest **actual BOM** from PLM/ERP per real product — not class averages — via
  standard BOM import formats first, bespoke connectors later.
- **Partner factor/EPD feeds** replacing static CSVs, behind the same data-layer
  interface — evaluate sustamize's factor API and One Click LCA's machine-readable
  EPD outputs (ILCD+EPD / OpenEPD) rather than building a competing factor database.
  *(An Environmental Product Declaration (EPD) is a standardized, independently verified
  report of a product's lifecycle environmental impacts, including embodied CO₂.)*
- **Full lifecycle unification:** merge Modules 1–3 under one cradle-to-grave engine
  (A1–C4 + Module D), with a lifecycle-stage dimension on every emission line.
- Supplier-specific carbon factors tied to a supplier master.
- Add A4–A5 (transport & installation) coverage.
- Replace indicative Module 4 factory-energy estimates with **metered factory gas &
  electricity** per plant and product line (MES/EMS integration); add Scope 1 fugitive
  SF₆ leakage; gross C1–C4 emissions from partner process data.

### 🔮 Phase 3 — Decision Intelligence  *(9–18 mo)*
**Theme: from calculator to advisor.**

- **Abatement economics as the signature output:** extend the shipped per-lever €/t
  ranking into full **marginal abatement cost curves** (CO₂ vs. €) linking Module 1 +
  Module 3 — uncontested white space across all five competitors scanned.
- **Optimisation:** "hit −30% CO₂ at minimum cost" — a solver selects material levers.
- **Gate-KPI artifacts:** exportable kg CO₂e/kVA pass/fail objects for PLM design reviews.
- Sensitivity / what-if analysis and Monte Carlo over the uncertainty ranges.
- SBTi targets enter only as *constraints* on portfolio scenarios — corporate-target
  tooling is deliberately left to corporate-carbon platforms (carbmee, Makersite, Sphera).

### 🌐 Phase 4 — Platform & Scale  *(18 mo+)*
**Theme: multi-user, governed, integrated.**

- Multi-tenant, role-based access (R&D, procurement, sustainability).
- **Narrow, open gate API** so PLM gates call the engine programmatically — CO₂ as a
  hard design condition; exports aligned with OpenEPD / ILCD machine-readable formats.
- Audit trail and versioned assumptions, plus **third-party methodology validation**
  (the GUTcert / DEKRA pattern competitors use) instead of self-asserted assurance.
- Regional grid factors, multi-currency.
- CBAM/CSRD: emit compliant *inputs* to dedicated reporting tools (already shipped
  audit-grade by Makersite, sustamize, carbmee) rather than building a competing engine.

---

## Competitive context (July 2026)

Full scan: **[competitors/summarize-competitor.md](competitors/summarize-competitor.md)**
(five vendors: Makersite, sustamize, carbmee, Sphera/GaBi, One Click LCA).

- **Commoditized:** BOM-based A1–A3 PCF — shipped by all five. Not our moat.
- **Uncontested (ours):** use-phase loss economics (B1–B6 → TCO/payback), gate-ready
  kg CO₂e/kVA, per-lever €/t abatement ranking, quantified factor uncertainty,
  transformer EOL decision logic — plus open-source, engineer-first adoption that
  quote-only enterprise vendors structurally can't match.
- **Primary threat:** Makersite (High, directional) — ships the cost+carbon-in-PLM
  thesis horizontally and now owns PCF-exchange rails (SiGREEN → Mattermaps).
  Watch trigger: a heavy-electrical-equipment vertical template.
- **Already in the vertical:** Schneider Electric (Makersite, One Click LCA) and
  Siemens Energy (carbmee) — beachheads exist, but no transformer-specific product yet.
- **Strategy:** partner for data (sustamize, One Click LCA), interoperate with the
  PCF-exchange networks, and out-run everyone on the decision layer.

---

## What each phase means for the data model

The core trajectory: **from constants-in-code → a versioned, sourced, relational model.**

| Phase | Data-model evolution |
|-------|----------------------|
| **1 (done)** | Coefficients, BOM, EOL recovery rates, energy/evaluation assumptions & factory-energy per unit extracted to sourced CSVs with uncertainty + provenance; scenarios/runs persisted in `scenario` + `simulation_run` tables (SQLite). Module 4 reads the factory-energy CSV for Scope 1 & 2 estimates. |
| **2** | `product` + `bom_line` tables fed by real PLM/ERP; factors gain supplier + lifecycle-stage dimensions; static CSVs swapped for partner factor/EPD feeds. |
| **3** | Time-series `volume_forecast` (year × region); optimisation & MAC-curve views read cost + carbon jointly; scenario results become comparable over time. |
| **4** | Owner / tenant on every record; temporal `valid_from` / `valid_to` on all assumptions; full audit trail for assurance; regional & regulatory dimensions. |

**Current schema (Phase 1)** — see [`README.md`](README.md#data-model-phase-1) for the ER diagram:

- `MATERIAL_FACTOR` — sourced carbon-intensity factors (CSV, read-only)
- `BOM_LINE` — bill-of-material masses per transformer class (CSV, read-only)
- `RECOVERY_FACTOR` — per-component end-of-life recovery rates & routes (CSV, read-only)
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
- Module 4 rebuckets Modules 1–3 into GHG-Protocol Scope 1/2/3 for corporate reporting.
  Scope 1 & 2 use indicative factory-energy estimates — full metered factory data is a
  **Phase 2** deliverable.
- Full cradle-to-grave integration (A1–C4 + Module D) is a **Phase 2** deliverable.

---

*Maintained by Raka Adrianto — Sustainability, Product, Data ·
[LinkedIn](https://www.linkedin.com/in/lugasraka/)*
