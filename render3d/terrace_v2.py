"""Medieval terrace, closer to the reference frame: 3D sunlit stone terrace and
parapet, painted backdrop far behind (pre-blurred: depth of field), 2D cut-out
characters and props standing in 3D and casting real shadows.
Run: python3.13 render3d/terrace_v2.py <asset_dir> <out.png> [samples]"""
import math
import sys
import time

import bpy

A, OUT_PNG = sys.argv[1], sys.argv[2]
SAMPLES = int(sys.argv[3]) if len(sys.argv) > 3 else 16


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


def mat(name, col, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(col)
    b.inputs["Roughness"].default_value = rough
    return m


def brick_mat(name, c1, c2, mortar, scale, row=0.45, width=0.9):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    b = nt.nodes["Principled BSDF"]
    br = nt.nodes.new("ShaderNodeTexBrick")
    for k, v in (("Color1", c1), ("Color2", c2), ("Mortar", mortar)):
        br.inputs[k].default_value = lin(v)
    br.inputs["Scale"].default_value = scale
    br.inputs["Mortar Size"].default_value = 0.02
    br.inputs["Brick Width"].default_value = width
    br.inputs["Row Height"].default_value = row
    tc = nt.nodes.new("ShaderNodeTexCoord")
    nt.links.new(tc.outputs["Object"], br.inputs["Vector"])
    nt.links.new(br.outputs["Color"], b.inputs["Base Color"])
    b.inputs["Roughness"].default_value = 0.9
    return m


def box(name, loc, scale, material, coll=None):
    bpy.ops.mesh.primitive_cube_add(location=loc)
    o = bpy.context.active_object
    o.name, o.scale = name, scale
    o.data.materials.append(material)
    if coll:
        move(o, coll)
    return o


def move(o, coll):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    coll.objects.link(o)


def card(name, png, loc, height, flat=False, cast=True, strength=1.0, coll=None):
    """Image card with alpha. Upright (facing -Y, toward the camera) or flat on the floor."""
    img = bpy.data.images.load(png)
    w, h = img.size
    bpy.ops.mesh.primitive_plane_add(location=loc, rotation=(0 if flat else math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.name = name
    o.scale = (height * w / h / 2, height / 2, 1)
    if not flat:
        o.location.z = loc[2] + height / 2
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], em.inputs["Color"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    o.visible_shadow = cast
    move(o, coll or CARDS)
    return o


bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
t0 = time.time()
CARDS = bpy.data.collections.new("cards")
PROPS = bpy.data.collections.new("props")
sc.collection.children.link(CARDS)
sc.collection.children.link(PROPS)

world = bpy.data.worlds.new("sky")
sc.world = world
world.use_nodes = True
world.node_tree.nodes["Background"].inputs["Color"].default_value = lin("#cfe0f2")
world.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.55

# warm stone terrace, parapet with coping, a gold line in the floor (as in the reference)
box("floor", (0, 2, -0.05), (14, 14, 0.05), brick_mat("floor", "#e8cfa8", "#d6b994", "#7d6152", 2.2, row=0.5, width=0.5), PROPS)
box("floor_line", (0, 0.5, 0.005), (0.05, 6, 0.005), mat("gold", "#e2b54a"), PROPS)
box("parapet", (0, 3.4, 0.55), (9, 0.25, 0.55), brick_mat("wall", "#efe3cf", "#e3d5bd", "#a8958a", 3.0), PROPS)
box("coping", (0, 3.4, 1.12), (9, 0.33, 0.06), mat("coping", "#f4e9d6"), PROPS)
box("bench", (0.9, 2.6, 0.45), (0.9, 0.35, 0.45), brick_mat("bench", "#d9c7aa", "#ccb898", "#9a8676", 3.0), PROPS)

# painted backdrop far away (blurred by the lens), banners, props, characters
card("backdrop", f"{A}/a_backdrop.png", (0, 30, -6), 30, cast=False, strength=1.0)
card("banner_red", f"{A}/a_banner_red.png", (-2.15, 2.9, 0), 4.6)
card("banner_teal", f"{A}/a_banner_teal.png", (2.25, 2.9, 0), 4.6)
card("barrel", f"{A}/a_barrel.png", (1.05, 1.5, 0), 2.3)
if not __import__("os").environ.get("NOCHARS"):  # NOCHARS=1: background plate only (2D characters go on top)
    card("king_red", f"{A}/king_red.png", (-1.05, 0.65, 0), 2.75)
    card("smith", f"{A}/smith.png", (0.05, 1.05, 0), 2.55)
    card("king_teal", f"{A}/king_teal.png", (1.3, 0.6, 0), 2.75)
card("anvil", f"{A}/a_anvil.png", (-0.35, -0.1, 0), 0.95)
card("table", f"{A}/a_table.png", (0, -2.25, 0.02), 2.2, flat=True, cast=False)

# warm low sun from behind-left: long shadows toward the camera-right, like the reference
bpy.ops.object.light_add(type="SUN", rotation=(math.radians(64), 0, math.radians(-145)))
sun = bpy.context.active_object
sun.data.energy = 4.0
sun.data.color = (1.0, 0.9, 0.76)
sun.data.angle = math.radians(4)

bpy.ops.object.camera_add(location=(0.05, -3.45, 1.45), rotation=(math.radians(84), 0, 0))
cam = bpy.context.active_object
cam.data.lens = 24
cam.data.dof.use_dof = True
cam.data.dof.focus_distance = 3.9
cam.data.dof.aperture_fstop = 1.2
sc.camera = cam

sc.render.resolution_x, sc.render.resolution_y = 720, 1280
sc.view_settings.view_transform = "Standard"
sc.render.use_freestyle = True
sc.render.line_thickness_mode = "ABSOLUTE"
sc.render.line_thickness = 1.4
fs = sc.view_layers[0].freestyle_settings
ls = fs.linesets[0] if len(fs.linesets) else fs.linesets.new("outlines")
if ls.linestyle is None:
    ls.linestyle = bpy.data.linestyles.new("outline")
ls.linestyle.color = (0.23, 0.16, 0.17)
ls.select_by_collection = True
ls.collection = PROPS
ls.collection_negation = "INCLUSIVE"
sc.render.engine = "CYCLES"
sc.cycles.device = "CPU"
sc.cycles.samples = SAMPLES
sc.cycles.use_denoising = True
sc.cycles.max_bounces = 4
sc.render.filepath = OUT_PNG
t1 = time.time()
bpy.ops.render.render(write_still=True)
print(f"scene build {t1 - t0:.1f}s, render {time.time() - t1:.1f}s ({SAMPLES} samples)")
