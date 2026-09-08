import bpy

# ============================================================
# WHA SUITE 220 — EXISTING CONDITIONS BASE MODEL
# Merge 4 Design LLC / Aubyn Architecture LLC
# April 2026
# Dimensions in meters (Bonsai/IFC native)
# ============================================================

def ft(feet, inches=0):
    return (feet + inches/12) * 0.3048

def ins(inches):
    return inches * 0.0254

# ── KEY DIMENSIONS ───────────────────────────────────────────
ROOM_220_LENGTH  = ft(24)
ROOM_220_WIDTH   = ft(19)
CEILING_HT       = ft(9)
DOOR_WIDTH_D01   = ins(42)
SILL_HT          = ft(2, 10.5)
CMU_THICK        = ins(8)
GWB_THICK        = ins(4.5)
HEAD_HT          = ft(7, 4)
WALL_HT          = ft(9, 6)

ROOM_220A_L      = ft(20)
ROOM_220A_W      = ft(15)
ROOM_220B_L      = ft(15)
ROOM_220B_W      = ft(12)
ROOM_220C_L      = ft(18)
ROOM_220C_W      = ft(14)
ROOM_220D_L      = ft(12)
ROOM_220D_W      = ft(10)
ROOM_220E_L      = ft(12)
ROOM_220E_W      = ft(10)
ROOM_221_L       = ft(10)
ROOM_221_W       = ft(7.5)

# ── CLEAR SCENE ──────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# ── HELPER FUNCTIONS ─────────────────────────────────────────
def make_box(name, x, y, z, lx, ly, lz):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(
        x + lx/2, y + ly/2, z + lz/2
    ))
    obj = bpy.context.active_object
    obj.name = name
    obj.scale = (lx, ly, lz)
    bpy.ops.object.transform_apply(scale=True)
    return obj

def get_or_create_material(name, color_rgba):
    if name in bpy.data.materials:
        return bpy.data.materials[name]
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Base Color'].default_value = color_rgba
        if color_rgba[3] < 1.0:
            mat.blend_method = 'BLEND'
            bsdf.inputs['Alpha'].default_value = color_rgba[3]
    return mat

def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

def move_to_collection(obj, col_name):
    col = bpy.data.collections.get(col_name)
    if not col:
        col = bpy.data.collections.new(col_name)
        bpy.context.scene.collection.children.link(col)
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    col.objects.link(obj)

# ── MATERIALS ────────────────────────────────────────────────
mat_cmu     = get_or_create_material("CMU_Wall",       (0.85, 0.83, 0.78, 1.0))
mat_gwb     = get_or_create_material("GWB_Partition",  (0.95, 0.94, 0.90, 1.0))
mat_partial = get_or_create_material("Partial_Wall",   (0.30, 0.45, 0.75, 1.0))
mat_floor   = get_or_create_material("Concrete_Slab",  (0.60, 0.58, 0.55, 1.0))
mat_ceiling = get_or_create_material("ACT_Ceiling",    (0.97, 0.97, 0.96, 1.0))
mat_window  = get_or_create_material("Window_Glass",   (0.60, 0.80, 0.95, 0.3))
mat_door    = get_or_create_material("Door_Wood",      (0.65, 0.45, 0.25, 1.0))
mat_mep     = get_or_create_material("MEP_Element",    (0.90, 0.60, 0.10, 1.0))

# ============================================================
# SUITE LAYOUT
# Origin (0,0,0) = SW corner of Room 220
# X = East (24ft length), Y = North (19ft width), Z = Up
# ============================================================

walls    = []
floors   = []
ceilings = []
windows  = []
doors    = []
mep      = []

# ── ROOM 220 — MAIN (24' × 19') ─────────────────────────────
# South wall (exterior / window wall)
w = make_box("Wall_220_South", 0, -CMU_THICK, 0, ROOM_220_LENGTH, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# North wall
w = make_box("Wall_220_North", 0, ROOM_220_WIDTH, 0, ROOM_220_LENGTH, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# West wall
w = make_box("Wall_220_West", -CMU_THICK, -CMU_THICK, 0, CMU_THICK, ROOM_220_WIDTH + CMU_THICK*2, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# East wall — split for door D-01
door_d01_y = ROOM_220_WIDTH * 0.35
w = make_box("Wall_220_East_S", ROOM_220_LENGTH, 0, 0, CMU_THICK, door_d01_y, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220_East_N", ROOM_220_LENGTH, door_d01_y + DOOR_WIDTH_D01, 0,
             CMU_THICK, ROOM_220_WIDTH - door_d01_y - DOOR_WIDTH_D01, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# Door header D-01
w = make_box("Wall_220_DoorHdr_D01", ROOM_220_LENGTH, door_d01_y, ft(7),
             CMU_THICK, DOOR_WIDTH_D01, WALL_HT - ft(7))
assign_material(w, mat_cmu); walls.append(w)

# ── ROOM 220A — BLUE ROOM (20' × 15') ───────────────────────
b220a_y = ROOM_220_WIDTH + CMU_THICK

w = make_box("Wall_220A_North", 0, b220a_y + ROOM_220A_W, 0, ROOM_220A_L, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220A_West", -CMU_THICK, b220a_y, 0, CMU_THICK, ROOM_220A_W, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220A_East", ROOM_220A_L, b220a_y, 0, CMU_THICK, ROOM_220A_W, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# ── ROOM 220B — WORK ROOM (15' × 12') ───────────────────────
b220b_x = ROOM_220_LENGTH + CMU_THICK

w = make_box("Wall_220B_East", b220b_x + ROOM_220B_L, 0, 0, CMU_THICK, ROOM_220B_W, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220B_North", b220b_x, ROOM_220B_W, 0, ROOM_220B_L, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220B_South", b220b_x, -CMU_THICK, 0, ROOM_220B_L, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# ── ROOM 220C — L-SHAPED ANTEROOM (18' × 14') ───────────────
b220c_x = b220b_x
b220c_y = ROOM_220B_W + CMU_THICK

w = make_box("Wall_220C_East", b220c_x + ROOM_220C_L, b220c_y, 0, CMU_THICK, ROOM_220C_W, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_220C_North", b220c_x, b220c_y + ROOM_220C_W, 0, ROOM_220C_L, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# Partial-height partition (~6' tall, blue GWB)
w = make_box("Partition_220C_Partial", b220c_x + ft(5), b220c_y + ft(3), 0,
             GWB_THICK, ft(8), ft(6))
assign_material(w, mat_partial); walls.append(w)

# ── ROOM 220D — SMALL OFFICE GWB (12' × 10') ─────────────────
b220d_x = b220c_x + ROOM_220C_L + CMU_THICK

w = make_box("Wall_220D_West",  b220d_x,              0,             0, GWB_THICK, ROOM_220D_W, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

w = make_box("Wall_220D_East",  b220d_x + ROOM_220D_L, 0,            0, GWB_THICK, ROOM_220D_W, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

w = make_box("Wall_220D_South", b220d_x,              -GWB_THICK,    0, ROOM_220D_L, GWB_THICK, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

w = make_box("Wall_220D_North", b220d_x,               ROOM_220D_W, 0, ROOM_220D_L, GWB_THICK, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

# ── ROOM 220E — SMALL OFFICE (12' × 10') ────────────────────
b220e_y = ROOM_220D_W + GWB_THICK

w = make_box("Wall_220E_East",  b220d_x + ROOM_220E_L, b220e_y, 0, GWB_THICK, ROOM_220E_W, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

w = make_box("Wall_220E_North", b220d_x, b220e_y + ROOM_220E_W, 0, ROOM_220E_L, GWB_THICK, WALL_HT)
assign_material(w, mat_gwb); walls.append(w)

# ── ROOM 221 — VESTIBULE (10' × 7.5') ───────────────────────
b221_x = -ROOM_221_L - CMU_THICK

w = make_box("Wall_221_West",  b221_x - CMU_THICK, -CMU_THICK, 0, CMU_THICK, ROOM_221_W + CMU_THICK*2, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_221_North", b221_x - CMU_THICK, ROOM_221_W,  0, ROOM_221_L + CMU_THICK, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

w = make_box("Wall_221_South", b221_x - CMU_THICK, -CMU_THICK,  0, ROOM_221_L + CMU_THICK, CMU_THICK, WALL_HT)
assign_material(w, mat_cmu); walls.append(w)

# ── FLOORS ───────────────────────────────────────────────────
slab = ins(4)

for name, x, y, lx, ly in [
    ("Floor_220",  0,         0,         ROOM_220_LENGTH, ROOM_220_WIDTH),
    ("Floor_220A", 0,         b220a_y,   ROOM_220A_L,     ROOM_220A_W),
    ("Floor_220B", b220b_x,   0,         ROOM_220B_L,     ROOM_220B_W),
    ("Floor_220C", b220c_x,   b220c_y,   ROOM_220C_L,     ROOM_220C_W),
    ("Floor_220D", b220d_x,   0,         ROOM_220D_L,     ROOM_220D_W),
    ("Floor_220E", b220d_x,   b220e_y,   ROOM_220E_L,     ROOM_220E_W),
    ("Floor_221",  b221_x,    0,         ROOM_221_L,      ROOM_221_W),
]:
    f = make_box(name, x, y, -slab, lx, ly, slab)
    assign_material(f, mat_floor); floors.append(f)

# ── CEILINGS ─────────────────────────────────────────────────
ctile = ins(1)

for name, x, y, lx, ly in [
    ("Ceiling_220",  0,       0,       ROOM_220_LENGTH, ROOM_220_WIDTH),
    ("Ceiling_220A", 0,       b220a_y, ROOM_220A_L,     ROOM_220A_W),
    ("Ceiling_220B", b220b_x, 0,       ROOM_220B_L,     ROOM_220B_W),
    ("Ceiling_220C", b220c_x, b220c_y, ROOM_220C_L,     ROOM_220C_W),
    ("Ceiling_220D", b220d_x, 0,       ROOM_220D_L,     ROOM_220D_W),
]:
    c = make_box(name, x, y, CEILING_HT, lx, ly, ctile)
    assign_material(c, mat_ceiling); ceilings.append(c)

# ── WINDOWS ──────────────────────────────────────────────────
win_d  = ins(6)
win_ht = HEAD_HT - SILL_HT

for name, x, y, z, lx, ly, lz in [
    ("Window_W01_South",    ft(2),               -win_d,            SILL_HT, ft(20), win_d,  win_ht),
    ("Window_W02_West",     -win_d,               ft(7),            SILL_HT, win_d,  ft(4),  win_ht),
    ("Window_W03_220A",     ft(6),                b220a_y+ROOM_220A_W, SILL_HT, ft(8), win_d, win_ht),
    ("Window_W04_220C",     b220c_x + ft(2),      b220c_y - win_d,  SILL_HT, ft(4),  win_d,  win_ht),
    ("Window_W05_220D",     b220d_x + ft(1),      -win_d,           SILL_HT, ft(4),  win_d,  win_ht),
    ("Window_IW01_Interior",b220b_x+ROOM_220B_L,  b220c_y + ft(2),  SILL_HT, win_d,  ft(3),  ft(3)),
]:
    win = make_box(name, x, y, z, lx, ly, lz)
    assign_material(win, mat_window)
    win.display_type = 'WIRE'
    windows.append(win)

# ── DOORS ────────────────────────────────────────────────────
door_ht = ft(7)
ddep    = ins(2)

for name, x, y, z, lx, ly, lz in [
    ("Door_D01",     ROOM_220_LENGTH,      door_d01_y,      0, ddep,      DOOR_WIDTH_D01, door_ht),
    ("Door_D02_220A",ROOM_220_LENGTH,      b220a_y + ft(2), 0, ddep,      ft(3),          door_ht),
    ("Door_D03_220C",b220c_x + ft(3),      b220c_y,         0, ft(3),     ddep,           door_ht),
    ("Door_D04_220B",b220b_x+ROOM_220B_L,  ft(4),           0, ddep,      ft(3),          door_ht),
    ("Door_D05_220D",b220d_x,              ft(2),           0, GWB_THICK, ft(3),          door_ht),
    ("Door_D06_220E",b220d_x,              b220e_y + ft(1), 0, GWB_THICK, ft(3),          door_ht),
]:
    d = make_box(name, x, y, z, lx, ly, lz)
    assign_material(d, mat_door); doors.append(d)

# ── MEP PLACEHOLDERS ─────────────────────────────────────────
# Sink PL-01
m = make_box("Plumbing_PL01_Sink",
             b220b_x + ROOM_220B_L - ins(24), ROOM_220B_W - ins(8), ins(34),
             ins(24), ins(20), ins(6))
assign_material(m, mat_mep); mep.append(m)

# Raceway EL-02 in 220D
m = make_box("Electrical_EL02_Raceway",
             b220d_x + ft(1), ROOM_220D_W - ins(1), ins(35),
             ft(6), ins(1), ins(2))
assign_material(m, mat_mep); mep.append(m)

# HVAC Diffuser HV-01 in 220C
m = make_box("HVAC_HV01_Diffuser",
             b220c_x + ft(12), b220c_y + ft(10), CEILING_HT,
             ins(24), ins(24), ins(1))
assign_material(m, mat_mep); mep.append(m)

# ── ORGANIZE COLLECTIONS ─────────────────────────────────────
for obj, col_name in (
    [(w, "EC_Walls")    for w in walls]   +
    [(f, "EC_Floors")   for f in floors]  +
    [(c, "EC_Ceilings") for c in ceilings]+
    [(w, "EC_Windows")  for w in windows] +
    [(d, "EC_Doors")    for d in doors]   +
    [(m, "EC_MEP")      for m in mep]
):
    move_to_collection(obj, col_name)

# ── FRAME VIEW ───────────────────────────────────────────────
bpy.ops.object.select_all(action='SELECT')
for area in bpy.context.screen.areas:
    if area.type == 'VIEW_3D':
        with bpy.context.temp_override(area=area):
            bpy.ops.view3d.view_selected()
        break
bpy.ops.object.select_all(action='DESELECT')

# ── REPORT ───────────────────────────────────────────────────
print("=" * 50)
print("WHA Suite 220 — Base Model Complete")
print(f"  Walls:    {len(walls)}")
print(f"  Floors:   {len(floors)}")
print(f"  Ceilings: {len(ceilings)}")
print(f"  Windows:  {len(windows)}")
print(f"  Doors:    {len(doors)}")
print(f"  MEP:      {len(mep)}")
print("=" * 50)
print("NEXT STEPS:")
print("  1. Review model in 3D viewport")
print("  2. Adjust estimated dims as needed")
print("  3. File > Export > Industry Foundation Classes (.ifc)")
print("  4. Open IFC in Revit")
print("=" * 50)
