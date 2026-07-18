# Competitive Landscape Summary — Transformer Decarbonization Manager

Synthesis of five per-competitor analyses (Makersite, sustamize, carbmee, Sphera/GaBi, One Click LCA) against our open-source transformer decarbonization prototype. Date: July 2026.

## 1. The five competitors at a glance

| Competitor | One-line positioning | Threat level |
|---|---|---|
| Makersite | AI-powered product-lifecycle-intelligence platform: cost+carbon+compliance digital twins inside PLM workflows, now owning PCF-exchange rails (SiGREEN→Mattermaps) | High (directional); Medium head-to-head today |
| sustamize | Data-as-a-Service: 150k+ validated CO₂e factor database with API-first embedding into ERP/PLM/cost tools | Medium (mostly potential supplier) |
| carbmee | Enterprise "Environmental Intelligence" suite (CCF+SCF+PCF) with audit-grade CBAM/CSRD compliance; Siemens Energy logo | Medium, trending High |
| Sphera (GaBi) | 30-year LCA incumbent: 20k+ DEKRA-verified datasets, portfolio LCA automation, expert-to-non-expert product tiers | Medium |
| One Click LCA | Horizontal LCA/EPD SaaS leader (construction gravity) industrializing EPD generation, expanding into MEP/electrical | Medium |

## 2. Capability comparison matrix

Values derived from each file's section 4 (Full / Partial / None). "Us" reflects the prototype as implemented today; roadmap items marked explicitly.

| Capability | Makersite | sustamize | carbmee | Sphera (GaBi) | One Click LCA | Us (prototype today) |
|---|---|---|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | Partial | Partial | Partial | Partial | Partial | **Full** |
| EOL/circularity & Module D credits | Partial | Partial | Partial | Partial | Full | **Full** |
| BOM-based A1–A3 PCF | Full | Full | Full | Full | Full | Full (manual CSV factors) |
| Portfolio scenario simulation & comparison | Full | Partial | Partial | Full | Partial | **Full** |
| Uncertainty ranges & data provenance | Partial | Partial | Partial | Partial | Partial | **Full** (sourced CSVs, bounds) |
| Gate-ready design KPIs (kg CO₂e/kVA) | Partial | None | Partial | None | Partial | **Full** |
| Abatement cost (€/t CO₂) ranking | Partial | None | Partial | None | None | **Full** |
| Scenario persistence & export | Full | Partial | Partial | Partial | Full | Full (SQLite/CSV, prototype-grade) |
| EPD data feeds / automation | Full | None | Partial | Full | Full | None (Phase 2 roadmap) |
| PLM/ERP integration | Full | Full | Full | Full | Partial | None (Phase 2/4 roadmap) |
| Public API | Full | Full | Full | None | Partial | None (Phase 4 roadmap) |
| Regulatory reporting (CBAM/CSRD) | Full | Full | Full | Partial | Partial | None (Phase 4 roadmap) |
| Transformer/electrical-equipment domain focus | None | None | Partial | Partial | Partial | **Full** |

Pattern check: A1–A3 PCF is Full for all five (commoditized). Use-phase economics, gate KPIs, abatement ranking, and quantified uncertainty are Partial-or-None for all five (our four working modules).

## 3. Positioning map

X-axis: after-the-fact reporting & compliance ↔ design-time decision support. Y-axis: generalist / cross-industry ↔ electrical-equipment specific.

| Quadrant | Player | Justification |
|---|---|---|
| Generalist × After-the-fact | carbmee | Sells enterprise carbon accounting + submission-ready CBAM/CSRD to C-suite/procurement; use moment is reporting, not design review |
| Generalist × After-the-fact | Sphera (GaBi) | LCAs and EPDs are reports produced by sustainability experts; no design-gate or economics layer |
| Generalist × After-the-fact | sustamize | Factor data infrastructure feeding PCF/Scope 3 compliance; decision support delegated to partners |
| Generalist × After-the-fact (leaning design) | One Click LCA | Gravity is EPD disclosure ("EPDs win tenders"); design alternatives exist but serve compliance outputs |
| Generalist × Design-time | Makersite | The only competitor whose thesis (cost+carbon jointly at design/procurement time, inside PLM) matches ours — but horizontal, no domain physics |
| Electrical-specific × After-the-fact | (contested edge) | One Click LCA's MEP/TM65 vertical and Schneider Electric data sharing are the closest encroachment; carbmee's Siemens Energy logo similarly signals entry |
| Electrical-specific × Design-time | **Us — alone** | Transformer loss physics (B1–B6), kVA-normalized gate KPIs, retrofill logic, €/t ranking; no competitor occupies this quadrant |

## 4. Key takeaways

- **Everyone already ships A1–A3 BOM-based PCF** (Full ×5) with data layers we cannot match (140+ Makersite sources, 150k+ sustamize factors, 20k+ DEKRA-verified Sphera datasets, 500k+ One Click LCA datapoints). Our Module 3's factor layer is not a moat; the gate KPI, uncertainty bounds, and €/t ranking built on top of it are.
- **Nobody ships use-phase loss economics.** All five are Partial on B1–B6: they model generic use-phase energy, none model transformer load/no-load losses → NPV TCO → payback. This is the single largest uncontested capability.
- **Nobody productizes abatement-cost ranking** (3× None, 2× Partial). A per-lever €/t CO₂ output — our abatement ranking and Phase 3 MAC ambition — has no direct equivalent in any competitor's public product.
- **Our Phase 2 and Phase 4 roadmap items are their shipping products.** Live EPD feeds (Makersite, Sphera, One Click LCA), PLM/ERP integration (Makersite, sustamize, carbmee, Sphera), public APIs (Makersite, sustamize, carbmee), CBAM/CSRD reporting (Makersite, sustamize, carbmee) all exist today. We are building toward their present — partner, don't rebuild.
- **Consolidation signal: Makersite acquired SiGREEN → Mattermaps (June 2026)**, combining calculation engine + PCF-exchange network (Catena-X, TfS, PACT). This is a platform play to own the rails through which supplier PCF data flows — the infrastructure layer our Phase 4 gate checks would ultimately sit on.
- **Competitors are already inside our vertical.** Schneider Electric uses Makersite (EPDs across 200k+ SKUs) and shares product data via One Click LCA; Siemens Energy (a transformer OEM) appears on carbmee's logo wall. No transformer-specific product exists yet, but the beachheads do.
- **Quantified uncertainty is unproductized everywhere** (Partial ×5). All claim "audit-ready" provenance; none publish numeric uncertainty ranges per factor/result. Our uncertainty-first transparent CSV layer is a durable, defensible differentiator for the auditor-skeptic niche.
- **Two "competitors" are more valuable as suppliers.** sustamize (factor data) and One Click LCA (EPD data via ILCD+EPD/OpenEPD/ISO 22057) map directly onto our Phase 2 data-feed needs and structurally lack our decision layer.

## 5. White-space opportunities for us

- **Use-phase loss economics (B1–B6 → NPV TCO, payback):** uncontested across all five; the dominant lifecycle impact of a transformer is precisely what none of them model.
- **Gate-ready domain KPIs (kg CO₂e/kVA):** no competitor has a design-gate concept or rating-normalized KPI; we can own the pass/fail artifact for PLM design reviews.
- **€/t abatement ranking per design lever:** absent everywhere; extends naturally into Phase 3 MAC curves — claim it now before a platform vendor adds it as a feature.
- **Transformer-specific EOL decision logic:** One Click LCA covers C1–C4/Module D for standards compliance, but no one offers retrofill-vs-decommissioning decision support (fluids, CRGO/copper recovery economics).
- **Uncertainty as a first-class product feature:** sourced factors with explicit ranges and validity dates, inspectable end-to-end — the opposite of every competitor's black-box SaaS.
- **Open-source, zero-friction bottom-up adoption:** all five are quote-only enterprise sales with no self-serve path (Sphera's 45-day trial and sustamize's 14-day trial excepted); an engineer-led pilot motion is structurally unavailable to them.

## 6. Roadmap implications (Phase 2–4)

### Phase 2 — live PLM/EPD feeds + cradle-to-grave

- **Accelerate:** EPD/factor data ingestion via partnership. Evaluate sustamize's API (JSON, sandbox, ISO 14064-3-validated factors) to replace/validate our sourced CSVs, and One Click LCA's machine-readable outputs (ILCD+EPD, OpenEPD, ISO 22057) for supplier-specific A1–A3 data (steel, copper, electrical steel, insulation, MEP/electronics). Both files independently conclude these two are primarily data suppliers, not rivals.
- **De-prioritize:** building our own factor database. We cannot out-curate 150k+ validated sustamize factors or 20k+ DEKRA-reviewed Sphera datasets; our CSVs should become a transparent reference layer validated against commercial feeds, not a competing database.
- **Partner instead of build:** PLM connectors. Makersite (Teamcenter/Windchill), Sphera, and sustamize already own enterprise PLM plumbing; our Phase 2 entry should be standard BOM import formats (and later Mattermaps-network PCF exchange compatibility) rather than bespoke connectors.

### Phase 3 — optimization / MAC curves / SBTi

- **Accelerate:** abatement-cost ranking → full MAC curves. This is our clearest white space (None ×3, Partial ×2) and no file shows any competitor moving toward it. Ship per-lever €/t as the signature output of the portfolio simulator.
- **Accelerate:** gate-KPI artifacts (kg CO₂e/kVA pass/fail) as exportable design-review objects — the workflow seam nobody covers.
- **De-prioritize/skip:** SBTi corporate-target tooling and corporate carbon accounting. carbmee (CCF module, all tiers), Makersite (Scope 1–3), and Sphera (ESG suite) already own corporate-level decarbonization; we should stay at the product/design layer and reference corporate targets only as constraints.

### Phase 4 — platform, API, audit, CBAM/CSRD

- **Accelerate:** a narrow, open public API for PLM-gate carbon checks — the specific seam One Click LCA publicly lacks (no Teamcenter/Windchill/3DX listed) and where openness beats Makersite's enterprise-gated API. Align exports with OpenEPD/ILCD machine-readable formats for interoperability.
- **De-prioritize/skip:** building CBAM/CSRD reporting engines. Makersite (named CBAM product), sustamize (compliance data), and carbmee ("full CBAM compliance in 3 months") ship audit-grade reporting; we should emit compliant inputs to those tools, not compete with them.
- **Partner instead of build:** audit credibility. Pursue third-party validation of our methodology/data layer (the sustamize–GUTcert ISO 14064-3 pattern, or DEKRA-style review à la Sphera) rather than self-asserting audit-readiness. Do **not** build EPD generation — One Click LCA, Makersite, and Sphera own it; position permanently as the design-decision layer upstream of EPDs.

## 7. Threat ranking & watch triggers

| Competitor | Threat level | What would make it worse (watch trigger) | Recommended response |
|---|---|---|---|
| Makersite | High (directional) | A "heavy electrical equipment" vertical template on their platform; deeper Schneider Electric engagement toward transformers; Mattermaps adding gate-KPI features | Accelerate domain moat (loss physics, gate KPIs); build Mattermaps/Catena-X-compatible export rather than competing with the network; lean on open-source transparency |
| carbmee | Medium (trending High) | Published Siemens Energy case study; "Circularity & Ecodesign" pillar extending into B/C/D modules; ecodesign features for EU transformer regulation | Differentiate on use-phase economics and bottom-up engineer adoption; monitor quarterly |
| One Click LCA | Medium | Transformer/electrical-equipment-specific EPD templates; PLM-gate integrations; portfolio-simulator features absorbing our use case | Pursue EPD-data partnership early; never position as an EPD tool; exploit their PLM gap with our Phase 4 gate API |
| Sphera (GaBi) | Medium | Consulting arm hand-building transformer LCAs for a large OEM; opening a public API; LCA Automation owning the PLM-gate interface | Coexist: position as the decision layer upstream of their LCA infrastructure; keep data layer interoperable |
| sustamize | Medium (indirect) | Embedded by Siemens/tset/cost-engineering partners into gate-review tooling — our niche powered silently by their data | Integrate their API first (make them our supplier before a rival does); validate our CSVs against their factors |

## Appendix

Source files (all local):

- [competitor-makersite.md](competitor-makersite.md)
- [competitor-sustamize.md](competitor-sustamize.md)
- [competitor-carbmee.md](competitor-carbmee.md)
- [competitor-sphera-gabi.md](competitor-sphera-gabi.md)
- [competitor-one-click-lca.md](competitor-one-click-lca.md)
