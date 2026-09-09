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

def _item_rects(e):
    import ifcopenshell.util.placement as _PL
    rects=[]; tx=ty=0.0
    if e.ObjectPlacement:
        try:
            Mx=_PL.get_local_placement(e.ObjectPlacement); tx=float(Mx[0][3])*M2FT; ty=float(Mx[1][3])*M2FT
        except Exception: pass
    if not e.Representation: return rects
    for r in e.Representation.Representations:
        if r.RepresentationIdentifier!="Body": continue
        for it in r.Items:
            if not it.is_a("IfcExtrudedAreaSolid"): continue
            ix=iy=0.0
            if it.Position and it.Position.Location:
                c=it.Position.Location.Coordinates; ix=c[0]*M2FT; iy=(c[1]*M2FT if len(c)>1 else 0.0)
            prof=it.SweptArea; xs=[]; ys=[]
            if prof.is_a("IfcArbitraryClosedProfileDef") and prof.OuterCurve.is_a("IfcPolyline"):
                for pt in prof.OuterCurve.Points:
                    xs.append(pt.Coordinates[0]*M2FT+ix+tx); ys.append(pt.Coordinates[1]*M2FT+iy+ty)
            elif prof.is_a("IfcRectangleProfileDef"):
                hx=prof.XDim/2.0*M2FT; hy=prof.YDim/2.0*M2FT
                xs=[ix+tx-hx,ix+tx+hx]; ys=[iy+ty-hy,iy+ty+hy]
            if xs and ys: rects.append((min(xs),min(ys),max(xs),max(ys)))
    return rects

def load_model(path):
    f=ifcopenshell.open(path); s=ifcopenshell.geom.settings()
    for k in ("use-world-coords","USE_WORLD_COORDS"):
        try: s.set(k,True); break
        except Exception: pass
    els=[]
    for cls in ("IfcWall","IfcWallStandardCase","IfcFooting","IfcSlab","IfcBeam","IfcColumn","IfcMember","IfcOpeningElement","IfcDoor","IfcWindow"):
        for e in f.by_type(cls):
            try:
                b=_bbox(s,e); b.update(cls=("IfcWall" if cls=="IfcWallStandardCase" else cls), name=e.Name or "")
                if e.is_a("IfcFooting"): b["item_rects"]=_item_rects(e)
                els.append(b)
            except Exception: pass
    return f, els

def thk(e): return min(e["x1"]-e["x0"], e["y1"]-e["y0"])
def plan_ov(a,b):
    ox=min(a["x1"],b["x1"])-max(a["x0"],b["x0"]); oy=min(a["y1"],b["y1"])-max(a["y0"],b["y0"])
    return (ox,oy) if (ox>0 and oy>0) else None
def _is_partition(e):
    # Non-bearing, slab-borne partition: thin (<6in) AND not embedded below slab (z0 > -0.5 ft).
    # Excluded from foundation checks per confirmed design (D. Ainsworth, 2026-09-08):
    # interior 4in partitions carry no floor load and sit on the slab -> no footing required.
    return thk(e) < 0.5 and e["z0"] > -0.5
def foundation_walls(els):
    return [e for e in els if e["cls"]=="IfcWall" and e["z0"]<FOUNDATION_Z_MAX and not _is_partition(e)]

RULES=[]
def rule(id,title,category,citation):
    def deco(fn):
        fn.meta=dict(id=id,title=title,category=category,citation=citation); RULES.append(fn); return fn
    return deco

# ---- CODED RULES (append here to grow the audit) ----
@rule("FTG-01","Footing wider than its wall","footing","IRC R403.1 / Table R403.1")
def _(els,cfg):
    out=[]; segs=[]
    for e in els:
        if e["cls"]=="IfcFooting":
            for r in (e.get("item_rects") or [(e["x0"],e["y0"],e["x1"],e["y1"])]): segs.append((r,e["z0"]))
    def rov(w,r):
        ox=min(w["x1"],r[2])-max(w["x0"],r[0]); oy=min(w["y1"],r[3])-max(w["y0"],r[1]); return ox>0 and oy>0
    def rthk(r): return min(r[2]-r[0],r[3]-r[1])
    for w in foundation_walls(els):
        under=[r for (r,z0) in segs if z0<=w["z0"]+0.1 and rov(w,r)]
        if not under: out.append(("ERROR",w["name"]+": no footing segment under wall")); continue
        if all(rthk(r)<=thk(w)+0.02 for r in under):
            out.append(("ERROR","%s: footing %.2fft not wider than wall %.2fft"%(w["name"],min(rthk(r) for r in under),thk(w))))
    return out or [("PASS","all foundation walls bear on a wider footing segment")]

@rule("FTG-02","Footings continuous, not overlapping segments","footing","IRC R403.1")
def _(els,cfg):
    foot=[e for e in els if e["cls"]=="IfcFooting"]; items=[]
    for i,e in enumerate(foot):
        for r in (e.get("item_rects") or [(e["x0"],e["y0"],e["x1"],e["y1"])]): items.append((r,i))
    ov=0; ex=[]
    for a in range(len(items)):
        for b in range(a+1,len(items)):
            ra,ia=items[a]; rb,ib=items[b]
            if ia==ib: continue
            ox=min(ra[2],rb[2])-max(ra[0],rb[0]); oy=min(ra[3],rb[3])-max(ra[1],rb[1])
            if ox>0.1 and oy>0.1:
                ov+=1
                if len(ex)<4: ex.append("%s x %s (%.1fx%.1fft)"%(foot[ia]["name"],foot[ib]["name"],ox,oy))
    return [("ERROR","%d overlapping footing segments across separate elements (fragmented, not one continuous footing); e.g. %s"%(ov,"; ".join(ex)))] if ov else [("PASS","footings continuous / non-overlapping across elements")]

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
    groups={}
    for e in pw: groups.setdefault(round(thk(e),1),[]).append(round(e["z1"],1))
    bad=[]
    for t,tops in groups.items():
        if max(tops)-min(tops)>0.17: bad.append("%.1fft-thick group tops %s"%(t,sorted(set(tops))))
    if bad: return [("ERROR","non-uniform bearing within a same-thickness wall group (each bearing tier must top level): %s"%("; ".join(bad)))]
    return [("PASS","each bearing tier tops uniformly: %s"%({t:sorted(set(v)) for t,v in groups.items()}))]

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
