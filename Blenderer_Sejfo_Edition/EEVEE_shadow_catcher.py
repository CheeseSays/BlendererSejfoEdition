import bpy
import mathutils
import os
import typing


eevee_shadow_catcher = bpy.data.materials.new(name = "EEVEE_Shadow_Catcher")
if bpy.app.version < (5, 0, 0):
    eevee_shadow_catcher.use_nodes = True


eevee_shadow_catcher.alpha_threshold = 0.5
eevee_shadow_catcher.line_priority = 0
eevee_shadow_catcher.max_vertex_displacement = 0.0
eevee_shadow_catcher.metallic = 0.0
eevee_shadow_catcher.paint_active_slot = 0
eevee_shadow_catcher.paint_clone_slot = 0
eevee_shadow_catcher.pass_index = 0
eevee_shadow_catcher.refraction_depth = 0.0
eevee_shadow_catcher.roughness = 0.4000000059604645
eevee_shadow_catcher.show_transparent_back = True
eevee_shadow_catcher.specular_intensity = 0.5
eevee_shadow_catcher.use_backface_culling = False
eevee_shadow_catcher.use_backface_culling_lightprobe_volume = False
eevee_shadow_catcher.use_backface_culling_shadow = False
eevee_shadow_catcher.use_preview_world = False
eevee_shadow_catcher.use_raytrace_refraction = False
eevee_shadow_catcher.use_screen_refraction = False
eevee_shadow_catcher.use_sss_translucency = False
eevee_shadow_catcher.use_thickness_from_shadow = False
eevee_shadow_catcher.use_transparency_overlap = True
eevee_shadow_catcher.use_transparent_shadow = True
eevee_shadow_catcher.blend_method = 'BLEND'
eevee_shadow_catcher.displacement_method = 'BUMP'
eevee_shadow_catcher.preview_render_type = 'SPHERE'
eevee_shadow_catcher.surface_render_method = 'BLENDED'
eevee_shadow_catcher.thickness_mode = 'SPHERE'
eevee_shadow_catcher.volume_intersection_method = 'FAST'
eevee_shadow_catcher.specular_color = (1.0, 1.0, 1.0)
eevee_shadow_catcher.diffuse_color = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
eevee_shadow_catcher.line_color = (0.0, 0.0, 0.0, 0.0)

def shader_nodetree_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Shader Nodetree node group"""
    shader_nodetree = eevee_shadow_catcher.node_tree

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
    material_output.target = 'ALL'
    # Displacement
    material_output.inputs[2].default_value = (0.0, 0.0, 0.0)
    # Thickness
    material_output.inputs[3].default_value = 0.0

    # Node Transparent BSDF
    transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
    transparent_bsdf.name = "Transparent BSDF"
    # Color
    transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)

    # Node Emission
    emission = shader_nodetree.nodes.new("ShaderNodeEmission")
    emission.name = "Emission"
    # Color
    emission.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
    # Strength
    emission.inputs[1].default_value = 1.0

    # Node Diffuse BSDF
    diffuse_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfDiffuse")
    diffuse_bsdf.name = "Diffuse BSDF"
    # Color
    diffuse_bsdf.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
    # Roughness
    diffuse_bsdf.inputs[1].default_value = 0.0
    # Normal
    diffuse_bsdf.inputs[2].default_value = (0.0, 0.0, 0.0)

    # Node Shader to RGB
    shader_to_rgb = shader_nodetree.nodes.new("ShaderNodeShaderToRGB")
    shader_to_rgb.name = "Shader to RGB"

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

    color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.8454546928405762)
    color_ramp_cre_1.alpha = 1.0
    color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)


    # Node Mix Shader
    mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
    mix_shader.name = "Mix Shader"

    # Set locations
    shader_nodetree.nodes["Material Output"].location = (645.79248046875, 323.4210205078125)
    shader_nodetree.nodes["Transparent BSDF"].location = (-114.39779663085938, 133.02207946777344)
    shader_nodetree.nodes["Emission"].location = (-105.24452209472656, 245.03561401367188)
    shader_nodetree.nodes["Diffuse BSDF"].location = (-447.9857482910156, 342.8215026855469)
    shader_nodetree.nodes["Shader to RGB"].location = (-225.2999267578125, 353.6590576171875)
    shader_nodetree.nodes["Color Ramp"].location = (-29.011865615844727, 481.9655456542969)
    shader_nodetree.nodes["Mix Shader"].location = (304.4345703125, 282.4414978027344)

    # Set dimensions
    shader_nodetree.nodes["Material Output"].width  = 140.0
    shader_nodetree.nodes["Material Output"].height = 100.0

    shader_nodetree.nodes["Transparent BSDF"].width  = 140.0
    shader_nodetree.nodes["Transparent BSDF"].height = 100.0

    shader_nodetree.nodes["Emission"].width  = 140.0
    shader_nodetree.nodes["Emission"].height = 100.0

    shader_nodetree.nodes["Diffuse BSDF"].width  = 150.0
    shader_nodetree.nodes["Diffuse BSDF"].height = 100.0

    shader_nodetree.nodes["Shader to RGB"].width  = 140.0
    shader_nodetree.nodes["Shader to RGB"].height = 100.0

    shader_nodetree.nodes["Color Ramp"].width  = 240.0
    shader_nodetree.nodes["Color Ramp"].height = 100.0

    shader_nodetree.nodes["Mix Shader"].width  = 140.0
    shader_nodetree.nodes["Mix Shader"].height = 100.0


    # Initialize shader_nodetree links

    # diffuse_bsdf.BSDF -> shader_to_rgb.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Diffuse BSDF"].outputs[0],
        shader_nodetree.nodes["Shader to RGB"].inputs[0]
    )
    # shader_to_rgb.Color -> color_ramp.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Shader to RGB"].outputs[0],
        shader_nodetree.nodes["Color Ramp"].inputs[0]
    )
    # color_ramp.Color -> mix_shader.Factor
    shader_nodetree.links.new(
        shader_nodetree.nodes["Color Ramp"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[0]
    )
    # mix_shader.Shader -> material_output.Surface
    shader_nodetree.links.new(
        shader_nodetree.nodes["Mix Shader"].outputs[0],
        shader_nodetree.nodes["Material Output"].inputs[0]
    )
    # emission.Emission -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Emission"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[1]
    )
    # transparent_bsdf.BSDF -> mix_shader.Shader
    shader_nodetree.links.new(
        shader_nodetree.nodes["Transparent BSDF"].outputs[0],
        shader_nodetree.nodes["Mix Shader"].inputs[2]
    )

    return shader_nodetree


if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    shader_nodetree = shader_nodetree_node_group(node_tree_names)
    node_tree_names[shader_nodetree_node_group] = shader_nodetree.name

