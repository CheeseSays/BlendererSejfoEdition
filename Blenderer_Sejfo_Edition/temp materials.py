import bpy
import mathutils
import os
import typing


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

    shader_nodetree = shader_nodetree_node_group(node_tree_names)
    node_tree_names[shader_nodetree_node_group] = shader_nodetree.name

    shader_nodetree_1 = shader_nodetree_node_group_1(node_tree_names)
    node_tree_names[shader_nodetree_node_group_1] = shader_nodetree_1.name

    shader_nodetree_2 = shader_nodetree_node_group_2(node_tree_names)
    node_tree_names[shader_nodetree_node_group_2] = shader_nodetree_2.name

    shader_nodetree_3 = shader_nodetree_node_group_3(node_tree_names)
    node_tree_names[shader_nodetree_node_group_3] = shader_nodetree_3.name

    shader_nodetree_4 = shader_nodetree_node_group_4(node_tree_names)
    node_tree_names[shader_nodetree_node_group_4] = shader_nodetree_4.name

