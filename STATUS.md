# Studio Status — Master Context File
> Paste this file at the start of any Claude session to restore full context instantly.
> Update this file at the end of every session with what was completed and what's next.
> GitHub: github.com/werm4d/studio-content | Live hub: werm4d.github.io/studio-content/

---

## The Firms

### Aubyn Architecture LLC
- **Principal:** David C. Ainsworth AIA
- **Tagline:** Form Function Fusion
- **Services:** Architecture, landscape, consulting. Architect-Led Design-Build (ALDB).
- **Licensed:** Delaware · Pennsylvania · Connecticut
- **Address:** 215 N Market St. Suite 317, Wilmington DE 19801
- **Phone:** 203 506 2413
- **Email:** david@aubynarch.com (Proton Mail)
- **Web:** aubynarch.com
- **Platform:** Proton Mail, Proton Drive
- **Team:** David (primary), Travis (sometimes)
- **Brand colors:** Primary #9dab3a (PMS 383 chartreuse), Grey #59595c
- **Font:** SaintAubyn-II.otf (lowercase only, OTTO/CFF)
- **Logo files:** aa-icon-mark_arch.svg, aa-lockup-full_2.svg, aa-wordmark-outlined-dark.svg, aa-wordmark-outlined-green.svg, SaintAubyn-II.otf, AUBYN.png (banner, bg removable)

### Merge 4 Design LLC (M4D)
- **Tagline:** Wilmington-Rooted. Built to Deliver.
- **Address:** 500 Delaware Ave. Ste 1 #1551, Wilmington, DE 19899
- **Phone:** +1 302 367 5726 | **Email:** info@merge4design.com | **Web:** merge4design.com
- **Platform:** Microsoft 365 (Teams, SharePoint, Outlook)
- **Brand colors:** Green #196b23, Near-black #111111
- **Logo:** M4D-Color.png (JPEG 179x128px), M4D.png (banner, bg removable)

### M4Di™ — Merge 4 Development Institute
- **Web:** m4di.org | **Focus:** Predevelopment cost intelligence. OI Tool, ALDi Tracker, ALDDB.
- **Website file:** m4di/website/M4Di_Website_v3.html (in repo)

---

## Team

### David C. Ainsworth — Principal, Aubyn Architecture + M4D
- **License:** Registered Architect — DE, PA, CT | **Memberships:** AIA, NCARB, MBE, DBE
- **AA:** 203.506.2413 | david@aubynarch.com
- **M4D:** 203.506.2413 | david4d@merge4design.com

### Trevor Knight — Principal, M4D
- **Credential:** ICC Certified Building Official (CBO) — highest ICC designation
- **Background:** 30 years, City of Wilmington License & Inspection. Helped author Wilmington Building Code Amendments. Board of Standards and Appeals, Plumbing Board of Appeals, Historic Review and Preservation Board.
- **Education:** BS Construction Management, Tuskegee University
- **Phone:** 302.367.5726 | **Email:** trevor4d@merge4design.com

### Leo L. Lynch — Principal, M4D
- **Background:** 40+ years East Coast. 30+ years City of Wilmington L&I — Deputy Commissioner and Acting Director.
- **Education:** Birmingham College of Art / Birmingham Institute of Art and Design, England
- **Memberships:** Wilmington Design Review and Preservation Commission
- **Phone:** 302.345.1072 | **Email:** leo4d@merge4design.com

### Travis Davis — Principal, M4D (+ Aubyn sometimes)
- **Role:** BIM production, 3D rendering, digital technology | **Memberships:** NCARB
- **Hardware:** Windows 11, i7-11800H, RTX 3070 8GB, 32GB RAM. OptiX/Blender Cycles. FLUX capable.
- **Phone:** 302.317.6608 | **Email:** travis4d@merge4design.com

---

## Pre-Inspection Observation Service (M4D ONLY)
- **Service:** Construction Phase Observation (CPO) — Trevor or Leo visit jobsite before each AHJ inspection phase and provide written corrective action list.
- **Available:** Residential + Commercial, already under construction. M4D only — NOT Aubyn Architecture.
- **Differentiator:** Trevor (ICC CBO) + Leo (former Acting Director Wilmington L&I) — combined 70+ years. They trained the inspectors.
- **Pricing:** Residential single $550–$750 · Program $2,500–$4,000 · Commercial single $900–$1,500 · Hourly NTE $200–$250/hr
- **Status:** One-pager complete · Added to M4D website · Needs fee proposal scope menu addition

---

## Hardware & Infrastructure
| Machine | Role |
|---|---|
| Lenovo ThinkPad P1 | Primary workstation (David) |
| Lenovo ThinkPad M550 | Ollama server (c-ops-server, Tailscale 100.88.106.33) |
| Microsoft 365 | M4D team (Teams, SharePoint, Outlook) |
| Proton Mail + Drive | Aubyn Architecture |
| GitHub studio-content | Single source of truth, both firms |

---

## Live Sites
| Site | URL | Status |
|---|---|---|
| Aubyn Architecture | aubynarch.com | Live · HTTPS confirmed |
| Merge 4 Design | merge4design.com | Live · HTTPS confirmed (fixed: deleted Hostinger AAAA + ftp A records from Cloudflare) |
| M4Di | werm4d.github.io/studio-content/m4di/website/M4Di_Website_v3.html | Live |
| Studio Dashboard | werm4d.github.io/studio-content/ | Live |
| Social Post Generator | werm4d.github.io/studio-content/shared/tools/social-post-generator.html | Live |

**Domain setup:** Both domains on Cloudflare. 4x A records (185.199.108-111.153) + CNAME www→werm4d.github.io. All DNS only (grey cloud). merge4design.com in own repo; aubynarch.com in own repo; studio-content = internal dashboard only.

**HTTPS fix note:** merge4design.com HTTPS was blocked by a leftover Hostinger AAAA record (IPv6) and ftp A record. Deleting both from Cloudflare DNS allowed Let's Encrypt certificate to issue. Both firm sites now fully secure.

---

## Business Cards
**Location:** studio-content/shared/tools/cards/
**Source PNGs:** studio-content/shared/tools/cards/source/
**Card dimensions:** 3.5" x 2" (2625x1495px at 750dpi) · QR code top-right at 3/4" x 3/4"

| File | Person | URL |
|---|---|---|
| card-david-aa.html | David — Aubyn Architecture | werm4d.github.io/studio-content/shared/tools/cards/card-david-aa.html |
| card-trevor-m4d.html | Trevor — M4D | werm4d.github.io/studio-content/shared/tools/cards/card-trevor-m4d.html |
| card-leo-m4d.html | Leo — M4D | werm4d.github.io/studio-content/shared/tools/cards/card-leo-m4d.html |
| card-david-m4d.html | David — M4D | werm4d.github.io/studio-content/shared/tools/cards/card-david-m4d.html |
| card-travis-m4d.html | Travis — M4D | werm4d.github.io/studio-content/shared/tools/cards/card-travis-m4d.html |

**Features:** Front + back display · QR top-right · Save to Contacts (.vcf) · SMS · Copy · Email · Share · LinkedIn · Add to Home Screen
**QR fix:** middot replaced with hyphen in vCard data (QRCode.js cannot handle non-ASCII)
**Home screen icon:** SVG embedded. If iOS shows letter D, upload 180x180px apple-touch-icon.png to repo root.
**Physical printing:** Digital cards eliminate need for printed cards — confirmed.

---

## Templates
| File | Firm | Status |
|---|---|---|
| M4D_Fee_Proposal_Template.docx | M4D | Complete — all 4 fee structures, AIA B101 clause |
| AA_Fee_Proposal_Template.docx | Aubyn | Complete — AA branded |
| M4D_Invoice_Template.xlsx | M4D | Complete — 5 sheets, 306 formulas |
| AA_Invoice_Template.xlsx | Aubyn | Complete — AA branded |
| M4D_MOU_Template.docx | M4D | Complete — 12 sections, 3 financial options |
| AA_MOU_Template.docx | Aubyn | Complete — AA branded |
| M4D_PreInspection_OnePager.docx | M4D | Complete — ICC CBO differentiator, fee schedule |
| AA_PreInspection_OnePager.docx | Aubyn | Exists but AA does NOT offer this service |

**Upload to:** _templates/merge4design/ and _templates/aubyn-architecture/ subfolders

---

## Layer 2 — Firm Infrastructure Checklist
- [x] Fee proposal template — both firms
- [x] Invoice template — both firms
- [x] MOU template — both firms
- [x] Pre-inspection one-pager — M4D
- [x] Business cards — all 5 team members, digital format
- [ ] Drawing title sheet — both firms
- [ ] Drawing cover sheet layout
- [ ] Code analysis drawing block template
- [ ] Newsletter template — both firms
- [ ] Correspondence templates — both firms
- [ ] Capabilities HTML — update in progress (separate chat)
- [ ] Update M4D-QUAL-2024.docx with 2026 info
- [ ] Brand guidelines site — saved for new project/chat (reference: brand.here.com, brand.dropbox.com)

## Layer 3 — Production Workflows
- [ ] AI pipeline: feasibility memo (prompt ready in repo)
- [ ] AI pipeline: spec writing (prompt ready in repo)
- [ ] Social media GitHub Actions automation
- [ ] M4Di.OI integration
- [ ] Apple Wallet .pkpass for business cards (optional)

---

## Pending Reminders
- Send card URLs to Trevor, Leo, Travis — each person gets their own URL
- Move AA logo SVGs from repo root to aubyn-architecture/brand/logos/
- Upload all template .docx/.xlsx to correct _templates/ subfolders
- Upload source PNGs to shared/tools/cards/source/
- Update dashboard index.html — add Business Cards section + Fee Tool v2 link
- Brand guidelines site — new project, new chat, new session
- M4Di_Website_v4.html — deploy path TBD (supersedes v3; staged in local website folder)
- Capabilities RFQ HTML retired from repo 07-04 — retained in BRAND-TEMPLATE as pursuit template; renderings now live on M4D website Work section
- CB CDC sweep: check SOQ PDFs + capabilities + any print collateral for fiscal-sponsorship or "Institute, Inc." language before circulation
- Claymont poster v6 ($203K / Fall 2026) — CLAYMONT HYBRID chat
- GOVERNANCE — naming: OI + ALDDB are internal-only marks; client/public surfaces use M4Di / ALDi / FeasOps + plain language. Entity: internal docs may reference CB CDC fiscal sponsorship as working plan; ALL public/client/funder surfaces say "M4Di — in formation" until executed.

---

## Session Log
| Date | Session focus | Output files | Next action |
|---|---|---|---|
| 2026-03 | Brand system, both websites | aubyn-architecture.html, merge4design.html | Deploy |
| 2026-03 | Social post generator | social-post-generator.html | GitHub Pages |
| 2026-03 | GitHub repo structure + dashboard | studio-repo.zip, index.html | Upload |
| 2026-03 | Fee proposal templates | M4D + AA fee proposal .docx | Upload to _templates/ |
| 2026-03 | Invoice templates | M4D + AA invoice .xlsx | Upload to _templates/ |
| 2026-03 | Pre-inspection research + team quals | STATUS.md | Upload |
| 2026-03 | MOU + pre-inspection one-pagers | 4x .docx files | Upload to _templates/ |
| 2026-03 | Domain setup, M4D website CPO update | merge4design.html | Upload to merge4design repo |
| 2026-03 | Business cards all 5, QR fix, home screen icons | 5x card .html files | Upload to cards/, send URLs |
| 2026-03 | HTTPS fix (Hostinger AAAA record), brand guidelines planning | STATUS.md | Upload STATUS.md, start brand guidelines session |
| 2026-07-04 | M4D website Work section (Claymont feat. + Soulfully Conscious + LaMott) deployed; OI/ALDDB nomenclature scrub both sites; M4Di formation language (CB CDC removed from public); FeasOps repriced $4/8/12K; Fee Tool v2 built (Option A/B calc, AA merged, drafting comparison) | index.html (merge4design repo), M4Di_Website_v4.html, M4D_AA_FeeTool_2026_v2.html | Upload Fee Tool v2 to shared/tools/, delete old fee schedule + capabilities RFQ HTML, deploy M4Di v4 |

---

## How to Resume
1. Go to github.com/werm4d/studio-content
2. Open STATUS.md, copy all contents
3. Paste into new Claude chat or project
4. Describe what to work on
5. End of session: update log + reminders, commit STATUS.md
