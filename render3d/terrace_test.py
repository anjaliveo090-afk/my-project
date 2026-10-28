"""3D test of the medieval terrace (reference frame 1) in Blender.
2D characters stand in the 3D set as cut-out cards that cast real shadows.
Run: python3.13 render3d/terrace_test.py <cutout_dir> <out.png> [cycles|eevee] [samples]"""
import math
import sys
import time

import bpy

CUT, OUT_PNG = sys.argv[1], sys.argv[2]
ENGINE = sys.argv[3] if len(sys.argv) > 3 else "cycles"
SAMPLES = int(sys.argv[4]) if len(sys.argv) > 4 else 24


def hexrgb(h, a=1.0):
    h = h.lstrip("#")
    srgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in srgb]
    return (*lin, a)


def mat(name, col, rough=0.8, metal=0.0, emit=0.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = hexrgb(col)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    if emit:
        b.inputs["Emission Color"].default_value = hexrgb(col)
        b.inputs["Emission Strength"].default_value = emit
    return m


def brick_mat(name, c1, c2, mortar, scale=3.0):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    br = nt.nodes.new("ShaderNodeTexBrick")
    br.inputs["Color1"].default_value = hexrgb(c1)
    br.inputs["Color2"].default_value = hexrgb(c2)
    br.inputs["Mortar"].default_value = hexrgb(mortar)
    br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = 0.025
    br.inputs["Brick Width"].default_value = 0.9
    br.inputs["Row Height"].default_value = 0.45
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.9
    return m


def add(obj_op, name, loc, scale=(1, 1, 1), rot=(0, 0, 0), material=None, **kw):
    obj_op(location=loc, rotation=rot, **kw)
    o = bpy.context.active_object
    o.name = name
    o.scale = scale
    if material:
        o.data.materials.append(material)
    bpy.ops.object.shade_smooth() if obj_op in (bpy.ops.mesh.primitive_uv_sphere_add, bpy.ops.mesh.primitive_cylinder_add) else None
    return o


def card(name, png, loc, height):
    """Upright cut-out card facing the camera, alpha from the PNG, emissive so the
    flat 2D colours stay exact; still casts shadows on the 3D floor."""
    img = bpy.data.images.load(png)
    w, h = img.size
    bpy.ops.mesh.primitive_plane_add(location=loc, rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.name = name
    o.scale = (height * w / h / 2, height / 2, 1)
    o.location.z = loc[2] + height / 2
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    m.blend_method = "HASHED" if hasattr(m, "blend_method") else None
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    em = nt.nodes.new("ShaderNodeEmission")
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    em.inputs["Strength"].default_value = 1.0
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    CARDS.objects.link(o)
    bpy.context.scene.collection.objects.unlink(o)
    return o


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
t0 = time.time()
CARDS = bpy.data.collections.new("cards")  # 2D cut-outs: no 3D outlines around their cards
sc.collection.children.link(CARDS)
PROPS = bpy.data.collections.new("props")
sc.collection.children.link(PROPS)


def to_props(*names):
    for n in names:
        for o in [o for o in bpy.data.objects if o.name.startswith(n)]:
            for c in list(o.users_collection):
                c.objects.unlink(o)
            PROPS.objects.link(o)

# world: sky gradient + ambient
world = bpy.data.worlds.new("sky")
sc.world = world
world.use_nodes = True
wn = world.node_tree
bg = wn.nodes["Background"]
grad = wn.nodes.new("ShaderNodeTexGradient")
mapn = wn.nodes.new("ShaderNodeMapping")
tc = wn.nodes.new("ShaderNodeTexCoord")
ramp = wn.nodes.new("ShaderNodeValToRGB")
mapn.inputs["Rotation"].default_value = (0, math.radians(90), 0)
wn.links.new(tc.outputs["Generated"], mapn.inputs["Vector"])
wn.links.new(mapn.outputs["Vector"], grad.inputs["Vector"])
wn.links.new(grad.outputs["Fac"], ramp.inputs["Fac"])
ramp.color_ramp.elements[0].color = hexrgb("#a9cdf3")
ramp.color_ramp.elements[1].color = hexrgb("#5f88d0")
wn.links.new(ramp.outputs["Color"], bg.inputs["Color"])
bg.inputs["Strength"].default_value = 1.0

# terrace floor, parapet
add(bpy.ops.mesh.primitive_plane_add, "floor", (0, 2, 0), (12, 12, 1), material=brick_mat("floor", "#dcc3a5", "#cdb293", "#8a777b", 9.0))
add(bpy.ops.mesh.primitive_cube_add, "parapet", (0, 4.2, 0.55), (9, 0.25, 0.55), material=brick_mat("wall", "#eadcc6", "#ddcdb4", "#a8958a", 7.0))
add(bpy.ops.mesh.primitive_cube_add, "coping", (0, 4.2, 1.13), (9, 0.32, 0.05), material=mat("coping", "#f2e6d2"))

# backdrop: hills, mountains with snow, castles, trees, clouds
green = mat("hill", "#86b86c")
add(bpy.ops.mesh.primitive_plane_add, "land", (0, 40, -0.5), (80, 40, 1), material=green)
for i, (x, y, s) in enumerate(((-14, 60, 9), (2, 70, 12), (16, 62, 10), (-30, 75, 13), (30, 78, 12))):
    add(bpy.ops.mesh.primitive_cone_add, f"mtn{i}", (x, y, s * 0.9 - 1), (s, s * 0.6, s * 0.9), material=mat(f"m{i}", "#8aa4d6"), vertices=6)
    add(bpy.ops.mesh.primitive_cone_add, f"snow{i}", (x, y, s * 1.45 - 1), (s * 0.31, s * 0.19, s * 0.29), material=mat(f"s{i}", "#f4f6fb"), vertices=6)
for i, (x, y, roof) in enumerate(((-9, 30, "#c9403a"), (10, 32, "#1f8a92"))):
    wallm = mat(f"cw{i}", "#eeeae4")
    add(bpy.ops.mesh.primitive_cube_add, f"keep{i}", (x, y, 1.5), (1.6, 1.0, 1.5), material=wallm)
    for j, dx in enumerate((-1.8, 0, 1.8)):
        h = 4.2 if j == 1 else 3.2
        add(bpy.ops.mesh.primitive_cylinder_add, f"tw{i}{j}", (x + dx, y, h / 2), (0.45, 0.45, h / 2), material=wallm)
        add(bpy.ops.mesh.primitive_cone_add, f"rf{i}{j}", (x + dx, y, h + 0.7), (0.6, 0.6, 0.7), material=mat(f"r{i}{j}", roof))
for i in range(40):
    x = -26 + (i * 7.3) % 52
    y = 14 + (i * 5.1) % 20
    add(bpy.ops.mesh.primitive_cone_add, f"pine{i}", (x, y, 1.0), (0.7, 0.7, 1.4), material=mat(f"pn{i}", "#3f7f55"))
cloudm = mat("cloud", "#ffffff", emit=0.35)
for i, (x, y, z, s) in enumerate(((-8, 45, 16, 3.0), (7, 50, 20, 3.6), (14, 40, 12, 2.4))):
    for k, (dx, dz, ss) in enumerate(((-1.4, 0, 1.0), (0, 0.6, 1.3), (1.4, 0.1, 1.0), (0.6, -0.4, 0.9))):
        add(bpy.ops.mesh.primitive_uv_sphere_add, f"cl{i}{k}", (x + dx * s, y, z + dz * s), (ss * s, ss * s * 0.8, ss * s * 0.8), material=cloudm)

# banners
for x, col in ((-2.2, "#c9403a"), (2.2, "#1f8a92")):
    add(bpy.ops.mesh.primitive_cylinder_add, "pole", (x, 3.6, 2.4), (0.04, 0.04, 2.4), material=mat("wood", "#6b4a2a"))
    add(bpy.ops.mesh.primitive_plane_add, "flag", (x + 0.55 * (1 if x < 0 else -1), 3.58, 3.9), (0.5, 1.0, 1), (math.radians(90), 0, 0), material=mat("flag" + col, col))

# props: anvil on stump, barrel with spears, war table in the foreground
wood = mat("stump", "#a26b35")
iron = mat("iron", "#9aa0aa", rough=0.35, metal=0.8)
add(bpy.ops.mesh.primitive_cylinder_add, "stump", (-0.35, -0.5, 0.35), (0.38, 0.38, 0.35), material=wood)
add(bpy.ops.mesh.primitive_cube_add, "anvil_base", (-0.35, -0.5, 0.82), (0.18, 0.14, 0.12), material=iron)
add(bpy.ops.mesh.primitive_cube_add, "anvil_top", (-0.27, -0.5, 1.0), (0.48, 0.18, 0.08), material=iron)
add(bpy.ops.mesh.primitive_cylinder_add, "barrel", (1.3, 1.5, 0.45), (0.38, 0.38, 0.45), material=mat("barrel", "#9a6a3e"))
for k, dx in enumerate((-0.12, 0.0, 0.12)):
    add(bpy.ops.mesh.primitive_cylinder_add, f"sp{k}", (1.3 + dx, 1.5, 1.4), (0.025, 0.025, 1.0), material=wood)
    add(bpy.ops.mesh.primitive_cone_add, f"tip{k}", (1.3 + dx, 1.5, 2.55), (0.07, 0.07, 0.18), material=iron)
add(bpy.ops.mesh.primitive_cylinder_add, "table_red", (0, -2.9, 0.12), (0.9, 0.9, 0.05), material=mat("tred", "#c9403a"), vertices=64)
add(bpy.ops.mesh.primitive_cylinder_add, "table_rim", (0, -2.9, 0.1), (0.98, 0.98, 0.05), material=mat("trim", "#e2b54a"), vertices=64)

# characters as cut-out cards
card("king_red", f"{CUT}/king_red.png", (-1.15, 0.7, 0), 2.55)
card("smith", f"{CUT}/smith.png", (0.1, 1.2, 0), 2.4)
card("king_teal", f"{CUT}/king_teal.png", (1.3, 0.7, 0), 2.55)
to_props("stump", "anvil", "barrel", "sp", "tip", "table", "pole", "flag", "parapet", "coping")

# light: low warm sun from behind-left for long shadows, soft fill from the sky
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(62), 0, math.radians(-150)))
sun = bpy.context.active_object
sun.data.energy = 3.2
sun.data.color = (1.0, 0.93, 0.82)
sun.data.angle = math.radians(3)

# camera: eye level, slightly above, shallow depth of field like the reference
bpy.ops.object.camera_add(location=(0, -4.2, 1.6), rotation=(math.radians(86), 0, 0))
cam = bpy.context.active_object
cam.data.lens = 26
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 4.5
cam.data.dof.aperture_fstop = 0.9
sc.camera = cam

sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.render.film_transparent = False
sc.view_settings.view_transform = "Standard"
sc.render.use_freestyle = True
sc.render.line_thickness_mode = "ABSOLUTE"
sc.render.line_thickness = 1.6
fs = sc.view_layers[0].freestyle_settings
lset = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("outlines")
if lset.linestyle is None:
    lset.linestyle = bpy.data.linestyles.new("outline")
lset.linestyle.color = (0.18, 0.13, 0.15)
lset.select_by_collection = True
lset.collection = PROPS  # outlines only on near props; the blurred backdrop stays soft
lset.collection_negation = "INCLUSIVE"
if ENGINE == "eevee":
    sc.render.engine = "BLENDER_EEVEE"
    sc.eevee.taa_render_samples = SAMPLES
else:
    sc.render.engine = "CYCLES"
    sc.cycles.device = "CPU"
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 4
sc.render.filepath = OUT_PNG
t1 = time.time()
bpy.ops.render.render(write_still=True)
print(f"scene build {t1 - t0:.1f}s, render {time.time() - t1:.1f}s ({ENGINE}, {SAMPLES} samples)")
