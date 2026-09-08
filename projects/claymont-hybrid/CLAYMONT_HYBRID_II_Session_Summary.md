# CLAYMONT HYBRID II — Session Summary for Project Migration

**Project:** AE24-002 Claymont Street Townhouses
**Address:** 1316–1324 N. Claymont Street, Wilmington, DE 19802
**Owner:** L.E.E.P., Inc. (Gwenevere Motley, Executive Director)
**AOR:** David C. Ainsworth, AIA — Aubyn Architecture LLC
**Lead Firm:** Merge 4 Design LLC
**Source chat:** April 2026 cross-project session covering OED meeting prep, then Claymont SIP/CLT panel review work
**Migration target:** CLAYMONT HYBRID II project lane

---

## 1. What this session produced — Claymont deliverables

Three Claymont-related deliverables came out of this chat. All four files are in `/mnt/user-data/outputs/` from the source chat.

### 1.1 Reviewer Response Memo — formal version
- **File:** `Claymont_Reviewer_Response_AE24-002.docx` (also `.pdf`)
- **Format:** 6-page memo on Aubyn Architecture letterhead
- **Audience:** plan reviewer or AHJ-level recipient
- **Content:** Six numbered Q&A on the SIP/CLT panel submission, plus a closing summary of supplemental information to be provided
- **Sign-off:** David C. Ainsworth, AIA as AOR

### 1.2 Reviewer Response — email version for Larry Carson
- **Format:** Email body, peer-to-peer technical tone, no letterhead
- **Audience:** Larry Carson, peer-review structural engineer (Carson Structural / RMGC)
- **Subject line:** "Re: Claymont SIP/CLT panel review — answers and what I'm chasing down"
- **Content:** Same six questions answered in shorter prose, plus three adjacent items not in the formal memo: F&P bracing/party-wall internal inconsistency, Panelwrights wrong-jurisdiction code reference, missing CLT party wall layout sheet
- **To send with:** Latest architectural set (foundation-only permit submission, ~10MB) as attachment

### 1.3 A-502 Internal QA Review
- **File:** `A502_Review_Comments_AE24-002.docx` (also `.pdf`)
- **Format:** 11-page memo on Aubyn letterhead
- **Audience:** Internal Aubyn / Merge 4 Design QA prior to next reissue of A-502
- **Content:** 26 numbered comments organized into three categories:
  - 10 clarity comments (#01–#10)
  - 8 constructability comments (#11–#18)
  - 8 compliance comments (#19–#26)
- **Resolution pathway:** Comments grouped into three tracks — Architect's hand (10), EOR coordination (9), Manufacturer coordination (3, with overlap)

---

## 2. Substantive project findings to carry forward

### 2.1 F&P structural ambiguity is RESOLVED by A-502

**This is the single most important takeaway from the session.**

The Fenster & Panel structural review carried an internal inconsistency between Section 2.0 (CLT party walls as short-direction bracing) and the Bracing Scope language ("Where walls party, walls are nominated as steel frames by other"). This was previously flagged as F2 in the CLAYMONT HYBRID II analysis.

A-502 resolves it: **the party walls are CMU at the basement story and 5-ply CLT (TerraLam TL500S 6.875") at the upper stories, with the transition occurring at the first-floor line via a non-shrink grout bed and Rothoblaas TCP300 plate connectors.** The end walls follow the same pattern — CMU at the basement (Detail 1) transitioning to 6-1/2" SIP at the upper stories (Details 3 and 4).

Both descriptions in F&P were partly true. They were describing different stories. The "steel frames" language in F&P appears stale and should be removed on the next reissue.

### 2.2 SIP envelope is full perimeter — not rear elevations only

A reviewer question asked whether SIP was rear-only. Definitive answer from Acme Sheet P1 (Wall Panel Layout): **walls B through Z plus 3DD–3GG are all SIP** — that's the full perimeter envelope of the four-unit row including front, rear, both ends, and stairwell vertical.

The CLT scope from Panelwrights is interior only — second floor diaphragm, roof deck, and party walls between units.

### 2.3 Larry Carson is peer-review structural — NOT EOR

This is a context-correction worth carrying forward. The **EOR seat is still open** per AHJ comment list CR-01 (no S-series structural sheets submitted). Larry's role is peer review of the F&P SIP/CLT structural work and our coordination — not stamping the structural drawings.

The peer-review-plus-AOR model that's been described in CBai TECH STACK applies here: Aubyn does CBai-assisted structural logic, Larry reviews and gives feedback, but a separate licensed structural engineer must seat as EOR before permit issuance. The threshold for peer-review-only (3 stories and under, residential, simple structural system) is met by Claymont, but the AHJ has flagged the missing S-series sheets as permit-blocking.

**Action item:** Confirm EOR engagement before full building permit application.

### 2.4 ESR-4689 conformance — actionable items

The F&P SIP transverse check used 28 psf as the conservative uniform pressure. ESR-4689 Tables 8 and 9 give:
- 36-inch openings: ~25 psf — **exceeds**
- 72-inch openings: ~19 psf — **exceeds**
- Solid walls: substantially higher — within allowable

Three resolution paths in order of preference:

1. **Refined ASCE 7-16 Chapter 30 C&C analysis** at the actual zone and height. For a 2-story residential at the Claymont site this almost certainly drops C&C pressures below ESR-4689 tabulated values for most opening configurations. EOR's calc.
2. **Project-specific lintel / header design** at openings beyond the table limits. Standard SIP-industry practice.
3. **Acme manufacturer engineering judgment letter** for any opening configurations remaining outside ESR-4689 after #1 and #2.

A separate ESR-4689 issue surfaced from A-502 review: **the SIP bearing condition at Detail 3 (end wall) deviates from ESR-4689 conditions of use** — the detail shows the SIP bearing directly on a grout bed without the prescribed treated wood bottom plate, sill anchor bolts, sill gasket, or SIP-to-bottom-plate fastening. Either revise the detail to add the ESR-4689 components, or get Acme engineering judgment for the deviating condition.

### 2.5 Panelwrights cover sheet — wrong jurisdiction

The Panelwrights CLT shop drawing cover sheet (PW Job #26-012, 3/6/2026 rev. 3/12/2026) cites the **2018 Virginia Residential Code** as the design loads basis. Wrong jurisdiction. Claymont is governed by the City of Wilmington adopted code (2018 IRC/IBC family with Delaware amendments).

The actual loads Panelwrights used (20 psf snow, 90 mph wind, SDC B) are reasonable for the Wilmington site, but the **code reference on the title block needs to be corrected before the package goes near the AHJ.** Action item flagged with Panelwrights for next reissue.

### 2.6 Acme drawings — clerical year typo

The Acme Panel SIP set (file `LEEP-Claymont_revised_v2_SIP_dwg_3-30-26.pdf`) has cover and submission date "31 March 2026" but the title block shows "Revision 03-30-25" and "Revision 03-31-25." The 2025 in the revision dates is a clerical year typo; everything else on the sheets correctly says March 2026. Action item flagged with Acme for next reissue.

### 2.7 Panelwrights transmittal — missing CLT party wall sheet

The Panelwrights set as transmitted contains only three sheets: CS (cover), P-1 (second floor CLT), P-2 (roof deck CLT). **There is no CLT party wall layout sheet.**

Three possibilities:
1. Panelwrights produced a separate CLT party wall sheet (P-3 or later) that wasn't included in this transmittal.
2. The party walls are being detailed by the EOR rather than fabricated as panelized CLT.
3. The party wall is something other than CLT — the F&P "steel frames by other" language and the A-502 detail showing CLT bearing on CMU need to be reconciled with what Panelwrights is actually fabricating.

Action item: chase with Panelwrights and confirm. This is the same item that was previously open from the F&P bracing/party-wall ambiguity (Section 2.1 above).

### 2.8 Panel size and delivery logistics — order of magnitude

For site planning, capital stack, and logistics coordination:

**SIP wall panels (Acme):**
- 6-1/2" thick (confirmed on Sheet P7 details)
- Standard production envelope: up to 8'-0" wide × 24'-0" long
- For Claymont, expect most panels in 8' × 8' to 8' × 16' range
- Weight: ~3.5–4 lb/SF; an 8' × 16' panel is ~450–510 lb
- Within standard 53' × 8'-6" flatbed envelope; no oversize permits

**CLT panels (Panelwrights / TerraLam TL500S):**
- 6-7/8" thick, 5-ply (confirmed on A-502)
- Standard widths 4'-0" or 8'-0", lengths up to 60'-0"
- For four 16'-wide units, floor and roof panels likely 8' × 14' to 8' × 16'
- Weight: ~17–18 lb/SF; an 8' × 16' floor panel is ~2,200–2,300 lb
- Within standard flatbed envelope; crane required on site for placement

**Total package:** approximately 4–6 flatbed deliveries combined, plus crane. Exact panel-by-panel breakdown will land with the supplemental schedules requested from Acme and Panelwrights.

### 2.9 A-502 detail sheet — top three issues

Of the 26 comments in the A-502 review, three are highest-impact and worth highlighting at the top of any future Claymont session:

**Top-1 — SIP-to-CMU bearing detail (D-3, comment #13).** The SIP shown bearing directly on grout bed without bottom plate, anchor bolts, sill gasket, or SIP-to-plate fastening. Deviates from ESR-4689 conditions of use. Either fix the detail or get Acme EJ.

**Top-2 — 2HR rating bases not cited (comments #19, #21).** Both the CLT party wall and the SIP end wall are labeled "2HR" without a UL listing, Intertek listing, or NDS calculation reference on the sheet. AHJs read ratings literally. Add citation lines: "2HR FIRE-RESISTANCE RATING — ESTABLISHED BY [BASIS], CALCULATIONS BY [EOR], ON FILE WITH ARCHITECT."

**Top-3 — CMU thickness inconsistency (D-1 vs D-3, comment #9).** Detail 1 shows 8" CMU foundation. Detail 3 shows 10" CMU "continuous from foundation." 2-inch offset somewhere — typo or real transition. 30-second fix to reconcile.

---

## 3. Document control / context-correction items

### 3.1 Naming correction — Dr. Rev. Keeling

**Memory edit added during session:** "CB CDC contact: Dr. Rev. Keeling (Central Baptist CDC). Use exactly this form — 'Dr. Rev. Keeling' — in all deliverables, letters, and references. Do NOT use any first or middle name. The expanded name previously appearing in project context belongs to a deceased person and must never be reproduced."

This appeared in OED brief content, not Claymont, but it's been corrected across the OED v2 deliverables. Worth noting here so the constraint propagates if CB CDC gets referenced in any Claymont deliverable in the future (unlikely but possible if M4Di OI Tool ever runs against Claymont as a benchmark project).

### 3.2 Larry Carson spelling

Larry **Carson** (with an 's'), not Carlson. Carson Structural / RMGC. Earlier in chat history I (Claude) used "Carson" inconsistently. Confirmed correct form is **Carson** per CBai Tech Stack chat and the AIA contract proposal records.

---

## 4. Open items at session close

These items are not blocking but should be addressed before the full building permit submission:

### 4.1 Acme & Panelwrights supplemental schedules
- Per-panel SIP schedule from Acme: width × height × thickness × opening cutouts × weight per mark
- Per-panel CLT schedule from Panelwrights: same fields, both floor (P-1) and roof (P-2)
- CLT party wall layout — confirm whether separate sheet exists or whether scope changed

### 4.2 Panelwrights code reference correction
- Cover sheet currently cites 2018 VRC; correct to City of Wilmington / Delaware on next reissue

### 4.3 Acme year typo correction
- Revision dates show 2025; cover and submission date show 2026; correct on next reissue

### 4.4 EOR engagement
- AHJ comment CR-01 — no S-series structural sheets in the foundation permit submission
- EOR must be engaged before full building permit application
- EOR scope includes: footing schedule, CMU foundation wall design, garage door lintel design, refined ASCE 7 C&C analysis for SIP openings, NDS Chapter 16 char-method calc for CLT 2HR rating, foundation-to-existing tieback or independence statement

### 4.5 A-502 reissue
- 26 comments to address per the internal review memo
- Track 1 (architect's hand) — 10 comments, single afternoon
- Track 2 (EOR coordination) — 9 comments, single agenda with EOR
- Track 3 (manufacturer coordination) — 3 comments, single packaged inquiry to Acme

### 4.6 Unit configuration confirmation
- A-502 review comment #25: confirm whether floor in Detail 2 separates dwelling units (stacked) or is intra-unit (side-by-side).
- If unit-separating, IRC R302.3 requires 1HR rating; current detail shows 1 layer 1/2" GWB which is inadequate.
- If intra-unit, no rating required and 1/2" GWB is fine; add clarifying note.

---

## 5. Project state at session close

### Foundation permit
- Submitted as foundation-only permit
- AHJ comment list returned with 47 open items (4 critical, 26 corrections, 8 information requests, 9 flags) — per CLAYMONT HYBRID source chat April 2026
- Critical items CR-01 through CR-04 are blocking permit issuance

### Panel fabrication
- Acme SIP: shop drawings issued 31 March 2026; supplemental schedule pending
- Panelwrights CLT: shop drawings issued 3/6/2026 rev. 3/12/2026; supplemental schedule and party wall layout pending
- Panel delivery dates not confirmed in source chat; foundation permit issuance gates the rest of the schedule

### Architectural set
- Aubyn detail sheet A-502 current at 04/23/2026
- Full architectural set (A-100 through A-501 series) at April 2026 issue level
- Next reissue should incorporate the 26 A-502 review comments plus any Track 2 EOR feedback

### Structural
- F&P structural review on file
- Open items per F&P review: SIP transverse check at openings, CLT char-method calc citation, party wall system clarification (now resolved by A-502 — see 2.1 above)
- EOR seat open

---

## 6. Files produced this session — full list

All in `/mnt/user-data/outputs/` from source chat:

**Claymont deliverables:**
- `Claymont_Reviewer_Response_AE24-002.docx` — formal 6-page reviewer Q&A memo
- `Claymont_Reviewer_Response_AE24-002.pdf` — same, PDF
- `A502_Review_Comments_AE24-002.docx` — 11-page internal QA review (26 comments)
- `A502_Review_Comments_AE24-002.pdf` — same, PDF
- Email body for Larry Carson — generated as message_compose output, not saved to file (capture from source chat if needed)

**Non-Claymont deliverables from same source chat (NOT for this lane):**
- `Wilmington_OED_Brief_v2.pdf` — OED meeting brief v2 with Section 9 (Riverfront East Parcel B + 1601 Jessup)
- `Wilmington_OED_Brief_v2_screen.html` — Zoom version
- `Wilmington_OED_Brief_PRINT_v2.html` — print source
- `OED_Letter_A_Merge4Ward_DRAFT.docx` — OED letter of support, Merge4Ward
- `OED_Letter_B_M4Di_CBCDC_DRAFT.docx` — OED letter of support, M4Di / CB CDC

---

## 7. Next session priorities — Claymont

In rough order of urgency:

1. **A-502 Track 1 markup** — 10 architect's-hand comments in single afternoon; relabel detail titles, fix copy-paste grout-bed note, add face designators on rated assemblies, add reference bubble sheet keys, specify firestop products
2. **EOR engagement** — required before full building permit; AHJ already flagged
3. **Acme inquiry** — packaged single-message inquiry covering SIP bottom plate condition (#13), 2HR end wall rating basis (#21), and ESR-4689 SIP-to-CMU bearing deviation (#23)
4. **Panelwrights inquiry** — supplemental schedule, party wall layout sheet, cover sheet code reference correction
5. **Larry Carson follow-up** — once Acme and Panelwrights respond, share consolidated package; F&P bracing/party-wall ambiguity now resolved by A-502 (Section 2.1) — confirm with Larry that this closes F2
6. **Foundation permit response** — address the 4 critical items (CR-01 through CR-04) and the 26 corrections from the AHJ comment list

---

*End of session summary. Migrate to CLAYMONT HYBRID II project lane.*
