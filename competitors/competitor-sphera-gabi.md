# Competitor Analysis — Sphera (GaBi)

## 1. Overview & positioning
Sphera is the enterprise incumbent in LCA software, built on 30+ years of GaBi heritage. It positions itself as "the only LCA solution that unites the world's most comprehensive environmental data, enterprise-grade software, and expert consulting," claiming 1,500+ sustainability-leader customers across all industries. The LCA portfolio is a tiered product family on the SpheraCloud platform:

- **LCA for Experts (LCA FE)** — the former GaBi desktop-class expert tool; precision modeling for up to 25 LCAs, ~1,000 ready models, downloadable with a 45-day free trial.
- **LCA Automation** — portfolio-scale automated LCA generation ("results in minutes"), with vertical variants for discrete, process, and chemical manufacturing.
- **LCA Calculator** — cloud-based, simplified "snapshot" of LCA FE aimed at non-experts; produces LCAs and EPDs with scenario comparison and one-click reports.
- **LCA BOM Import** — add-on to LCA FE that semi-automates LCA creation from imported bills of materials, targeting automotive, aerospace, and electronics.
- **Managed LCA Content (MLC)** — the proprietary data moat: 20,000+ DEKRA-verified datasets across 60+ industries, bi-annual expert updates, Data-on-Demand custom datasets.

Positioning is horizontal and enterprise-grade: data quality, auditability, and scale — not domain-specific design decision support.

## 2. Target users & customers
- **LCA practitioners / sustainability experts** (LCA FE, BOM Import): hotspot analysis, custom model building, EPD publication.
- **Non-expert stakeholders** (LCA Calculator): product/design staff who need quick footprints and EPDs without LCA expertise.
- **Manufacturers with complex BOMs** (LCA Automation Discrete Manufacturing, BOM Import): explicitly automotive, aerospace, electronics; integrates with PLM/ERP for rolling, portfolio-wide LCAs.
- **Enterprise sustainability/Scope 3 programs** (LCA Automation, MLC): portfolio transparency tied to climate goals.
- Named references on public pages: Audi, Bosch, Dell, Exxon, Interface, Lenovo (logos); Eastman (LCA Automation testimonial); Saint-Gobain (EPD program, LCA FE + Calculator); Whirlpool (lifecycle hotspots). Served industries listed: Chemicals & Life Sciences, Consumer Services & Technology, Financial Services, Hazardous Materials, Industrials & Manufacturing, Oil & Gas. No transformer/OEM-specific reference is published.

## 3. Business model & pricing (public info)
- Enterprise B2B SaaS on SpheraCloud; all products are demo-request/"talk to an expert" sales — **no public pricing disclosed**.
- **LCA for Experts** is the only self-serve entry point: downloadable with a 45-day free trial (lead-gen motion).
- **Managed LCA Content** is monetized as data subscriptions: 13 standard bundles + 8 premium bundles (e.g., Premium Energy, Premium Metals, Electrics & Electronics, Manufacturing & EoL), plus paid **Data-on-Demand** custom datasets.
- **Consulting** (LCA/PCF services, EPD services, circular economy, SBTi, Scope 3 accounting) is a separate revenue line that pulls software through.
- Training Center (paid regional/private/on-demand sessions) monetizes the expertise barrier.
- Contract values, seat counts, and bundle prices: not publicly disclosed.

## 4. Capability mapping vs. our product
| Our capability | Their equivalent | Coverage (Full/Partial/None) | Notes |
|---|---|---|---|
| Use-phase TCO & carbon ROI (B1–B6) | Use-phase modeling inside LCA FE custom models | Partial | Full-lifecycle modeling can include use-phase energy, but no TCO/NPV/payback economics and no transformer loss (load/no-load) constructs; everything is user-built. |
| EOL/circularity & Module D credits | Manufacturing & End-of-Life data bundle (900+ datasets), EOL scenario models, circular economy consulting | Partial | C1–C4 treatment is strong and data-backed; explicit Module D crediting and retrofill-vs-decommission economics are not marketed as product features. |
| BOM-based A1–A3 product carbon footprint | LCA BOM Import; LCA Automation Discrete Manufacturing | Full | Direct competitor to our A1–A3 engine: BOM upload → automated footprint against 20K+ datasets. Far more mature data layer. |
| Portfolio scenario simulation & comparison | LCA Automation (portfolio-wide); LCA Calculator & BOM Import (scenario comparison of design alternatives) | Full | Scenario compare exists at both expert and non-expert tiers; no fleet-volume CO₂ simulator with gate KPIs, but portfolio automation exceeds ours in scale. |
| Uncertainty ranges & data provenance | DEKRA third-party verification, expert-maintained datasets, documented modeling principles | Partial | Provenance/quality assurance is excellent (DEKRA review, bi-annual updates); quantitative uncertainty ranges on outputs are not publicly marketed. |
| Gate-ready design KPIs (e.g. kg CO₂e/kVA) | — | None | No design-gate workflow concept, no normalized per-rating KPIs, no PLM gate pass/fail artifacts. |
| Abatement cost (€/t CO₂) ranking | — | None | Not publicly disclosed anywhere in the LCA product line; closest is corporate decarbonization-strategy consulting. |
| Scenario persistence & export | Customizable report templates, shareable calculations/reports, database server for centralized models | Partial | Persistence/export exist via reports and SpheraCloud LCA Database Server; lightweight save/compare/CSV iteration like ours is not the focus. |
| EPD data feeds / EPD automation | LCA Calculator (LCAs + EPDs), EPD services consulting, Construction bundle with company EPDs | Full | Saint-Gobain runs its EPD program on LCA FE + Calculator. No evidence of machine-readable EPD *import* feeds (e.g., EC3/ILCD ingestion). |
| PLM/ERP integration | BOM Import (CAD/PLM integration); LCA Automation ("seamless no-touch integrations into supplier systems", PLM/ERP) | Full | Their clearest structural advantage over our Phase 2–4 roadmap; already deployed at enterprise scale. |
| Public API | — | None | Integrations are marketed, but no public/developer API is disclosed on product pages. |
| Regulatory reporting (CBAM/CSRD) | Separate SpheraCloud ESG/Environmental Accounting suite; regulatory content hub; ESRS commentary | Partial | LCA outputs feed compliance, but CBAM/CSRD reporting lives in other Sphera products, not the LCA tools themselves. |
| Transformer / electrical-equipment domain focus | Electrics & Electronics bundle (450+ datasets), Premium Battery/REE/Precious Metals bundle | Partial | Relevant LCI data exists (cables, ICs, rare earths, magnets), but no transformer models, loss physics, or kVA-normalized metrics. |

## 5. Lifecycle coverage (A1–A3 / A4–A5 / B / C / D)
- **A1–A3:** Full. Core strength — BOM Import and LCA Automation generate cradle-to-gate footprints from 20K+ process datasets.
- **A4–A5:** Full (modelable). Transport and construction/installation processes are in MLC scope; must be assembled by the user in LCA FE.
- **B (use phase):** Full (modelable). Energy datasets (incl. Premium Energy, 100+ country grid mixes, Scope 2/3 split) support use-phase modeling; no built-in transformer loss models.
- **C (EOL):** Full. Dedicated Manufacturing & EoL bundles (standard + premium) with parameterized recycling, incineration, landfill, hazardous-waste models.
- **D (beyond system boundary):** Not explicitly marketed. EOL/recycling datasets imply credit modeling is possible in expert hands, but no productized Module D workflow.
- Net: cradle-to-grave is fully covered as a *modeling capability*; nothing is pre-packaged for a specific product category.

## 6. Data, provenance & integrations
- **Managed LCA Content:** 20,000+ datasets, ~500 models, 60+ industry associations, organized into 13 standard + 8 premium bundles; bi-annual expert updates; public dataset search portal (lcadatabase.sphera.com).
- **Verification:** third-party critical review by DEKRA (review statement published); documented LCA modeling principles — provenance and audit-readiness are core selling points.
- **Extensibility:** Data-on-Demand for custom datasets; access to third-party LCI databases; users can create/import their own models in LCA FE.
- **Integrations:** CAD and PLM integration via BOM Import; PLM/ERP and supplier-system integration via LCA Automation; SpheraCloud LCA Database Server for centralized, multi-user data management.
- **Gaps vs. our data layer:** no published per-dataset uncertainty ranges surfaced to end users in marketing; no evidence of EPD feed ingestion; API access not publicly disclosed.

## 7. Strengths
- **Data moat:** 20K+ DEKRA-verified datasets with bi-annual updates is the industry benchmark; hard to replicate.
- **Full lifecycle depth:** true cradle-to-grave modeling across all EN 15978-style modules, in expert hands.
- **Enterprise scalability:** LCA Automation generates portfolio-wide LCAs in minutes with no-touch PLM/ERP/supplier integration — exactly the plumbing our Phase 2/4 roadmap aspires to.
- **Tiered user coverage:** expert (LCA FE), semi-automated (BOM Import), non-expert (Calculator) tiers lower adoption friction inside large orgs.
- **EPD production:** proven EPD programs (Saint-Gobain) on standard tooling.
- **Credibility & brand:** 30+ years, 1,500+ customers, analyst recognition (Green Quadrant leader 2023), consulting arm to close capability gaps.

## 8. Weaknesses / gaps
- **No cost+carbon coupling:** no TCO, NPV, payback, or €/t abatement constructs — environmental metrics only; design-trade-off economics are out of scope.
- **No domain specificity for transformers:** no loss modeling (B1–B6 from load/no-load losses), no kVA-normalized KPIs, no retrofill/decommission decision logic.
- **No design-gate workflow:** nothing produces gate-ready artifacts for PLM reviews; LCAs are reports, not pass/fail design inputs.
- **Expertise barrier & cost opacity:** enterprise sales, no public pricing, training center needed for proficiency; heavyweight for a single engineer's design question.
- **Generic EOL:** Module D crediting and circularity decision support require custom modeling or consulting.
- **Uncertainty not productized:** data quality is assured via verification, but quantitative uncertainty bounds on results are not marketed.
- **Closed platform:** no public API disclosed; automation is sold as enterprise projects, not developer self-service.

## 9. Differentiation — where we win / where they win
This is **incumbent generalist platform vs. focused domain tool**: Sphera sells horizontal, auditable LCA infrastructure to enterprise sustainability teams; we sell (as an open-source prototype) a transformer-specific design-decision instrument to engineers and gate reviewers.

**Where we win**
- Transformer physics out of the box: B1–B6 loss-based use-phase CO₂ and TCO, kg CO₂e/kVA gate KPI — none of which Sphera can produce without weeks of expert modeling.
- Cost+carbon combined at design time: NPV TCO, payback, and €/t abatement ranking per lever — Sphera has no economics layer at all.
- Decision framing Sphera doesn't productize: retrofill vs. decommission with Module D credits; portfolio fleet scenarios with uncertainty bounds and CSV export in minutes.
- Accessibility: open-source, transparent sourced CSVs with provenance/validity dates, zero procurement friction vs. enterprise sales cycles.
- Speed to insight for a design engineer: purpose-built UI vs. configuring a generalist expert tool.

**Where they win**
- Data depth and verification: 20K+ DEKRA-reviewed datasets across 60+ industries vs. our small curated CSV set — we lose on coverage, credibility at audit, and maintenance.
- Full cradle-to-grave (A4–A5, C, D) modeling maturity; our A1–A3 + B + C coverage is partial until Phase 2.
- Enterprise plumbing: live PLM/ERP/CAD integrations, database server, multi-user governance, EPD generation, regulatory reporting suite — our Phase 4 roadmap items they already ship.
- Brand trust, installed base (1,500+ customers), and a consulting arm that can hand-build anything the software lacks — including, in principle, transformer LCAs.

## 10. Threat level (High/Medium/Low) + rationale
**Medium.**

- **As a capability benchmark: High.** On A1–A3 BOM-based footprinting, data provenance, EPDs, and PLM integration, Sphera is strictly superior and already deployed — any enterprise IT-led evaluation will shortlist them.
- **As a direct competitor for our use case: Low-to-Medium.** Sphera does not address use-phase loss economics, cost+carbon ROI, gate-ready transformer KPIs, or abatement-cost ranking, and reaching those answers in GaBi requires expert users, custom models, and enterprise contracts. The buyer (sustainability team) and moment of use (annual/portfolio reporting) differ from ours (design engineer at a PLM gate).
- **Escalation risk:** Sphera's consulting arm or a discrete-manufacturing automation engagement could close the domain gap for a large transformer OEM account; their PLM integrations also mean they could own the gate interface we target in Phase 4. Open-source transparency and domain specificity are the durable moat — data breadth is not.

## 11. Sources
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/lca-automation/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/lca-automation-discrete-manufacturing/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/lca-for-experts/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/managed-lca-content/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/lca-bom-import/
- https://sphera.com/solutions/product-stewardship/life-cycle-assessment-software-and-data/lca-calculator/
