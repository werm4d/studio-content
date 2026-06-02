Studio Status — Master Context File
> Paste this file at the start of any Claude session to restore full context instantly.
> Update this file at the end of every session with what was completed and what's next.
> GitHub: github.com/werm4d/studio-content | Live hub: werm4d.github.io/studio-content/
---
The Firms
Aubyn Architecture LLC
Principal: David C. Ainsworth AIA
Tagline: Form Function Fusion
Services: Architecture, landscape, consulting. Architect-Led Design-Build (ALDB).
Licensed: Delaware · Pennsylvania · Connecticut
Address: 215 N Market St. Suite 317, Wilmington DE 19801
Phone: 203 506 2413
Email: david@aubynarchitecture.com (Proton Mail)
Web: aubynarchitecture.com
Platform: Proton Mail, Proton Drive
Team: David (primary), Travis (sometimes)
Brand colors: Primary #9dab3a (PMS 383 chartreuse), Grey #59595c
Font: SaintAubyn-II.otf (lowercase only, OTTO/CFF)
Logo files:
aa-icon-mark_arch.svg — C-arc icon + rotated "architecture" wordmark
aa-lockup-full_2.svg — horizontal lockup, tight viewBox 190 0 352 84
aa-wordmark-outlined-dark.svg — solid #59595c fills, use for inline web
aa-wordmark-outlined-green.svg — #9dab3a fills
SaintAubyn-II.otf — display font, base64 embedded in website
Merge 4 Design LLC (M4D)
Tagline: Wilmington-Rooted. Built to Deliver.
Focus: Senior-led, community-centered architecture. Deep Wilmington regulatory fluency.
Address: 500 Delaware Ave. Ste 1 #1551, Wilmington, DE 19899
Phone: +1 302 367 5726
Email: info@merge4design.com
Web: merge4design.com
Platform: Microsoft 365 (Teams, SharePoint, Outlook)
Brand colors: Green #196b23, Near-black #111111
Logo: M4D-Color.png (JPEG 179x128px) — vector refinement pending
M4Di™ — Merge 4 Development Institute
Web: m4di.org
Focus: Predevelopment cost intelligence platform. OI Tool, ALDi Tracker, ALDDB.
Website file: m4di/website/M4Di_Website_v3.html (in repo)
Integration point: Connects to project folder structure at Layer 3 of AI pipeline
---
Team
David C. Ainsworth — Principal, Aubyn Architecture + M4D
Role: Architecture lead, predevelopment, estimating, OI Tool, project management
License: Registered Architect — Delaware, Pennsylvania, Connecticut
Education: B.Arch + BS Landscape Architecture, City College / CUNY
Memberships: AIA, NCARB
Experience: 20+ years — residential, community, commercial, institutional, healthcare
Trevor Knight — Principal, M4D
Role: Business development, building code analysis, regulatory compliance, GMD/Strategy
Credential: ICC Certified Building Official (CBO) — highest ICC designation
Background: 30 years, City of Wilmington License & Inspection Department. Instrumental in adopting City of Wilmington Building Code Amendments. Served on Board of Standards and Appeals, Plumbing Board of Appeals, Historic Review and Preservation Board.
Education: BS Construction Management, Tuskegee University
Key strength: Former senior official of the exact AHJ that inspects M4D projects. Knows what Wilmington inspectors look for at every phase.
Construction experience: Refrigerated/dry storage warehouses, dock construction at Port of Wilmington. Commercial, industrial, residential, mixed-use.
Leo L. Lynch — Principal, M4D
Role: Operations, grants, design lead, specifications
Background: 40+ years East Coast (FL to DE/PA). 30+ years City of Wilmington License & Inspection — including Deputy Commissioner and Acting Director.
Education: Birmingham College of Art / Birmingham Institute of Art and Design, England
Memberships: Wilmington Design Review and Preservation Commission
Key strength: Former acting director of Wilmington L&I. Deep expertise in building safety compliance, institutional and community projects, historic preservation.
Travis Davis — Principal, M4D (+ Aubyn sometimes)
Role: Delivery, BIM production, 3D rendering, digital technology
Background: 8+ years — civic, community, commercial, multi-family
Education: BS Architecture & Environmental Design, Morgan State University; AAS Architecture Engineering Technology + AAS Construction Management Technology, Delaware Tech
Memberships: NCARB (completing requirements for architect registration)
Hardware: Windows 11, Intel i7-11800H, NVIDIA RTX 3070 8GB, 32GB RAM. Use OptiX in Blender Cycles. FLUX workflow capable.
---
Pre-Inspection Observation Service (M4D)
Service name: Construction Phase Observation (CPO) / Pre-Inspection Architectural Observation
Description: Trevor or Leo visit the jobsite prior to each scheduled AHJ inspection phase (footings, foundation, framing, rough-ins, pre-drywall, etc.) and provide a written corrective action list so the contractor can fix issues before the official inspector arrives. Available for residential and commercial projects already under construction.
Competitive differentiator: Trevor (ICC CBO) and Leo (former Acting Director, Wilmington L&I) are the former senior officials of the same inspection department. Combined 70+ years in building code compliance and regulatory oversight. They know exactly what inspectors look for because they trained them.
Pricing (recommended):
Residential single visit: $550–$750 + written report
Residential full program (5–6 phases): $2,500–$4,000
Commercial single visit: $900–$1,500
Commercial full program: Hourly NTE at $200–$250/hr
Reimbursables: Mileage beyond local radius at IRS rate
Certifications relevant: Trevor holds ICC CBO (supersedes all inspector certifications). CCPIA membership recommended for commercial marketing.
Status: Service defined. Needs: website copy, one-pager, addition to fee proposal scope menu.
---
Hardware & Infrastructure
Machine	Role
Lenovo ThinkPad P1	Primary workstation (David)
Lenovo ThinkPad M550	Ollama local AI server (hostname: c-ops-server, Tailscale IP: 100.88.106.33)
Microsoft 365	M4D team collaboration (Leo, Trevor, Travis, David)
Proton Mail + Drive	Aubyn Architecture comms + storage
GitHub (studio-content repo)	Single source of truth, both firms
Ollama server: Use for routine/repetitive AI tasks. Reserve Claude API for high-value tasks.
Kai: M4D internal AI Chief of Staff persona on M550/Ollama stack. Underlying model = Claude.
---
What's Been Built
Websites (all live at werm4d.github.io/studio-content/)
File	Status	Notes
aubyn-architecture/website/aubyn-architecture.html	✓ Live	ALDB section: heading+para static, button sticky. Tab fix applied (addEventListener). Cloudflare script removed.
merge4design/website/merge4design.html	✓ Live	M4D-Color.png logo in nav+footer. "Senior-led" copy removed. New CTA heading. Footer rebuilt (original was truncated).
m4di/website/M4Di_Website_v3.html	✓ Live	M4Di site v3
index.html (root)	✓ Live	Studio dashboard — 3 firm cards, tools, pipeline, team. All links open in new tab.
Dashboard URL: werm4d.github.io/studio-content/
Share with team: This is the one URL that gives access to everything.
Brand Assets — Aubyn Architecture
Located in `aubyn-architecture/brand/logos/`:
aa-icon-mark_arch.svg, aa-lockup-full_2.svg (uploaded to repo root — move to logos folder)
aa-wordmark-outlined-dark.svg, aa-wordmark-outlined-green.svg
SaintAubyn-II.otf in `aubyn-architecture/brand/fonts/`
Brand Assets — Merge 4 Design
M4D-Color.png in `merge4design/brand/logos/`
Social Post Generator
File: shared/tools/social-post-generator.html
Live URL: werm4d.github.io/studio-content/shared/tools/social-post-generator.html
Claude API powered. Both firms, Instagram + LinkedIn. Per-visit fee ~$0.01.
Templates (in _templates/ folders)
File	Firm	Status
M4D_Fee_Proposal_Template.docx	M4D	✓ Complete — BW print-friendly, M4D logo header, all 4 fee structures, AIA B101 clause
AA_Fee_Proposal_Template.docx	Aubyn	✓ Complete — same structure, AA logo header, chartreuse accent
M4D_Invoice_Template.xlsx	M4D	✓ Complete — 5 sheets, 306 formulas, zero errors, fee + reimbursables
AA_Invoice_Template.xlsx	Aubyn	✓ Complete — same structure, AA branded
---
Architecture — The Three Layers
Layer 1 — Foundation ✓ COMPLETE
GitHub repo live. All folders, templates, collaboration protocol, AI pipeline prompts.
Layer 2 — Firm Infrastructure (in progress)
[x] Fee proposal template — both firms
[x] Invoice template — both firms
[ ] MOU template — both firms ← NEXT
[ ] Drawing title sheet — both firms
[ ] Drawing cover sheet layout
[ ] Code analysis drawing block template
[ ] Newsletter template — both firms
[ ] Correspondence templates — both firms
[ ] Pre-Inspection Observation one-pager (new service)
[ ] Update M4D-QUAL-2024.docx with current team info + CPO service
Layer 3 — Production Workflows
[ ] AI design pipeline: feasibility memo generator (prompt ready in repo)
[ ] AI design pipeline: spec writing (prompt ready in repo)
[ ] Social media GitHub Actions automation
[ ] Website domain cutover (aubynarchitecture.com + merge4design.com)
[ ] M4Di.OI integration
---
Team Collaboration Protocol
See `shared/collaboration/protocol.md` for full details.
Quick reference:
Teams (M4D): daily comms, project discussions, files — Leo/Trevor/Travis/David
Proton Mail (Aubyn): all Aubyn client correspondence
GitHub (both): all deliverables, templates, website code, project folders
Claude sessions: always paste STATUS.md to restore context
---
AI Pipeline Prompts (ready to use)
`shared/ai-pipeline/prompts/01-feasibility.md` — zoning analysis → feasibility memo
`shared/ai-pipeline/prompts/03-spec-writing.md` — project description → CSI specs
---
Active Projects
Add client projects here as they start.
---
Session Log
Date	Session focus	Output files	Next action
2026-03	Brand system, both websites	aubyn-architecture.html, merge4design.html	Deploy websites
2026-03	Social post generator prototype	social-post-generator.html	GitHub Pages setup
2026-03	GitHub repo structure + dashboard	studio-repo.zip, index.html	Upload all files
2026-03	Fee proposal templates	M4D_Fee_Proposal_Template.docx, AA_Fee_Proposal_Template.docx	Upload to _templates/
2026-03	Invoice templates	M4D_Invoice_Template.xlsx, AA_Invoice_Template.xlsx	Upload to _templates/
2026-03	Pre-inspection service research + team quals review	STATUS.md update	Upload STATUS.md to repo root
---
How to Resume in a New Claude Session
Go to github.com/werm4d/studio-content
Open STATUS.md, copy all contents
Paste into new Claude chat (in the project or here)
Say what you want to work on
At end of session: update Session Log, commit STATUS.md
Pending Reminders
AA logo SVGs (aa-icon-mark_arch.svg, aa-lockup-full_2.svg) uploaded to repo root — move to aubyn-architecture/brand/logos/
Update aubyn-architecture.html and document headers with new AA SVG logos (pending in project chat)
Update M4D-QUAL-2024.docx with 2026 info in a future session
Domain cutover: identify registrar for aubynarchitecture.com and merge4design.com
