# Competitor Analysis — One Click LCA

## 1. Overview & positioning
One Click LCA (Helsinki-based, One Click LCA Ltd.) is a mature, commercial LCA & EPD SaaS platform with two pillars: (a) design & construction LCA for buildings/infrastructure, and (b) a manufacturing suite for product LCAs, product carbon footprints (PCF), and automated EPD generation. Positioning: "The leading sustainability platform across industries" — AI-powered LCA & EPD software with "all the world's data" (500,000+ qualified LCA datasets, 170+ countries, 140+ standards/methods, 20+ integrations). The manufacturing offering targets full lifecycle product LCA (ISO 14040/44), PCF (ISO 14067), and verified EPDs (EN 15804, ISO 14025/21930), with regulatory alignment to CPR, CBAM, and ESPR. It is a horizontal, generalist platform — not an engineering-decision tool for a specific product domain. Its commercial gravity is compliance and disclosure (EPDs win tenders), not design-time cost/carbon optimization.

## 2. Target users & customers
- Manufacturing side: sustainability managers, product managers, engineers, and commercial teams at product manufacturers — explicitly "no LCA expertise required."
- Verticals: construction products (core), mechanical & electrical (MEP) products, and "other manufacturing" (electronics, complex products). Sector-specific EPD generators exist for concrete, luminaires, electronics, and HVAC.
- Named customers (from site logos/case studies): ArcelorMittal, Kingspan, Geberit, Wienerberger, Uponor, Lindab, Reynaers Aluminium, Peikko, Metsec, Whitecroft Lighting, Saint-Gobain, Genuit, Saudi Readymix, Blue Marble. Schneider Electric shares product data via the platform (press release referenced on MEP page).
- Adjacent users: AEC firms (AECOM, Arcadis, Ramboll, WSP, Foster+Partners) who consume EPD data — this makes One Click LCA a two-sided data marketplace between manufacturers and specifiers.

## 3. Business model & pricing (public info)
Quote-based SaaS subscription ("Request a quote" — no public list prices). Three manufacturing tiers:
- **Business**: EPD Generator module for one local standard (EN 15804+A1/+A2, INIES/PEP, NMD, ISO 21930/TRACI, NRMCA concrete); Excel import, IFC viewer, SolidWorks/Autodesk Inventor integrations; ISO 27001.
- **Expert Pack** (most popular): adds Materials Compass benchmarking, customized private LCA datasets, EPD templates, EPD Quality/Plausibility Checkers, dedicated account manager.
- **Power Pack**: unlimited project EPDs, free Manufacturer Pages (up to 50 EPDs), internal EPD verification, custom EPD templates.
Licensing: named-user or concurrent (3 users share 1 license, 1 active session). Add-ons: full Ecoinvent, Carbon Minds databases, company SSO. Sector EPD generators (luminaire, electronics, HVAC, concrete end-to-end verified) are "on request" upgrades. Actual prices: not publicly disclosed. Free tiers exist for educators/students/researchers. Enterprise plans via "Enterprise solutions."

## 4. Capability mapping vs. our product

| Our capability | Their equivalent | Coverage (Full/Partial/None) | Notes |
|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | LCA modeling of B-stage emissions ("Calculate all life-cycle stages including B stage emissions") | Partial | They quantify B-stage impacts; no NPV/TCO/payback economics. For transformers, no losses/load-profile modeling — B1–B6 for electrical equipment would need manual setup. |
| EOL/circularity & Module D credits | Full EN 15804 module set incl. C1–C4 and D in LCA/EPD engine | Full | Standard-compliant C & D modeling is core to EN 15804 EPDs. No transformer-specific retrofill/estering vs. decommissioning logic. |
| BOM-based A1–A3 product carbon footprint | Product Carbon Tool + Product LCA; BOM import via Excel, CAD (SolidWorks, Inventor), SAP S/4HANA BOM | Full | Their core strength; 500k+ datasets, generic + supplier-specific EPD data, multi-site/multi-product averaging. |
| Portfolio scenario simulation & comparison | "Create, copy, edit & lock alternatives"; compare alternatives with tables/charts; portfolio overview | Partial | Design-option comparison per product; no fleet-volume portfolio simulator with saved named scenarios as a decision workflow. |
| Uncertainty ranges & data provenance | Verified datasets, EPD Quality/Plausibility Checkers, audit trails | Partial | Data quality is managed (verification, plausibility), but explicit quantitative uncertainty bounds on results are not advertised. |
| Gate-ready design KPIs (e.g. kg CO₂e/kVA) | Compliance-oriented outputs (GWP per declared unit, EPD tables) | Partial | KPIs are per declared/functional unit for EPDs, not configurable engineering gate KPIs like kg CO₂e/kVA at a design review. |
| Abatement cost (€/t CO₂) ranking | Not found on fetched pages | None | They mention "consider carbon pricing during procurement" (MEP page) but no MAC/abatement-cost ranking feature is publicly visible. |
| Scenario persistence & export | Cloud projects, folders, archive; machine-readable outputs (ILCD+EPD, ISO 22057, OpenEPD); report downloads | Full | Mature persistence, versioning, and export far beyond our SQLite/CSV prototype. |
| EPD data feeds / EPD automation | EPD Generator, Pre-Verified EPD Generator, EPD Hub publishing, EPD Usage Analytics, Manufacturer Pages | Full | Industry-leading; publish to EPD Hub in one click; verification workflows; this is their core moat. |
| PLM/ERP integration | SAP S/4HANA BOM integration; CAD integrations (SolidWorks, Inventor); Excel/CSV; custom XML/JSON/web services | Partial | ERP yes (SAP); no named PLM-system (Teamcenter/Windchill/3DX) integration publicly listed. |
| Public API | "API integration" for data import (PCF page); custom integrations via web services | Partial | API is referenced for data onboarding; no public developer API documentation found on fetched pages. Scope not publicly disclosed. |
| Regulatory reporting (CBAM/CSRD) | CBAM/CPR/ESPR compliance guidance; CBAM explicitly supported in PCF reporting; EN 15804, ISO 14067 | Partial | CBAM yes (product-level embedded emissions); CSRD corporate reporting is not their stated scope on fetched pages. |
| Transformer / electrical-equipment domain focus | MEP products vertical (TM65 data), electronics EPD generator, "electrical products" listed under PCF coverage | Partial | Electrical equipment is a served category, but there is no transformer-specific modeling (losses, kVA rating, oil/retrofill, core/copper mass breakdowns). |

## 5. Lifecycle coverage (A1–A3 / A4–A5 / B / C / D)
Full cradle-to-grave coverage is the core promise: EN 15804 modules A1–A3 (production), A4–A5 (transport/construction), B-stage (use — explicitly "Calculate all life-cycle stages including B stage emissions"), C1–C4 (end-of-life), and Module D (beyond-system-boundary benefits) as required for compliant EPDs. PCF tool markets "cradle-to-grave emissions for any product" and "production to disposal." Coverage is standards-driven and generic — depth per module depends on user-supplied foreground data; B-stage for electrical products (e.g., transformer no-load/load losses over 30+ years) is not pre-modeled for the domain the way our prototype does.

## 6. Data, provenance & integrations
- **Data**: 500,000+ qualified LCA/EPD datapoints; generic materials/energy/process database; standard LCI sources (AusLCI, BAFU, Federal LCA Commons, Idemat, PlasticsEurope, ProBas, Worldsteel, WEEE); Ecoinvent (subset included, full DB as add-on); Carbon Minds (add-on); CEPE via membership; extensive verified global EPD database incl. manufacturer-specific MEP EPDs and CIBSE TM65 data.
- **Provenance/quality**: EPD Quality Checker, EPD Plausibility Checker, verification workflows with full audit trails, machine-readable outputs (ILCD+EPD, ISO 22057, OpenEPD), AI-assisted data mapping with inconsistency flagging.
- **Integrations (20+)**: BIM (Revit, Tekla, Archicad, IFC, Navisworks, Solibri, Vectorworks, Allplan, Bentley iTwin, Trimble Connect), energy (IES-VE, DesignBuilder), manufacturing/CAD (SolidWorks, Autodesk Inventor), ERP (SAP S/4HANA BOM), Excel/CSV, Procore, Qflow, custom XML/JSON/web services. Security: ISO 27001, SOC2, Cyber Essentials Plus; SSO add-on.

## 7. Strengths
- **EPD industrialization**: guided 6-step EPD workflow, pre-verified generators (EN 15804, INIES/PEP, NMD, ISO 21930/TRACI), one-click EPD Hub publishing, internal verification — reduces EPD lead time "from months to days."
- **Data moat**: largest construction LCA/EPD database; verified, supplier-specific data; two-sided network effect (manufacturers publish → AEC specifies).
- **Compliance breadth**: 140+ standards/methods, CPR/CBAM/ESPR positioning, regional EPD program operators.
- **Enterprise maturity**: ISO 27001/SOC2, audit trails, multi-site averaging, portfolio management, SAP S/4HANA BOM import, concurrent licensing, 170+ countries.
- **Momentum in electrical/MEP**: MEP Carbon Tool with TM65 data, electronics EPD generator, Schneider Electric data partnership — encroaching on our domain.

## 8. Weaknesses / gaps
- **No engineering economics**: no TCO/NPV/payback, no €/t abatement ranking — carbon is a disclosure metric, not a design-time decision variable combined with cost.
- **No transformer domain model**: no kVA-rated functional KPIs, no loss modeling (B1 use-phase for electrical equipment is generic), no oil/retrofill/EOL scenarios specific to transformers.
- **Quote-only pricing** and mandatory paid onboarding ("mandatory for commercial use") — high entry barrier vs. a free open-source prototype.
- **Black-box SaaS**: proprietary; uncertainty quantification on results not publicly advertised; API scope not publicly documented.
- **PLM gap**: SAP and CAD covered, but no named PLM (Teamcenter, Windchill, 3DEXPERIENCE) integrations publicly listed — our Phase 4 PLM-gate API targets exactly this seam.
- **Construction gravity**: brand, database, and templates are construction-centric; discrete electrical-equipment manufacturing is a newer adjacency.

## 9. Differentiation — where we win / where they win

**Where we win**
- Design-time decision support: combined cost+carbon (TCO, payback, €/t abatement) vs. their compliance/disclosure orientation.
- Transformer specificity: B1–B6 loss modeling, kg CO₂e/kVA gate KPIs, retrofill vs. decommissioning — none of which they offer out of the box.
- Transparency & price: open-source, sourced CSVs with explicit uncertainty ranges and validity dates; zero license cost for evaluation.
- PLM-gate fit (roadmap): API-first gate checks for design reviews — a workflow they don't target.

**Where they win**
- Everything EPD: generation, verification, publishing, analytics — we have none and should not build it.
- Data breadth/verification, enterprise security, standards coverage, and market trust (G2 4.5/5, global brand).
- Scale & persistence: multi-user cloud, audit trails, machine-readable EPD exports.

**Competitor vs. EPD-data-partner assessment**: One Click LCA is simultaneously (a) an indirect competitor for a manufacturer's sustainability budget, and (b) the most credible **EPD data source** for our Phase 2 "live EPD data feed." Their database aggregates exactly the supplier-specific A1–A3 factors (steel, copper, electrical steel, insulation, MEP/electronics EPDs) our Portfolio CO₂ Simulator needs. Practical stance: treat them primarily as a **data/partner channel** (EPD data consumption via their machine-readable formats — ILCD+EPD, OpenEPD, ISO 22057 — or commercial data licensing) and only secondarily as a competitor. Risk: data licensing terms and API access are not publicly disclosed; partnership viability must be validated commercially. Positioning guardrail: we must never position as an "EPD tool" — we are the design-decision layer upstream of EPDs.

## 10. Threat level (High/Medium/Low) + rationale
**Medium.** Direct functional overlap with our three modules is low (they lack TCO/abatement economics, transformer physics, and gate KPIs), and partnership-as-data-source is plausible. However, threat is not Low because: (1) they are well-funded, enterprise-grade, and already moving into electrical/MEP manufacturing with SAP BOM integration — the same BOM-driven A1–A3 workflow as our Portfolio simulator; (2) their platform could add "portfolio scenario" or eco-design features and absorb our use case for customers already paying for their suite; (3) procurement preference for established vendors (ISO 27001/SOC2) disadvantages an open-source prototype in enterprise IT reviews. Threat rises to High if they ship transformer/electrical-equipment-specific templates or PLM-gate integrations before our Phase 4.

## 11. Sources
- https://oneclicklca.com (homepage)
- https://oneclicklca.com/software/manufacturing (manufacturing suite overview)
- https://oneclicklca.com/software/manufacturing/epd-generator
- https://oneclicklca.com/software/manufacturing/product-carbon-footprint
- https://oneclicklca.com/pricing/product-lca-and-epd-pricing
- https://oneclicklca.com/why-us/capabilities/integrations
- https://oneclicklca.com/industries/manufacturing/mep-products
