# fbs_audit.py - FBS Constructability Audit
# Merge 4 Design / M4Di. Codifies the Wood-Framed Constructability Standard (memory rule #19)
# as CODED checks that run on an IFC model and return PASS/ERROR/FLAG with citations - so the
# audit runs mechanically, not from recall. Run as a hard gate before calling a model "verified".
# Rule lifecycle (README): identified -> logged in fbs_rules_backlog.yaml -> coded as @rule -> committed.
import ifcopenshell, ifcopenshell.geom, datetime
M2FT = 3.280839895
FOUNDATION_Z_MAX = 3.0  # ft; element base below this = foundation level

def _bbox(s,e):
    sh=ifcopenshell.geom.create_shape(s,e); v=sh.geometry.verts
    xs=[v[i]*M2FT for i in range(0,len(v),3)]; ys=[v[i+1]*M2FT for i in range(0,len(v),3)]; zs=[v[i+2]*M2FT for i in range(0,len(v),3)]
    b=dict(x0=min(xs),y0=min(ys),z0=min(zs),x1=max(xs),y1=max(ys),z1=max(zs)); del sh; return b

def load_model(path):
    f=ifcopenshell.open(path); s=ifcopenshell.geom.settings()
    for k in ("use-world-coords","USE_WORLD_COORDS"):
        try: s.set(k,True); break
        except Exception: pass
    els=[]
    for cls in ("IfcWall","IfcWallStandardCase","IfcFooting","IfcSlab","IfcBeam","IfcColumn","IfcMember","IfcOpeningElement","IfcDoor","IfcWindow"):
        for e in f.by_type(cls):
            try:
                b=_bbox(s,e); b.update(cls=("IfcWall" if cls=="IfcWallStandardCase" else cls), name=e.Name or ""); els.append(b)
            except Exception: pass
    return f, els

def thk(e): return min(e["x1"]-e["x0"], e["y1"]-e["y0"])
def plan_ov(a,b):
    ox=min(a["x1"],b["x1"])-max(a["x0"],b["x0"]); oy=min(a["y1"],b["y1"])-max(a["y0"],b["y0"])
    return (ox,oy) if (ox>0 and oy>0) else None
def foundation_walls(els): return [e for e in els if e["cls"]=="IfcWall" and e["z0"]<FOUNDATION_Z_MAX]

RULES=[]
def rule(id,title,category,citation):
    def deco(fn):
        fn.meta=dict(id=id,title=title,category=category,citation=citation); RULES.append(fn); return fn
    return deco

# ---- CODED RULES (append here to grow the audit) ----
@rule("FTG-01","Footing wider than its wall","footing","IRC R403.1 / Table R403.1")
def _(els,cfg):
    out=[]; ftgs=[e for e in els if e["cls"]=="IfcFooting"]
    for w in foundation_walls(els):
        under=[ft for ft in ftgs if plan_ov(w,ft) and ft["z0"]<=w["z0"]+0.1]
        if not under: out.append(("ERROR",w["name"]+": no footing under wall")); continue
        if all(thk(ft)<=thk(w)+0.02 for ft in under):
            out.append(("ERROR","%s: footing %.2fft not wider than wall %.2fft"%(w["name"],min(thk(ft) for ft in under),thk(w))))
    return out or [("PASS","all foundation walls have a wider footing")]

@rule("FTG-02","Footings continuous, not overlapping segments","footing","IRC R403.1")
def _(els,cfg):
    ftgs=[e for e in els if e["cls"]=="IfcFooting"]; ov=0; ex=[]
    for i in range(len(ftgs)):
        for j in range(i+1,len(ftgs)):
            o=plan_ov(ftgs[i],ftgs[j])
            if o and o[0]>0.1 and o[1]>0.1:
                ov+=1
                if len(ex)<4: ex.append("%s x %s (%.1fx%.1fft)"%(ftgs[i]["name"],ftgs[j]["name"],o[0],o[1]))
    return [("ERROR","%d overlapping footing-segment pairs - modeled as per-segment rectangles, not one continuous mitered strip; e.g. %s"%(ov,"; ".join(ex)))] if ov else [("PASS","footings non-overlapping")]

@rule("FTG-03","Footing bottom below frost line","footing","IRC R403.1.4")
def _(els,cfg):
    fd=cfg.get("frost_depth_ft"); gz=cfg.get("grade_z_ft",0.0)
    ftgs=[e for e in els if e["cls"]=="IfcFooting"]
    if not ftgs: return [("FLAG","no footings")]
    emb=gz-min(e["z0"] for e in ftgs)
    if fd is None: return [("FLAG","frost depth not set (config['frost_depth_ft']) - provide per Wilmington DE amendment. Current min embedment below grade = %.2fft"%emb)]
    return [("PASS","deepest footing %.2fft >= frost %.2fft"%(emb,fd))] if emb>=fd-0.01 else [("ERROR","footing embedment %.2fft < frost %.2fft - short by %.2fft"%(emb,fd,fd-emb))]

@rule("WALL-01","One wall per line (no overlapping parallel walls)","wall","IRC R404 / constructability")
def _(els,cfg):
    fw=foundation_walls(els); out=[]
    for i in range(len(fw)):
        for j in range(i+1,len(fw)):
            o=plan_ov(fw[i],fw[j])
            if o and o[0]>0.3 and o[1]>0.3:
                out.append(("ERROR","%s and %s overlap %.1fx%.1fft - double wall on one line"%(fw[i]["name"],fw[j]["name"],o[0],o[1])))
    return out or [("PASS","no double walls")]

@rule("WALL-02","Uniform bearing height at a level","wall","IRC R301.1 load path; HUD RSDG")
def _(els,cfg):
    pw=[e for e in foundation_walls(els) if (e["z1"]-e["z0"])>3.0]
    if not pw: return [("FLAG","no full-height foundation walls")]
    tops=sorted(set(round(e["z1"],1) for e in pw))
    if max(tops)-min(tops)>0.17:
        return [("ERROR","foundation walls top out at multiple elevations %s ft (spread %.2fft) - floor above cannot bear evenly"%(tops,max(tops)-min(tops)))]
    return [("PASS","uniform bearing top %s"%tops)]

@rule("WALL-03","No floating elements / supported below","wall","IRC R301.1 load path; rule #19 'no floating elements'")
def _(els,cfg):
    supports=[e for e in els if e["cls"] in ("IfcWall","IfcFooting","IfcSlab","IfcBeam","IfcColumn")]; out=[]; fl=0
    for e in els:
        if e["cls"] not in ("IfcWall","IfcColumn"): continue
        if e["z0"]<FOUNDATION_Z_MAX: continue
        if not any(sp is not e and plan_ov(e,sp) and abs(sp["z1"]-e["z0"])<0.5 for sp in supports):
            fl+=1
            if len(out)<6: out.append(("ERROR","%s (base z=%.1fft) has no support below - floating"%(e["name"],e["z0"])))
    return out or [("PASS","all walls/columns supported below")]

@rule("OPEN-01","Every opening has a header/lintel","opening","IRC R606 (masonry lintel) / R602.7 (header)")
def _(els,cfg):
    ops=[e for e in els if e["cls"]=="IfcOpeningElement"]; beams=[e for e in els if e["cls"]=="IfcBeam"]
    if not ops: return [("PASS","no openings")]
    missing=sum(1 for op in ops if not any(plan_ov(op,b) and abs(b["z0"]-op["z1"])<0.7 for b in beams))
    return [("ERROR","%d/%d openings have no header/lintel modeled (IfcBeam count=%d); wide masonry openings (garage doors) require a designed lintel"%(missing,len(ops),len(beams)))] if missing else [("PASS","all openings headed")]

def audit(path, config=None, stamp=False):
    cfg=dict(frost_depth_ft=None,grade_z_ft=0.0); cfg.update(config or {})
    f, els = load_model(path)
    lines=[]; ne=nf=np=0
    for fn in RULES:
        res=fn(els,cfg); m=fn.meta
        order={"ERROR":0,"FLAG":1,"PASS":2}; tag=["ERROR","FLAG","PASS"][min((order[s] for s,_ in res),default=2)]
        lines.append("### [%s] %s - %s  `[%s]`"%(tag,m["id"],m["title"],m["citation"]))
        for sev,msg in res:
            ne+=sev=="ERROR"; nf+=sev=="FLAG"; np+=sev=="PASS"
            lines.append("- **%s** - %s"%(sev,msg))
        lines.append("")
    ts=datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    result="FAIL" if ne else ("PASS-with-flags" if nf else "PASS")
    hdr="# FBS Constructability Audit\n**Model:** `%s`  |  %s  |  rules: %d\n**RESULT: %s** - ERRORS %d | FLAGS %d | PASS %d\n\n---\n"%(path.replace("\\","/").split("/")[-1],ts,len(RULES),result,ne,nf,np)
    summary=dict(errors=ne,flags=nf,passes=np,result=result,rules=len(RULES))
    if stamp:
        try:
            import ifcopenshell.api
            proj=f.by_type("IfcProject")[0]
            ps=ifcopenshell.api.run("pset.add_pset",f,product=proj,name="FBS_Standards")
            ifcopenshell.api.run("pset.edit_pset",f,pset=ps,properties={"LastConstructabilityAudit":ts,"AuditResult":result,"AuditErrors":ne,"AuditFlags":nf})
            f.write(path)
        except Exception as ex: summary["stamp_error"]=str(ex)
    return hdr+"\n".join(lines), summary
