# Design Team Workflow
**M4Di / Merge 4 Design / Aubyn Architecture**
*Last updated: 2026-03-27*

---

## Overview

This document describes how the CBai platform integrates with the design tool stack used by M4D and Aubyn Architecture. The goal is a workflow where the design process feels like a back-and-forth conversation between team members and Claude — from M4Di ROM through design through construction, with ALDi tracking through closeout.

Claude is not a CAD engine. It sits at the center of the workflow as the **intelligence layer** — interpreting natural language intent, generating structured instructions, writing scripts, automating document production, and translating between phases. The handoffs between tools — and between team members — feel like a conversation rather than a file transfer.

---

## Tool Roles

### Rhino 3D + Grasshopper
**Role:** Computational geometry engine
**What it handles:** Complex massing, parametric site constraints, algorithmic geometry — FAR calculations that drive envelope, setback-driven massing, structural grid optimization.
**Claude's role:** Writes Grasshopper definitions from natural language descriptions. Team member describes design intent → Claude writes the parametric logic → team member runs it.

*Example prompt:* "Generate a massing that maximizes GFA within a 35-foot height limit, 15-foot front setback, and 8-foot side setbacks on this site."

---

### Snaptrude
**Role:** Program-to-massing bridge
**What it handles:** Accepts Excel program imports directly from M4Di.Oi™ workbook and produces live-linked 3D models. Exports to Revit. Right tool for P2 test fit phase.
**Claude's role:** Upstream — generating the program schedule from a client brief. Downstream — writing the narrative that describes massing options for the decision memo.

**Key workflow:** Program defined in OI Tool → imported into Snaptrude → massing generated → concept renderings produced → narrative drafted by Claude.

---

### Blender + Bonsai
**Role:** BIM authoring (IFC-native) + rendering engine
**What it handles:**
- Bonsai: native IFC BIM authoring — walls, slabs, doors, spaces, properties, schedules, quantities. Every element is a genuine IFC entity with proper semantic meaning.
- Blender Cycles: photorealistic rendering competitive with any paid renderer.
**Claude's role:** Bonsai MCP server connects Claude directly to the live IFC model. Claude can query spatial structure, list entities, extract quantities, export drawings, and modify elements via natural language.

**Key Bonsai MCP tools available:**
- `get_ifc_project_info` — project name, description, entity counts
- `list_ifc_entities` — list walls, doors, spaces by type
- `get_ifc_properties` — all properties of a specific element by GlobalId
- `get_ifc_spatial_structure` — full hierarchy: site → building → storeys → spaces
- `get_ifc_quantities` — area, volume, length with filters
- `export_drawing_png` — 2D/3D drawings as high-resolution PNG
- `export_bc3_budget` — construction cost budget file linked to IFC quantities

**IFC as universal format:** IFC is the open standard that every BIM tool reads and writes. A model built in Bonsai is immediately readable by Revit, Snaptrude, and ArchiCAD without conversion loss.

---

### Revit (LT → Full)
**Role:** Construction document engine
**What it handles:** Permit-ready and CD-level drawings. The industry standard for complex institutional projects.
**Claude's role:** Generates Dynamo scripts (Revit's visual programming environment) that automate repetitive tasks — sheet setup, view creation, title block population, schedule generation. Also generates specification sections, code compliance narratives, drawing notes from project parameters.

**Current status:** Revit LT subscribed. Upgrading to full Revit. Check if AEC Collection subscription includes Forma at no additional cost.

---

### SketchUp
**Role:** Fastest concept visualization
**What it handles:** Quick client presentations, early-stage massing studies, board-ready visualization. Ruby API scriptable by Claude.
**Claude's role:** Writes Ruby scripts for automation. Generates presentation content to accompany SketchUp exports.

**Cost:** SketchUp Go at $119/year.

---

### Autodesk Forma
**Role:** Environmental analysis layer
**What it handles:** Seven core analyses — sun hours, wind comfort, noise, microclimate, embodied carbon, operational energy, solar potential — all cloud-based, results in seconds.
**Claude's role:** Interprets Forma analysis outputs and incorporates them into P2 decision memos and client narratives.

**Note:** If M4D already subscribes to Autodesk AEC Collection, Forma is included at no additional cost. Verify immediately.

---

## The Claude Integration Points

Claude sits between human intent and tool execution at four points:

### 1. Intake Stage
Claude reads a client brief or RFP and generates:
- Structured room program in OI Tool format
- Preliminary CSI scope list for ROM estimate
- Site constraint summary from publicly available zoning data
- List of questions to resolve at kickoff

### 2. Massing Stage
Claude translates approved program and site constraints into Grasshopper or Dynamo scripts that generate compliant massing options. Plain language design intent → parametric logic → options meeting constraint envelope.

### 3. Documentation Stage
Claude generates:
- Specification sections from project parameters
- Code compliance narratives
- Drawing notes and sheet index structures
- General notes, abbreviation lists, code summary sheets (first draft, architect reviews and stamps)

### 4. Closeout Stage
Claude reads the final construction documents and ALDi Budget Tracker and produces:
- M4Di project closeout record (ALDDB data row)
- Final variance reconciliation
- Community benefit impact statement
- Funder closeout report

---

## Session Examples

### Craig + Trevor — New Project Feasibility
Both open browsers to CBai server URL → same project workspace loaded with OI Tool output, site data, grant package, Regrid parcel data.

Craig: *"Run a preliminary capital stack scan against this project — $2.1M hard cost, IDD residential, Wilmington Delaware, faith-based nonprofit owner."*

CBai reads project context → returns structured list of applicable funding programs with eligibility flags.

Trevor: *"What does the USDA Community Facilities direct loan require for documentation?"*

CBai answers from loaded context. Conversation saved to project workspace. Both can see each other's prompts.

---

### Craig + Travis — Design Session
Travis has Blender open with Bonsai and the site IFC model loaded. Bonsai MCP server running on his workstation, connected to CBai.

Craig in CBai: *"Travis, pull the square footage of all community spaces on the ground floor."*

Travis triggers in CBai: *"Get IFC quantities for all IfcSpace elements on the ground floor with function classification Community."*

CBai calls Bonsai MCP → returns answer in conversation.

Craig: *"That's 20% short of the program requirement — what are our options for expanding without exceeding the setback envelope?"*

CBai has site constraints document loaded → reasons through options → Travis starts modeling → Craig reviews Snaptrude program view.

---

### Travis — Presentation Production (Solo)
Travis: *"Generate the cover sheet text for the Harrison St. presentation — project name, client, date, design team, project description from the brief."*

CBai drafts it.

Travis: *"Write the project narrative for the community benefit section — pull from the funding justification binder."*

CBai reads the loaded document → drafts presentation-quality paragraph. Travis exports renders from Blender, assembles presentation, written content already done.

---

### Leo — Grant Screening (Solo)
Leo's workspace has the grant program spreadsheet loaded as context.

Leo: *"What federal programs does a $2.1M IDD residential facility in New Castle County, Delaware qualify for, and what is the earliest application window?"*

CBai reasons through loaded program data → returns structured answer with deadlines → Leo plans the funding calendar.

---

## Project Evolution Path

```
M4Di ROM (Gate 0)
    ↓
P1 Site Feasibility — Regrid + Zoneomics + QGIS + PolicyMap
    ↓
P2 Test Fit — Snaptrude program import + massing + Forma analysis
    ↓
P3 Concept Package — Rhino/Grasshopper or Bonsai massing + Blender renders
    ↓
Schematic Design — Bonsai IFC model + Snaptrude live-linked program
    ↓
Design Development — ALDi Gate 2 (75% DD estimate)
    ↓
Construction Documents — Revit CDs + specs + code narratives
    ↓
Permit Submission — Coordinated package
    ↓
Construction — ALDi Gate 3/4 (SOV tracking, draw requests)
    ↓
Closeout — ALDi Gate 4 (final reconciliation + ALDDB data row)
```

---

## File Format Interoperability

| From | To | Format | Notes |
|---|---|---|---|
| OI Tool | Snaptrude | Excel (.xlsx) | Direct program import |
| Bonsai | Revit | IFC (.ifc) | Open standard, no conversion loss |
| Bonsai | Rhino | IFC or OBJ | Clean geometry handoff |
| Rhino | Revit | via Rhino.Inside.Revit | Live link available |
| Snaptrude | Revit | .rvt | Clean export with parameters |
| Blender | Any | OBJ, FBX, glTF | Standard 3D formats |
| Giraffe | Any | GeoJSON, DXF, IFC | Universal export |
