# M4Di 6-Layer Coverage Map
**M4Di — Merge 4 Development Institute**
*Last updated: 2026-03-27*

---

## Background

The core M4Di thesis: private developers have a 1-layer problem (does the return on equity work?). Community nonprofits have a 6-layer problem. No existing feasibility tool is built for the 6-layer problem. This document maps M4Di's current coverage across all six layers and identifies the product gaps.

**Coverage ratings:** Covered ✅ | Partial ⚠️ | Gap ❌

---

## Layer 1 — Capital Stack Assembly
*Structuring multiple funding sources into a coherent, stackable project budget*

**Overall coverage: ~35%**

| Capability | Status | Notes |
|---|---|---|
| Hard cost ROM baseline | ✅ Covered | M4Di.Oi™ produces the construction cost number that anchors every capital stack conversation |
| Total project investment | ✅ Covered | TOTAL PROJECT BUDGET sheet aggregates hard + soft + owner contingency |
| Soft cost fee schedule | ✅ Covered | AE fees auto-calculated per AIA schedule |
| Capital source identification | ⚠️ Partial | Funding justification binder describes project context but doesn't map to specific programs |
| Source compatibility check | ⚠️ Partial | No tool checks whether two sources have conflicting eligibility rules |
| Multi-source pro forma | ❌ Gap | No tool models a 10–12 source capital stack with layered debt, grant, equity, deferred fee |
| Gap financing calculator | ❌ Gap | Can't automatically calculate the gap between project cost and available sources |
| LIHTC / NMTC modeling | ❌ Gap | Tax credit equity structures not modeled anywhere in current toolset |

**Key insight:** The hard cost ROM is solid. Everything downstream — how the money is assembled — is largely unaddressed. A project with a perfect cost estimate can still be unfundable if the capital stack doesn't close.

**Data collection strategy:** CB CDC pilot is the first real capital stack. Document the methodology as the work is done. Extract the M4Di Capital Stack Template from the first real example — don't wait to build the template before doing the project.

---

## Layer 2 — Regulatory Overlays
*Licensing, certification, and program-specific compliance requirements beyond standard building code*

**Overall coverage: ~20%**

| Capability | Status | Notes |
|---|---|---|
| Zoning constraints scan | ✅ Covered | P1 deliverable covers basic zoning, code, and use classification |
| ADA / occupancy classification | ✅ Covered | Addressed implicitly through program definition and CSI scope |
| Site-specific environmental | ⚠️ Partial | Environmental screening (Phase I) is optional add-on only |
| DHSS / CMS licensing (IDD) | ❌ Gap | Delaware DHSS ICF/IID standards not integrated into program templates |
| HRSA / FQHC requirements | ❌ Gap | Federally Qualified Health Center governance requirements not addressed |
| HCBS Medicaid waiver rules | ❌ Gap | Affects site selection and building configuration for IDD residential projects |
| Distance / group home ordinances | ❌ Gap | Municipal distance restrictions common in Delaware not checked in zoning scan |
| Faith-based governance overlay | ❌ Gap | Congregation ownership structures affect financing instrument eligibility |

**Key insight:** The zoning scan covers building code but not program-specific licensing standards that determine whether a project is actually deliverable for M4Di's target client types.

**Data collection strategy:** Build typology checklists demand-first. IDD comes first (MaxWellness is active). Faith-based second (CB CDC is current pilot). FQHC third when first health center client appears. Source: Delaware DHSS Division of Developmental Services licensing standards (publicly available).

---

## Layer 3 — Grant Eligibility
*Identifying, qualifying for, and documenting eligibility for grant funding programs*

**Overall coverage: ~25%**

| Capability | Status | Notes |
|---|---|---|
| Community benefit narrative | ✅ Covered | P3 deliverable includes short-form community benefit narrative draft |
| Funding justification binder | ✅ Covered | P3 produces funder-facing package with project summary and capital readiness materials |
| PolicyMap demographic context | ⚠️ Partial | Identified as Year 1 add-on — not yet integrated into standard P1/P2 workflow |
| Grant program screener | ❌ Gap | No tool takes project type + location + owner type and outputs matched grant programs |
| Opportunity zone / NMTC overlay | ❌ Gap | Not checked whether site falls in NMTC-eligible census tract or Qualified Opportunity Zone |
| HUD / USDA program eligibility | ❌ Gap | Community Facilities, Section 108, CDBG-DR eligibility rules not mapped |
| CDFI certification criteria | ❌ Gap | CDFI loan underwriting requirements not templated |

**Key insight:** The funding justification binder produces materials a grant writer uses — not a tool that tells the team which grants they qualify for before they engage the grant writer.

**Data collection strategy:** The grant screener is a research project, not a software project. First version is a structured spreadsheet (not software) mapping program characteristics to project characteristics. 20 programs, Delaware/Mid-Atlantic focus. Leo Lynch owns this build.

---

## Layer 4 — Procurement Documentation
*Competitive, compliant, auditable selection of all consultants and contractors*

**Overall coverage: ~75%** ← M4Di's strongest layer

| Capability | Status | Notes |
|---|---|---|
| AE RFP/RFQ package | ✅ Covered | Complete and field-tested on CB CDC package |
| Bid leveling template | ✅ Covered | Included in P3 deliverable set |
| Selection memo template | ✅ Covered | Supports grant compliance and audit trail |
| COI / conflict of interest checklist | ✅ Covered | Procurement toolkit includes COI disclosure framework |
| Procurement integrity statement | ✅ Covered | Standalone document for grant submissions |
| Scoring matrix | ✅ Covered | Evaluation criteria and scoring framework included |
| GC / CM procurement | ⚠️ Partial | RFP/RFQ framework exists for AE services only — GC/CM not yet developed |
| Davis-Bacon / prevailing wage | ❌ Gap | Federal labor standards compliance documentation not addressed. Adds 15–25% to labor costs if triggered |

**Key insight:** The procurement documentation set is genuinely comprehensive for AE services. The gap is that it stops at AE selection. The next procurement event is the GC/CM — M4Di has no tools for that phase yet.

**Next build:** GC/CM RFP template, subcontractor scope packages, bid leveling for hard cost proposals, Davis-Bacon compliance checklist. Data inputs already defined in OI Tool (CSI divisions, bid packages).

---

## Layer 5 — Community Governance
*Board decision-making, stakeholder alignment, and organizational authorization structures*

**Overall coverage: ~60%**

| Capability | Status | Notes |
|---|---|---|
| Decision gate framework | ✅ Covered | Go / No-Go / Not-Yet structure with defined inputs and approval checkpoints |
| Board-ready decision memo | ✅ Covered | Standard template for presenting options, budgets, risks to leadership |
| Steering committee charter | ✅ Covered | Roles, decision rights, meeting cadence documented |
| Site comparison matrix | ✅ Covered | Side-by-side comparison of site options for board decision |
| Stakeholder engagement structure | ⚠️ Partial | Referenced in MOU as CB CDC responsibility — no defined M4Di methodology |
| Funder reporting cadence | ⚠️ Partial | Monthly progress summary structure defined — detailed templates not yet built |
| Community benefit measurement | ❌ Gap | No framework for defining, measuring, or reporting community benefit outcomes |
| Congregation / membership authorization | ❌ Gap | Faith-based clients often require membership votes — no process template exists |

**Key insight:** The governance toolkit is well developed for internal decision structure. The gap is the external accountability layer — how clients demonstrate community benefit to funders.

**Next build:** Community Benefit Scorecard tab in ALDi Budget Tracker. Fields: jobs created, households served, community services delivered, accessible square footage. Auto-summarizes into one-page funder-facing impact statement.

---

## Layer 6 — Funder Reporting
*Ongoing documentation of project progress, cost controls, and outcomes for grant and loan compliance*

**Overall coverage: ~20%**

| Capability | Status | Notes |
|---|---|---|
| ALDi Budget Tracker | ✅ Covered | 4-column design-to-construction cost tracking is M4Di's strongest product for this layer |
| Variance log | ✅ Covered | Tracks divergence from ROM baseline across design phases |
| Monthly progress summary | ⚠️ Partial | Format defined in fiscal sponsorship agreement — no standardized template yet |
| Gate dashboard | ⚠️ Partial | GATE DASHBOARD tab exists but not yet a reportable funder-facing output |
| CDFI draw request package | ❌ Gap | AIA G702/703 format adapted for CDFI — not in current toolset |
| Grant closeout / impact report | ❌ Gap | No template for grant closeout documentation |
| Audit trail documentation | ❌ Gap | Full trace from Gate 0 ROM through final cost reconciliation not yet exportable |
| CDFI compliance auto-report | ❌ Gap | Budget Tracker data → CDFI-format reporting package. Data exists; output format does not |

**Key insight:** The ALDi Budget Tracker holds all the data that funder reporting requires. The gap is that the data doesn't yet flow automatically into funder-required formats. The tracker is a database; the reporting layer on top of it is the product that doesn't exist yet.

**Next build (highest leverage):** Monthly Progress Report PDF generator — auto-populates from Budget Tracker: budget status (ROM vs. current vs. actual), variance narrative (>15% flags), gate status, next-step actions.

---

## Summary

| Layer | Coverage | Priority Build |
|---|---|---|
| L1 Capital Stack | 35% | Multi-source pro forma template (from CB CDC pilot) |
| L2 Regulatory Overlays | 20% | IDD checklist (MaxWellness), faith-based checklist (CB CDC) |
| L3 Grant Eligibility | 25% | Grant screener spreadsheet (Leo Lynch) |
| L4 Procurement | 75% | GC/CM RFP template set |
| L5 Community Governance | 60% | Community Benefit Scorecard (new ALDi tab) |
| L6 Funder Reporting | 20% | Monthly Progress Report PDF generator |

**The pattern:** Layers 4+5 have data — build output pipelines. Layers 1+2+3 need data — collect demand-first from live projects.
