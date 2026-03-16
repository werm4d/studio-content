# Team Collaboration Protocol

**Last updated:** March 2026  
**Applies to:** Merge 4 Design LLC + Aubyn Architecture LLC

---

## The rule of one platform per purpose

Every communication and file has exactly one home. No hunting across platforms.

| What | Where | Who |
|---|---|---|
| M4D daily comms | Microsoft Teams | Leo, Trevor, Travis, David |
| M4D project files (working) | SharePoint / OneDrive | Leo, Trevor, Travis, David |
| M4D client email | Outlook | Leo, Trevor, Travis, David |
| Aubyn client email | Proton Mail | David |
| Aubyn working files | Proton Drive | David |
| All final deliverables | This GitHub repo | Everyone |
| Brand assets | This GitHub repo | Everyone |
| Website code | This GitHub repo | Everyone |
| AI pipeline outputs | This GitHub repo | Everyone |

---

## Microsoft Teams — M4D channels

| Channel | Purpose |
|---|---|
| General | Announcements, firm-wide updates |
| Projects | Active project discussions (one thread per project) |
| Business Dev | Proposals, leads, client relationship notes |
| Admin | Invoicing, scheduling, operations |
| Random | Everything else |

**Rule:** Keep client-sensitive content out of Random. If it's about a project, it goes in Projects.

---

## File naming convention

All files follow this pattern:

```
YYYY-MM-DD_[FIRM]_[PROJECT-CODE]_[DESCRIPTION]_v[N].[ext]
```

Examples:
```
2026-03-15_AA_BROADKILL_FeeProposal_v1.docx
2026-04-01_M4D_WALNUT-ST_SchematicDrawings_v2.pdf
2026-03-20_AA_FirmTemplate_TitleSheet_v1.dwg
```

**Firm codes:** `AA` = Aubyn Architecture, `M4D` = Merge 4 Design  
**Project codes:** Short all-caps abbreviation of project name

---

## GitHub commit messages

When committing to this repo, use this format:

```
[FIRM] [action]: [brief description]

Examples:
AA website: update ALDB section button behavior
M4D brand: add vector logo refinement
SHARED tools: update social post generator prompts
AA project/broadkill: add feasibility memo
```

---

## Claude AI sessions — how to not lose context

1. **Start every session:** Paste `STATUS.md` from the root of this repo
2. **During session:** Work normally
3. **End every session:** Update the Session Log table in `STATUS.md` and commit

This means any team member can pick up any AI workflow without starting from scratch.

---

## Project handoffs between team members

When handing a project from one person to another:

1. Update `project.md` in the project folder — current status, outstanding items, next action
2. Post in the Teams Projects channel: "Handing [PROJECT] to [NAME] — see project.md"
3. Commit any working files to GitHub
4. 15-minute verbal or Teams call to walk through anything not in the file

---

## Weekly rhythm (suggested)

| Day | What |
|---|---|
| Monday | Quick Teams check-in — active projects, blockers (15 min) |
| Wednesday | Business dev review — proposals in progress, leads |
| Friday | Commit any open files, update STATUS.md |

---

## Decision log

When a significant decision is made about either firm — pricing, process, tools, strategy — log it here so the reasoning isn't lost.

| Date | Decision | Rationale | Who |
|---|---|---|---|
| 2026-03 | GitHub as neutral ground for both firms | Free, version-controlled, platform-agnostic | David |
| 2026-03 | Ollama for routine AI, Claude API for complex tasks | Cost management | David |
