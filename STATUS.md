# Studio Status — Master Context File
> Paste this file at the start of any Claude session to restore full context instantly.
> Update this file at the end of every session with what was completed and what's next.

---

## The Firms

### Aubyn Architecture LLC
- **Principal:** David C. Ainsworth AIA
- **Tagline:** Form Function Fusion
- **Services:** Architecture, landscape, consulting. Architect-Led Design-Build (ALDB).
- **Licensed:** Delaware · Pennsylvania · Connecticut
- **Address:** 215 N Market St. Suite 317, Wilmington DE 19801
- **Phone:** 203 506 2413
- **Email:** info@aubynarchitecture.com
- **Web:** aubynarchitecture.com
- **Platform:** Proton Mail, Proton Drive
- **Team:** David (primary), Travis (sometimes)
- **Brand colors:** Primary #9dab3a (PMS 383 chartreuse), Grey #59595c
- **Font:** SaintAubyn-II.otf (lowercase only, OTTO/CFF)

### Merge 4 Design LLC
- **Principals:** David, Leo, Trevor, Travis
- **Tagline:** Wilmington-Rooted. Built to Deliver.
- **Focus:** Senior-led, community-centered architecture. Deep Wilmington regulatory fluency.
- **Address:** 500 Delaware Ave. Ste 1 #1551, Wilmington, DE 19899
- **Phone:** +1 302 367 5726
- **Web:** merge4design.com
- **Platform:** Microsoft 365 (Teams, SharePoint, Outlook)
- **Brand colors:** Green #196b23, Near-black #111111
- **Logo:** M4D-Color.png (JPEG, 179x128px) — vector refinement pending

### M4Di.OI
- AI-integrated design intelligence system (separate Claude chat)
- Connects to both firms at Layer 3 of the production pipeline
- Integration point: this GitHub repo / shared project folder structure

---

## Hardware & Infrastructure

| Machine | Role |
|---|---|
| Lenovo ThinkPad P1 | Primary workstation (David) |
| Lenovo ThinkPad M550 | Ollama local AI server |
| Microsoft 365 | M4D team collaboration (Leo, Trevor, Travis, David) |
| Proton Mail + Drive | Aubyn Architecture comms + storage |
| GitHub (this repo) | Single source of truth, both firms, neutral ground |

**Ollama server:** Use for routine/repetitive AI tasks (drafting, template filling). Reserve Claude API for high-value tasks (spec writing, code analysis, complex documents).

---

## What's Been Built

### Aubyn Architecture website
- **File:** `aubyn-architecture/website/aubyn-architecture.html`
- **Status:** Complete, production-ready
- **Features:** SaintAubyn-II font embedded, all SVG logos inline, ALDB sticky section with floating CTA, contact form, footer © 2026
- **Hosting:** Needs deployment (GitHub Pages or current host replacement)

### Merge 4 Design website
- **File:** `merge4design/website/merge4design.html`
- **Status:** Complete, production-ready
- **Features:** M4D-Color.png logo in nav + footer, all "Senior-led" copy updated, new CTA heading
- **Note:** Original uploaded file was truncated — footer was rebuilt cleanly
- **Hosting:** Needs deployment

### Brand assets — Aubyn Architecture
Located in `aubyn-architecture/brand/logos/`:
- `aa-icon-mark.svg` — C-arc icon, fill #9dab3a, viewBox 0 0 500 500
- `aa-lockup-full_2.svg` — horizontal lockup, viewBox 190 0 352 84 (tight crop)
- `aa-icon-mark_arch.svg` — icon + rotated "architecture" wordmark
- `aa-wordmark-outlined-dark.svg` — solid #59595c fills, 17 paths (use for inline web)
- `aa-wordmark-outlined-green.svg` — #9dab3a fills
- `SaintAubyn-II.otf` in `aubyn-architecture/brand/fonts/`
- Font base64 saved for web embedding (18,188 chars)

### Brand assets — Merge 4 Design
Located in `merge4design/brand/logos/`:
- `M4D-Color.png` — primary logo mark (JPEG despite .png extension)
- Vector refinement of M4D mark is pending

### Social Post Generator
- **File:** `shared/tools/social-post-generator.html`
- **Status:** Working prototype, deployed to GitHub Pages
- **Features:** Firm selector (AA / M4D), content type (project/article/update), Instagram + LinkedIn output, Claude API powered, copy-to-clipboard, character counts
- **GitHub Pages URL:** https://[USERNAME].github.io/studio-content/social-post-generator.html
- **Next:** Wire into GitHub Actions for automated post generation on content push

---

## Architecture — The Three Layers

### Layer 1 — Foundation (this repo) ✓ IN PROGRESS
Single source of truth. All assets, templates, project files, workflows. GitHub = neutral ground for both firms.

### Layer 2 — Firm Infrastructure (build in priority order)
- [ ] Fee proposal template — Aubyn Architecture
- [ ] Fee proposal template — Merge 4 Design
- [ ] MOU template — both firms
- [ ] Drawing title sheet — both firms
- [ ] Drawing cover sheet layout — both firms
- [ ] Code analysis drawing block templates
- [ ] Newsletter template — Aubyn Architecture
- [ ] Newsletter template — Merge 4 Design
- [ ] Correspondence templates — both firms

### Layer 3 — Production Workflows (add as needed)
- [ ] AI design pipeline: feasibility memo generator
- [ ] AI design pipeline: site analysis → program doc
- [ ] AI design pipeline: spec writing (CSI format)
- [ ] AI design pipeline: Grasshopper/Dynamo script generation
- [ ] AI design pipeline: kit of parts / fabrication package
- [ ] Social media automation (GitHub Actions + Claude API)
- [ ] M4Di.OI integration
- [ ] Website deployment (both firms)

---

## Team Collaboration Protocol
See `shared/collaboration/protocol.md` for full details.

**Quick reference:**
- **Teams** (M4D): daily comms, project discussions, file sharing between Leo/Trevor/Travis/David
- **Proton Mail** (Aubyn): all Aubyn client correspondence
- **GitHub** (both): all deliverables, templates, website code, project folders
- **Claude sessions**: always paste STATUS.md to restore context

---

## Active Projects
_Add client projects here as they start. Each gets a folder under the relevant firm._

---

## Session Log
_Append a line here at the end of every Claude session._

| Date | Session focus | Output files | Next action |
|---|---|---|---|
| 2026-03 | Brand system, both websites | aubyn-architecture.html, merge4design.html | Deploy websites |
| 2026-03 | Social post generator prototype | social-post-generator.html | GitHub Pages setup |
| 2026-03 | GitHub repo structure | This repo | Upload all files, set up Pages |

---

## How to Resume in a New Claude Session
1. Open this file
2. Paste the full contents into a new Claude chat
3. Say what you want to work on
4. Claude will have full context immediately
