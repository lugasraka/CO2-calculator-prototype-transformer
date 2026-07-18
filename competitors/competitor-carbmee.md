# Competitor Analysis — carbmee

## 1. Overview & positioning

carbmee is a Berlin-based enterprise software vendor positioning itself as an "Environmental Intelligence" platform. Its core product, **carbmee EIS™ (Environmental Intelligence System)**, is an AI-native "system of action" for environmental data, built on a granular transactional data foundation that connects products, sites, and supply chains. The platform spans three module families sold in all pricing tiers: **Company Carbon Accounting (CCF)**, **Supply Chain Emissions Management (SCF)**, and **Product Carbon Footprint (PCF)**, plus add-ons (API, Studio analytics, carbmee DB, advanced analytics, engineering services). Positioning language — "From BOM to Boardroom", "reduce Risk, Cost & Carbon", "real P&L impact beyond compliance" — targets enterprise manufacturers with complex supply chains rather than single-product LCA users. Marketing claims 5.8 Gt CO₂e "under management" (the homepage separately shows "85 Mt", an inconsistency worth noting) and an ROI study claiming 345% operational ROI and 4-month break-even. The company also sells compliance packages for CBAM, CSRD, EUDR, PPWR, and a Digital Battery Passport solution.

## 2. Target users & customers

- Primary buyer: enterprise manufacturers with global, multi-tier supply chains (automotive, manufacturing, consumer goods, electronics/semiconductor, aviation are the named industry pages).
- Named users by function: procurement & supply chain (sourcing decisions, RFPs), R&D (eco-design, PCF analysis of new materials), finance (sustainability/regulatory reporting), sustainability teams, supplier management.
- Publicly displayed customers (logo wall + case studies): Everllence (ex-MAN Energy Solutions), ZF, Schaeffler, Knorr-Bremse, Zeiss, Signify, KWS, Heraeus, Maersk, Lufthansa Technik, Ravensburger, Steinbeis, Speira, Purem, GF/Anglo American, Boeing, Skylotec — and **Siemens Energy, a transformer OEM** (logo shown; no linked case study publicly visible).
- Company size, funding, headcount: not publicly disclosed on fetched pages.

## 3. Business model & pricing (public info)

- B2B SaaS, quote-only. Four tiers — **Small, Medium, Large ("Most popular"), Enterprise** — all "Request Quote"; no list prices published.
- All tiers include CCF, SCF, PCF, carbmee DB, and CSRD support. Differentiation is by add-ons:
  - Carbon Forecasting, CBAM, EUDR, carbmee API: Large/Enterprise only.
  - carbmee Studio: not in Small; Advanced Analytics & Engineering Services: Large/Enterprise only.
  - Implementation and Supplier Engagement service levels: Light (Small) → Pro (Medium/Large) → Strategic (Enterprise).
- Also monetizes consulting ("carbmee Consulting") and managed onboarding ("from kickoff to full carbon visibility in 3 months", "full CBAM compliance within 3 months").
- Exact pricing: not publicly disclosed.

## 4. Capability mapping vs. our product

| Our capability | Their equivalent | Coverage (Full/Partial/None) | Notes |
|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | Carbon Cost Forecasting; "environmental ROI" framing | Partial | They forecast carbon *costs* (ETS/CBAM exposure) at company/supply-chain level; no public evidence of product-level use-phase loss modeling (e.g. transformer no-load/load losses → NPV TCO). B-module physics is our white space. |
| EOL/circularity & Module D credits | "Environmental Impact Management for Energy, Circularity & Ecodesign" solution page | Partial | Circularity named as a solution pillar, but no public detail on C1–C4 modeling or EN 15804 Module D recovery credits, retrofill vs. decommissioning logic. |
| BOM-based A1–A3 product carbon footprint | Dynamic PCF module + carbmee DB | Full | Core strength: SKU-level PCF from complex BOMs, "highly granular data for complex BOM", high geographical resolution for embedded emissions, live supplier data sync, material-swap simulation. |
| Portfolio scenario simulation & comparison | "Actionable Decarbonization Pathways and Scenario Modelling"; material-swap/procurement-shift simulation | Partial | Scenario modeling is claimed at PCF and supply-chain level; no public evidence of fleet/portfolio volume roll-ups with saved, comparable named scenarios as a first-class object. |
| Uncertainty ranges & data provenance | "Audit-ready", "audit-grade reports", AI data validation | Partial | Auditability is emphasized for compliance outputs; explicit per-factor uncertainty ranges/provenance metadata are not publicly disclosed. Our sourced-CSV provenance + uncertainty bounds are comparatively transparent by design. |
| Gate-ready design KPIs (e.g. kg CO₂e/kVA) | PCF hotspot analytics; eco-design insights for R&D | Partial | Generic eco-design decision support; no domain-specific normalized KPI (per-kVA, per-unit-loss) or PLM gate-review workflow artifacts publicly visible. |
| Abatement cost (€/t CO₂) ranking | "Most cost-effective reduction strategy"; Carbon Cost Forecasting | Partial | PCF page claims identifying "the most cost-effective reduction strategy", but a per-lever €/t ranking / MAC-style output is not publicly demonstrated. |
| Scenario persistence & export | Enterprise platform with central data model; Studio analytics | Partial | Persistence is inherent to a SaaS platform; explicit save/compare/export of design scenarios and CSV export are not publicly documented. |
| EPD data feeds / EPD automation | carbmee DB (SKU-level LCA data); Digital Battery Passport; supplier primary-data collection | Partial | Strong on supplier primary data + own LCA database; dedicated EPD ingestion/generation or EPD feed integration is not publicly disclosed. |
| PLM/ERP integration | carbmee EIS™ API; "works with any ERP, PLM, or procurement system"; JAGGAER partnership (RFQ module) | Full | Explicit ERP/PLM/procurement connectivity via API or CSV drag-and-drop; live JAGGAER procurement integration showcased. |
| Public API | carbmee EIS™ API | Full | Commercial API (Large/Enterprise add-on) for automated data collection and cross-department access to carbon data. Developer docs/pricing not public. |
| Regulatory reporting (CBAM/CSRD) | Dedicated CBAM, CSRD, EUDR, PPWR solutions; audit-grade EU-submission-ready reports | Full | Core commercial wedge; CBAM compliance "within 3 months" is a headline promise. |
| Transformer / electrical-equipment domain focus | Manufacturing & electronics/semiconductor industry pages; Siemens Energy logo | Partial | Horizontal platform, no transformer-specific models (losses, insulation fluids, CRGO steel, kVA normalization) publicly visible. Siemens Energy logo signals entry into our vertical — see §10. |

## 5. Lifecycle coverage (A1–A3 / A4–A5 / B / C / D)

- **A1–A3 (cradle-to-gate): strong.** This is the PCF module's center of gravity — BOM-level embedded emissions with geographic resolution and supplier primary data.
- **A4–A5: not publicly disclosed.** No explicit treatment of transport-to-site or installation phases found on fetched pages (though transactional Scope 3 categories likely cover upstream transport at corporate level).
- **B (use phase): weak/partial.** Carbon Cost Forecasting addresses future carbon *prices*, not product use-phase energy consumption modeling. No B1–B7-style use-stage engineering models publicly evidenced.
- **C (end-of-life): partial.** "Circularity" is a named solution pillar; C1–C4 process modeling is not publicly detailed.
- **D (beyond-system-boundary credits): not publicly disclosed.**
- Net: carbmee is optimized for corporate Scope 1–3 accounting + cradle-to-gate PCF, not full cradle-to-grave product LCA with use-phase and EOL engineering depth. Our B-phase TCO and C/D circularity modules are complementary-to-ahead in that narrow dimension.

## 6. Data, provenance & integrations

- **carbmee DB**: proprietary emission-factor/LCA database, pre-built datasets for complex BOMs, SKU-level granularity, "high geographical resolution for embedded emissions"; co-developed with industry partners; included in all pricing tiers.
- **AI-native data foundation**: real-time ingestion of transactions, supplier records, procurement data; automated mapping; AI validation; dedicated expert review during onboarding.
- **Supplier primary data**: structured supplier-engagement workflows with pre-built collection models (service-tiered Light/Pro/Strategic).
- **Integrations**: commercial API (agnostic to ERP/PLM/procurement systems), CSV drag-and-drop fallback, JAGGAER partnership embedding carbon data into RFQ processes, Catena-X PCF page (automotive data-space alignment).
- **Provenance/uncertainty**: "audit-ready/audit-grade" and "no black boxes" are the trust claims; explicit uncertainty quantification and per-datum source/validity metadata are not publicly disclosed. Our open CSV layer with provenance columns and uncertainty ranges is more inspectable, at prototype scale.

## 7. Strengths

- Full enterprise stack: CCF + SCF + PCF in every tier — one vendor covers corporate and product carbon.
- Regulatory moat: CBAM/CSRD/EUDR/PPWR packaged as audit-grade, submission-ready workflows with a 3-month time-to-compliance promise.
- Proprietary DB + supplier-engagement machinery: solves the Scope 3 primary-data problem at scale, which a prototype cannot.
- Enterprise integration story: API, JAGGAER partnership, Catena-X alignment, consulting/engineering services.
- Commercial proof: recognizable industrial logo wall (ZF, Schaeffler, Zeiss, Knorr-Bremse, Maersk, Boeing, Siemens Energy), case studies, ROI study (345% ROI, 4-month break-even claims).
- Positioning breadth: "Environmental Intelligence" framing expands beyond carbon into cost, risk, energy, ecodesign — budget-resilient vs. compliance-only tools.

## 8. Weaknesses / gaps

- Quote-only pricing, enterprise tiers gating API, forecasting, CBAM/EUDR — high entry barrier for mid-market and for engineering-led bottom-up adoption.
- No visible use-phase (B-module) engineering: no loss modeling, TCO/NPV payback for efficient designs, or energy-performance trade-off analysis at the product level.
- EOL/Module D depth not demonstrated despite "circularity" labeling.
- Horizontal platform: no transformer/electrical-equipment semantics (kVA normalization, CRGO/copper/fluid hotspots, IEC losses standards) publicly visible; domain fit requires configuration/services.
- Uncertainty quantification and factor-level provenance transparency not publicly evidenced — "audit-grade" ≠ open methodology.
- Inconsistent public metrics (5.8 Gt vs. 85 Mt CO₂e under management on different pages) suggests marketing numbers should be treated cautiously.
- Siemens Energy logo has no linked case study — depth of engagement in our vertical is unverifiable.
- Closed-source, no free/community tier; no self-serve evaluation path.

## 9. Differentiation — where we win / where they win

**Where we win**
- Use-phase economics: B1–B6 loss modeling → NPV TCO, lifetime CO₂, payback — carbmee has no public equivalent.
- Transformer-native KPIs (kg CO₂e/kVA), gate-review framing, and EOL/C1–C4 + Module D logic purpose-built for the domain.
- Transparent open-source data layer: sourced CSVs with provenance, uncertainty ranges, validity dates — inspectable by design vs. their black-box DB.
- Zero cost, self-serve, engineer-first adoption path vs. quote-only enterprise sales.
- Per-lever abatement cost (€/t) ranking as an explicit, comparable output.

**Where they win**
- Enterprise-grade Scope 3 / supplier primary-data collection at scale, with AI ingestion and managed onboarding.
- Regulatory compliance productization (CBAM/CSRD/EUDR/PPWR) with audit-grade outputs — our Phase 4 roadmap item, their shipping product.
- Real ERP/PLM/procurement integrations and a commercial API today (ours are roadmap).
- Proprietary emission-factor DB with geographic resolution vs. our static CSVs.
- Brand trust, case studies, and an existing Siemens Energy relationship inside our exact target vertical.

## 10. Threat level (High/Medium/Low) + rationale

**Threat level: Medium (trending High if they productize domain-specific PCF for electrical equipment).**

Rationale:
- *Different jobs-to-be-done today.* carbmee sells enterprise-wide carbon accounting + compliance to C-suite/procurement; we sell design-time cost+carbon decision support to engineering and gate reviewers. Direct feature collision is limited to BOM-based A1–A3 PCF — which is our Module 3 and their flagship.
- *Why not Low:* they already check several of our Phase 3/4 roadmap boxes (API, PLM/ERP integration, CBAM/CSRD, scenario modeling, multi-module platform), and the **Siemens Energy logo is a direct signal they are inside the transformer OEM segment** — the exact customer profile we target. If a customer's corporate function standardizes on carbmee, engineering tools risk being displaced by "good enough" platform PCF modules.
- *Why not High (yet):* no public evidence of use-phase loss/TCO modeling, EOL Module D depth, transformer-specific KPIs, or PLM gate-review artifacts; their go-to-market is top-down enterprise sales, not bottom-up design-engineering adoption; uncertainty/provenance transparency is a defensible niche for us.
- *Watch items:* any carbmee × Siemens Energy case study publication, ecodesign/EU-transformer-regulation features, EPD feed integrations, and extensions of their "Circularity & Ecodesign" pillar into B/C/D modules.

## 11. Sources

- https://www.carbmee.com (homepage — positioning, logo wall incl. Siemens Energy, "85 Mt CO₂e under management", ROI claims)
- https://www.carbmee.com/product/product-carbmee-eis (EIS platform capabilities, ZEISS quote, "5.8 Gt CO₂e under management")
- https://www.carbmee.com/solution/dynamic-product-carbon-footprints (Dynamic PCF: BOM-level PCF, supplier sync, material-swap simulation)
- https://www.carbmee.com/solution/the-only-carbon-management-and-accounting-platform (carbon accounting scope, onboarding, ERP/PLM connectivity, 3-month CBAM claim)
- https://www.carbmee.com/product/integrate-carbmee-eis-for-net-zero (API capabilities, departmental use cases, JAGGAER partnership)
- https://www.carbmee.com/pricing (tier structure Small/Medium/Large/Enterprise, module/add-on gating, quote-only)
- https://www.carbmee.com/customers (customer overview — returned minimal extractable content; logo evidence taken from homepage)
- https://www.carbmee.com/industries/manufacturing (manufacturing vertical positioning, Scope 3 focus)
- https://www.carbmee.com/product/carbmee-database (carbmee DB: SKU-level LCA data, geographic resolution, supplier footprints)
