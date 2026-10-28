"""3D characters in the medieval reference style, built in Blender so they get real
light (highlight on one side, shadow on the other) and outlines like the reference.
Proportions follow style3 (pixel-measured): head : body : legs = 1 : 1.1 : 1.05, wide
flat egg head, bean body, THICK dark limbs, ball hands, rounded feet. The face
(eyes, brows, mouth, moustache) is the same 2D design as style3, applied as a decal.
Units: metres, head half-width R = 0.5."""
import math
import os
import sys

import bmesh
import bpy
import cairo

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "animator"))
import style3  # noqa: E402

R = 0.5
HEM, SHOULDER = 1.7 * R, 3.45 * R
HEAD_Z = SHOULDER + 0.62 * R
DARK = "#3a2a2c"


def lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c) + (1.0,)


_MATS = {}


def mat(col, rough=0.6, metal=0.0):
    key = (col, rough, metal)
    if key in _MATS:
        return _MATS[key]
    m = bpy.data.materials.new(f"m{col}")
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = lin(col)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    _MATS[key] = m
    return m


def _link(o, coll):
    for c in list(o.users_collection):
        c.objects.unlink(o)
    coll.objects.link(o)


def _sphere(name, loc, scale, col, coll, rough=0.6, metal=0.0, segs=48):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segs, ring_count=segs // 2, location=loc)
    o = bpy.context.active_object
    o.name, o.scale = name, scale
    o.data.materials.append(mat(col, rough, metal))
    bpy.ops.object.shade_smooth()
    _link(o, coll)
    return o


def _cyl(name, loc, r, depth, col, coll, rot=(0, 0, 0), rough=0.6, metal=0.0, verts=32, r2=None):
    if r2 is None:
        bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc, rotation=rot)
    else:
        bpy.ops.mesh.primitive_cone_add(vertices=verts, radius1=r, radius2=r2, depth=depth, location=loc, rotation=rot)
    o = bpy.context.active_object
    o.name = name
    o.data.materials.append(mat(col, rough, metal))
    bpy.ops.object.shade_smooth()
    _link(o, coll)
    return o


def _tube(name, pts, radius, col, coll):
    """Thick limb: a smooth bezier tube through pts (3D points)."""
    cu = bpy.data.curves.new(name, "CURVE")
    cu.dimensions = "3D"
    cu.bevel_depth = radius
    cu.bevel_resolution = 6
    cu.use_fill_caps = True
    sp = cu.splines.new("BEZIER")
    sp.bezier_points.add(len(pts) - 1)
    for bp, p in zip(sp.bezier_points, pts):
        bp.co = p
        bp.handle_left_type = bp.handle_right_type = "AUTO"
    o = bpy.data.objects.new(name, cu)
    o.data.materials.append(mat(col, 0.55))
    coll.objects.link(o)
    return o


def _shell_behind(name, z0, z1, r_top, r_bot, y_off, col, coll, side_bias=0.0):
    """Cape: back half of a flared cone, hanging from the shoulders to the floor."""
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=False, segments=40, radius1=r_bot, radius2=r_top, depth=z1 - z0)
    for v in list(bm.verts):
        if v.co.y < -0.02:
            bm.verts.remove(v)
    bmesh.ops.solidify(bm, geom=bm.faces[:], thickness=0.02)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    o = bpy.data.objects.new(name, me)
    o.location = (side_bias, y_off, (z0 + z1) / 2)
    o.data.materials.append(mat(col, 0.7))
    for p in me.polygons:
        p.use_smooth = True
    coll.objects.link(o)
    return o


def face_png(path, spec, expr, sweat=False):
    """Draw the style3 face (eyes, brows, mouth, moustache) on a transparent image."""
    size = 1024
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, size, int(size * 0.8))
    c = cairo.Context(s)
    r = size / 2 * 0.98
    ch = style3.Char3("#ffffff", mustache=spec.get("mustache"))
    style3._face3(c, size / 2, size * 0.4, r, 0.8 * r, 0.05 * r, expr, 0.0, 0.0, ch, sweat)
    s.write_to_png(path)
    return path


def _decal(name, png, loc, w, h, coll):
    img = bpy.data.images.load(png)
    bpy.ops.mesh.primitive_plane_add(location=loc, rotation=(math.radians(90), 0, 0))
    o = bpy.context.active_object
    o.name = name
    o.scale = (w / 2, h / 2, 1)
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = img
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = 0.6
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(tex.outputs["Alpha"], mix.inputs["Fac"])
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(bsdf.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs["Surface"])
    o.data.materials.append(m)
    o.visible_shadow = False
    # bend the decal around the head a little so it sits on the surface
    sw = o.modifiers.new("bend", "SIMPLE_DEFORM")
    sw.deform_method = "BEND"
    sw.deform_axis = "Y"
    sw.angle = math.radians(70)
    _link(o, coll)
    return o


ARM_POSES = {  # hand position relative to the shoulder (x outward, y toward camera -, z up)
    "down": (0.12, -0.02, -0.82),
    "belly": (-0.3, -0.3, -0.62),
    "hold": (-0.18, -0.38, -0.55),
    "hip": (0.25, -0.05, -0.55),
    "up": (0.25, -0.05, 0.7),
    "point": (0.85, -0.25, 0.05),
    "show": (0.5, -0.3, 0.25),
    "spear": (0.22, -0.15, -0.38),
    "bags": (0.08, -0.06, -0.88),
}


def build(name, spec, loc, expr="neutral", arms=("down", "down"), items=(None, None), rot_z=0.0,
          scale=1.0, coll=None, tmp="/tmp"):
    """Build a character; spec keys: body, cape, crown, beard, mustache, apron, helmet, outfit."""
    coll = coll or bpy.context.scene.collection
    root = bpy.data.objects.new(name, None)
    coll.objects.link(root)
    parts = bpy.data.collections.new(name + "_parts")
    coll.children.link(parts) if isinstance(coll, bpy.types.Collection) else None
    made = []
    body = spec["body"]
    # feet + THICK legs
    for side in (-1, 1):
        made.append(_sphere(f"{name}_foot{side}", (side * 0.12, -0.05, 0.05), (0.1, 0.15, 0.06), DARK, parts, 0.5))
        made.append(_tube(f"{name}_leg{side}", [(side * 0.1, 0, HEM + 0.05), (side * 0.11, -0.01, 0.4), (side * 0.12, -0.03, 0.07)],
                          0.038, DARK, parts))
    # cape behind
    if spec.get("cape"):
        made.append(_shell_behind(f"{name}_cape", 0.04, SHOULDER - 0.05, 0.26, 0.62, 0.05, spec["cape"], parts, -0.12))
    # bean body
    made.append(_sphere(f"{name}_body", (0, 0, (HEM + SHOULDER) / 2 - 0.02), (0.36, 0.27, (SHOULDER - HEM) / 2 + 0.06), body, parts, 0.65))
    if spec.get("apron"):  # apron wraps the front of the body; shirt shows at the shoulders
        made.append(_sphere(f"{name}_apron", (0, -0.025, (HEM + SHOULDER) / 2 - 0.06),
                            (0.37, 0.265, (SHOULDER - HEM) / 2 + 0.02), spec["apron"], parts, 0.75))
        made.append(_sphere(f"{name}_shirt", (0, 0.0, SHOULDER - 0.12), (0.33, 0.25, 0.16), body, parts, 0.65))
    # head
    hz = HEAD_Z
    made.append(_sphere(f"{name}_head", (0, 0, hz), (R, 0.42, 0.8 * R), "#fcf6ef", parts, 0.5))
    png = face_png(os.path.join(tmp, f"face_{name}_{expr}.png"), spec, expr, spec.get("sweat", False))
    made.append(_decal(f"{name}_face", png, (0, -0.415, hz), 2 * R * 0.98, 0.8 * R * 2 * 0.98, parts))
    # beards
    if spec.get("beard") == "goatee":
        made.append(_cyl(f"{name}_goatee", (0, -0.33, hz - 0.33), 0.06, 0.17, "#6b3a22", parts,
                         rot=(math.radians(180 - 15), 0, 0), r2=0.0, verts=16))
    elif spec.get("beard") == "bib":
        made.append(_sphere(f"{name}_beard", (0, -0.27, hz - 0.28), (0.27, 0.16, 0.24), "#f4f1ec", parts, 0.8))
    elif spec.get("beard") == "long":
        made.append(_cyl(f"{name}_beard", (0, -0.28, hz - 0.55), 0.24, 0.65, "#f4f1ec", parts,
                         rot=(math.radians(180), 0, 0), r2=0.02, verts=24))
    # crowns / helmet
    top = hz + 0.8 * R * 0.72
    if spec.get("crown") == "gold":
        made.append(_cyl(f"{name}_crown", (0, 0, top), 0.36, 0.13, "#f2c443", parts, rough=0.3, metal=0.9, verts=48))
        for k in range(5):
            a = math.radians(-150 + k * 30)
            x, y = 0.34 * math.cos(a), 0.34 * math.sin(a) * 0.75
            made.append(_cyl(f"{name}_spike{k}", (x, y, top + 0.15), 0.06, 0.2, "#f2c443", parts, rough=0.3, metal=0.9, r2=0.0, verts=12))
            made.append(_sphere(f"{name}_ball{k}", (x, y, top + 0.26), (0.035, 0.035, 0.035), "#ffffff", parts, 0.3, segs=16))
        for k, gc in enumerate(("#d64a3a", "#3f6fd6", "#d64a3a")):
            a = math.radians(-120 + k * 30)
            made.append(_sphere(f"{name}_gem{k}", (0.37 * math.cos(a), 0.37 * math.sin(a) * 0.75, top), (0.03, 0.02, 0.03), gc, parts, 0.2, segs=16))
    elif spec.get("crown") == "silver":
        made.append(_cyl(f"{name}_crown", (0, 0, top), 0.38, 0.12, "#d9dde4", parts, rough=0.3, metal=0.9, verts=48))
        for k in range(3):
            a = math.radians(-130 + k * 40)
            x, y = 0.3 * math.cos(a), 0.3 * math.sin(a) * 0.75
            made.append(_sphere(f"{name}_bump{k}", (x, y, top + 0.13), (0.13, 0.08, 0.15), "#d9dde4", parts, 0.3, 0.9, segs=24))
            made.append(_sphere(f"{name}_ball{k}", (x, y, top + 0.29), (0.04, 0.04, 0.04), "#ffffff", parts, 0.3, segs=16))
            made.append(_sphere(f"{name}_gem{k}", (0.39 * math.cos(a), 0.39 * math.sin(a) * 0.75, top), (0.03, 0.02, 0.03), "#3fbfb0", parts, 0.2, segs=16))
    if spec.get("helmet"):
        made.append(_sphere(f"{name}_helmet", (0, 0, hz + 0.05), (R * 1.04, 0.44, 0.8 * R * 0.9), "#c9ced8", parts, 0.3, 0.8))
    # THICK arms + ball hands (+ items)
    for i, side in enumerate((-1, 1)):
        sx, sz = side * 0.3, SHOULDER - 0.12
        dx, dy, dz = ARM_POSES.get(arms[i], ARM_POSES["down"])
        hx, hy, hz2 = sx + side * dx, dy - 0.05, sz + dz
        ex, ey, ez = (sx + hx) / 2 + side * 0.1, (dy - 0.05) / 2, (sz + hz2) / 2
        made.append(_tube(f"{name}_arm{side}", [(sx, -0.02, sz), (ex, ey, ez), (hx, hy, hz2)], 0.034, DARK, parts))
        made.append(_sphere(f"{name}_hand{side}", (hx, hy, hz2), (0.065, 0.065, 0.065), DARK, parts, 0.5, segs=24))
        it = items[i]
        if it == "spear":
            made.append(_cyl(f"{name}_shaft", (hx, hy - 0.02, hz2 + 0.35), 0.022, 2.2, "#b07a3a", parts))
            made.append(_cyl(f"{name}_tip", (hx, hy - 0.02, hz2 + 1.55), 0.06, 0.26, "#d9dde4", parts, rough=0.25, metal=0.9, r2=0.0, verts=16))
        elif it == "shield":
            rot = (math.radians(90), 0, 0)
            made.append(_cyl(f"{name}_sh_rim", (hx + side * 0.05, hy - 0.12, hz2 + 0.1), 0.42, 0.05, "#f2c443", parts, rot=rot, rough=0.3, metal=0.8, verts=48))
            made.append(_cyl(f"{name}_sh_ring", (hx + side * 0.05, hy - 0.15, hz2 + 0.1), 0.36, 0.03, "#3fbfb0", parts, rot=rot, verts=48))
            made.append(_cyl(f"{name}_sh_face", (hx + side * 0.05, hy - 0.17, hz2 + 0.1), 0.26, 0.03, "#d9dde4", parts, rot=rot, rough=0.25, metal=0.9, verts=48))
            made.append(_sphere(f"{name}_sh_boss", (hx + side * 0.05, hy - 0.19, hz2 + 0.1), (0.09, 0.05, 0.09), "#eef1f5", parts, 0.2, 0.9))
        if arms[i] == "bags":
            made.append(_sphere(f"{name}_bag{side}", (hx, hy - 0.02, hz2 - 0.13), (0.14, 0.12, 0.13), "#e8c477", parts, 0.8))
    for o in made:
        o.parent = root
    root.location = loc
    root.rotation_euler = (0, 0, rot_z)
    root.scale = (scale, scale, scale)
    return root, parts


KING_RED = dict(body="#e8452f", cape="#a8424a", crown="gold", beard="goatee")
KING_TEAL = dict(body="#2fb3a8", cape="#25807d", crown="silver", beard="bib")
SMITH = dict(body="#8d8f97", apron="#d38a35", mustache="handlebar")
