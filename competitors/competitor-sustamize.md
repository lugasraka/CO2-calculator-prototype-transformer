# Competitor Analysis — sustamize

## 1. Overview & positioning

sustamize is a German carbon-data company positioned as a **Data-as-a-Service provider of verified CO₂e reference data** for Product Carbon Footprint (PCF) and Scope 3 calculations. Its positioning is data-first, not workflow-first: the core asset is "one of the most comprehensive CO₂e databases worldwide" (150,000+ emission factor datasets, 2M+ CO₂e reference values, 240+ country energy mixes), wrapped in a web app (sustamizer®), PCF tooling (Matcher, Assembler, Interpreter, MPN Search), and an API-first integration layer. Methodology claims alignment with the GHG Protocol Product Standard and ISO 14067, with third-party validation under ISO 14064-3 (GUTcert). It targets Scope 3, CBAM/CSRD, and ESG compliance use cases rather than engineering decision support for a specific product category.

## 2. Target users & customers

sustamize segments explicitly by role and industry:

- **Roles:** cost engineers, procurement teams (Scope 3 sourcing decisions), product designers (eco-design, material comparison), sustainability/ESG consultants.
- **Industries:** manufacturing, software providers (embed CO₂e data into their own tools), consulting firms, non-EU suppliers needing EU-compliant data.
- **Customers/partners (publicly shown):** Siemens Digital Industries Software (testimonial by VP Sustainability), raumedic, SEMPACT, shouldcosting, PolarixPartner, Polymertal; partner logos include SAP Partner, Climatiq, Catena-X, tset, PwC-adjacent tcon. Claims "Trusted by 100+ companies."
- Also offers free academic access programs.

Their sweet spot is horizontal, cross-industry PCF data — not electrical-equipment or transformer specialists.

## 3. Business model & pricing (public info)

- **Model:** licensed data access (Data-as-a-Service) + SaaS tools (sustamizer) + API access + services (PCF Service, custom data research).
- **Acquisition:** 14-day free trial (register → explore data → "choose a license"), demo booking via Calendly, self-service login on sustamizer.com.
- **Pricing:** not publicly disclosed — "flexible data licenses tailored to your business needs" is the only public statement; no price tiers or rate cards on the site.
- Partner ecosystem model: software and consulting partners embed sustamize data (e.g. shouldcosting, Indec integrations).

## 4. Capability mapping vs. our product

| Our capability | Their equivalent | Coverage (Full/Partial/None) | Notes |
|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | Use phase listed as a PCF life-cycle stage; energy-mix database (240+ regions) | Partial | They model use-phase emissions inside a PCF, but no TCO/NPV/payback economics, no loss-differentiated B-stage modeling. Cost linkage exists only via third-party cost-engineering partners (tset, shouldcosting, Indec). |
| EOL/circularity & Module D credits | End-of-life stage (disposal, recycling, reuse) in PCF scope; materials DB includes recycling values; "eco-design and circular strategies" mentioned | Partial | EOL emissions yes; EN 15978-style Module D recovery credits, retrofill-vs-decommissioning logic not disclosed. |
| BOM-based A1–A3 product carbon footprint | Assembler, Interpreter, Matcher, MPN Search; cradle-to-gate and cradle-to-grave boundaries | Full | Their core product. AI-assisted BOM mapping to emission factors, ISO 14067-compliant PCFs. |
| Portfolio scenario simulation & comparison | "Scenario Modeling" via API; "simulate scenarios and PCFs," compare design/sourcing alternatives; PolarixPartner cites scenario calculations | Partial | Scenario comparison of PCFs exists, but no evidence of fleet-level portfolio rollups, saved scenario sets, or compare/export UX comparable to ours. |
| Uncertainty ranges & data provenance | Provenance, structured documentation, traceable factors, ISO 14064-3 validation, ILCD-compliant DBs | Partial | Provenance is strong and validated; explicit numeric uncertainty ranges per factor are not publicly disclosed. |
| Gate-ready design KPIs (e.g. kg CO₂e/kVA) | PCF results in kg CO₂e; hotspot analysis | None | No domain-normalized KPIs or design-gate concept. |
| Abatement cost (€/t CO₂) ranking | Not mentioned on any fetched page | None | "Identify decarbonization levers and save costs" qualitatively, but no €/t ranking or MAC logic. |
| Scenario persistence & export | sustamizer Data Hub; managed datasets; partner software integration | Partial | Persistence inside their SaaS implied; explicit save/compare/CSV export workflow not publicly described. |
| EPD data feeds / EPD automation | Not offered; secondary data from LCA studies, industry datasets, scientific publications | None | They position as the data source itself; EPD ingestion/automation not disclosed. |
| PLM/ERP integration | "API-first integration embeds climate data into existing ERP, PLM, cost engineering, and procurement workflows"; CAD/BOM inputs via API | Full | Integration is a headline capability, incl. Siemens partnership credibility. |
| Public API | sustamize API (JSON), database-specific endpoints, API Sandbox | Full | Documented API-first architecture; access gated behind license/contact. |
| Regulatory reporting (CBAM/CSRD) | Dedicated regulations pages; CBAM supplier workflows; CSRD/ESPR/DPP readiness; audit-ready data | Full | Core compliance narrative; supports reporting rather than filing the reports themselves. |
| Transformer / electrical-equipment domain focus | Electronics DB (wires, connectors, sensors); manufacturing-industry pages | None | Generic horizontal data; no transformer, kVA, or loss-modeling content anywhere. |

## 5. Lifecycle coverage (A1–A3 / A4–A5 / B / C / D)

- **A1–A3 (cradle-to-gate):** full strength — materials, electronics, production processes, energy mixes, standard parts.
- **A4–A5:** logistics database (transport modes, kg CO₂e/km, g CO₂e/tkm, packaging) covers A4-style distribution; A5 not explicitly broken out.
- **B (use phase):** supported as a PCF life-cycle stage ("use phase: operational energy consumption"), backed by 240+ regional energy mixes — but generic energy consumption, not equipment loss models.
- **C (end-of-life):** included in cradle-to-grave scope (disposal, recycling, reuse); materials DB includes recycling values.
- **D (beyond-system-boundary credits):** not publicly disclosed.
- Supports both cradle-to-gate and cradle-to-grave system boundaries, user-selected.

## 6. Data, provenance & integrations

- **Data:** bottom-up modeled factors (no data gaps claim), updated twice a year; categories: materials (4,600+), electronics (660+, 41 categories/850 subclasses), production (790+, 400+ manufacturing technologies), logistics (120+), energy mixes (240+ countries/regions), consumer products (130+), standard parts (160+), chemicals (140+).
- **Provenance:** factors derived from peer-reviewed LCA studies, industry datasets, scientific publications, standardized environmental reports; IPCC GWP conversions; ILCD-compliant; GHG Protocol + ISO 14067 aligned; independently validated under ISO 14064-3 by GUTcert; structured documentation for audit-readiness.
- **Integrations:** JSON API with database-specific endpoints and a sandbox; web app (sustamizer); partner software ecosystem (tset, shouldcosting, Indec, Climatiq, SAP); Catena-X member; docs portal at docs.sustamizer.com.
- **AI tooling:** Matcher (AI BOM-name → factor mapping), Interpreter (BOM paste → matched CO₂ values), MPN search for electronics.

## 7. Strengths

- Database breadth and depth: arguably the largest independent CO₂e factor set for manufacturing, with granular regional and process differentiation.
- Credibility stack: ISO 14064-3 third-party validation, GHG Protocol/ISO 14067 alignment, twice-yearly updates — directly addresses audit-readiness pain.
- API-first architecture designed to be embedded — strong partner ecosystem (Siemens, tset, shouldcosting, Climatiq, Catena-X).
- AI-assisted BOM mapping (Matcher/Interpreter) attacks the biggest PCF scaling bottleneck: data wrangling.
- Low-friction entry: 14-day free trial, self-serve app, no-LCA-expertise tooling (Assembler).
- Horizontal reach across cost engineering, procurement, design, and sustainability roles.

## 8. Weaknesses / gaps

- No engineering economics: no TCO, NPV, payback, or €/t abatement ranking — carbon without the cost-side decision math (cost linkage delegated to partners).
- No domain depth for transformers/electrical equipment: no loss models, no kVA-normalized KPIs, no design-gate workflow.
- Module D / circularity credits and use-phase equipment-specific modeling not publicly disclosed.
- Pricing opaque; license gating slows evaluation vs. an open-source prototype.
- Closed data: factors inspectable for provenance but the product is a licensed black box vs. our fully transparent CSV/SQLite stack.
- Portfolio-level fleet simulation, uncertainty ranges, and scenario persistence UX are not evidenced publicly.
- Marketing site has quality issues (template placeholder text, typo'd "Standart Parts"), suggesting web presence maturity lags data maturity.

## 9. Differentiation — where we win / where they win

**Where we win**

- Decision-grade economics at design time: TCO + carbon ROI, payback, and €/t abatement ranking vs. their carbon-only factors.
- Transformer-domain specificity: B1–B6 loss modeling, kg CO₂e/kVA gate KPIs, retrofill logic — none of which they touch.
- Full lifecycle including explicit EOL/Module D circularity planning; they stop at generic EOL.
- Transparency: open-source, fully inspectable factors with uncertainty ranges; free to evaluate and extend.

**Where they win**

- Data scale, regionalization, validation, and update cadence — we cannot out-curate 150k+ validated factors.
- Integrations and enterprise readiness: API, PLM/ERP embedding, partner ecosystem, compliance narrative (CBAM/CSRD/DPP).
- Production-grade SaaS with trial onboarding vs. our prototype maturity.

**Competitor vs. partner/supplier assessment:** sustamize is **primarily a potential data supplier, secondarily a competitor**. Overlap is limited to our Portfolio CO₂ Simulator's A1–A3 factor layer; they have no TCO, no transformer KPIs, no gate workflow. The rational strategy is to treat their API as a candidate Phase 2 data feed (replacing/validating our sourced CSVs) while competing on domain workflow and cost-carbon decision logic they structurally lack. Risk: they could be embedded by a PLM/cost-engineering partner into exactly our gate-review niche — watch the Siemens and tset partnerships.

## 10. Threat level: **Medium**

As a direct competitor the threat is low — different buyer problem (data procurement vs. design-gate decision support), no transformer domain, no TCO economics. But Medium overall because: (1) their API-first embedded model means they could silently power a competing PLM-integrated gate tool via partners (Siemens, tset); (2) enterprise buyers may prefer one validated data vendor + partner software over an in-house prototype; (3) if we don't integrate commercial-grade factors, our prototype's credibility on audit-readiness suffers. Most probable relationship is supplier/partner, and an integration option should be evaluated before treating them as a rival.

## 11. Sources

- https://www.sustamize.com
- https://www.sustamize.com/carbon-data-platform
- https://www.sustamize.com/carbon-database
- https://www.sustamize.com/product-carbon-footprint-calculation
- https://www.sustamize.com/integration-api
- https://www.sustamize.com/sustamizer
- https://www.sustamize.com/scope-3-procurement
- https://www.sustamize.com/carbon-data-for-product-design
