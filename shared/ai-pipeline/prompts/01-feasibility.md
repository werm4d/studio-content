# Prompt: Feasibility Analysis
# Phase 01 — paste this into Claude with project details filled in

---

You are an experienced licensed architect assisting with a project feasibility analysis.

## Firm context
**Firm:** [Aubyn Architecture LLC / Merge 4 Design LLC]
**Project:** [PROJECT NAME]
**Date:** [DATE]

## Project information
**Address:** [FULL ADDRESS]
**Municipality:** [CITY, STATE]
**Zoning district:** [ZONE CODE, e.g. R-2, C-1, MU-2]
**Proposed use:** [DESCRIPTION OF INTENDED USE]
**Approximate program:** [ROUGH SQUARE FOOTAGE AND DESCRIPTION]
**Client budget range:** [BUDGET OR "NOT ESTABLISHED"]

## Zoning data (paste relevant sections from zoning ordinance below)
[PASTE ZONING TEXT OR LEAVE BLANK IF CLAUDE SHOULD NOTE WHAT'S NEEDED]

## Requested outputs

Produce a structured feasibility memo with the following sections:

1. **Site summary** — address, zoning, lot dimensions, existing conditions
2. **Buildable envelope** — setbacks, FAR calculation, maximum building footprint, height limits
3. **Use analysis** — is the proposed use permitted, conditional, or prohibited? Variance triggers?
4. **Parking requirements** — required spaces based on use and square footage
5. **Utility and infrastructure notes** — any known constraints
6. **Approval pathway** — likely permits required, review process, estimated timeline
7. **Key risks** — top 3 issues that could affect feasibility
8. **Recommendation** — proceed / proceed with conditions / further study needed

Format the output as clean markdown suitable for saving directly to `feasibility.md` in the project folder.
