# CBai Platform Architecture
**M4Di — Merge 4 Development Institute**
*Last updated: 2026-03-27*

---

## Overview

CBai (Claude-Based AI) is M4Di's internal AI platform — a team-wide intelligence layer connecting the M4Di predevelopment methodology, the OI Tool, the ALDi Budget Tracker, and the design tool stack. It is not a single product but a three-layer architecture running on M4Di's local server infrastructure.

The goal: every session feels like a natural back-and-forth conversation between team members and a Chief of Staff who knows every project, every tool, and every methodology decision M4Di has made.

---

## Three-Layer Architecture

### Layer 1 — Intelligence Core: Anthropic API

**What it is:** Claude Sonnet accessed via the Anthropic API (not claude.ai consumer product).

**Why API, not local LLM:**
- Claude Sonnet's reasoning capability is significantly ahead of any locally runnable open-source model for M4Di's use cases: multi-document analysis, Grasshopper script generation, procurement documentation drafting, and 6-layer feasibility reasoning.
- API calls are **not used for model training** by default for API customers. Project data stays in context windows, not Anthropic's training pipeline.
- Local LLMs (Ollama, LM Studio) remain available for routine tasks on the M550 server — CBai uses the API for high-value outputs only.

**Cost signal:** ~$3/million input tokens (Claude Sonnet). At M4Di's current project volume (4–8 active projects), estimated $50–150/month in API usage.

---

### Layer 2 — Team Interface: Open WebUI

**What it is:** A self-hosted, Docker-based web interface that gives all four partners a shared browser-based chat interface connected to the Anthropic API.

**Why Open WebUI:**
- Supports Anthropic Claude as a backend provider natively.
- Multi-user with separate accounts and project workspaces.
- Conversation history stored locally on M4Di's server — not on Anthropic's infrastructure.
- Active development community (45,000+ GitHub stars as of early 2026).
- Free and open source (MIT license).

**What lives on the server:**
- Open WebUI Docker instance
- All project workspace documents and context files
- Conversation history for every project
- The CBai system prompt (see `CBai_System_Prompt_DRAFT.md` — private, gitignored)
- M4Di.Oi™ workbooks, ALDi Budget Trackers, deliverable templates
- IFC model files and Blender project files (via network share)

**What goes to Anthropic (API calls only):**
- Text of each prompt and the loaded document context for that session
- Nothing stored permanently on Anthropic's end for API customers

**Deployment:** Docker on ThinkPad M550 (local Ollama server, repurposed as CBai host).

---

### Layer 3 — Design Tool Bridge: MCP Servers

**What it is:** Model Context Protocol (MCP) servers running on individual design workstations, connecting CBai to active design tools.

**Current MCP integrations:**
- **Bonsai MCP** (`github.com/JotaDeRodriguez/Bonsai_mcp`) — connects Claude to IFC models open in Blender/Bonsai. Enables natural language queries against live building models.

**Planned MCP integrations:**
- Rhino/Grasshopper MCP — connect Claude to active parametric definitions
- Custom M4Di MCP — connect Claude to OI Tool data and ALDi Budget Tracker

**How it works:** MCP servers are local to each workstation. They create a socket connection to the Open WebUI interface during collaborative sessions. Claude can call MCP tools mid-conversation to query or modify the active design model.

---

## Session Types

| Session | Participants | Primary Tools | CBai Role |
|---|---|---|---|
| New project feasibility | Craig + Trevor | OI Tool, Regrid/Zoneomics data | Capital stack scan, grant eligibility, site constraint summary |
| Design development | Craig + Travis | Bonsai/Blender (IFC), Snaptrude | Query IFC model, translate design intent to Grasshopper scripts, generate spec narratives |
| Presentation production | Travis (solo) | Blender renders, Snaptrude | Draft cover sheet text, project narrative, community benefit section |
| Grant screening | Leo (solo) | Grant program spreadsheet | Match project characteristics to programs, flag application windows |
| Partner sync | All four | Project workspace docs | Meeting prep, decision memo drafts, task tracking |

---

## Full Tool Stack and Cost

| Component | Tool | Cost |
|---|---|---|
| Intelligence core | Anthropic API (Claude Sonnet) | ~$50–150/mo usage |
| Team interface | Open WebUI (self-hosted, Docker) | Free |
| BIM authoring | Blender + Bonsai | Free |
| Claude–BIM bridge | Bonsai MCP server | Free (open source) |
| Parametric design | Rhino + Grasshopper | Already licensed |
| CD production | Revit LT → full Revit | Already subscribed |
| Concept modeling | SketchUp Go | $119/yr |
| Program–massing bridge | Snaptrude Org | $1,200/yr |
| Site data | Regrid + Zoneomics API | Variable, low |
| Rendering | Blender Cycles | Free |
| Server hardware | ThinkPad M550 (existing) | $0 new cost |

**Total new annual spend: ~$1,400–$2,000/yr + API usage.**

---

## What Makes CBai Proprietary

The individual tools above are available to anyone. CBai's proprietary value is the combination of:

1. **The CBai system prompt** — defines M4Di's methodology, team roles, project structure, and the Paul Bogle persona. Lives on the server. Never leaves it.
2. **Project workspace structures** — each project's context documents, loaded into the workspace at session start.
3. **M4Di methodology embedded in context** — the OI Tool, ALDi gate framework, 6-layer feasibility structure, unit price library, regional factor methodology.
4. **ALDDB data** — every closed project feeds benchmark data that makes future estimates more defensible. This compounds with every engagement.

No competitor can replicate CBai by buying the same software stack. They would also need the methodology, the team knowledge, and the ALDDB data.

---

## Privacy and Security Summary

| Data type | Where it lives | Goes to Anthropic? |
|---|---|---|
| Project documents | Local server | Only as context during active API session |
| Conversation history | Local server (Open WebUI DB) | No |
| IFC model files | Local workstation / network share | No |
| CBai system prompt | Local server | Only as system prompt in API calls |
| API call content | Anthropic API | Yes — but not used for training |

---

## Related Documents

- `M4Di_6Layer_Coverage_Map.md` — current coverage analysis across 6 predevelopment problem layers
- `Design_Team_Workflow.md` — Blender/Bonsai/Rhino/Snaptrude/Revit integration strategy
- `Bonsai_MCP_Setup_Guide.md` — step-by-step server setup
- `Open_WebUI_Setup_Guide.md` — Docker deployment on M550
- `CBai_System_Prompt_DRAFT.md` — **PRIVATE / GITIGNORED**
- `hardware_specs.md` — server hardware documentation (existing)
