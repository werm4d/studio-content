# FBS Constructability Audit
Executable constructability + building-standards checks for FBS/Aubyn IFC models. Codifies the
Wood-Framed Constructability Standard (memory rule #19) as coded checks so the audit runs
mechanically - not from recall - and is run as a HARD GATE before any structural model is called "verified."

## Run
    from fbs_audit import audit
    md, summary = audit("model.ifc", config={"frost_depth_ft": 2.5})   # frost per local code
    # audit(..., stamp=True) also writes an FBS_Standards pset (audit result + timestamp) onto IfcProject

## Gate
Run before presenting any structural model. result="FAIL" (any ERROR) => do NOT call it verified;
fix, or list the open FLAGS. Present the report alongside the model.

## Growing the audit - rule lifecycle
Living rulebase. When a new constructability rule, building standard, or design rule is identified:
1. LOG it in fbs_rules_backlog.yaml (title, category, citation, source) - immediately, so nothing is lost.
2. CODE it as an @rule(id,title,category,citation) function in fbs_audit.py (append to the RULES section).
3. TEST against a known-bad model (it must catch the case that motivated it).
4. COMMIT - move the backlog entry to status: coded.
Every rule carries its citation + source, so the rulebase is itself auditable. The audit only grows.

## Coded now
FTG-01 footing wider than wall | FTG-02 continuous footings | FTG-03 below frost |
WALL-01 one wall per line | WALL-02 uniform bearing height | WALL-03 no floating elements | OPEN-01 openings headed.
Backlog (identified, to code): see fbs_rules_backlog.yaml.
