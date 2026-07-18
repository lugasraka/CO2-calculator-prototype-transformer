# Competitor Analysis — Makersite

## 1. Overview & positioning
Makersite (Makersite GmbH, Stuttgart) positions itself as an **AI-powered "Product Lifecycle Intelligence" platform**: a cloud SaaS that connects a manufacturer's product data (BOMs from CAD/PLM/ERP) to a large harmonized supply-chain database, producing digital twins of products that can be analyzed across cost, carbon/environment, compliance, health/safety (EHS), and supply-chain risk simultaneously. The pitch is "one model, multi-output": from a single product digital twin, teams generate LCAs, PCFs, EPDs, Scope 1–3 reports, should-costs, and compliance checks — claimed to be up to 50x faster than traditional methods. Unlike pure carbon-accounting tools, Makersite sells *multi-criteria decision support at design and procurement time*, which puts it conceptually closest to our product's thesis (cost + carbon jointly, at design time) — but generic and horizontal rather than transformer-specific.

Strategically important: in June 2026 Makersite completed the acquisition of **SiGREEN from Siemens AG**, rebranded as **Mattermaps** — Siemens' PCF and supply-chain carbon-data exchange platform (multi-network: TfS, Catena-X, PACT). Mattermaps continues as a standalone exchange platform, but Makersite plans to feed its AI/data assets into it. This moves Makersite from "LCA tool vendor" toward owning both the calculation engine *and* the network through which PCF data flows between suppliers and OEMs — a direct play to become the default infrastructure for Scope 3 / product-level carbon data exchange.

## 2. Target users & customers
Makersite explicitly targets four personas, overlapping almost 1:1 with ours:
- **Engineers / product designers** — ecodesign, material alternatives, cost and compliance checks without expert gatekeepers; claims ~10% faster time-to-market and ≥20% fewer design failures.
- **Procurement** — should-costing, supplier comparison, deep-tier supply-chain visibility.
- **Sustainability experts** — automated LCA/PCF/Scope 3, EPD generation at scale.
- **Compliance/EHS experts** — REACH, RoHS, POP, Prop 65, PFAS tracking.

Named customers (from the site): Microsoft (Surface Pro 10 ecodesign), Lenovo (configuration-level PCFs for ThinkPad), Barco (automated LCAs/PEFs for EU Taxonomy), Cummins, Schaeffler, 3M, and — most relevant to us — **Schneider Electric**, which is using Makersite to scale EPDs and ecodesign across >200,000 SKUs. Schneider's presence signals Makersite already has a beachhead in electrical equipment, adjacent to transformers.

## 3. Business model & pricing (public info)
Annual SaaS subscription, three tiers, all **"custom price"** (no public numbers; actual € amounts not publicly disclosed):
- **Pro** — consultants/small business: 1 user, 2,000 "Material Components", multi-tenant cloud.
- **Teams** — up to 10 users, 4,000 Material Components, Makersite Connect, technical support.
- **Enterprise** — 10+ users, 50,000 Material Components, dedicated cloud hosting, enterprise SLA, custom integrations (extra cost).

Commercial terms: 12-month licenses paid annually upfront by wire transfer; multi-year possible; volume discounts for Teams/Enterprise; overage handled via quarterly/semi-annual usage reviews rather than automatic charges. The "Material Component" metering unit (BOM/parts line items) means cost scales with portfolio breadth — a pricing model oriented to large manufacturers, not to a single engineering team experimenting with one product line.

## 4. Capability mapping vs. our product

| Our capability | Their equivalent | Coverage (Full/Partial/None) | Notes |
|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | Full cradle-to-grave LCA incl. use phase; should-costing apps | Partial | Makersite models use-phase impacts generically via activity-based LCA, but there is no transformer-loss (load/no-load) model, no NPV/payback framing for high-efficiency designs. Cost side is purchase/should-cost, not lifetime TCO from energy losses. |
| EOL/circularity & Module D credits | Cradle-to-grave LCA incl. disposal; recycled-materials apps | Partial | Full LCA scope implies C1–C4 and recycling credits, but no explicit Module D retrofill-vs-decommissioning decision workflow for transformers; not marketed as a circularity planner. |
| BOM-based A1–A3 product carbon footprint | Core strength: automated LCA/PCF from BOMs mapped to 140+ data sources | Full | This is their flagship use case (Lenovo PCFs, Barco LCAs). Far more automated and data-rich than our CSV-factor approach. |
| Portfolio scenario simulation & comparison | Digital-twin "what-if" scenarios, compare multiple designs simultaneously; portfolio dashboards | Full | Interactive scenario comparison across criteria is a headline feature ("Discover all the What-ifs"). |
| Uncertainty ranges & data provenance | Harmonized data ecosystem, expert quality checks, "audit-proof" claims; traceability emphasized | Partial | Provenance/traceability is claimed, but explicit quantified uncertainty ranges (as in our CSV uncertainty fields) are not publicly documented. |
| Gate-ready design KPIs (e.g. kg CO₂e/kVA) | Ecodesign criteria embedded in Teamcenter/Windchill design workflows; ESPR/DPP readiness | Partial | They embed sustainability into PLM workflows (the gate *process*), but a domain-normalized KPI like kg CO₂e/kVA is ours alone; they offer generic multi-criteria dashboards. |
| Abatement cost (€/t CO₂) ranking | Cost and carbon analyzed side-by-side (should-cost + LCA) | Partial | Joint cost/carbon trade-offs exist, but no explicit per-lever €/t abatement-cost ranking or MAC-curve feature is publicly documented. |
| Scenario persistence & export | Cloud platform with saved models; export of visualizations/data for reports and internal systems | Full | Enterprise-grade persistence and sharing exceeds our SQLite/CSV prototype approach. |
| EPD data feeds / EPD automation | End-to-end EPD automation at scale; program-operator compliance (PEP Ecopassport, EPD Norge, EPD International, IBU); guided tool verification | Full | Major differentiator for them; Schneider Electric scaling EPDs across 200k+ SKUs. Our roadmap item is already their shipping product. |
| PLM/ERP integration | API-first; Teamcenter Sustainability LCA (Siemens Xcelerator), PTC Windchill, Autodesk Fusion, Ansys; 10+ default importers | Full | Deepest PLM integration story in the category — sustainability inside the engineering workflow, exactly our Phase 4 ambition. |
| Public API | "API-first principle" stated; Makersite Connect in Teams/Enterprise tiers | Full | Documented as a design principle; detailed API docs not public, but availability is explicit. |
| Regulatory reporting (CBAM/CSRD) | Dedicated CBAM compliance automation page; Scope 3 software; EU Taxonomy/PEF (Barco case); ESPR/DPP positioning | Full | CBAM is a named product offering; CSRD-adjacent via Scope 3 and EU Taxonomy reporting. |
| Transformer / electrical-equipment domain focus | None transformer-specific; horizontal across electronics, automotive, chemicals, CPG | None | Schneider Electric (electrical equipment) is a customer, but no transformer physics (losses, kVA rating, insulation fluids, core steel grades) anywhere in the product. |

## 5. Lifecycle coverage (A1–A3 / A4–A5 / B / C / D)
Makersite claims **full cradle-to-grave** coverage via activity-based LCA modeling: raw materials and manufacturing (A1–A3), downstream lifecycle, use phase (B), and end-of-life/disposal (C, with recycling credits implying D). Their marketing explicitly says "from raw material to end of life" and "how they are made, used, and disposed of." In practice the depth of use-phase modeling depends on user-supplied activity data — for transformers, the dominant B-phase (decades of electrical losses) would need to be modeled manually; there is no built-in losses engine. Our product today covers A1–A3 (bottom-up BOM), B1–B6 (losses → TCO/CO₂), and C1–C4 + Module D explicitly, with transformer-specific models — narrower automation, deeper domain semantics.

## 6. Data, provenance & integrations
- **Data foundation**: 140+ (FAQ says 150+) integrated public/private data sources; 36,000+ industrial processes, 600,000+ environmental impacts, 100,000+ materials with physical properties; claims ~34% of global supply chains covered. Partners include ecoinvent and Carbon Minds.
- **AI/knowledge graph**: proprietary mapping engine auto-links BOM line items to supply-chain data; recommendation engine fills model gaps; expert quality checks for "audit-proof" results.
- **Integrations**: Siemens Teamcenter (Sustainability Lifecycle Assessment, part of Xcelerator), PTC Windchill, Autodesk Fusion, Ansys; CAD/ERP/PLM/PDM importers; open API.
- **Mattermaps (ex-SiGREEN)**: supplier↔buyer PCF data exchange across TfS, Catena-X, PACT networks — primary-data collection channel that feeds the calculation platform.
- **Security/compliance**: ISO 27001 (Bureau Veritas), TISAX, GDPR-verified; multi-tenant or dedicated cloud hosting.

## 7. Strengths
- **Data moat**: the breadth of the harmonized database plus AI BOM-mapping removes the #1 LCA bottleneck (data collection/mapping); very hard for a prototype or new entrant to replicate.
- **Full-lifecycle, multi-criteria in one model**: carbon, cost, compliance, EHS, risk from a single digital twin — matches how decisions are actually made.
- **PLM-native**: Teamcenter/Windchill/Autodesk/Ansys integrations put sustainability inside the design workflow, not in a separate tool — directly addresses our target users' environment.
- **EPD at industrial scale**: program-operator compliance (PEP, IBU, EPD International/Norge) and the Schneider Electric 200k-SKU deal prove scalable declaration automation.
- **Network ownership via Mattermaps**: acquiring SiGREEN gives them the PCF exchange rails (Catena-X, TfS, PACT) — a two-sided platform play competitors lack.
- **Enterprise credibility**: ISO 27001/TISAX, named Fortune-500 customers, Forrester study, partner network (Hitachi, Accenture, Siemens, PTC).

## 8. Weaknesses / gaps
- **No domain depth for transformers**: no losses model (load/no-load), no kVA-normalized KPIs, no TCO-from-efficiency logic, no retrofill/EOL decision workflows. A transformer manufacturer gets a generic LCA tool, not a design-trade-off tool for efficiency classes.
- **Opaque, enterprise-priced**: all tiers "custom price," annual upfront, component-metered — high friction for a single product line or mid-size manufacturer; no self-serve evaluation path.
- **Use-phase economics are not the product**: their cost apps are should-cost/purchase-cost oriented; lifetime NPV/payback of high-efficiency designs (our Module 1) is not a marketed capability.
- **Uncertainty handling not public**: provenance is claimed, but explicit uncertainty ranges on factors/results (our standard feature) are not documented publicly.
- **Black-box risk**: AI auto-mapping plus proprietary data raises verifier/auditor questions for regulated declarations; they counter with "guided tool verification," but it's a services-heavy path.
- **Complexity/overhead**: 50+ apps and enterprise integrations imply onboarding effort (they sell implementation services); overkill for a focused decarbonization decision.

## 9. Differentiation — where we win / where they win

**Where we win**
- Transformer physics and economics: B1–B6 losses → NPV TCO, payback, and kg CO₂e/kVA gate KPIs are decisions Makersite's generic LCA cannot express out of the box.
- Speed-to-insight and accessibility: open-source, self-hosted, zero license cost vs. custom-priced annual enterprise contracts — we fit a pilot team, they fit a corporate rollout.
- Transparent data layer: sourced CSVs with provenance, uncertainty ranges, and validity dates — auditable by construction, vs. their proprietary mapped database.
- Focused decision workflows (TCO/ROI, EOL retrofill, portfolio abatement €/t) instead of a 50-app platform requiring enablement.

**Where they win**
- Automation and data scale: AI BOM-mapping against 140+ sources vs. our manual CSV factor tables; they already do live EPD/LCA at portfolio scale (our Phase 2).
- PLM/ERP integration today (Teamcenter, Windchill, Autodesk, Ansys) vs. our Phase 4 roadmap.
- Enterprise readiness: security certifications, SLAs, multi-tenant cloud, audit support, named customers in adjacent electrical equipment (Schneider).
- Network effects: Mattermaps gives them supplier primary-data exchange (Catena-X/TfS/PACT) — a data flywheel we cannot match.

## 10. Threat level (High/Medium/Low) + rationale
**High** (as a directional/strategic threat; Medium as an immediate head-to-head threat).

Rationale: Makersite's stated thesis — cost + carbon + compliance jointly, inside design workflows, via PLM — is precisely our product's end-state vision, and they already execute it at enterprise scale with the data, integrations, certifications, and customer logos (including Schneider Electric in electrical equipment) to prove it. The SiGREEN→Mattermaps acquisition extends them into the PCF data-exchange network, making them a candidate *platform* for exactly the PLM-gate carbon KPIs we prototype. If a transformer OEM's sustainability or PLM organization goes shopping, Makersite is a credible incumbent. Mitigants: they have no transformer-domain modeling (losses, kVA KPIs, TCO-from-efficiency, retrofill), their pricing/procurement friction excludes the pilot-team segment we serve, and our open-source transparency and uncertainty-first data layer answer the auditor-skeptic niche. The realistic threat is not feature-for-feature competition today, but Makersite (or a partner) templating a "heavy electrical equipment" vertical on top of their platform — their Schneider relationship is the early-warning signal to watch.

## 11. Sources
- https://makersite.io/ (homepage: positioning, customers, partners, workflow)
- https://makersite.io/makersite-ai-data-apps/ (AI/data foundation, FAQ, integrations, security)
- https://makersite.io/features-and-benefits/ (feature set, business/environment/compliance/health apps)
- https://makersite.io/pricing/ (tiers, Material Component metering, contract terms)
- https://makersite.io/for-engineers/ (engineer persona, claims on TTM/design failures, ecodesign)
- https://makersite.io/get-to-net-zero/epd-automation-and-scale/ (EPD automation, Schneider Electric case, program operators)
- https://makersite.io/siemens-makersite-real-time-sustainability-in-product-development/ (Teamcenter integration, ESPR/DPP positioning)
- https://makersite.io/press/sigreen-becomes-mattermaps-as-makersite-completes-ownership-transition/ (SiGREEN → Mattermaps acquisition and strategy)
