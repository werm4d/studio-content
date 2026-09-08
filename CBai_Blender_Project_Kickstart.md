# CBai / Blender — Project Kickstart & Knowledge Base
**Merge 4 Design LLC + Aubyn Architecture LLC**
**Co-owners: David Ainsworth (lead) + Travis Davis (visualization lead)**
**April 2026 — Internal Reference Document**

---

## What This Project Folder Is For

This is the dedicated knowledge base for everything related to the CBai/Blender design and visualization workflow at M4D and Aubyn Architecture. It covers:

- The full technical stack (hardware, software, AI endpoints, integrations)
- Repeatable workflow playbooks by project type
- Travis's onboarding path to CBai and the BunkerAI server
- The live collaboration strategy for David + Travis working together in real time
- Prompt libraries, troubleshooting notes, and lessons learned
- The integration roadmap (Regrid, Bonsai MCP, Claude Code, Pattern Signal)

**This is a living document.** Every session that produces a new technique, prompt, or workflow decision should be captured here. It is the institutional memory for the firm's AI-augmented design practice.

---

## Part 1 — The Stack

### 1.1 Hardware

| Device | Role | IP | Notes |
|---|---|---|---|
| Lenovo ThinkPad P1 | Primary design workstation. Blender + Bonsai + Ladybug. Rendering, BIM modeling, Claude.ai sessions. | LAN (DHCP) | David's primary machine. |
| Lenovo ThinkPad M550 (`c-ops-server`) | BunkerAI server. Ollama, Open WebUI (port 3000), Flask (M4Di Terminal, APEX Terminal). Ubuntu Linux, CUDA-enabled. | 192.168.0.50 | Dedicated server role. Tailscale enabled. |
| Alienware m15 R2 (`DESKTOP-AUBYNAR`) | ComfyUI server. AI image rendering assist. RTX 2080 Max-Q, 8GB VRAM, 476GB free on D: drive for model storage. Windows 11 Pro. | 192.168.0.19 | Evaluate before commissioning — run `nvidia-smi` to confirm CUDA. Tailscale + ProtonVPN active. |

All three machines are on the same LAN. The M550 exposes its Ollama endpoint at `http://192.168.0.50:11434`. The Alienware will expose ComfyUI at `http://192.168.0.19:[port]` once commissioned — the ComfyUI-BlenderAI-node addon on the P1 points to the Alienware as a remote rendering server, keeping heavy inference off both the P1 and the M550.

### 1.2 Software Stack

| Layer | Tool | Version / Notes |
|---|---|---|
| 3D / BIM | Blender | Current stable. Primary design environment. |
| BIM Integration | Bonsai (formerly BlenderBIM) | IFC-native BIM addon for Blender. Enables real building geometry, not just visual massing. |
| Conceptual BIM / AI Design | Snaptrude | Browser-based BIM platform. 2 seats (David + Travis). AI agents for space planning, site analysis, zoning compliance. Export to Revit with full parametric data — the key handoff tool for CD production. Use for rapid concept generation and the Snaptrude → Revit → drafter workflow. |
| Environmental Analysis | Ladybug Tools | Blender plugins: Ladybug (solar, climate) and Honeybee (energy, shading). Installed on P1. |
| Rendering | Blender Cycles | GPU-accelerated photorealistic rendering. Final client-facing output. |
| AI Rendering Assist | ComfyUI | Node-based Stable Diffusion frontend. Target install: Alienware m15 (ComfyUI server). Connected to Blender via ComfyUI-BlenderAI-node addon. Handles AI enhancement pass before Cycles final render. Status: planned — pending Alienware commission. |
| Field Capture — Interior / Small Site | Polycam | LiDAR scan + photogrammetry on iPhone (12 Pro+ for LiDAR). Exports GLB/OBJ/FBX directly to Blender. Generates floor plans, point clouds, and room meshes. Best tool for existing building as-built capture. |
| Field Capture — Video to 3D | Luma AI | Free cloud-based Gaussian Splatting from iPhone video. Walk a space, upload video, receive photorealistic 3D reconstruction. No LiDAR required. Best fast-path for small interior fitout projects. |
| Gaussian Splat → Blender | SplatForge | Blender addon. Imports Luma AI / Polycam Gaussian Splat (.PLY) directly into Blender. Supports 16M+ splat scenes. Used as the design base for interior fitout projects. |
| Local AI | Ollama | Running on M550. LAN-accessible at `http://192.168.0.50:11434`. |
| Local AI Model | Llama 3.1 8B | Pulled on M550. Handles routine queries and offline sessions. |
| Local AI UI | Open WebUI | M550, port 3000. Claude-Bogle persona active. Team accounts: Trevor, Leo, Travis, David. |
| Cloud AI | Claude (Anthropic API) | Primary AI for high-value outputs. Accessed via claude.ai or API. |
| Dual-Path AI | M4Di Terminal AI Advisor | Cloud or local selector. Local mode protects ALDDB data. |
| Markup + Review | Bluebeam | PDF markup for CD review cycles with external drafter. Redline, comment, track revisions. Standard tool for the Snaptrude → Revit → drafter → Bluebeam → stamp workflow. |
| Project Management | Microsoft 365 | M4D team. david4d@, travis4d@, leo4d@, trevor4d@ merge4design.com |
| Source Control | GitHub (`werm4d` org) | Repos: aubynarch, merge4design, m4di, merge4ward, studio-content |

### 1.3 AI Personas and Endpoints

**Claude-Bogle** — the local AI persona running in Open WebUI on the M550. Named after Paul Bogle. Carries the full M4Di system prompt: firm methodology, ALDi gate system, FeasOps framework, ALDDB context, and project type knowledge. Used by the team for routine predevelopment queries, ROM drafting assistance, and internal tool help without routing sensitive data to the cloud.

**Claude (Anthropic API / claude.ai)** — full-capability cloud AI. Used for complex reasoning, document generation, code production, and any output that will be client-facing or requires maximum quality. This is the "expensive tool" reserved for where it matters most.

**Dual-path principle:** Local Ollama for iteration, exploration, and data-sensitive work. Cloud Claude for final outputs and heavy lifting. This is the BunkerAI philosophy — platform independence, data protection, cost control.

---

## Part 2 — The Workflow System

### 2.0 Project Type Framework

All M4D/Aubyn projects follow the same pre-design sequence (property records → scope → fee proposal). From field capture onward, the workflow branches by project type. Four types are defined:

| Type | Description | Capture Method | Capture Tools |
|---|---|---|---|
| **Vacant lot** | New construction on undeveloped land | Perimeter photos + QGIS parcel data | Polycam (photo mode), QGIS, Regrid |
| **Existing building** | Exterior and/or interior renovation | LiDAR room scan + exterior photogrammetry | Polycam LiDAR (iPhone 12 Pro+), Matterport (virtual tour only) |
| **Interior fitout** | Interior space(s) only | Video walkthrough → Gaussian Splat | Luma AI (free), Polycam LiDAR |
| **Large site / campus** | Multi-acre, multi-building | Drone photogrammetry + LiDAR | Hired drone service, Polycam LiDAR (buildings), QGIS |

**Field capture notes:**
- Luma AI is the fast-path for small interiors: shoot iPhone video of the space, upload, cloud processing returns a Gaussian Splat. SplatForge addon brings it into Blender. No LiDAR hardware required.
- Polycam LiDAR (iPhone 12 Pro+) gives ±0.5" dimensional accuracy. Standard photogrammetry gives ±2–4". Use LiDAR for any project where dimensions matter.
- Matterport is a client deliverable tool (virtual tour), not a design model source. Keep it on the sideline as an optional add-on service.
- Campus-scale sites require drone photogrammetry — hire a service for now. This is a future tool addition.

### 2.1 The Master Workflow — Site Data to Presentation

This is the generalized workflow applicable to any M4D/Aubyn project. Steps 1–2 are universal. Step 3 branches by project type. Steps 4–8 reconverge for all types.

```
STEP 1 — PROPERTY RECORDS + PARCEL DATA
Tool: Regrid API + NCC/City GIS + CBai
Input: Parcel ID or address
Output: Owner, lot area, zoning district, setbacks, deed history, permit
        history — imported as data layer. CBai runs zoning check and confirms
        by-right use, setback math, conditional use triggers.
Note: For Wilmington city parcels use Chapter 48 (not NCC UDC).

STEP 2 — SCOPE DESCRIPTION + FEE PROPOSAL
Tool: OI Tool / M4Di Terminal + CBai
Input: Project type, program targets, structural system, schedule
Output: G0 ROM draft (CBai-assisted), fee proposal issued under M4D or
        Aubyn Architecture, PSA executed before design begins.

STEP 3 — FIELD CAPTURE [BRANCHES BY PROJECT TYPE]
--- VACANT LOT ---
Tool: Polycam (photo mode) + iPhone video
Protocol: Perimeter walk with 70%+ photo overlap. Key dimensions by tape
          or laser. Street context photos. Solar orientation noted.

--- EXISTING BUILDING ---
Tool: Polycam LiDAR (iPhone 12 Pro+) + iPhone video
Protocol: Interior room-by-room scan. Exterior perimeter photogrammetry.
          Key dimensions verified with tape. Allow 2–4 hrs typical house.

--- INTERIOR FITOUT ---
Tool: Luma AI (fast path) or Polycam LiDAR
Protocol: Slow iPhone video walking space → upload to Luma AI → Gaussian
          Splat output. Or Polycam LiDAR for dimensional accuracy.
          SplatForge addon imports Gaussian Splat into Blender.

--- CAMPUS / LARGE SITE ---
Tool: Hired drone photogrammetry + Polycam LiDAR (individual buildings)
Protocol: 80%+ photo overlap on drone flight. QGIS assembles all layers.
          Individual buildings scanned with Polycam LiDAR.

STEP 4 — BASE MODEL
Tool: Blender + Bonsai + QGIS
Input: Field capture data from Step 3
Output: 3D site/space model with parcel boundary, topography, setbacks,
        regulatory planes, and datum established. As-built mesh for
        renovation and fitout projects.

STEP 5 — MASSING / LAYOUT OPTIONS (2–3 schemes)
Tool: Blender IFC massing + Snaptrude (rapid concept) + CBai
Input: Base model + program requirements
Output: Massing volumes or layout plans per scheme. CBai runs ROM QUICK
        CHECK on each scheme. Snaptrude can generate rapid layout options
        from text prompt as a starting point for fitout projects.

STEP 6 — SCHEMATIC / DESIGN DEVELOPMENT BIM
Tool: Bonsai BIM (IFC-native) + CBai
Input: Selected scheme + structural system logic
Output: Schematic BIM — room assignments, structural bay logic, MEP zone
        blocking. CBai checks code compliance: egress, ADA, occupancy.

STEP 7 — ENVIRONMENTAL ANALYSIS [new construction + campus]
Tool: Ladybug + Honeybee
Input: Schematic BIM + Wilmington DE EPW climate file
Output: Solar insolation map, shading study, drainage flow analysis.
        CBai interprets results for PV sizing, shading adequacy, ROM impact.

STEP 8 — MATERIALS + RENDERINGS
Tool: Blender Cycles + ComfyUI (Alienware, planned)
Input: Schematic BIM + material palette decisions
Output: 2–3 photorealistic renderings. ComfyUI AI enhancement pass before
        Cycles final render (once Alienware is commissioned).

STEP 9 — QUANTITY EXPORT + ROM RECONCILIATION
Tool: Bonsai IFC export → OI Tool / M4Di Terminal
Input: Confirmed floor areas, wall areas, unit counts from BIM
Output: Quantity-verified ROM; ALDi G0/G1 locked; ALDDB row initiated.

STEP 10 — SD/DD PACKAGE + PRESENTATION
Tool: Snaptrude export + PowerPoint / PDF
Input: Bonsai BIM + renderings + ROM data
Output: SD or DD-level drawing package (plans, sections, elevations, key
        details). Client presentation deck. Snaptrude model exported for
        Revit handoff.
```

### 2.2 Step Ownership

| Step | Primary | Support | Notes |
|---|---|---|---|
| 1 — Property records | David | — | David confirms zoning interpretation; CBai runs code check |
| 2 — Fee proposal | David | CBai | CBai drafts ROM; David reviews and locks |
| 3 — Field capture | Travis + David | — | Both in field; Travis leads capture protocol |
| 4 — Base model | Travis | David | Travis builds; David reviews setbacks and site constraints |
| 5 — Massing / layout | Travis + David | CBai | Collaborative — David drives program; Travis drives 3D |
| 6 — Schematic BIM | Travis + David | CBai | Collaborative — see live collaboration strategy in Part 4 |
| 7 — Environmental | Travis | David | Travis runs; David interprets for ROM and design decisions |
| 8 — Renderings | Travis | David | Travis owns; David reviews accuracy vs. design intent |
| 9 — ROM reconciliation | David | Travis | David owns numbers; Travis confirms Bonsai area takeoffs |
| 10 — SD/DD + presentation | Travis | David | Travis assembles; David reviews ROM data and code compliance |

### 2.3 CD Production Workflow — Snaptrude → Revit → Drafter → Bluebeam

The gap between renderings/SD-DD and stamped construction documents is managed through a **contract documentation service model**: David and Travis carry the project through SD/DD level, then hand off to an external Revit drafter for CD production. David stamps and submits.

**Why this model:**
- CD production is the most time-intensive, least creative phase
- A competent drafter with a firm's template can produce 80–90% of a typical CD set with minimal back-and-forth
- David's time is better spent on design decisions, CBai-assisted code review, and client management
- Bluebeam markup cycles replace in-person coordination — efficient async workflow

**The handoff package (what the drafter receives):**

| Item | Source | Notes |
|---|---|---|
| Snaptrude model export | Snaptrude → Revit (.RVT) | Full parametric data, walls/doors/windows as Revit families — not just geometry |
| SD/DD drawing set (PDF) | Bonsai / Blender export | Plans, sections, elevations, key details at schematic level |
| Project brief (1 page) | David fills out per project | AHJ jurisdiction, applicable code cycle, occupancy type, construction type, special requirements |
| M4D/Aubyn Revit template | studio-content repo | Title block, sheet organization, line weights, view templates, common family library |
| Bluebeam markup legend | studio-content repo | Color/symbol key: what red means, what blue means, cloud vs. delta |

**The cycle:**
```
David + Travis deliver SD/DD package + Snaptrude model
    ↓
Drafter builds Revit CD set using M4D template
    ↓
Drafter submits PDF for review
    ↓
David markups in Bluebeam (2–3 revision cycles typical)
    ↓
Drafter returns 98% complete set
    ↓
David final review → stamp → submit to AHJ or owner
```

**Finding the drafter — options:**

- **Local (preferred for complex projects):** Wilmington/Philadelphia corridor, $35–$65/hr. Better for projects with frequent back-and-forth.
- **Remote architectural drafting service:** India/Philippines-based firms fluent in Revit and US codes. 24–48 hr turnaround. $18–$35/hr. Works well for straightforward residential and fitout CDs.
- **Build the relationship over time:** Identify one reliable drafter (local or remote) and establish a standing arrangement. Consistency > price shopping.

**Standards package (build once, use forever):**
The Revit template, family library, sheet standards, and Bluebeam markup legend need to be built and stored in the `studio-content` GitHub repo. This is a one-time investment that makes every subsequent handoff faster and cleaner. Target: build the template set during a slow week, not in the middle of a deadline.

### 2.4 Project-Specific Workflow Instances

As specific projects develop their own CBai workflows, document them here as named instances of the master workflow above.

**Active instances:**
- `LOBDEL_AVE_v1` — 4-row, 36-unit row house development, City of Wilmington R-3. Steps 1–2 ready to execute. Vacant lot type. See ROM document M2_2026_004 v3.
- `CLAYMONT_HYBRID_v1` — CLT/SIP 4-unit townhouse, 1316–1324 N. Claymont St. Existing building type. See dedicated Claymont Hybrid project chat.



## Part 3 — Travis Onboarding Plan

Travis is the visualization and delivery lead. The CBai/Blender onboarding has two tracks running in parallel: (A) software and workflow competency, and (B) server access and AI tool integration. These are independent — Track B can start immediately; Track A depends on Travis's current Blender baseline.

### 3.1 Track A — Software and Workflow Competency

**Baseline assessment first.** Before assigning any tasks, David and Travis should do a 30-minute screen share to establish: what version of Blender Travis is running, whether Bonsai is installed and active, whether Ladybug/Honeybee is installed, and what Travis's current IFC/BIM workflow looks like (if any). This determines which steps below are already covered and which need attention.

**Phase 1 — Blender + Bonsai Fundamentals (Week 1-2)**
Target: Travis can build a site model from a parcel boundary and generate massing volumes with correct setbacks.

- [ ] Confirm Blender installation and version (recommend current LTS)
- [ ] Install/update Bonsai addon; verify IFC import/export works
- [ ] Complete Bonsai quick-start: create a simple wall, floor, and slab in IFC mode
- [ ] Import a test parcel boundary (use Lobdel Ave site as live example)
- [ ] Set up project datum, orientation, and regulatory setback planes
- [ ] Build first massing block — confirm dimensions against parcel math

**Phase 2 — Environmental Tools (Week 2-3)**
Target: Travis can run a basic solar insolation study and interpret results.

- [ ] Confirm Ladybug and Honeybee installation
- [ ] Download Wilmington DE EPW climate file (EnergyPlus weather data)
- [ ] Run solar insolation study on Lobdel Ave massing — generate heat map
- [ ] Run shading study between two rows — validate 20ft drive aisle adequacy
- [ ] Export results as image for ROM documentation

**Phase 3 — Rendering Pipeline (Week 3-4)**
Target: Travis can produce a photorealistic exterior rendering matching M4D/Aubyn's material palette.

- [ ] Confirm GPU render capability (CUDA or OptiX on Travis's workstation)
- [ ] Establish Wilmington urban material library in Blender:
  - Brick base course (dark utility brick, Flemish bond pattern)
  - Fiber cement panel (painted, horizontal lap or board-and-batten)
  - Wood accent trim (painted, medium tone)
  - Asphalt shingle roofing (dark gray)
  - Street-level concrete / pavers
- [ ] Produce first test render of Lobdel Ave Scenario I massing
- [ ] Photomatch Lobdel Ave street view (source reference photo in Step 1 site visit)
- [ ] Establish render settings standard: resolution, samples, output format

**Phase 4 — Field Capture Tools (Week 4-5)**
Target: Travis can capture an existing space and generate a usable base model in Blender.

- [ ] Install Polycam on iPhone (confirm LiDAR capability — requires iPhone 12 Pro+)
- [ ] Complete first LiDAR room scan of a test space (office, home room — any interior)
- [ ] Export as GLB from Polycam → import to Blender → verify dimensions against tape measure
- [ ] Run Blender mesh optimization: Decimate modifier, remove duplicate vertices
- [ ] Complete first Luma AI capture: shoot iPhone video of a space → upload → review Gaussian Splat output
- [ ] Install SplatForge addon in Blender → import Luma AI .PLY file → confirm splat renders correctly
- [ ] Document preferred capture protocol (photo count, video length, lighting conditions)

**Phase 5 — Snaptrude + CD Handoff Workflow (Week 5-6)**
Target: Travis can use Snaptrude for rapid concept generation and prepare the handoff package for a Revit drafter.

- [ ] Log in to Snaptrude (David has 2 seats — Travis account setup)
- [ ] Complete Snaptrude quick-start: generate a simple building from a text prompt
- [ ] Import a site plan or drawing as a reference layer
- [ ] Build a schematic design in Snaptrude using a Bonsai model as visual reference
- [ ] Export Snaptrude model to Revit (.RVT) — verify parametric data survived export
- [ ] Review M4D Revit template (when built) — understand sheet structure and family library
- [ ] Complete one Bluebeam markup round-trip: receive PDF, add redlines, return for revision

**Phase 4 — BIM Quantity Export (Week 4+)**
Target: Travis can export floor areas and unit counts from a Bonsai BIM model and deliver them in a format David can feed directly into the M4Di OI Tool.

- [ ] Learn Bonsai area schedule export (IFC quantity takeoff)
- [ ] Produce test export from Lobdel Ave schematic BIM
- [ ] Confirm format compatible with M4Di OI Tool input assumptions
- [ ] Establish export template that becomes the standard handoff from Travis to David at Step 7

### 3.2 Track B — Server Access and AI Tools

This track is independent of Blender skill level and can start immediately.

**Week 1 — Open WebUI Access**
- [ ] Travis connects to Open WebUI at `http://192.168.0.50:3000` from his machine on the LAN (or via VPN if remote)
- [ ] Log in with Travis's team account (already created)
- [ ] Confirm Claude-Bogle persona is active and responding to M4Di queries
- [ ] Test a ROM-related query and a Blender/visualization query
- [ ] Understand the difference between local Ollama responses and Claude API responses in the dual-path selector

**Week 1-2 — M4Di Terminal Orientation**
- [ ] Travis accesses M4Di Terminal via Flask app on M550
- [ ] Walk through the Overview, OI Estimate, ALDi Budget, and AI Advisor tabs
- [ ] Travis understands that the AI Advisor dual-path selector routes to either local Ollama or Claude API depending on data sensitivity
- [ ] Travis understands which data stays local (ALDDB unit prices, project-specific cost data) vs. what can go to cloud Claude (structural queries, code generation, general research)

**Week 2 — Workflow Integration**
- [ ] Travis understands how to use Claude.ai (cloud) from his own account for visualization-specific queries
- [ ] Travis knows the prompt conventions for Blender/Bonsai questions (be specific about addon version, IFC schema version, and what output format is needed)
- [ ] Travis has the Claude-Bogle system prompt context so he understands what CBai "knows" vs. what it doesn't
- [ ] Travis and David do a first collaborative session using the live collaboration protocol (see Part 4)

---

## Part 4 — Live Collaboration Strategy

This is the most important section for day-to-day practice. The goal is a workflow where David and Travis can work on the same project simultaneously — David driving program and cost decisions, Travis driving geometry and visualization — with CBai as a shared assistant that both can query in real time.

### 4.1 The Collaboration Model

The fundamental structure is **one shared design session with two parallel roles:**

**David's role during live collaboration:**
- Holds the program brief (unit count, sizes, setbacks, cost targets)
- Interprets zoning and regulatory constraints
- Queries CBai for ROM implications, cost checks, and ALDi gate decisions
- Reviews Travis's model for constructability, structural logic, and cost alignment
- Makes go/no-go decisions on design moves based on cost impact

**Travis's role during live collaboration:**
- Operates Blender/Bonsai — builds, adjusts, and visualizes
- Queries CBai for Blender-specific techniques, material setups, and rendering decisions
- Communicates model changes to David verbally or via screen share
- Exports takeoffs and BIM data at David's request

**CBai's role during live collaboration:**
- Answers David's cost and program queries in real time
- Answers Travis's Blender/Bonsai technique queries in real time
- Helps both think through design decisions by referencing project context
- Does NOT make design decisions — it informs them

### 4.2 Session Setup — Recommended Protocol

**Option A — Same Room (Optimal)**
David and Travis work at adjacent screens. David on the P1 with Claude.ai open. Travis on his workstation with Blender open. Both can query CBai independently. Screen sharing is physical — just point at each other's monitors. This is the fastest and most effective collaboration mode.

**Option B — Remote / Screen Share**
David and Travis on a video call with screen share. Travis shares his Blender screen. David has Claude.ai open on his own screen. Both query CBai via their respective sessions. A shared document (M365 Word or Teams channel) serves as the live scratchpad for design decisions and cost checks.

**Option C — Shared Open WebUI Session (Local Network)**
Both David and Travis are connected to Open WebUI on the M550. They use a shared conversation thread (if Open WebUI supports shared threads in the installed version) or parallel threads with a naming convention (e.g., `LOBDEL_SESSION_20260410_DAVID` and `LOBDEL_SESSION_20260410_TRAVIS`). This keeps sensitive project data local and off cloud endpoints during early design iteration.

### 4.3 Prompt Conventions for Live Sessions

Establish these conventions so CBai responses are immediately useful without back-and-forth:

**For David (cost/program queries):**
```
Format: [PROJECT CODE] | [QUESTION TYPE] | [SPECIFIC QUESTION]
Example: LOBDEL | COST CHECK | If we switch Row 1 from 18ft to 20ft units 
         and drop from 9 to 8 per row, what's the ROM impact at Scenario B 
         modular pricing?
```

**For Travis (Blender/Bonsai queries):**
```
Format: [TOOL] | [VERSION/ADDON] | [SPECIFIC QUESTION]
Example: BONSAI | current version | How do I assign a IfcWall to a specific 
         IfcBuildingStorey and confirm it's included in the area schedule?
```

**For shared design decisions:**
```
Format: DESIGN DECISION | [TOPIC] | [CONTEXT] | [QUESTION]
Example: DESIGN DECISION | UNIT DEPTH | We're at 35ft deep units in Scenario I. 
         Travis says we can get to 38ft without changing row spacing. David 
         wants to know if that changes the 3BR/2BA program. What does 
         18ft x 38ft x 2-story get us vs 18ft x 35ft?
```

### 4.4 Decision Logging

Every live session should produce a **session log** — a short document (even just a running Teams message thread or a text file) that captures:

1. What design decisions were made and why
2. What CBai queries produced the key insights
3. What was ruled out and the reason
4. What open items remain for the next session

This log becomes the basis for the CBai project folder update after each session. Travis owns log creation; David reviews and approves before it's added to the project folder.

### 4.5 What CBai Cannot Do in a Live Session

Be explicit with Travis about the limits:

- CBai cannot see Travis's Blender screen. It responds to verbal or typed descriptions only. Travis needs to translate what he's seeing into a clear question.
- CBai cannot run Blender scripts or modify the model directly (until Claude Code + Bonsai MCP integration is active — see roadmap below).
- CBai does not remember previous sessions unless the project context document is pasted at the start of a new conversation. Always start a new session by pointing CBai at this kickstart document or the relevant project summary.
- Local Ollama (Claude-Bogle) is less capable than cloud Claude for complex reasoning. Use local for routine iteration; use cloud for critical decisions and final outputs.

---

## Part 5 — Integration Roadmap

These are pending and active integrations that expand the CBai/Blender workflow capability.

### 5.1 Regrid API — Parcel Data Auto-Population (Priority: HIGH)
**Status:** Planned. Not yet implemented.
**What it does:** Automatically pulls parcel dimensions, zoning, ownership, and lot area. Eliminates manual GIS lookup at Step 1.
**Integration target:** First into the M4Di OI Tool (ZONING & CODE ANALYSIS tab), then as a Blender script that imports a parcel boundary directly into the site model.
**Prerequisite:** Regrid API key (contact Regrid for nonprofit pricing). David to initiate.

### 5.2 ComfyUI — AI Rendering Assist (Priority: HIGH)
**Status:** Evaluate — Alienware hardware confirmed capable (RTX 2080 Max-Q, 8GB VRAM).
**What it does:** Node-based Stable Diffusion frontend. AI enhancement pass on Blender renders before Cycles final. Connected to Blender via ComfyUI-BlenderAI-node addon. Alienware serves as the dedicated ComfyUI server on LAN.
**Next steps:** Run `nvidia-smi` on Alienware to confirm CUDA. Install ComfyUI. Install ComfyUI-BlenderAI-node on P1 pointing to Alienware as remote server.
**Model source:** CivitAI — architecture-specific checkpoints (SDXL + FLUX workflows confirmed for archviz use).

### 5.3 Snaptrude — Conceptual BIM + Revit Handoff (Priority: HIGH — ACTIVE)
**Status:** Active. 2 seats in use (David + Travis).
**What it does:** Browser-based BIM platform with AI agents for space planning, site analysis, zoning compliance. Key capability: exports directly to Revit with full parametric family data — walls, doors, windows arrive as schedulable Revit families, not just geometry. This is the missing link in the Blender → CD production pipeline.
**Workflow position:** Step 5 (rapid concept generation from text prompt) and Step 10 (SD/DD package → Revit export for drafter handoff).
**Travis onboarding:** Phase 5 of Track A. See Part 3.

### 5.4 Luma AI + SplatForge — Video to 3D Base Model (Priority: HIGH — ACTIVE)
**Status:** Active. Free tool, no installation required for Luma AI. SplatForge addon needs Blender install.
**What it does:** Luma AI processes iPhone video into a Gaussian Splat 3D reconstruction (cloud, free). SplatForge imports the resulting .PLY file into Blender for use as a design base. Best fast-path for interior fitout projects — no LiDAR hardware needed.
**Workflow position:** Step 3 field capture (interior fitout type).

### 5.5 Bonsai MCP — Direct Blender Control from CBai (Priority: MEDIUM)
**Status:** Deferred pending M550 server stabilization.
**What it does:** Connects CBai to Blender via MCP, allowing Claude to read and write model data directly — querying room areas, updating dimensions, running analysis — without Travis translating manually.
**Prerequisite:** M550 fully stabilized. Do not attempt until server setup is confirmed complete.

### 5.6 Goose AI — Agent Automation (Priority: MEDIUM — EVALUATE)
**Status:** Evaluate after M550 stable.
**What it does:** Open-source local AI agent (Linux Foundation AAIF). Runs Claude + Ollama. MCP-native. Candidate task: write and run Blender Python scripts via agent. Apache 2.0.
**Prerequisite:** M550 stable. Test one real task before committing to stack.

### 5.7 Claude Code — Script Generation (Priority: MEDIUM)
**Status:** Deferred pending M550 server stabilization.
**What it does:** Claude writes and runs Python scripts for Blender automation — batch material assignment, procedural geometry, area schedule formatting.
**Prerequisite:** M550 fully stable. Install after Bonsai MCP is confirmed working.

### 5.8 M4D Revit Template + Standards Package (Priority: HIGH — BUILD WHEN READY)
**Status:** Not yet built. Required before CD drafter workflow can operate efficiently.
**What it needs:** Revit template (.RTE) with M4D title block, sheet organization, line weights, view templates, and common family library. Bluebeam markup legend. Project brief one-pager format.
**Storage:** `studio-content` GitHub repo. Build once, use on every project.

### 5.9 Pattern Signal Migration to M550 (Priority: LOW — SEPARATE TRACK)
**Status:** Planned. Currently on Vercel. Migrate when M550 stable.

### 5.10 ClimateStudio / Grasshopper (Priority: LOW — FUTURE)
**Status:** Not yet evaluated. Ladybug covers current needs.



## Part 6 — Prompt Library

This section grows over time as David and Travis discover prompts that work reliably. Seed entries below; add to this list after each session.

### Site Modeling
```
PROMPT: I'm setting up a new site model in Bonsai for [PROJECT NAME]. 
The parcel is [WIDTH]ft x [DEPTH]ft, [ZONING], in [CITY]. 
Front setback [X]ft, rear [Y]ft, side [Z]ft. 
I want to set up reference planes for all setbacks and a site grid at [UNIT WIDTH]ft intervals. 
Walk me through the Bonsai workflow to create these as IfcGrid elements.
```

### Massing Yield Check
```
PROMPT: MASSING YIELD | [PROJECT] | Site is [W]ft x [D]ft. 
Setbacks: front [X]ft, rear [Y]ft, end sides [Z]ft. 
Drive aisles [A]ft. Units [UW]ft wide x [UD]ft deep, max [N] per row (building code). 
If I add a [N]-row layout with [N]-row configurations, confirm unit count, 
total depth used, and surplus depth. Flag any compliance issues.
```

### ROM Quick Check
```
PROMPT: ROM QUICK CHECK | [PROJECT] | [SCENARIO] | 
Current unit count [N], unit size [SF]. 
If I change to [NEW COUNT] units at [NEW SF], using Scenario B modular pricing 
at current Mid-Atlantic rates, what's the approximate total ROM change 
and new per-unit gap vs $215K target? Use the M4Di OI methodology.
```

### Material Assignment (Blender)
```
PROMPT: BLENDER MATERIAL | I need to create a principled BSDF material 
in Blender Cycles that matches [MATERIAL DESCRIPTION]. 
Give me the exact node setup: base color, roughness, metallic, 
normal map settings, and any procedural texture nodes needed.
```

### Render Setup
```
PROMPT: RENDER SETUP | BLENDER CYCLES | 
I'm rendering a [BUILDING TYPE] in an urban context. 
Time of day: [MORNING/MIDDAY/LATE AFTERNOON]. Season: [SEASON]. 
Sky conditions: [CLEAR/OVERCAST/PARTLY CLOUDY]. 
Recommend HDRI lighting setup, sun angle, camera settings (focal length, aperture), 
and denoising configuration for a photorealistic client presentation render.
```

### Field Capture — Polycam to Blender
```
PROMPT: POLYCAM IMPORT | BLENDER | 
I've exported a Polycam LiDAR scan as GLB. The space is [DESCRIPTION].
Walk me through: (1) importing GLB to Blender, (2) optimizing the mesh with
Decimate modifier without losing key geometry, (3) aligning to real-world 
coordinates, (4) setting up Bonsai IFC elements over the scan as the design base.
```

### Field Capture — Luma AI to Blender
```
PROMPT: LUMA AI TO BLENDER | SPLATFORGE |
I have a Gaussian Splat .PLY file from Luma AI for [SPACE DESCRIPTION].
Walk me through importing it into Blender using SplatForge, setting the 
correct scale, and using it as a visual reference base for a new layout design.
```

### Snaptrude Rapid Concept
```
PROMPT: SNAPTRUDE CONCEPT | [PROJECT TYPE] |
I need to generate a rapid concept layout for [PROJECT DESCRIPTION].
Site: [DIMENSIONS or ADDRESS]. Program: [ROOM LIST / SF TARGETS].
Generate 2-3 layout options. Flag any zoning or code issues I should
check before committing to a scheme.
```

### CD Drafter Brief
```
PROMPT: CD DRAFTER BRIEF | [PROJECT NAME] |
Prepare a one-page project brief for an external Revit drafter.
Project type: [TYPE]. AHJ: [JURISDICTION]. Code cycle: [IBC YEAR].
Occupancy: [TYPE]. Construction type: [TYPE]. 
Special requirements: [LIST].
Format as a clear single-page brief the drafter can reference throughout CD production.
```

---

## Part 7 — Session Log Archive

Add session logs here after each collaborative session. Format:

```
SESSION LOG — [DATE] — [PROJECT CODE] — [PARTICIPANTS]
Design decisions made: [list]
Key CBai queries: [list key prompts and responses that mattered]
Ruled out: [list with reasons]
Open items: [list]
Next session focus: [brief]
Files updated: [list any Blender files, ROM versions, or documents]
```

---

```
SESSION LOG — 2026-04-09 — STACK/TOOLWATCH — David Ainsworth
Design decisions made:
  - Tool Watch Protocol established (see Part 9) — Option A (session-opening scan)
    adopted as standing SOP; Option B (M550 cron automation) deferred to after
    Goose is running on M550
  - ComfyUI identified as the correct SD entry point for 2026 — NOT AUTOMATIC1111
  - ComfyUI-BlenderAI-node addon confirmed as the integration path for Blender ↔ SD
  - A1111 downgraded to "superseded / skip" in palette — Forge is the maintained fork
    if A1111-compatible extensions are ever needed

Key CBai queries / findings:
  - Goose AI: moved from Block to Linux Foundation AAIF; MCP-native; runs Claude + Ollama;
    Apache 2.0. Evaluated as PALETTE TOOL — test one real task before stack commitment.
    Candidate task: write + run a Blender Python script to export IFC wall areas to CSV.
  - AUTOMATIC1111: community has largely migrated to ComfyUI (node-based, more flexible)
    and Forge (A1111 fork with better VRAM management). A1111 still works but is no longer
    the leading edge for professional workflows.
  - ComfyUI: node-based SD frontend with confirmed Blender addon (ComfyUI-BlenderAI-node)
    that allows ComfyUI to serve as a remote render engine from inside Blender. Can run on
    M550 as a visualization assist server — same model as Ollama for text. HIGH priority
    for Travis evaluation.
  - CivitAI: model repository (not a tool). Source for architecture-specific SD checkpoints
    and LoRAs. Note: confirmed community archviz workflows (SDXL + FLUX) available that
    enhance Blender/SketchUp renders to photorealistic output.
  - Civitai ArchViz workflow (PH's Archviz x AI): designed to enhance renderings from any
    3D software output — Blender included. Stage 1 SDXL, Stage 2 FLUX detailing, Stage 3
    FLUX upscale. Worth bookmarking for Travis.

Ruled out:
  - AUTOMATIC1111 as primary SD install — superseded by ComfyUI. Skip.
  - GooseAI (goose.ai) — different product, cloud NLP API. Not relevant. Goose we want
    is the open-source agent at goose-docs.ai / github.com/aaif-goose/goose.

Open items:
  - Travis workstation GPU spec needed before committing to ComfyUI install
    (need 8GB+ VRAM for SDXL; 12GB+ for FLUX)
  - Goose test task to be defined and run once M550 is fully stable
  - ComfyUI-BlenderAI-node to be added to Travis Track A onboarding (Phase 3+)
  - Option B cron-based feed monitor spec to be drafted as future Goose task

Next session focus:
  - Travis baseline assessment (Blender version, GPU, Bonsai status)
  - OR: ComfyUI install planning if Travis hardware is confirmed

Files updated:
  - CBai_Blender_Project_Kickstart.md — Part 7 session log opened, Part 9 Tool Watch
    Protocol added, Part 6 Prompt Library (no new prompts this session)
```

---

```
SESSION LOG — 2026-04-10 — STACK/WORKFLOW/HARDWARE — David Ainsworth

Design decisions made:
  - CBai/Blender project workflow formalized as project-type-branching system:
    4 types (Vacant lot, Existing building, Interior fitout, Campus/large site)
    each with its own field capture method and tool chain
  - Luma AI confirmed as fast-path for interior fitout capture: iPhone video →
    Gaussian Splat → SplatForge → Blender. Free, no LiDAR hardware required.
  - Polycam LiDAR (iPhone 12 Pro+) confirmed as primary capture tool for existing
    buildings. ±0.5" accuracy. Exports GLB directly to Blender.
  - Matterport sidelined — client deliverable tool (virtual tour), not a design
    model source. Available as optional add-on service only.
  - Snaptrude confirmed active: 2 seats (David + Travis). Repositioned in workflow
    as (a) rapid concept generator from text prompt and (b) the Snaptrude → Revit
    export path that makes the CD drafter handoff model work.
  - CD production workflow adopted: contract documentation service model.
    David + Travis carry project to SD/DD. Hand off Snaptrude model + SD/DD PDF
    package to external Revit drafter using M4D template. Bluebeam markup cycles
    (2-3 rounds). David stamps and submits. Drafter sourcing: local ($35-65/hr)
    or remote architectural drafting service ($18-35/hr).
  - M4D Revit template + standards package flagged as HIGH priority build item —
    prerequisite for CD drafter workflow. Store in studio-content GitHub repo.
  - Master workflow expanded from 8 to 10 steps. Added Step 3 (field capture,
    branched by project type) and Step 9 (ROM reconciliation distinct from Step 10
    SD/DD package).
  - Alienware m15 R2 fully commissioned as ComfyUI server:
    RTX 2080 Max-Q, 8GB VRAM, CUDA 13.1. LAN: 192.168.0.19:8188.
    Startup task scheduled. Firewall rule added. Ethernet set to Private.
    BlenderAI-node addon on P1 confirmed connected to Alienware.
    First test generation complete — pipeline verified end to end.
  - SDXL base model downloaded to D:\ComfyUI\models\checkpoints\ on Alienware.
    Architecture-specific CivitAI checkpoint selection deferred to next session
    (Tool Watch item).
  - Merge4Ward ownership corrected: all 5 principals (David, Travis, Trevor, Leo,
    Gwen Motley) — NOT David and Gwen only. Saved to memory.
  - SENTINEL v4 produced: ECOSYSTEM tab added with interactive entity map,
    20 clickable nodes, detail panels. Adapted to Sentinel CSS variables for
    auto dark/light theme. sendPrompt() replaced with static panel (appropriate
    for standalone HTML).

Key CBai findings:
  - Snaptrude Spring 2026 release targets LOD 300-350 — schematic design through
    end of SD without leaving platform. Revit export delivers full parametric
    families, not just geometry. This is the missing link in the CD pipeline.
  - Luma AI + SplatForge confirmed working 2026 pipeline: free cloud GS processing,
    Blender addon supports 16M+ splat scenes. Fast-path for fitout projects.
  - Polycam → Blender: GLB export, Decimate modifier for poly reduction, mesh
    aligns to real-world coordinates. Bonsai IFC elements placed over scan mesh.
  - ComfyUI image quality with SDXL base alone is rough — base model needs refiner
    pass or architecture-specific checkpoint. CivitAI archviz checkpoints are the
    fix. Deferred to next Tool Watch session.

Ruled out / sidelined:
  - Matterport as design model source — virtual tour tool only
  - v1-5-pruned model as default — switched to sd_xl_base_1.0.safetensors

Open items:
  - CivitAI architecture checkpoint selection and download to Alienware
  - M4D Revit template + standards package (build when schedule allows)
  - Travis GPU spec received? (sent Device Manager instructions — response pending)
  - Travis Day 1 session: schedule for tomorrow or Sunday
  - SENTINEL ecosystem tab: update Merge4Ward ownership to all 5 principals
  - ROM v3 Merge4Ward ownership: confirm correction in document
  - Regrid API key (nonprofit pricing — David to initiate)
  - AI Advisor API key prompt feature in M4Di Terminal (flagged from prior session)

Next session focus:
  - Travis baseline assessment + Day 1 install session
  - CivitAI archviz model selection and first proper architectural render test
  - Goose AI test task on M550

Files updated:
  - CBai_Blender_Project_Kickstart.md — full workflow rewrite (Parts 1-2-3-5-6-8)
  - M4D_Travis_Day1_Setup.docx — new document, 5-part onboarding guide
  - SENTINEL_v4.html — ECOSYSTEM tab added
  - Merge4Ward_G0_ROM_v3_April2026.docx — political language corrected throughout
```

---

## Part 8 — Quick Reference Card

For Travis to keep handy during sessions:

| I want to... | Tool | Where |
|---|---|---|
| Pull parcel data | Regrid API (manual for now) | NCC GIS or Regrid.com |
| Start a new site model | Bonsai in Blender | P1 workstation |
| Capture an existing interior (fast) | Luma AI video → SplatForge | Shoot iPhone video → lumalabs.ai → import .PLY via SplatForge in Blender |
| Capture an existing interior (accurate) | Polycam LiDAR | iPhone 12 Pro+ → export GLB → import to Blender |
| Generate a rapid concept layout | Snaptrude | snaptrude.com — David's account (2 seats) |
| Export Snaptrude model to Revit | Snaptrude export | Snaptrude → Export → Revit (.RVT) — full parametric data |
| Query CBai locally (data-sensitive) | Open WebUI — Claude-Bogle | `http://192.168.0.50:3000` |
| Query CBai in cloud (complex output) | Claude.ai | claude.ai / your account |
| Check ROM impact of a design change | Claude.ai — ROM QUICK CHECK prompt | Use prompt format in Part 6 |
| Access M4Di Terminal | Flask app on M550 | `http://192.168.0.50:[port]` |
| Run solar analysis | Ladybug in Blender | P1 workstation |
| Export area schedule from BIM | Bonsai IFC quantity takeoff | Bonsai addon in Blender |
| Run AI image enhancement | ComfyUI via Blender | N-panel → ComfyUI tab (remote: 192.168.0.19:8188) |
| Open ComfyUI directly in browser | ComfyUI web UI | `http://192.168.0.19:8188` |
| Render final image | Blender Cycles | P1 — GPU render |
| Mark up CD drawings for drafter | Bluebeam | PDF markup — use firm markup legend |
| Log a session decision | Session Log (Part 7 of this doc) | Add entry here |

---

## Contacts & Access

| Resource | Detail |
|---|---|
| BunkerAI / M550 | `c-ops-server` at `192.168.0.50` — Ubuntu Linux, LAN only |
| Open WebUI | `http://192.168.0.50:3000` — Travis team account already created |
| Ollama API | `http://192.168.0.50:11434` — LAN access only |
| ComfyUI server (Alienware) | `http://192.168.0.19:8188` — LAN + Tailscale remote |
| ComfyUI in Blender | N-panel → ComfyUI tab → Remote server → 192.168.0.19:8188 |
| Model loaded (Ollama) | Llama 3.1 8B |
| ComfyUI models folder | `D:\ComfyUI\models\checkpoints\` on Alienware |
| GitHub org | `werm4d` — repos: aubynarch, merge4design, m4di, merge4ward, studio-content |
| Snaptrude | snaptrude.com — 2 seats (David + Travis) |
| David | david4d@merge4design.com / david@aubynarch.com |
| Travis | travis4d@merge4design.com |



## Part 9 — Tool Watch Protocol

### Purpose

The AI tool landscape moves fast. New open-source tools, Blender integrations, SD models, MCP extensions, and agent frameworks appear weekly. The goal of the Tool Watch protocol is to ensure the CBai/Blender stack stays current without team members needing to monitor social media, YouTube ads, or product newsletters themselves. CBai handles the scan; the team gets a verdict.

**Core philosophy:** If it's worth having, CBai will surface it. Scroll past the Instagram ad with confidence.

---

### Standing SOP — Session-Opening Scan (Option A)

**Every time a new session opens in this project chat, CBai runs a brief tool scan before getting into the work.**

The scan takes approximately 60 seconds and checks:
- Futurepedia (AI tool directory, architecture/visualization category)
- GitHub trending (Blender addons, MCP extensions, open-source agents)
- Recent ComfyUI / Stable Diffusion community developments
- Any flagged tool categories relevant to active projects

**Output format — one of two responses:**

> *"Nothing new worth flagging this session. Proceeding."*

or

> *"🔔 TOOL WATCH NOTE — [Tool Name] — [one-paragraph summary and verdict]. Full evaluation below if relevant."*

The scan does not interrupt the session — it precedes it. If nothing is worth flagging, it's a one-liner and we move on.

---

### Tool Evaluation Criteria

When a new tool is identified, CBai evaluates it against four questions:

1. **Does it replace something we already have?** If yes — is it better enough to justify migration cost?
2. **Does it fill a gap in the stack?** (e.g., something Steps 1–8 currently can't do well)
3. **Does it run locally / respect BunkerAI principles?** Cloud-only SaaS that touches project data gets a lower score.
4. **Is it actually production-ready, or is it hype?** GitHub stars ≠ reliability. Look for: active commits, real user workflows, architecture-specific use cases documented.

---

### Tool Status Tiers

| Tier | Label | Meaning |
|---|---|---|
| ✅ STACK | Permanent addition | Integrated into the master workflow |
| 🔧 PALETTE | Available when needed | Not in core stack; pulled in by project type or output need |
| 🧪 EVALUATE | Testing recommended | Promising but unproven for our workflow |
| ⏸ DEFERRED | Hold | Good tool, wrong time — revisit when gate condition is met |
| ❌ SKIP | Not relevant | Superseded, cloud-only, wrong use case, or hype |

---

### Current Palette — Tool Watch Entries

| Tool | Tier | Category | Gate / Notes |
|---|---|---|---|
| Goose AI | 🧪 EVALUATE | Agent / automation | Test on M550 after server stable. Candidate task: Blender Python script via agent. |
| ComfyUI | 🧪 EVALUATE | AI image rendering | Travis GPU check first (need 8GB+ VRAM). High priority. |
| ComfyUI-BlenderAI-node | 🧪 EVALUATE | Blender ↔ SD integration | Dependent on ComfyUI install. Blender addon, direct integration. |
| CivitAI ArchViz workflows | 🔧 PALETTE | Model / workflow library | Use when ComfyUI is running. Source for architecture SD checkpoints + LoRAs. |
| AUTOMATIC1111 (A1111) | ❌ SKIP | AI image rendering | Superseded by ComfyUI + Forge in 2026. Extension library is larger but workflow is slower. |
| Forge (A1111 fork) | 🔧 PALETTE | AI image rendering | Better VRAM mgmt than A1111. Only if A1111-compatible extensions are specifically needed. |
| Regrid API | ⏸ DEFERRED | Parcel data | David to initiate nonprofit pricing contact. First Path A OI Tool integration. |
| Bonsai MCP | ⏸ DEFERRED | Blender ↔ CBai control | Gate: M550 fully stable. High value when active. |
| Claude Code | ⏸ DEFERRED | Script generation | Gate: M550 fully stable. Do not install until server setup confirmed complete. |
| Pattern Signal (migration) | ⏸ DEFERRED | Internal app | Separate track. Migrate from Vercel to M550 when server is ready. |
| ClimateStudio / Grasshopper | ❌ SKIP | Environmental analysis | Ladybug/Honeybee covers current needs. Revisit only if Rhino enters the stack. |

---

### Option B — Automated Feed Monitor (Future)

Once Goose AI is running on the M550, build a cron-based feed monitor:
- Weekly cron job on M550 pulls Futurepedia RSS + GitHub trending (Blender, MCP, SD categories)
- Raw feed piped through Claude-Bogle for summarization and verdict scoring
- Output written to a `tool_watch_log.md` file in the `studio-content` repo
- CBai references this file at session open instead of doing a live search

**Gate:** Goose evaluated and running on M550. Spec to be drafted in a separate session.

---

---

## Part 10 — Full Workflow Vision + Capability Map

### 10.1 The Vision

A semi-automated CBai workflow enabling David and Travis to collaborate — individually or together — from project intake through construction documents under a common M4D/Aubyn Architecture office standard. Seven stages:

| Stage | Description |
|---|---|
| **1 — Intake + Feasibility** | Property records, parcel data, OI Tool ROM (M4Di ALDi G0) |
| **2 — Code / Zoning Analysis** | Chapter 48 / NCC UDC, life safety, zoning overlays, 6-layer coverage |
| **3 — Schematic Design + Renderings** | Massing, Bonsai BIM, Ladybug environmental, Cycles + AI renders |
| **4 — Design Development** | Structural and MEP knowledge integration to peer-review threshold |
| **5 — Specifications** | Division-by-division specs from Bogle drawing standards baseline |
| **6 — Construction Documents** | Snaptrude → Revit → external drafter → Bluebeam → stamp |
| **7 — Drafter Handoff** | DD package + template + markup cycle → 98% complete CD set |

The handoff model applies specifically to Stage 7: David and Travis carry the project through DD, hand the package to a CAD/Revit drafter with the M4D template and standards, provide Bluebeam markup feedback across 2-3 cycles, David stamps and submits. This model scales to projects like MaxWellness and Lobdel Ave when CD production volume requires outside support.

---

### 10.2 Current Software Stack (P1 — David)

| Software | Version | Role | Notes |
|---|---|---|---|
| Revit LT | 2026 | BIM / CD production | **UPGRADE REQUIRED — see 10.4** |
| AutoCAD LT | 2026 | 2D drafting backup | LT adequate; Standard not required |
| Blender | 5.0 | Design + visualization | Upgrade to 5.1 — verify Bonsai compatibility first |
| Bonsai (BlenderBIM) | Current | IFC-native BIM in Blender | Core workflow tool |
| Rhino 8 | 8 | Analysis + parametric | **Underutilized — see 10.3** |
| Inkscape | Current | Vector graphics / diagrams | Supplementary |
| Bluebeam | Current | PDF markup / CD review | CD drafter markup cycles |
| Snaptrude | 2 seats | Conceptual BIM + Revit export | David + Travis |
| Polycam | Pro | Field capture — LiDAR + photogrammetry | iPhone 12 Pro+ for LiDAR |

**Alienware m15 R2 (ComfyUI server):** Legacy SketchUp installed — useful only as Veras substrate for AI rendering tests. Not maintained as a design tool. ComfyUI is the primary Alienware role.

---

### 10.3 Rhino 8 — Underutilized Asset

Rhino 8 is installed on the P1 and includes Grasshopper. This unlocks a parallel analysis environment that was not fully recognized in earlier workflow planning:

| Capability | Via Rhino/Grasshopper | Status |
|---|---|---|
| Urban mobility analysis (Walkscore, Streetscore, Amenityscore) | **Urbano plugin** | Free — install and use now. No additional software needed. |
| Structural form-finding + FEA | **Karamba3D** | Grasshopper plugin. Peer-review level structural analysis. |
| Solar, daylight, energy simulation | **Ladybug/Honeybee** | More powerful in Rhino/GH than Blender. Same EPW files. |
| AI-enhanced rendering | **Veras plugin** | Rhino 8 is a supported platform. Direct competitor path to Blender Cycles + ComfyUI. |
| Parametric design | **Grasshopper** | More mature parametric environment than Blender Geometry Nodes for analysis tasks. |

**Decision:** Use Rhino/Grasshopper for analysis-heavy work (structural, environmental, urban mobility). Use Blender/Bonsai for BIM geometry and visualization. They are complementary, not competing. This also means Urbano is available today — no new software purchase required.

**Action:** Install Urbano plugin in Grasshopper. Test on Lobdel Ave or M-Well site for walkability and street vitality analysis. This feeds M4Di predevelopment narratives and grant applications directly.

---

### 10.4 Critical Software Decisions

Three decisions that unlock the most workflow capability. In priority order:

**Decision 1 — Upgrade Revit LT → Revit Standard (CRITICAL)**

Revit LT blocks:
- Worksharing — David and Travis cannot collaborate on the same Revit model simultaneously
- API access — no Dynamo automation, no Hypar integration, no batch processing
- Full family editor — limited family creation capability
- The entire CD drafter handoff model depends on a full Revit environment

Cost: approximately $300-400/yr additional subscription cost. Value: every downstream workflow capability.

**Decision 2 — Build M4D Revit Template (HIGH PRIORITY)**

One-time investment, permanent return. The template package stored in `studio-content` GitHub repo includes:
- Revit template (.RTE): title block (M4D and Aubyn Architecture variants), sheet organization, line weights, view templates
- Common family library: wall types, door/window families, annotation families
- Bluebeam markup legend: color/symbol key for CD review cycles
- Project brief format: AHJ, code cycle, occupancy, construction type — one-pager David fills per project

Build this during a slow week, not mid-deadline. Travis leads the template build with David's standards input.

**Decision 3 — Regrid API Key (HIGH PRIORITY)**

Closes the manual parcel data gap at Step 1 of every project. Contact Regrid for nonprofit pricing through M4Di. First integration target: OI Tool ZONING & CODE ANALYSIS tab auto-population. David to initiate contact.

---

### 10.5 Capability Map — Current vs. Full Stack

Honest assessment of workflow automation percentage by stage:

| Stage | Current | With Full Stack | Primary Gap |
|---|---|---|---|
| 1 — Intake + ROM | 70% | 90% | Regrid API key |
| 2 — Code / zoning analysis | 75% | 80% | Always requires David's licensed judgment |
| 3 — Schematic + renderings | 60% | 85% | Travis onboarding + Bonsai MCP |
| 4 — DD (structural/MEP) | 40% | 65% | Peer review model + Karamba3D |
| 5 — Specifications | 55% | 70% | No master spec system integration |
| 6 — CDs for permit | 30% | 75% | Revit upgrade + template + drafter |
| 7 — Drafter handoff | 50% | 85% | Revit upgrade + template |

**No stage reaches 100%.** David's licensed judgment, stamp, and final review are permanent fixtures at every stage. The goal is not full automation — it is maximizing productive output per hour of David and Travis time.

---

### 10.6 MEP and Structural — The Peer Review Model

**Structural:**
- CBai-assisted structural logic (bay sizes, load path, structural system selection) brings the design to a well-reasoned starting point
- Karamba3D in Rhino/Grasshopper runs quick structural checks — member sizing, deflection, buckling — at peer-review level
- Structural EOR (Larry Carson / RMGC or equivalent) reviews and stamps David's work rather than generating it from scratch
- **Threshold:** 3 stories and under, simple structural system, residential or light commercial = peer review model works. Above this = full EOR required.

**MEP:**
- CBai handles zone blocking, system selection logic, equipment sizing rules of thumb, and code compliance flags
- Ladybug/Honeybee covers passive mechanical (solar, thermal, natural ventilation potential)
- Licensed MEP engineer provides peer review and stamp on David's coordinated design
- HVAC load calculations, plumbing fixture unit calculations, electrical load calculations always require MEP engineer's numbers

**Civil:**
- Stormwater, grading, utility coordination — harder to partial-engineer than structural or MEP
- Most projects require full civil engineering service, not peer review
- Exception: simple infill projects where civil scope is minimal (interior fitouts, renovations without site work)

---

### 10.6.1 SE Peer Review — Remote Consultant Setup

M4D has access to a retired but licensed structural engineer available for consulting and peer review. He works from home without current software. The following workflow gives him full peer review capability at zero to minimal cost.

**The framing:** For peer review he does not need to run analysis himself — he reviews David's analysis outputs and structural drawings, then stamps the peer review letter. Software requirements are minimal.

**Recommended software stack for the SE:**

| Tool | Cost | Role |
|---|---|---|
| SkyCiv (free tier) | $0 | Browser-based beam/column/frame checks — no install required |
| SkyCiv Professional | $49/month | Full 3D FEA, load combinations, AISC/ACI/NDS code checks — subscribe per active project only |
| EngineeringPaper.xyz | Free | Browser-based structural calculation documentation with code references |
| Bluebeam Studio Session | $0 (uses David's license) | PDF markup and drawing review — SE joins David's session, no license needed |

**The peer review workflow — step by step:**

1. David runs Karamba3D in Grasshopper for preliminary structural logic, member sizing, and deflection checks
2. David exports results as PDF — load diagrams, deflection plots, member schedule
3. David packages: structural PDF outputs + structural drawing set → shared via Bluebeam Studio session
4. SE reviews PDF outputs and drawings in Bluebeam, marks up comments
5. SE runs independent spot checks on critical members using SkyCiv free tier or EngineeringPaper.xyz
6. SE documents his independent calculations
7. SE stamps and signs peer review letter

**Total cost to SE:** $0 standard projects / $49 per month on projects requiring full FEA depth.

**Bluebeam Studio access:** David initiates the Studio session from his existing Bluebeam license. SE joins via browser link — no Bluebeam license required on his end.

**If SE wants a more familiar tool (RISA-generation engineers):** RISA-2D perpetual license is approximately $600-700 one-time — within the $800 budget and well-known to engineers trained on that platform. Only purchase if SE specifically requests it after evaluating SkyCiv.

---

### 10.7 Amanbh997 Skills Integration (Pending M550 Install)

Two Claude Code skill repositories confirmed for M550 installation — next session priority:

**Claude-skills-for-Computational-Designers** (18 skills, 7 Python calculators):
- `structural_checker.py` — beam/column/deflection quick checks (Eurocode 3/ASCE)
- `solar_calculator.py` — sun position, radiation, shadow geometry (Ladybug cross-check)
- `material_estimator.py` — embodied carbon and material quantities (CLT/SIP projects, grant narratives)
- `fabrication_calculator.py` — CNC, 3D print, laser cut time and cost

**Urban-Design-Skills-Claude** (15 skills, 6 Python calculators):
- `block_optimizer.py` — optimal perimeter block dimensions for target FAR (Lobdel Ave yield analysis)
- `density_calculator.py` — site area + FAR → DU/ha, persons/ha, GFA breakdown
- `far_calculator.py` — massing yield with use-split breakdown
- `walkability_scorer.py` — Walk Score proxy from amenity distances (feeds grant narratives)
- `green_space_analyzer.py` — open space compliance vs. WHO/UN-Habitat standards
- `parking_calculator.py` — parking requirements with transit and TDM reductions

**Install protocol:** Clone both repos to M550, drop `skills/` folders into Claude Code project directory. First validation test: `block_optimizer.py` on Lobdel Ave parcel.

---

### 10.8 Tool Watch Updates — April 2026

Updates to the tool status palette based on evaluation sessions:

| Tool | Tier | Update |
|---|---|---|
| Veras (EvolveLab / Chaos) | ✅ STACK | AI rendering at Revit stage. Revit 2026 supported. Rhino 8 also supported. Try web version first on any existing render. |
| Hypar | 🧪 EVALUATE | Test on M-Well Phase 1 program — space planning from room count/adjacency. Revit export with full parametric data. Free tier available. |
| Notion AI | 🔧 PALETTE | Project management / institutional memory layer for Trevor and Leo. Not a replacement for Claude Projects. Evaluate for ops use. |
| Urbano | ✅ STACK | Available NOW via Rhino 8 + Grasshopper. Free plugin. No Rhino purchase required — already owned. Install in next Rhino session. |
| Snaptrude | ✅ STACK | 2 seats active (David + Travis). Repositioned as primary conceptual BIM and Revit export tool. Spring 2026 release targets LOD 300-350. |
| Luma AI + SplatForge | ✅ STACK | Interior fitout fast-path capture. Free cloud GS processing. SplatForge imports to Blender. |
| Polycam | ✅ STACK | Existing building LiDAR capture. GLB export to Blender. |
| ComfyUI | ✅ STACK | Commissioned on Alienware. SDXL base model loaded. CivitAI archviz checkpoint selection pending. |
| Claude-skills (Amanbh997) | ⏸ DEFERRED | Gate: M550 + Claude Code setup. High priority next session. |
| Urban-Design-Skills (Amanbh997) | ⏸ DEFERRED | Gate: M550 + Claude Code setup. High priority next session. Urbano-equivalent for Rhino-free environments. |
| ClimateStudio / Grasshopper | ❌ SKIP | Ladybug/Honeybee in Rhino/GH covers this. Already owned via Rhino 8. |

---

*Document status: ACTIVE — update after each session.*
*Last updated: 2026-04-17 — David Ainsworth / CBai Project Kickstart*
*This document is internal to Merge 4 Design LLC and Aubyn Architecture LLC. Not for external distribution.*
