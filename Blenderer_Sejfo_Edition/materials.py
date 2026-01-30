import bpy
import mathutils
import os
import typing

# MARK: - Glass - Default
glass___default = bpy.data.materials.new(name = "Glass - Default")
if bpy.app.version < (5, 0, 0):
    glass___default.use_nodes = True


glass___default.alpha_threshold = 0.5
glass___default.line_priority = 0
glass___default.max_vertex_displacement = 0.0
glass___default.metallic = 0.0
glass___default.paint_active_slot = 0
glass___default.paint_clone_slot = 0
glass___default.pass_index = 0
glass___default.refraction_depth = 0.0
glass___default.roughness = 0.4000000059604645
glass___default.show_transparent_back = True
glass___default.specular_intensity = 0.5
glass___default.use_backface_culling = False
glass___default.use_backface_culling_lightprobe_volume = False
glass___default.use_backface_culling_shadow = False
glass___default.use_preview_world = False
glass___default.use_raytrace_refraction = True
glass___default.use_screen_refraction = True
glass___default.use_sss_translucency = False
glass___default.use_thickness_from_shadow = False
glass___default.use_transparency_overlap = True
glass___default.use_transparent_shadow = True
glass___default.blend_method = 'BLEND'
glass___default.displacement_method = 'BUMP'
glass___default.preview_render_type = 'SHADERBALL'
glass___default.surface_render_method = 'BLENDED'
glass___default.thickness_mode = 'SPHERE'
glass___default.volume_intersection_method = 'FAST'
glass___default.specular_color = (1.0, 1.0, 1.0)
glass___default.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___default.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_glass(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___default.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.05958548188209534
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 0.07727272808551788
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 1.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output.001
    material_output_001 = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output_001.name = "Material Output.001"
    material_output_001.is_active_output = False
    material_output_001.target = 'CYCLES'
    # Displacement
    material_output_001.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Glass BSDF
    glass_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf.name = "Glass BSDF"
    glass_bsdf.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    # Roughness
    glass_bsdf.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf.inputs[6].default_value = 1.3300000429153442

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Glass BSDF.001
    glass_bsdf_001 = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf_001.name = "Glass BSDF.001"
    glass_bsdf_001.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf_001.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    # Roughness
    glass_bsdf_001.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf_001.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf_001.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf_001.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf_001.inputs[6].default_value = 1.3300000429153442

    # Node Fresnel
    fresnel = shader_nodetree.nodes.new("ShaderNodeFresnel")
    fresnel.name = "Fresnel"
    # IOR
    fresnel.inputs[0].default_value = 54.599998474121094
    # Normal
    fresnel.inputs[1].default_value = (0.0, 0.0, 0.0)

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Mix Shader.001
    mix_shader_001 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_001.name = "Mix Shader.001"
    # Fac
    mix_shader_001.inputs[0].default_value = 1.0

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Principled BSDF"].location = (-141.76763916015625, 155.83154296875)
    shader_nodetree.nodes["Material Output.001"].location = (654.529052734375, 644.0345458984375)
    shader_nodetree.nodes["Glass BSDF"].location = (184.10842895507812, 691.1384887695312)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (161.25888061523438, -404.6147766113281)
    shader_nodetree.nodes["Glass BSDF.001"].location = (168.1807861328125, -232.54254150390625)
    shader_nodetree.nodes["Fresnel"].location = (176.09983825683594, -115.24836730957031)
    shader_nodetree.nodes["Mix Shader"].location = (393.1517333984375, -214.63412475585938)
    shader_nodetree.nodes["Mix Shader.001"].location = (516.3298950195312, 212.0856475830078)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output.001"].width  = 140.0
    shader_nodetree.nodes["Material Output.001"].height = 100.0

    shader_nodetree.nodes["Glass BSDF"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Glass BSDF.001"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF.001"].height = 100.0

    shader_nodetree.nodes["Fresnel"].width  = 140.0
    shader_nodetree.nodes["Fresnel"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Mix Shader.001"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.001"].height = 100.0


    # Initialize shader_nodetree links

    # glass_bsdf.BSDF -> material_output_001.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output.001"].inputs[0]
    )
    # value.Value -> material_output_001.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output.001"].inputs[3]
    )
    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # glass_bsdf_001.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF.001"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # fresnel.Factor -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Fresnel"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # principled_bsdf.BSDF -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[1]
    )
    # mix_shader.Shader -> mix_shader_001.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.001"].inputs[2]
    )
    # mix_shader_001.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.001"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

# MARK: - Aluminium - Black Paint
aluminium___black_paint = bpy.data.materials.new(name = "Aluminium - Black Paint")
if bpy.app.version < (5, 0, 0):
    aluminium___black_paint.use_nodes = True


aluminium___black_paint.alpha_threshold = 0.5
aluminium___black_paint.line_priority = 0
aluminium___black_paint.max_vertex_displacement = 0.0
aluminium___black_paint.metallic = 0.0
aluminium___black_paint.paint_active_slot = 0
aluminium___black_paint.paint_clone_slot = 0
aluminium___black_paint.pass_index = 0
aluminium___black_paint.refraction_depth = 0.0
aluminium___black_paint.roughness = 0.4000000059604645
aluminium___black_paint.show_transparent_back = True
aluminium___black_paint.specular_intensity = 0.5
aluminium___black_paint.use_backface_culling = False
aluminium___black_paint.use_backface_culling_lightprobe_volume = False
aluminium___black_paint.use_backface_culling_shadow = False
aluminium___black_paint.use_preview_world = False
aluminium___black_paint.use_raytrace_refraction = False
aluminium___black_paint.use_screen_refraction = False
aluminium___black_paint.use_sss_translucency = False
aluminium___black_paint.use_thickness_from_shadow = False
aluminium___black_paint.use_transparency_overlap = True
aluminium___black_paint.use_transparent_shadow = True
aluminium___black_paint.blend_method = 'HASHED'
aluminium___black_paint.displacement_method = 'BUMP'
aluminium___black_paint.preview_render_type = 'SHADERBALL'
aluminium___black_paint.surface_render_method = 'DITHERED'
aluminium___black_paint.thickness_mode = 'SPHERE'
aluminium___black_paint.volume_intersection_method = 'FAST'
aluminium___black_paint.specular_color = (1.0, 1.0, 1.0)
aluminium___black_paint.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
aluminium___black_paint.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_1(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = aluminium___black_paint.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.34331512451171875, 0.34331512451171875, 0.34331512451171875, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.20000000298023224
    # IOR
    principled_bsdf.inputs[3].default_value = 1.1978000402450562
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 1.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.1409090906381607
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.1978000402450562
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (0.0, 0.0, 0.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (10.0, 300.0)
    shader_nodetree.nodes["Material Output"].location = (300.0, 300.0)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

# MARK: Aluminium - Anodized
aluminium___anodized = bpy.data.materials.new(name = "Aluminium - Anodized")
if bpy.app.version < (5, 0, 0):
    aluminium___anodized.use_nodes = True


aluminium___anodized.alpha_threshold = 0.5
aluminium___anodized.line_priority = 0
aluminium___anodized.max_vertex_displacement = 0.0
aluminium___anodized.metallic = 0.0
aluminium___anodized.paint_active_slot = 0
aluminium___anodized.paint_clone_slot = 0
aluminium___anodized.pass_index = 0
aluminium___anodized.refraction_depth = 0.0
aluminium___anodized.roughness = 0.4000000059604645
aluminium___anodized.show_transparent_back = True
aluminium___anodized.specular_intensity = 0.5
aluminium___anodized.use_backface_culling = False
aluminium___anodized.use_backface_culling_lightprobe_volume = False
aluminium___anodized.use_backface_culling_shadow = False
aluminium___anodized.use_preview_world = False
aluminium___anodized.use_raytrace_refraction = False
aluminium___anodized.use_screen_refraction = False
aluminium___anodized.use_sss_translucency = False
aluminium___anodized.use_thickness_from_shadow = False
aluminium___anodized.use_transparency_overlap = True
aluminium___anodized.use_transparent_shadow = True
aluminium___anodized.blend_method = 'HASHED'
aluminium___anodized.displacement_method = 'BUMP'
aluminium___anodized.preview_render_type = 'SHADERBALL'
aluminium___anodized.surface_render_method = 'DITHERED'
aluminium___anodized.thickness_mode = 'SPHERE'
aluminium___anodized.volume_intersection_method = 'FAST'
aluminium___anodized.specular_color = (1.0, 1.0, 1.0)
aluminium___anodized.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
aluminium___anodized.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_2(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = aluminium___anodized.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.5363636612892151
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.027272701263427734
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.09999999403953552
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Noise Texture
    noise_texture = shader_nodetree.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 66.5
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Color Ramp
    color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    # Initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.0
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.15622200071811676, 0.15622200071811676, 0.15622200071811676, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(1.0)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (0.4997302293777466, 0.4997302293777466, 0.4997302293777466, 1.0)


    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MIX'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 0.5
    # B_Color
    mix.inputs[7].default_value = (0.5, 0.5, 0.5, 1.0)

    # Node Mix.001
    mix_001 = shader_nodetree.nodes.new("ShaderNodeMix")
    mix_001.name = "Mix.001"
    mix_001.blend_type = 'SCREEN'
    mix_001.clamp_factor = True
    mix_001.clamp_result = False
    mix_001.data_type = 'RGBA'
    mix_001.factor_mode = 'UNIFORM'
    # Factor_Float
    mix_001.inputs[0].default_value = 0.18333333730697632
    # A_Color
    mix_001.inputs[6].default_value = (0.3636070191860199, 0.3636070191860199, 0.3636070191860199, 1.0)

    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (378.696533203125, 236.2528076171875)
    shader_nodetree.nodes["Material Output"].location = (668.696533203125, 236.2528076171875)
    shader_nodetree.nodes["Noise Texture"].location = (-596.4815673828125, 214.90475463867188)
    shader_nodetree.nodes["Mapping"].location = (-776.4816284179688, 174.90475463867188)
    shader_nodetree.nodes["Texture Coordinate"].location = (-956.4816284179688, 174.90475463867188)
    shader_nodetree.nodes["Color Ramp"].location = (-237.798828125, 55.9814567565918)
    shader_nodetree.nodes["Mix"].location = (89.97578430175781, 111.14208221435547)
    shader_nodetree.nodes["Mix.001"].location = (-137.54478454589844, 321.6379089355469)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Noise Texture"].width  = 140.0
    shader_nodetree.nodes["Noise Texture"].height = 100.0

    shader_nodetree.nodes["Mapping"].width  = 140.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Mix.001"].width  = 140.0
    shader_nodetree.nodes["Mix.001"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # mapping.Vector -> noise_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Noise Texture"].inputs[0]
    )
    # noise_texture.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # texture_coordinate.Object -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[3],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )
    # mix.Result -> principled_bsdf.Roughness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF"].inputs[2]
    )
    # color_ramp.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # mix_001.Result -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix.001"].outputs[2],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # noise_texture.Color -> mix_001.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Mix.001"].inputs[7]
    )

    return shader_nodetree

# MARK: - Aluminium - Polished
aluminium___polished = bpy.data.materials.new(name = "Aluminium - Polished")
if bpy.app.version < (5, 0, 0):
    aluminium___polished.use_nodes = True


aluminium___polished.alpha_threshold = 0.5
aluminium___polished.line_priority = 0
aluminium___polished.max_vertex_displacement = 0.0
aluminium___polished.metallic = 0.0
aluminium___polished.paint_active_slot = 0
aluminium___polished.paint_clone_slot = 0
aluminium___polished.pass_index = 0
aluminium___polished.refraction_depth = 0.0
aluminium___polished.roughness = 0.4000000059604645
aluminium___polished.show_transparent_back = True
aluminium___polished.specular_intensity = 0.5
aluminium___polished.use_backface_culling = False
aluminium___polished.use_backface_culling_lightprobe_volume = False
aluminium___polished.use_backface_culling_shadow = False
aluminium___polished.use_preview_world = False
aluminium___polished.use_raytrace_refraction = False
aluminium___polished.use_screen_refraction = False
aluminium___polished.use_sss_translucency = False
aluminium___polished.use_thickness_from_shadow = False
aluminium___polished.use_transparency_overlap = True
aluminium___polished.use_transparent_shadow = True
aluminium___polished.blend_method = 'HASHED'
aluminium___polished.displacement_method = 'BUMP'
aluminium___polished.preview_render_type = 'SHADERBALL'
aluminium___polished.surface_render_method = 'DITHERED'
aluminium___polished.thickness_mode = 'SPHERE'
aluminium___polished.volume_intersection_method = 'FAST'
aluminium___polished.specular_color = (1.0, 1.0, 1.0)
aluminium___polished.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
aluminium___polished.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_3(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = aluminium___polished.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.34331512451171875, 0.34331512451171875, 0.34331512451171875, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.20000000298023224
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (10.0, 300.0)
    shader_nodetree.nodes["Material Output"].location = (300.0, 300.0)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

# MARK: Aluminium - Profiles
aluminium___profiles = bpy.data.materials.new(name = "Aluminium - Profiles")
if bpy.app.version < (5, 0, 0):
    aluminium___profiles.use_nodes = True


aluminium___profiles.alpha_threshold = 0.5
aluminium___profiles.line_priority = 0
aluminium___profiles.max_vertex_displacement = 0.0
aluminium___profiles.metallic = 0.0
aluminium___profiles.paint_active_slot = 0
aluminium___profiles.paint_clone_slot = 0
aluminium___profiles.pass_index = 0
aluminium___profiles.refraction_depth = 0.0
aluminium___profiles.roughness = 0.4000000059604645
aluminium___profiles.show_transparent_back = True
aluminium___profiles.specular_intensity = 0.5
aluminium___profiles.use_backface_culling = False
aluminium___profiles.use_backface_culling_lightprobe_volume = False
aluminium___profiles.use_backface_culling_shadow = False
aluminium___profiles.use_preview_world = False
aluminium___profiles.use_raytrace_refraction = False
aluminium___profiles.use_screen_refraction = False
aluminium___profiles.use_sss_translucency = False
aluminium___profiles.use_thickness_from_shadow = False
aluminium___profiles.use_transparency_overlap = True
aluminium___profiles.use_transparent_shadow = True
aluminium___profiles.blend_method = 'HASHED'
aluminium___profiles.displacement_method = 'BUMP'
aluminium___profiles.preview_render_type = 'SHADERBALL'
aluminium___profiles.surface_render_method = 'DITHERED'
aluminium___profiles.thickness_mode = 'SPHERE'
aluminium___profiles.volume_intersection_method = 'FAST'
aluminium___profiles.specular_color = (1.0, 1.0, 1.0)
aluminium___profiles.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
aluminium___profiles.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_4(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = aluminium___profiles.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.699999988079071
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node RGB
    rgb = shader_nodetree.nodes.new("ShaderNodeRGB")
    rgb.name = "RGB"

    rgb.outputs[0].default_value = (0.5028774738311768, 0.5028774738311768, 0.5028774738311768, 1.0)
    # Node Mix
    mix = shader_nodetree.nodes.new("ShaderNodeMix")
    mix.name = "Mix"
    mix.blend_type = 'MULTIPLY'
    mix.clamp_factor = True
    mix.clamp_result = False
    mix.data_type = 'RGBA'
    mix.factor_mode = 'UNIFORM'
    # Factor_Float
    mix.inputs[0].default_value = 0.25833332538604736

    # Node Noise Texture
    noise_texture = shader_nodetree.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # Scale
    noise_texture.inputs[2].default_value = 50.099998474121094
    # Detail
    noise_texture.inputs[3].default_value = 4.399999618530273
    # Roughness
    noise_texture.inputs[4].default_value = 1.0
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 32.69999694824219, 0.1000000536441803)

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Color Ramp
    color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    # Initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.3090909421443939
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.6727274060249329)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (56.17237854003906, 363.8027038574219)
    shader_nodetree.nodes["Material Output"].location = (522.3564453125, 321.8752136230469)
    shader_nodetree.nodes["RGB"].location = (-459.73187255859375, 498.7275085449219)
    shader_nodetree.nodes["Mix"].location = (-124.0, 377.8094482421875)
    shader_nodetree.nodes["Noise Texture"].location = (-703.7507934570312, 272.7008056640625)
    shader_nodetree.nodes["Mapping"].location = (-883.7507934570312, 232.7008056640625)
    shader_nodetree.nodes["Texture Coordinate"].location = (-1063.750732421875, 232.7008056640625)
    shader_nodetree.nodes["Color Ramp"].location = (-487.9035339355469, 272.0517272949219)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["RGB"].width  = 140.0
    shader_nodetree.nodes["RGB"].height = 100.0

    shader_nodetree.nodes["Mix"].width  = 140.0
    shader_nodetree.nodes["Mix"].height = 100.0

    shader_nodetree.nodes["Noise Texture"].width  = 140.0
    shader_nodetree.nodes["Noise Texture"].height = 100.0

    shader_nodetree.nodes["Mapping"].width  = 140.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0


    # Initialize shader_nodetree links

    # mix.Result -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix"].outputs[2],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # rgb.Color -> mix.A
    shader_nodetree.links.new(
        shader_nodetree.nodes["RGB"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[6]
    )
    # mapping.Vector -> noise_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Noise Texture"].inputs[0]
    )
    # texture_coordinate.Generated -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[0],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )
    # noise_texture.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # color_ramp.Color -> mix.B
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Mix"].inputs[7]
    )
    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

# MARK: - Cast Iron - Burgundy Coat
cast_iron___burgundy_coat = bpy.data.materials.new(name = "Cast Iron - Burgundy Coat")
if bpy.app.version < (5, 0, 0):
    cast_iron___burgundy_coat.use_nodes = True


cast_iron___burgundy_coat.alpha_threshold = 0.5
cast_iron___burgundy_coat.line_priority = 0
cast_iron___burgundy_coat.max_vertex_displacement = 0.0
cast_iron___burgundy_coat.metallic = 0.0
cast_iron___burgundy_coat.paint_active_slot = 0
cast_iron___burgundy_coat.paint_clone_slot = 0
cast_iron___burgundy_coat.pass_index = 0
cast_iron___burgundy_coat.refraction_depth = 0.0
cast_iron___burgundy_coat.roughness = 0.4000000059604645
cast_iron___burgundy_coat.show_transparent_back = True
cast_iron___burgundy_coat.specular_intensity = 0.5
cast_iron___burgundy_coat.use_backface_culling = False
cast_iron___burgundy_coat.use_backface_culling_lightprobe_volume = False
cast_iron___burgundy_coat.use_backface_culling_shadow = False
cast_iron___burgundy_coat.use_preview_world = False
cast_iron___burgundy_coat.use_raytrace_refraction = False
cast_iron___burgundy_coat.use_screen_refraction = False
cast_iron___burgundy_coat.use_sss_translucency = False
cast_iron___burgundy_coat.use_thickness_from_shadow = False
cast_iron___burgundy_coat.use_transparency_overlap = True
cast_iron___burgundy_coat.use_transparent_shadow = True
cast_iron___burgundy_coat.blend_method = 'HASHED'
cast_iron___burgundy_coat.displacement_method = 'BUMP'
cast_iron___burgundy_coat.preview_render_type = 'SHADERBALL'
cast_iron___burgundy_coat.surface_render_method = 'DITHERED'
cast_iron___burgundy_coat.thickness_mode = 'SPHERE'
cast_iron___burgundy_coat.volume_intersection_method = 'FAST'
cast_iron___burgundy_coat.specular_color = (1.0, 1.0, 1.0)
cast_iron___burgundy_coat.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
cast_iron___burgundy_coat.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_5(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = cast_iron___burgundy_coat.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Noise Texture
    noise_texture = shader_nodetree.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.0
    # Scale
    noise_texture.inputs[2].default_value = 200.0
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Bump
    bump = shader_nodetree.nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.invert = False
    # Strength
    bump.inputs[0].default_value = 0.07499998807907104
    # Distance
    bump.inputs[1].default_value = 0.09999999403953552
    # Filter Width
    bump.inputs[2].default_value = 1.0
    # Normal
    bump.inputs[4].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK_SKIN'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.21061378717422485, 0.020156368613243103, 0.008679780177772045, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.5544041395187378
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.5932642221450806
    # IOR
    principled_bsdf.inputs[3].default_value = 1.4500000476837158
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface IOR
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 1.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.15272727608680725
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (0.7805147171020508, 0.7805147171020508, 0.7805147171020508, 1.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (0.0, 0.0, 0.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Color Ramp
    color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    # Initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.3181820511817932
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(1.0)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    # Set locations
    shader_nodetree.nodes["Mapping"].location = (-660.114013671875, 124.89411926269531)
    shader_nodetree.nodes["Texture Coordinate"].location = (-840.114013671875, 124.89411926269531)
    shader_nodetree.nodes["Noise Texture"].location = (-480.1140441894531, 164.8941192626953)
    shader_nodetree.nodes["Material Output"].location = (814.2041625976562, 303.7856140136719)
    shader_nodetree.nodes["Bump"].location = (207.7711944580078, -17.548728942871094)
    shader_nodetree.nodes["Principled BSDF"].location = (494.90203857421875, 171.2886199951172)
    shader_nodetree.nodes["Color Ramp"].location = (-292.9589538574219, 215.05368041992188)

    # Set dimensions
    shader_nodetree.nodes["Mapping"].width  = 140.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Noise Texture"].width  = 140.0
    shader_nodetree.nodes["Noise Texture"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Bump"].width  = 140.0
    shader_nodetree.nodes["Bump"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0


    # Initialize shader_nodetree links

    # mapping.Vector -> noise_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Noise Texture"].inputs[0]
    )
    # texture_coordinate.Generated -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[0],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )
    # noise_texture.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # bump.Normal -> principled_bsdf.Coat Normal
    shader_nodetree.links.new(
        shader_nodetree.nodes["Bump"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[23]
    )
    # color_ramp.Color -> bump.Height
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Bump"].inputs[3]
    )
    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree

# MARK: - Plastic - Black
plastic___black = bpy.data.materials.new(name = "Plastic - Black")
if bpy.app.version < (5, 0, 0):
    plastic___black.use_nodes = True


plastic___black.alpha_threshold = 0.5
plastic___black.line_priority = 0
plastic___black.max_vertex_displacement = 0.0
plastic___black.metallic = 0.0
plastic___black.paint_active_slot = 0
plastic___black.paint_clone_slot = 0
plastic___black.pass_index = 0
plastic___black.refraction_depth = 0.0
plastic___black.roughness = 0.4000000059604645
plastic___black.show_transparent_back = True
plastic___black.specular_intensity = 0.5
plastic___black.use_backface_culling = False
plastic___black.use_backface_culling_lightprobe_volume = False
plastic___black.use_backface_culling_shadow = False
plastic___black.use_preview_world = False
plastic___black.use_raytrace_refraction = False
plastic___black.use_screen_refraction = False
plastic___black.use_sss_translucency = False
plastic___black.use_thickness_from_shadow = False
plastic___black.use_transparency_overlap = True
plastic___black.use_transparent_shadow = True
plastic___black.blend_method = 'HASHED'
plastic___black.displacement_method = 'BUMP'
plastic___black.preview_render_type = 'SHADERBALL'
plastic___black.surface_render_method = 'DITHERED'
plastic___black.thickness_mode = 'SPHERE'
plastic___black.volume_intersection_method = 'FAST'
plastic___black.specular_color = (1.0, 1.0, 1.0)
plastic___black.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
plastic___black.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_6(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = plastic___black.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.002728324616327882, 0.002728324616327882, 0.002728324616327882, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.7863636016845703
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.3499999940395355
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.40272727608680725
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Noise Texture
    noise_texture = shader_nodetree.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '3D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # Scale
    noise_texture.inputs[2].default_value = 77.79999542236328
    # Detail
    noise_texture.inputs[3].default_value = 4.699999809265137
    # Roughness
    noise_texture.inputs[4].default_value = 0.4749999940395355
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Color Ramp
    color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    # Initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.0
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(1.0)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    # Node Bump
    bump = shader_nodetree.nodes.new("ShaderNodeBump")
    bump.name = "Bump"
    bump.invert = False
    # Strength
    bump.inputs[0].default_value = 0.10000002384185791
    # Distance
    bump.inputs[1].default_value = 1.0
    # Filter Width
    bump.inputs[2].default_value = 1.0
    # Normal
    bump.inputs[4].default_value = (0.0, 0.0, 0.0)

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (10.0, 300.0)
    shader_nodetree.nodes["Material Output"].location = (300.0, 300.0)
    shader_nodetree.nodes["Noise Texture"].location = (-764.8291015625, 231.29983520507812)
    shader_nodetree.nodes["Color Ramp"].location = (-565.6229858398438, 202.6844482421875)
    shader_nodetree.nodes["Bump"].location = (-225.37890625, 93.42343139648438)
    shader_nodetree.nodes["Mapping"].location = (-944.8291015625, 191.29983520507812)
    shader_nodetree.nodes["Texture Coordinate"].location = (-1124.8291015625, 191.29983520507812)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Noise Texture"].width  = 140.0
    shader_nodetree.nodes["Noise Texture"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0

    shader_nodetree.nodes["Bump"].width  = 140.0
    shader_nodetree.nodes["Bump"].height = 100.0

    shader_nodetree.nodes["Mapping"].width  = 140.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # noise_texture.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # color_ramp.Color -> bump.Height
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Bump"].inputs[3]
    )
    # bump.Normal -> principled_bsdf.Normal
    shader_nodetree.links.new(
        shader_nodetree.nodes["Bump"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[5]
    )
    # mapping.Vector -> noise_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Noise Texture"].inputs[0]
    )
    # texture_coordinate.Generated -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[0],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )
    # bump.Normal -> principled_bsdf.Coat Normal
    shader_nodetree.links.new(
        shader_nodetree.nodes["Bump"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[23]
    )

    return shader_nodetree

# MARK: Plywood
plywood = bpy.data.materials.new(name = "plywood")
if bpy.app.version < (5, 0, 0):
    plywood.use_nodes = True


plywood.alpha_threshold = 0.5
plywood.line_priority = 0
plywood.max_vertex_displacement = 0.0
plywood.metallic = 0.0
plywood.paint_active_slot = 0
plywood.paint_clone_slot = 0
plywood.pass_index = 0
plywood.refraction_depth = 0.0
plywood.roughness = 0.4000000059604645
plywood.show_transparent_back = True
plywood.specular_intensity = 0.5
plywood.use_backface_culling = False
plywood.use_backface_culling_lightprobe_volume = False
plywood.use_backface_culling_shadow = False
plywood.use_preview_world = False
plywood.use_raytrace_refraction = False
plywood.use_screen_refraction = False
plywood.use_sss_translucency = False
plywood.use_thickness_from_shadow = False
plywood.use_transparency_overlap = True
plywood.use_transparent_shadow = True
plywood.blend_method = 'HASHED'
plywood.displacement_method = 'DISPLACEMENT'
plywood.preview_render_type = 'SPHERE'
plywood.surface_render_method = 'DITHERED'
plywood.thickness_mode = 'SPHERE'
plywood.volume_intersection_method = 'FAST'
plywood.specular_color = (1.0, 1.0, 1.0)
plywood.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
plywood.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group_7(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = plywood.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Frame.001
    frame_001 = shader_nodetree.nodes.new("NodeFrame")
    frame_001.label = "Tiling"
    frame_001.name = "Frame.001"
    frame_001.use_custom_color = True
    frame_001.color = (0.3058430254459381, 0.3058430254459381, 0.3058430254459381)
    frame_001.label_size = 20
    frame_001.shrink = True

    # Node Textures
    textures = shader_nodetree.nodes.new("NodeFrame")
    textures.label = "Textures"
    textures.name = "Textures"
    textures.use_custom_color = True
    textures.color = (0.29431039094924927, 0.29431039094924927, 0.29431039094924927)
    textures.label_size = 20
    textures.shrink = True

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 1.5707963705062866)
    # Scale
    mapping.inputs[3].default_value = (2.0, 2.0, 2.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'BURLEY'
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.4500000476837158
    # Alpha
    principled_bsdf.inputs[4].default_value = 1.0
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 0.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.029999999329447746
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (0.0, 0.0, 0.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Normal Map
    normal_map = shader_nodetree.nodes.new("ShaderNodeNormalMap")
    normal_map.name = "Normal Map"
    normal_map.space = 'TANGENT'
    normal_map.uv_map = ""
    # Strength
    normal_map.inputs[0].default_value = 1.0

    # Node Image Texture.002
    image_texture_002 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_002.name = "Image Texture.002"
    image_texture_002.extension = 'REPEAT'
    if "plywood_rough_4k.png" in bpy.data.images:
        image_texture_002.image = bpy.data.images["plywood_rough_4k.png"]
    image_texture_002.image_user.frame_current = 1
    image_texture_002.image_user.frame_duration = 1
    image_texture_002.image_user.frame_offset = 3
    image_texture_002.image_user.frame_start = 1
    image_texture_002.image_user.tile = 0
    image_texture_002.image_user.use_auto_refresh = False
    image_texture_002.image_user.use_cyclic = False
    image_texture_002.interpolation = 'Linear'
    image_texture_002.projection = 'FLAT'
    image_texture_002.projection_blend = 0.0

    # Node Image Texture
    image_texture = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture.name = "Image Texture"
    image_texture.extension = 'REPEAT'
    if "plywood_diff_4k.png" in bpy.data.images:
        image_texture.image = bpy.data.images["plywood_diff_4k.png"]
    image_texture.image_user.frame_current = 1
    image_texture.image_user.frame_duration = 1
    image_texture.image_user.frame_offset = 3
    image_texture.image_user.frame_start = 1
    image_texture.image_user.tile = 0
    image_texture.image_user.use_auto_refresh = False
    image_texture.image_user.use_cyclic = False
    image_texture.interpolation = 'Linear'
    image_texture.projection = 'FLAT'
    image_texture.projection_blend = 0.0

    # Node Image Texture.003
    image_texture_003 = shader_nodetree.nodes.new("ShaderNodeTexImage")
    image_texture_003.name = "Image Texture.003"
    image_texture_003.extension = 'REPEAT'
    if "plywood_nor_4k.png" in bpy.data.images:
        image_texture_003.image = bpy.data.images["plywood_nor_4k.png"]
    image_texture_003.image_user.frame_current = 1
    image_texture_003.image_user.frame_duration = 1
    image_texture_003.image_user.frame_offset = 3
    image_texture_003.image_user.frame_start = 1
    image_texture_003.image_user.tile = 0
    image_texture_003.image_user.use_auto_refresh = False
    image_texture_003.image_user.use_cyclic = False
    image_texture_003.interpolation = 'Linear'
    image_texture_003.projection = 'FLAT'
    image_texture_003.projection_blend = 0.0

    # Node Displacement
    displacement = shader_nodetree.nodes.new("ShaderNodeDisplacement")
    displacement.name = "Displacement"
    displacement.space = 'OBJECT'
    # Height
    displacement.inputs[0].default_value = 0.0
    # Midlevel
    displacement.inputs[1].default_value = 0.5
    # Scale
    displacement.inputs[2].default_value = 0.0
    # Normal
    displacement.inputs[3].default_value = (0.0, 0.0, 0.0)

    # Set parents
    shader_nodetree.nodes["Texture Coordinate"].parent = shader_nodetree.nodes["Frame.001"]
    shader_nodetree.nodes["Mapping"].parent = shader_nodetree.nodes["Frame.001"]
    shader_nodetree.nodes["Normal Map"].parent = shader_nodetree.nodes["Textures"]
    shader_nodetree.nodes["Image Texture.002"].parent = shader_nodetree.nodes["Textures"]
    shader_nodetree.nodes["Image Texture"].parent = shader_nodetree.nodes["Textures"]
    shader_nodetree.nodes["Image Texture.003"].parent = shader_nodetree.nodes["Textures"]

    # Set locations
    shader_nodetree.nodes["Frame.001"].location = (-1491.0, 264.9999694824219)
    shader_nodetree.nodes["Textures"].location = (-686.9999389648438, 559.0)
    shader_nodetree.nodes["Material Output"].location = (703.9903564453125, 147.21337890625)
    shader_nodetree.nodes["Texture Coordinate"].location = (29.767333984375, -47.5142822265625)
    shader_nodetree.nodes["Mapping"].location = (259.354736328125, -39.6212158203125)
    shader_nodetree.nodes["Principled BSDF"].location = (85.40593719482422, 456.6664123535156)
    shader_nodetree.nodes["Normal Map"].location = (363.407958984375, -698.152587890625)
    shader_nodetree.nodes["Image Texture.002"].location = (29.62158203125, -536.22998046875)
    shader_nodetree.nodes["Image Texture"].location = (38.76513671875, -39.5299072265625)
    shader_nodetree.nodes["Image Texture.003"].location = (29.586181640625, -799.9056396484375)
    shader_nodetree.nodes["Displacement"].location = (134.77194213867188, -274.791015625)

    # Set dimensions
    shader_nodetree.nodes["Frame.001"].width  = 529.0
    shader_nodetree.nodes["Frame.001"].height = 414.9999694824219

    shader_nodetree.nodes["Textures"].width  = 533.9896240234375
    shader_nodetree.nodes["Textures"].height = 1101.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Mapping"].width  = 240.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Normal Map"].width  = 140.98968505859375
    shader_nodetree.nodes["Normal Map"].height = 100.0

    shader_nodetree.nodes["Image Texture.002"].width  = 277.5796203613281
    shader_nodetree.nodes["Image Texture.002"].height = 100.0

    shader_nodetree.nodes["Image Texture"].width  = 289.12432861328125
    shader_nodetree.nodes["Image Texture"].height = 100.0

    shader_nodetree.nodes["Image Texture.003"].width  = 294.28173828125
    shader_nodetree.nodes["Image Texture.003"].height = 100.0

    shader_nodetree.nodes["Displacement"].width  = 140.0
    shader_nodetree.nodes["Displacement"].height = 100.0


    # Initialize shader_nodetree links

    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # mapping.Vector -> image_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Image Texture"].inputs[0]
    )
    # image_texture_003.Color -> normal_map.Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.003"].outputs[0],
        shader_nodetree.nodes["Normal Map"].inputs[1]
    )
    # displacement.Displacement -> material_output.Displacement
    shader_nodetree.links.new(
        shader_nodetree.nodes["Displacement"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[2]
    )
    # mapping.Vector -> image_texture_002.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Image Texture.002"].inputs[0]
    )
    # mapping.Vector -> image_texture_003.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Image Texture.003"].inputs[0]
    )
    # image_texture.Color -> principled_bsdf.Base Color
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[0]
    )
    # normal_map.Normal -> principled_bsdf.Normal
    shader_nodetree.links.new(
        shader_nodetree.nodes["Normal Map"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[5]
    )
    # image_texture_002.Color -> principled_bsdf.Roughness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Image Texture.002"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[2]
    )
    # texture_coordinate.UV -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[2],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )

    return shader_nodetree

# MARK: LaserGrid material
lasergrid = bpy.data.materials.new(name = "LaserGrid")
if bpy.app.version < (5, 0, 0):
    lasergrid.use_nodes = True


lasergrid.alpha_threshold = 0.5
lasergrid.line_priority = 0
lasergrid.max_vertex_displacement = 0.0
lasergrid.metallic = 0.0
lasergrid.paint_active_slot = 0
lasergrid.paint_clone_slot = 0
lasergrid.pass_index = 0
lasergrid.refraction_depth = 0.029999999329447746
lasergrid.roughness = 0.4000000059604645
lasergrid.show_transparent_back = True
lasergrid.specular_intensity = 0.5
lasergrid.use_backface_culling = False
lasergrid.use_backface_culling_lightprobe_volume = False
lasergrid.use_backface_culling_shadow = False
lasergrid.use_preview_world = False
lasergrid.use_raytrace_refraction = True
lasergrid.use_screen_refraction = True
lasergrid.use_sss_translucency = True
lasergrid.use_thickness_from_shadow = True
lasergrid.use_transparency_overlap = True
lasergrid.use_transparent_shadow = False
lasergrid.blend_method = 'BLEND'
lasergrid.displacement_method = 'BUMP'
lasergrid.preview_render_type = 'SPHERE'
lasergrid.surface_render_method = 'BLENDED'
lasergrid.thickness_mode = 'SLAB'
lasergrid.volume_intersection_method = 'FAST'
lasergrid.specular_color = (1.0, 1.0, 1.0)
lasergrid.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
lasergrid.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_lasergrid(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = lasergrid.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK_SKIN'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.7888875007629395, 0.20000000298023224, 0.20000000298023224, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 0.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 1.0
    # IOR
    principled_bsdf.inputs[3].default_value = 1.4500000476837158
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface IOR
    principled_bsdf.inputs[11].default_value = 1.399999976158142
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.699999988079071
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 1.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 0.05000000074505806
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.10000000149011612
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (0.7888875007629395, 0.20000000298023224, 0.20000000298023224, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 1.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Noise Texture
    noise_texture = shader_nodetree.nodes.new("ShaderNodeTexNoise")
    noise_texture.name = "Noise Texture"
    noise_texture.noise_dimensions = '4D'
    noise_texture.noise_type = 'FBM'
    noise_texture.normalize = True
    # W
    noise_texture.inputs[1].default_value = 0.20999997854232788
    # Scale
    noise_texture.inputs[2].default_value = 108.19998931884766
    # Detail
    noise_texture.inputs[3].default_value = 2.0
    # Roughness
    noise_texture.inputs[4].default_value = 0.5
    # Lacunarity
    noise_texture.inputs[5].default_value = 2.0
    # Distortion
    noise_texture.inputs[8].default_value = 0.0

    # Node Mapping
    mapping = shader_nodetree.nodes.new("ShaderNodeMapping")
    mapping.name = "Mapping"
    mapping.vector_type = 'POINT'
    # Location
    mapping.inputs[1].default_value = (0.0, 0.0, 0.0)
    # Rotation
    mapping.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Scale
    mapping.inputs[3].default_value = (1.0, 1.0, 1.0)

    # Node Texture Coordinate
    texture_coordinate = shader_nodetree.nodes.new("ShaderNodeTexCoord")
    texture_coordinate.name = "Texture Coordinate"
    texture_coordinate.from_instancer = False

    # Node Color Ramp
    color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
    color_ramp.name = "Color Ramp"
    color_ramp.color_ramp.color_mode = 'RGB'
    color_ramp.color_ramp.hue_interpolation = 'NEAR'
    color_ramp.color_ramp.interpolation = 'LINEAR'

    # Initialize color ramp elements
    color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
    color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
    color_ramp_cre_0.position = 0.5090906620025635
    color_ramp_cre_0.alpha = 1.0
    color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(1.0)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (0.6414567232131958, 0.6414567232131958, 0.6414567232131958, 1.0)


    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.029999999329447746
    # Set locations
    shader_nodetree.nodes["Principled BSDF"].location = (-305.37158203125, 253.3663787841797)
    shader_nodetree.nodes["Material Output"].location = (600.0, 0.0)
    shader_nodetree.nodes["Noise Texture"].location = (-940.1906127929688, 107.82830047607422)
    shader_nodetree.nodes["Mapping"].location = (-1390.1346435546875, 83.440185546875)
    shader_nodetree.nodes["Texture Coordinate"].location = (-1570.1346435546875, 83.440185546875)
    shader_nodetree.nodes["Color Ramp"].location = (-705.15185546875, 125.52333068847656)
    shader_nodetree.nodes["Value"].location = (600.0, -160.0)

    # Set dimensions
    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Noise Texture"].width  = 140.0
    shader_nodetree.nodes["Noise Texture"].height = 100.0

    shader_nodetree.nodes["Mapping"].width  = 140.0
    shader_nodetree.nodes["Mapping"].height = 100.0

    shader_nodetree.nodes["Texture Coordinate"].width  = 140.0
    shader_nodetree.nodes["Texture Coordinate"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0


    # Initialize shader_nodetree links

    # mapping.Vector -> noise_texture.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mapping"].outputs[0],
        shader_nodetree.nodes["Noise Texture"].inputs[0]
    )
    # noise_texture.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Noise Texture"].outputs[1],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # color_ramp.Color -> principled_bsdf.Alpha
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Principled BSDF"].inputs[4]
    )
    # texture_coordinate.Object -> mapping.Vector
    shader_nodetree.links.new(
        shader_nodetree.nodes["Texture Coordinate"].outputs[3],
        shader_nodetree.nodes["Mapping"].inputs[0]
    )
    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )

    return shader_nodetree

glass___blue = bpy.data.materials.new(name = "Glass - Blue")
if bpy.app.version < (5, 0, 0):
    glass___blue.use_nodes = True


glass___blue.alpha_threshold = 0.5
glass___blue.line_priority = 0
glass___blue.max_vertex_displacement = 0.0
glass___blue.metallic = 0.0
glass___blue.paint_active_slot = 0
glass___blue.paint_clone_slot = 0
glass___blue.pass_index = 0
glass___blue.refraction_depth = 0.0
glass___blue.roughness = 0.4000000059604645
glass___blue.show_transparent_back = True
glass___blue.specular_intensity = 0.5
glass___blue.use_backface_culling = False
glass___blue.use_backface_culling_lightprobe_volume = False
glass___blue.use_backface_culling_shadow = False
glass___blue.use_preview_world = False
glass___blue.use_raytrace_refraction = True
glass___blue.use_screen_refraction = True
glass___blue.use_sss_translucency = False
glass___blue.use_thickness_from_shadow = False
glass___blue.use_transparency_overlap = True
glass___blue.use_transparent_shadow = True
glass___blue.blend_method = 'BLEND'
glass___blue.displacement_method = 'BUMP'
glass___blue.preview_render_type = 'SHADERBALL'
glass___blue.surface_render_method = 'BLENDED'
glass___blue.thickness_mode = 'SPHERE'
glass___blue.volume_intersection_method = 'FAST'
glass___blue.specular_color = (1.0, 1.0, 1.0)
glass___blue.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___blue.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_glass_blue(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___blue.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Node Glass BSDF
    glass_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf.name = "Glass BSDF"
    glass_bsdf.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf.inputs[0].default_value = (0.1842530071735382, 0.3881126642227173, 1.0, 1.0)
    # Roughness
    glass_bsdf.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf.inputs[6].default_value = 1.3300000429153442

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"
    # Fac
    mix_shader.inputs[0].default_value = 0.5499999523162842

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)
    shader_nodetree.nodes["Glass BSDF"].location = (318.3423156738281, 40.32552719116211)
    shader_nodetree.nodes["Mix Shader"].location = (591.265869140625, 38.663787841796875)
    shader_nodetree.nodes["Transparent BSDF"].location = (324.10430908203125, -158.48324584960938)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0

    shader_nodetree.nodes["Glass BSDF"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0


    # Initialize shader_nodetree links

    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # mix_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # glass_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )

    return shader_nodetree


glass___safety = bpy.data.materials.new(name = "Glass - Safety")
if bpy.app.version < (5, 0, 0):
    glass___safety.use_nodes = True


glass___safety.alpha_threshold = 0.5
glass___safety.line_priority = 0
glass___safety.max_vertex_displacement = 0.0
glass___safety.metallic = 0.0
glass___safety.paint_active_slot = 0
glass___safety.paint_clone_slot = 0
glass___safety.pass_index = 0
glass___safety.refraction_depth = 0.0
glass___safety.roughness = 0.4000000059604645
glass___safety.show_transparent_back = True
glass___safety.specular_intensity = 0.5
glass___safety.use_backface_culling = False
glass___safety.use_backface_culling_lightprobe_volume = False
glass___safety.use_backface_culling_shadow = False
glass___safety.use_preview_world = False
glass___safety.use_raytrace_refraction = True
glass___safety.use_screen_refraction = True
glass___safety.use_sss_translucency = False
glass___safety.use_thickness_from_shadow = False
glass___safety.use_transparency_overlap = True
glass___safety.use_transparent_shadow = True
glass___safety.blend_method = 'BLEND'
glass___safety.displacement_method = 'BUMP'
glass___safety.preview_render_type = 'SHADERBALL'
glass___safety.surface_render_method = 'BLENDED'
glass___safety.thickness_mode = 'SPHERE'
glass___safety.volume_intersection_method = 'FAST'
glass___safety.specular_color = (1.0, 1.0, 1.0)
glass___safety.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___safety.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_glass_safety(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___safety.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Node Glass BSDF
    glass_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf.name = "Glass BSDF"
    glass_bsdf.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf.inputs[0].default_value = (0.6535992622375488, 1.0, 0.030902907252311707, 1.0)
    # Roughness
    glass_bsdf.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf.inputs[6].default_value = 1.3300000429153442

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"
    # Fac
    mix_shader.inputs[0].default_value = 0.5499999523162842

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)
    shader_nodetree.nodes["Glass BSDF"].location = (318.3423156738281, 40.32552719116211)
    shader_nodetree.nodes["Mix Shader"].location = (591.265869140625, 38.663787841796875)
    shader_nodetree.nodes["Transparent BSDF"].location = (324.10430908203125, -158.48324584960938)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0

    shader_nodetree.nodes["Glass BSDF"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0


    # Initialize shader_nodetree links

    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # mix_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # glass_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )

    return shader_nodetree


glass___frosted = bpy.data.materials.new(name = "Glass - Frosted")
if bpy.app.version < (5, 0, 0):
    glass___frosted.use_nodes = True


glass___frosted.alpha_threshold = 0.5
glass___frosted.line_priority = 0
glass___frosted.max_vertex_displacement = 0.0
glass___frosted.metallic = 0.0
glass___frosted.paint_active_slot = 0
glass___frosted.paint_clone_slot = 0
glass___frosted.pass_index = 0
glass___frosted.refraction_depth = 0.0
glass___frosted.roughness = 0.4000000059604645
glass___frosted.show_transparent_back = True
glass___frosted.specular_intensity = 0.5
glass___frosted.use_backface_culling = False
glass___frosted.use_backface_culling_lightprobe_volume = False
glass___frosted.use_backface_culling_shadow = False
glass___frosted.use_preview_world = False
glass___frosted.use_raytrace_refraction = True
glass___frosted.use_screen_refraction = True
glass___frosted.use_sss_translucency = False
glass___frosted.use_thickness_from_shadow = False
glass___frosted.use_transparency_overlap = True
glass___frosted.use_transparent_shadow = True
glass___frosted.blend_method = 'BLEND'
glass___frosted.displacement_method = 'BUMP'
glass___frosted.preview_render_type = 'SHADERBALL'
glass___frosted.surface_render_method = 'BLENDED'
glass___frosted.thickness_mode = 'SPHERE'
glass___frosted.volume_intersection_method = 'FAST'
glass___frosted.specular_color = (1.0, 1.0, 1.0)
glass___frosted.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___frosted.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_glass_frosted(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___frosted.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.4227272868156433
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 0.47727271914482117
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (1.0, 1.0, 1.0, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 1.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 1.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.21181818842887878
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (1.0, 1.0, 1.0, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Principled BSDF"].location = (-141.76763916015625, 155.83154296875)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0


    # Initialize shader_nodetree links

    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # principled_bsdf.BSDF -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )

    return shader_nodetree


glass___smokey_black = bpy.data.materials.new(name = "Glass - smokey black")
if bpy.app.version < (5, 0, 0):
    glass___smokey_black.use_nodes = True


glass___smokey_black.alpha_threshold = 0.5
glass___smokey_black.line_priority = 0
glass___smokey_black.max_vertex_displacement = 0.0
glass___smokey_black.metallic = 0.0
glass___smokey_black.paint_active_slot = 0
glass___smokey_black.paint_clone_slot = 0
glass___smokey_black.pass_index = 0
glass___smokey_black.refraction_depth = 0.0
glass___smokey_black.roughness = 0.4000000059604645
glass___smokey_black.show_transparent_back = True
glass___smokey_black.specular_intensity = 0.5
glass___smokey_black.use_backface_culling = False
glass___smokey_black.use_backface_culling_lightprobe_volume = False
glass___smokey_black.use_backface_culling_shadow = False
glass___smokey_black.use_preview_world = False
glass___smokey_black.use_raytrace_refraction = True
glass___smokey_black.use_screen_refraction = True
glass___smokey_black.use_sss_translucency = False
glass___smokey_black.use_thickness_from_shadow = False
glass___smokey_black.use_transparency_overlap = True
glass___smokey_black.use_transparent_shadow = True
glass___smokey_black.blend_method = 'BLEND'
glass___smokey_black.displacement_method = 'BUMP'
glass___smokey_black.preview_render_type = 'SHADERBALL'
glass___smokey_black.surface_render_method = 'BLENDED'
glass___smokey_black.thickness_mode = 'SPHERE'
glass___smokey_black.volume_intersection_method = 'FAST'
glass___smokey_black.specular_color = (1.0, 1.0, 1.0)
glass___smokey_black.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___smokey_black.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_smokey_black(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___smokey_black.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.010080336593091488, 0.010580021888017654, 0.016261735931038857, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.4227272868156433
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 0.47727271914482117
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (0.017382808029651642, 0.017382808029651642, 0.017382808029651642, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 1.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 1.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.21181818842887878
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (0.04784040153026581, 0.04784040153026581, 0.04784040153026581, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)

    # Node Glass BSDF.001
    glass_bsdf_001 = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf_001.name = "Glass BSDF.001"
    glass_bsdf_001.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf_001.inputs[0].default_value = (0.11442021280527115, 0.11442021280527115, 0.11442021280527115, 1.0)
    # Roughness
    glass_bsdf_001.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf_001.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf_001.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf_001.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf_001.inputs[6].default_value = 1.3300000429153442

    # Node Fresnel
    fresnel = shader_nodetree.nodes.new("ShaderNodeFresnel")
    fresnel.name = "Fresnel"
    # IOR
    fresnel.inputs[0].default_value = 35.0
    # Normal
    fresnel.inputs[1].default_value = (0.0, 0.0, 0.0)

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Mix Shader.002
    mix_shader_002 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_002.name = "Mix Shader.002"
    # Fac
    mix_shader_002.inputs[0].default_value = 0.6499999761581421

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Principled BSDF"].location = (-141.76763916015625, 155.83154296875)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (161.25888061523438, -404.6147766113281)
    shader_nodetree.nodes["Glass BSDF.001"].location = (162.81045532226562, -217.31651306152344)
    shader_nodetree.nodes["Fresnel"].location = (176.09983825683594, -115.24836730957031)
    shader_nodetree.nodes["Mix Shader"].location = (393.1517333984375, -214.63412475585938)
    shader_nodetree.nodes["Mix Shader.002"].location = (466.82525634765625, 230.33627319335938)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Glass BSDF.001"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF.001"].height = 100.0

    shader_nodetree.nodes["Fresnel"].width  = 140.0
    shader_nodetree.nodes["Fresnel"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Mix Shader.002"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.002"].height = 100.0


    # Initialize shader_nodetree links

    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # glass_bsdf_001.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF.001"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # fresnel.Factor -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Fresnel"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # mix_shader_002.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.002"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # principled_bsdf.BSDF -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[1]
    )
    # mix_shader.Shader -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[2]
    )

    return shader_nodetree


glass___smokey_bronze = bpy.data.materials.new(name = "Glass - smokey bronze")
if bpy.app.version < (5, 0, 0):
    glass___smokey_bronze.use_nodes = True


glass___smokey_bronze.alpha_threshold = 0.5
glass___smokey_bronze.line_priority = 0
glass___smokey_bronze.max_vertex_displacement = 0.0
glass___smokey_bronze.metallic = 0.0
glass___smokey_bronze.paint_active_slot = 0
glass___smokey_bronze.paint_clone_slot = 0
glass___smokey_bronze.pass_index = 0
glass___smokey_bronze.refraction_depth = 0.0
glass___smokey_bronze.roughness = 0.4000000059604645
glass___smokey_bronze.show_transparent_back = True
glass___smokey_bronze.specular_intensity = 0.5
glass___smokey_bronze.use_backface_culling = False
glass___smokey_bronze.use_backface_culling_lightprobe_volume = False
glass___smokey_bronze.use_backface_culling_shadow = False
glass___smokey_bronze.use_preview_world = False
glass___smokey_bronze.use_raytrace_refraction = True
glass___smokey_bronze.use_screen_refraction = True
glass___smokey_bronze.use_sss_translucency = False
glass___smokey_bronze.use_thickness_from_shadow = False
glass___smokey_bronze.use_transparency_overlap = True
glass___smokey_bronze.use_transparent_shadow = True
glass___smokey_bronze.blend_method = 'BLEND'
glass___smokey_bronze.displacement_method = 'BUMP'
glass___smokey_bronze.preview_render_type = 'SHADERBALL'
glass___smokey_bronze.surface_render_method = 'BLENDED'
glass___smokey_bronze.thickness_mode = 'SPHERE'
glass___smokey_bronze.volume_intersection_method = 'FAST'
glass___smokey_bronze.specular_color = (1.0, 1.0, 1.0)
glass___smokey_bronze.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 0.22352829575538635)
glass___smokey_bronze.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_smokey_bronze(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = glass___smokey_bronze.node_tree

    # Start with a clean node tree
    for node in shader_nodetree.nodes:
        shader_nodetree.nodes.remove(node)
    shader_nodetree.color_tag = 'NONE'
    shader_nodetree.description = ""
    shader_nodetree.default_group_node_width = 140
    # Initialize shader_nodetree nodes

    # Node Material Output
    material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
    material_output.name = "Material Output"
    material_output.is_active_output = True
    material_output.target = 'EEVEE'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Principled BSDF
    principled_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfPrincipled")
    principled_bsdf.name = "Principled BSDF"
    principled_bsdf.distribution = 'MULTI_GGX'
    principled_bsdf.subsurface_method = 'RANDOM_WALK'
    # Base Color
    principled_bsdf.inputs[0].default_value = (0.17885418236255646, 0.031568195670843124, 0.011802139692008495, 1.0)
    # Metallic
    principled_bsdf.inputs[1].default_value = 1.0
    # Roughness
    principled_bsdf.inputs[2].default_value = 0.4227272868156433
    # IOR
    principled_bsdf.inputs[3].default_value = 1.5
    # Alpha
    principled_bsdf.inputs[4].default_value = 0.47727271914482117
    # Normal
    principled_bsdf.inputs[5].default_value = (0.0, 0.0, 0.0)
    # Diffuse Roughness
    principled_bsdf.inputs[7].default_value = 0.0
    # Subsurface Weight
    principled_bsdf.inputs[8].default_value = 0.0
    # Subsurface Radius
    principled_bsdf.inputs[9].default_value = (1.0, 0.20000000298023224, 0.10000000149011612)
    # Subsurface Scale
    principled_bsdf.inputs[10].default_value = 0.05000000074505806
    # Subsurface Anisotropy
    principled_bsdf.inputs[12].default_value = 0.0
    # Specular IOR Level
    principled_bsdf.inputs[13].default_value = 0.5
    # Specular Tint
    principled_bsdf.inputs[14].default_value = (0.017382808029651642, 0.017382808029651642, 0.017382808029651642, 1.0)
    # Anisotropic
    principled_bsdf.inputs[15].default_value = 0.0
    # Anisotropic Rotation
    principled_bsdf.inputs[16].default_value = 0.0
    # Tangent
    principled_bsdf.inputs[17].default_value = (0.0, 0.0, 0.0)
    # Transmission Weight
    principled_bsdf.inputs[18].default_value = 1.0
    # Coat Weight
    principled_bsdf.inputs[19].default_value = 1.0
    # Coat Roughness
    principled_bsdf.inputs[20].default_value = 0.21181818842887878
    # Coat IOR
    principled_bsdf.inputs[21].default_value = 1.5
    # Coat Tint
    principled_bsdf.inputs[22].default_value = (0.5949889421463013, 0.26044151186943054, 0.1255592554807663, 1.0)
    # Coat Normal
    principled_bsdf.inputs[23].default_value = (0.0, 0.0, 0.0)
    # Sheen Weight
    principled_bsdf.inputs[24].default_value = 0.0
    # Sheen Roughness
    principled_bsdf.inputs[25].default_value = 0.5
    # Sheen Tint
    principled_bsdf.inputs[26].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Color
    principled_bsdf.inputs[27].default_value = (1.0, 1.0, 1.0, 1.0)
    # Emission Strength
    principled_bsdf.inputs[28].default_value = 0.0
    # Thin Film Thickness
    principled_bsdf.inputs[29].default_value = 0.0
    # Thin Film IOR
    principled_bsdf.inputs[30].default_value = 1.3300000429153442

    # Node Value
    value = shader_nodetree.nodes.new("ShaderNodeValue")
    value.name = "Value"

    value.outputs[0].default_value = 0.0010000000474974513
    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (0.0735681876540184, 0.07748433947563171, 0.013032980263233185, 1.0)

    # Node Glass BSDF.001
    glass_bsdf_001 = shader_nodetree.nodes.new("ShaderNodeBsdfGlass")
    glass_bsdf_001.name = "Glass BSDF.001"
    glass_bsdf_001.distribution = 'MULTI_GGX'
    # Color
    glass_bsdf_001.inputs[0].default_value = (0.1144205778837204, 0.018194811418652534, 0.0076646748930215836, 1.0)
    # Roughness
    glass_bsdf_001.inputs[1].default_value = 0.0
    # IOR
    glass_bsdf_001.inputs[2].default_value = 1.5
    # Normal
    glass_bsdf_001.inputs[3].default_value = (0.0, 0.0, 0.0)
    # Thin Film Thickness
    glass_bsdf_001.inputs[5].default_value = 0.0
    # Thin Film IOR
    glass_bsdf_001.inputs[6].default_value = 1.3300000429153442

    # Node Fresnel
    fresnel = shader_nodetree.nodes.new("ShaderNodeFresnel")
    fresnel.name = "Fresnel"
    # IOR
    fresnel.inputs[0].default_value = 35.0
    # Normal
    fresnel.inputs[1].default_value = (0.0, 0.0, 0.0)

    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Node Mix Shader.002
    mix_shader_002 = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader_002.name = "Mix Shader.002"
    # Fac
    mix_shader_002.inputs[0].default_value = 0.6499999761581421

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (827.1918334960938, 332.5242614746094)
    shader_nodetree.nodes["Principled BSDF"].location = (-141.76763916015625, 155.83154296875)
    shader_nodetree.nodes["Value"].location = (180.0, 460.0)
    shader_nodetree.nodes["Transparent BSDF"].location = (161.25888061523438, -404.6147766113281)
    shader_nodetree.nodes["Glass BSDF.001"].location = (162.81045532226562, -217.31651306152344)
    shader_nodetree.nodes["Fresnel"].location = (176.09983825683594, -115.24836730957031)
    shader_nodetree.nodes["Mix Shader"].location = (393.1517333984375, -214.63412475585938)
    shader_nodetree.nodes["Mix Shader.002"].location = (466.82525634765625, 230.33627319335938)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Principled BSDF"].width  = 240.0
    shader_nodetree.nodes["Principled BSDF"].height = 100.0

    shader_nodetree.nodes["Value"].width  = 140.0
    shader_nodetree.nodes["Value"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Glass BSDF.001"].width  = 150.0
    shader_nodetree.nodes["Glass BSDF.001"].height = 100.0

    shader_nodetree.nodes["Fresnel"].width  = 140.0
    shader_nodetree.nodes["Fresnel"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0

    shader_nodetree.nodes["Mix Shader.002"].width  = 140.0
    shader_nodetree.nodes["Mix Shader.002"].height = 100.0


    # Initialize shader_nodetree links

    # value.Value -> material_output.Thickness
    shader_nodetree.links.new(
        shader_nodetree.nodes["Value"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[3]
    )
    # glass_bsdf_001.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Glass BSDF.001"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )
    # fresnel.Factor -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Fresnel"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # mix_shader_002.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader.002"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # principled_bsdf.BSDF -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Principled BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[1]
    )
    # mix_shader.Shader -> mix_shader_002.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Mix Shader.002"].inputs[2]
    )

    return shader_nodetree

if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    shader_nodetree = shader_nodetree_glass(node_tree_names)
    node_tree_names[shader_nodetree_glass] = shader_nodetree.name

    shader_nodetree_1 = shader_nodetree_node_group_1(node_tree_names)
    node_tree_names[shader_nodetree_node_group_1] = shader_nodetree_1.name

    shader_nodetree_2 = shader_nodetree_node_group_2(node_tree_names)
    node_tree_names[shader_nodetree_node_group_2] = shader_nodetree_2.name

    shader_nodetree_3 = shader_nodetree_node_group_3(node_tree_names)
    node_tree_names[shader_nodetree_node_group_3] = shader_nodetree_3.name

    shader_nodetree_4 = shader_nodetree_node_group_4(node_tree_names)
    node_tree_names[shader_nodetree_node_group_4] = shader_nodetree_4.name

    shader_nodetree_5 = shader_nodetree_node_group_5(node_tree_names)
    node_tree_names[shader_nodetree_node_group_5] = shader_nodetree_5.name

    shader_nodetree_6 = shader_nodetree_node_group_6(node_tree_names)
    node_tree_names[shader_nodetree_node_group_6] = shader_nodetree_6.name

    shader_nodetree_7 = shader_nodetree_node_group_7(node_tree_names)
    node_tree_names[shader_nodetree_node_group_7] = shader_nodetree_7.name

    shader_nodetree_8 = shader_nodetree_lasergrid(node_tree_names)
    node_tree_names[shader_nodetree_lasergrid] = shader_nodetree_8.name

    shader_nodetree_9 = shader_nodetree_glass_blue(node_tree_names)
    node_tree_names[shader_nodetree_glass_blue] = shader_nodetree_9.name

    shader_nodetree_10 = shader_nodetree_smokey_black(node_tree_names)
    node_tree_names[shader_nodetree_smokey_black] = shader_nodetree_10.name

    shader_nodetree_11 = shader_nodetree_smokey_bronze(node_tree_names)
    node_tree_names[shader_nodetree_smokey_bronze] = shader_nodetree_11.name

    shader_nodetree_12 = shader_nodetree_glass_safety(node_tree_names)
    node_tree_names[shader_nodetree_glass_safety] = shader_nodetree_12.name

    shader_nodetree_13 = shader_nodetree_glass_frosted(node_tree_names)
    node_tree_names[shader_nodetree_glass_frosted] = shader_nodetree_13.name