# AI Pipeline

Prompts and scripts for Claude-assisted production workflows.

## How it works

Each phase of a project has a prompt template in `prompts/`. To run a phase:

1. Open the relevant prompt file
2. Fill in the `[BRACKETED]` fields with project-specific data
3. Paste into Claude (or run via API script)
4. Save the output to the project folder
5. Update `project.md` to mark the phase complete

## Prompts

| File | Phase | Output |
|---|---|---|
| `prompts/01-feasibility.md` | Feasibility analysis | Feasibility memo (.md) |
| `prompts/02-site-analysis.md` | Pre-design site analysis | Site analysis + program doc |
| `prompts/03-spec-writing.md` | Construction documents | CSI-format spec sections |
| `prompts/04-grasshopper.md` | Schematic (Rhino) | Grasshopper script (.gh logic) |
| `prompts/05-dynamo.md` | Design dev (Revit) | Dynamo script (.dyn logic) |
| `prompts/06-kit-of-parts.md` | Fabrication | Component library + BOM |
| `prompts/07-social-post.md` | Marketing | Instagram + LinkedIn drafts |

## Scripts

| File | Purpose |
|---|---|
| `scripts/generate-social.py` | Calls Claude API to generate social posts from project.md |
| `scripts/deploy-sites.sh` | Deploys both websites to GitHub Pages |

## Local AI (Ollama)

For routine tasks that don't need full Claude capability, use the Ollama server:
- Drafting routine client emails from a template
- Filling in schedule fields
- Summarizing meeting notes

Connect at: `http://[M550-IP]:11434`

Recommended models for architecture work:
- `llama3` — general drafting
- `mistral` — structured document generation
- `codellama` — Grasshopper/Dynamo/Python script generation
