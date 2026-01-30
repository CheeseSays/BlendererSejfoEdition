import bpy, os.path


def is_blender_version(major, minor=0, patch=0, operator='>='):
    """
    Check Blender version against specified version.
    
    Args:
        major: Major version number
        minor: Minor version number (default: 0)
        patch: Patch version number (default: 0)
        operator: Comparison operator ('>=', '>', '<=', '<', '==', '!=')
    
    Returns:
        bool: True if version check passes
    """
    current = bpy.app.version
    target = (major, minor, patch)
    
    if operator == '>=':
        return current >= target
    elif operator == '>':
        return current > target
    elif operator == '<=':
        return current <= target
    elif operator == '<':
        return current < target
    elif operator == '==':
        return current == target
    elif operator == '!=':
        return current != target
    else:
        raise ValueError(f"Invalid operator: {operator}")


def setupSparks(mat_name,col):
  mat = bpy.data.materials.new(name=mat_name)
  mat.use_nodes = True
  nodes = mat.node_tree.nodes
  for node in nodes:
    nodes.remove(node)
  # create principled
  node_emission = nodes.new(type="ShaderNodeEmission")
  node_emission.location = 200,0
  node_emission.inputs[1].default_value = 50.0
  node_emission.inputs[0].default_value = col
  # create output node
  node_output = nodes.new(type='ShaderNodeOutputMaterial')   
  node_output.location = 600,0
  links = mat.node_tree.links
  link = links.new(node_emission.outputs[0], node_output.inputs[0])
  return mat


def setupMaterial(mat_name,
          col,
          color_map,
          metallic,
          roughness,
          normal_map,
          bumpiness, 
          clearcoat,
          clearcoat_rouhness,
          transparency,
          style,
          monochrome,
          simple_transparents = False):
  
  node_noise,node_math = None, None
  mat = bpy.data.materials.new(name=mat_name)
  mat.use_nodes = True
  nodes = mat.node_tree.nodes
  if monochrome:
    col = [float(x) for x in monochrome.split('|')]
    color_map = ''
    metallic = 0.0
    roughness = 1.0
    normal_map = ''
    bumpiness = 0
    clearcoat = 0
    clearcoat_rouhness = 0
    style = '__monochrome__' #this force skips and styling code
    transparency = 0.0
  if style in ['N/A', '']:
    if '_cast_metal' in mat.name:
      style = 'castmetal'
    elif '_pulver' in mat.name:
      style = 'pulver'
  for node in nodes:
    nodes.remove(node)
  #
  # Create principled shader
  #
  node_principled = nodes.new(type="ShaderNodeBsdfPrincipled")
  node_principled.location = 200,0
  node_principled.inputs['Metallic'].default_value = metallic
  # Blender 4.0+ renamed 'Specular' to 'Specular IOR Level'
  if 'Specular IOR Level' in node_principled.inputs:
    node_principled.inputs['Specular IOR Level'].default_value = 0.5
  elif 'Specular' in node_principled.inputs:
    node_principled.inputs['Specular'].default_value = 0.7
  node_principled.inputs['Roughness'].default_value = max(roughness, 0.01)
  # Blender 4.0+ renamed 'Clearcoat' to 'Coat Weight'
  if 'Coat Weight' in node_principled.inputs:
    node_principled.inputs['Coat Weight'].default_value = clearcoat
  elif 'Clearcoat' in node_principled.inputs:
    node_principled.inputs['Clearcoat'].default_value = clearcoat
  # Blender 4.0+ renamed 'Clearcoat Roughness' to 'Coat Roughness'
  if 'Coat Roughness' in node_principled.inputs:
    node_principled.inputs['Coat Roughness'].default_value = max(clearcoat_rouhness, 0.1)
  elif 'Clearcoat Roughness' in node_principled.inputs:
    node_principled.inputs['Clearcoat Roughness'].default_value = max(clearcoat_rouhness, 0.1)
  # create output node
  node_output = nodes.new(type='ShaderNodeOutputMaterial')   
  node_output.location = 600,0
  #
  # Base color or texture
  #
  node_texture = None
  if color_map and os.path.exists(color_map):
    node_texture = nodes.new(type='ShaderNodeTexImage')
    node_texture.location = -600,100
    texture_img = bpy.data.images.load(color_map)
    node_texture.image = texture_img
  else:
    # text color
    if len(col) == 3:
      ccolor = [0,0,0,1]
      ccolor[:3] = col
      col = tuple(ccolor)
    col = [x**2.2 for x in col] # gamma correction
    node_principled.inputs['Base Color'].default_value = col
  #
  # Transparency | Opacity
  #
  if transparency < 1.0: #opacity
    mat.blend_method = 'BLEND'
    if simple_transparents: #Force use tranparency shader
      mat = setup_transparent_shader(mat, col)
      return mat
    # Blender 4.0+ renamed 'Transmission' to 'Transmission Weight'
    if 'Transmission Weight' in node_principled.inputs:
      node_principled.inputs['Transmission Weight'].default_value = 1.0
    elif 'Transmission' in node_principled.inputs:
      node_principled.inputs['Transmission'].default_value = 1.0
    col = [x*0.8 + 0.2 for x in col] #make it brighter
    while len(col) < 4:
      col.append(0)
    node_principled.inputs['Base Color'].default_value = col
    
    # Raytracing is only available in Blender 5.0+
    # In 3.6-4.x, SSR is separate; in 5.0+ it's unified raytracing
    if is_blender_version(5, 0) and hasattr(bpy.context.scene.eevee, 'use_raytracing'):
        bpy.context.scene.eevee.use_raytracing = True
    
    # Screen-space refraction settings (check if available)
    if hasattr(mat, 'use_screen_refraction'):
        mat.use_screen_refraction = True
    if hasattr(mat, 'use_sss_translucency'):
        mat.use_sss_translucency = True
    if hasattr(mat, 'refraction_depth'):
        mat.refraction_depth = 0.03
    
    # roughness scaling as VC renders quite rough materials still as transparent
    scale_roughness_down = 0.3
    minimum_roughness = 0.1
    node_principled.inputs['Roughness'].default_value = max(roughness * scale_roughness_down, minimum_roughness)
  else:
    # Blender 4.0+ renamed 'Transmission' to 'Transmission Weight'
    if 'Transmission Weight' in node_principled.inputs:
      node_principled.inputs['Transmission Weight'].default_value = 0.0
    elif 'Transmission' in node_principled.inputs:
      node_principled.inputs['Transmission'].default_value = 0.0
  #
  # Styles
  #
  style_vals = style.lower().split('|')
  node_normalmap = None
  if normal_map and os.path.exists(normal_map):
    node_normalmap = nodes.new(type='ShaderNodeTexImage')
    node_normalmap.location = -600,-300
    normalmap_img = bpy.data.images.load(normal_map)
    node_normalmap.image = normalmap_img
    normalmap_img.colorspace_settings.name = 'Non-Color'
    #
    node_normalvector = nodes.new(type="ShaderNodeNormalMap")
    node_normalvector.location = -300,-300
    node_normalvector.inputs[0].default_value = bumpiness*2
  elif style_vals[0] == 'castmetal':
    try:
      strength = float( style_vals[1] )
    except:
      strength = 0.05
    try:
      text_scale = float(style_vals[2])
    except:
      text_scale = 400.0
    coordinates_node = nodes.new(type="ShaderNodeTexCoord")
    coordinates_node.location = -1600,-300

    node_principled.inputs['Roughness'].default_value = max(roughness*.6, .2) # decreasing the roughness a little but clmaping it above .2

    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.location = -1400,-300
    mapping_node.inputs['Scale'].default_value[0] = text_scale
    mapping_node.inputs['Scale'].default_value[1] = text_scale
    mapping_node.inputs['Scale'].default_value[2] = text_scale

    voronoi_node = nodes.new(type="ShaderNodeTexVoronoi")
    voronoi_node.location = -1000,-300
    voronoi_node.inputs[1].default_value = 200

    noise_node = nodes.new(type="ShaderNodeTexNoise")
    noise_node.location = -1000,-600
    noise_node.inputs[1].default_value = 600.0
    noise_node.inputs[2].default_value = 2.0
    noise_node.inputs[3].default_value = 5.0

    noise_node2 = nodes.new(type="ShaderNodeTexNoise")
    noise_node2.location = -1000,-900
    noise_node2.inputs[1].default_value = 10.0
    noise_node2.inputs[2].default_value = 2.0
    noise_node2.inputs[3].default_value = 80.0

    colorramp_node = nodes.new(type="ShaderNodeValToRGB")
    colorramp_node.location = -800,-300
    colorramp_node.color_ramp.elements[0].position = 0.5
    colorramp_node.color_ramp.elements[1].position = 0.65
    colorramp_node.color_ramp.elements[0].color = (1, 1, 1, 1)
    colorramp_node.color_ramp.elements[1].color = (0, 0, 0, 1)

    colorramp_node2 = nodes.new(type="ShaderNodeValToRGB")
    colorramp_node2.location = -800,-600
    colorramp_node2.color_ramp.elements[0].position = 0.25
    colorramp_node2.color_ramp.elements[1].position = 0.8
    colorramp_node2.color_ramp.elements[0].color = (1, 1, 1, 1)
    colorramp_node2.color_ramp.elements[1].color = (0, 0, 0, 1)

    colorramp_node3 = nodes.new(type="ShaderNodeValToRGB")
    colorramp_node3.location = -800,-900
    colorramp_node3.color_ramp.elements[0].position = 0.51
    colorramp_node3.color_ramp.elements[1].position = 0.675
    colorramp_node3.color_ramp.elements[0].color = (1, 1, 1, 1)
    colorramp_node3.color_ramp.elements[1].color = (0, 0, 0, 1)

    mix_node1 = nodes.new(type="ShaderNodeMixRGB")
    mix_node1.location = -400,-600
    mix_node1.blend_type = 'VALUE'
    mix_node1.inputs[0].default_value = 0.5

    mix_node2 = nodes.new(type="ShaderNodeMixRGB")
    mix_node2.location = -200,-300
    mix_node2.blend_type = 'VALUE'
    mix_node2.inputs[0].default_value = 0.66

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.location = 0,-300
    bump_node.inputs[0].default_value = strength
    bump_node.inputs[1].default_value = 1.0

    links = mat.node_tree.links
    link = links.new(coordinates_node.outputs[3], mapping_node.inputs[0])
    link = links.new(mapping_node.outputs[0], voronoi_node.inputs[0])
    link = links.new(voronoi_node.outputs[0], colorramp_node.inputs[0])
    link = links.new(colorramp_node.outputs[0], mix_node2.inputs[1])
    link = links.new(mapping_node.outputs[0], noise_node.inputs[0])
    link = links.new(mapping_node.outputs[0], noise_node2.inputs[0])
    link = links.new(noise_node.outputs[0], colorramp_node2.inputs[0])
    link = links.new(noise_node2.outputs[0], colorramp_node3.inputs[0])
    link = links.new(colorramp_node2.outputs[0], mix_node1.inputs[1])
    link = links.new(colorramp_node3.outputs[0], mix_node1.inputs[2])
    link = links.new(mix_node1.outputs[0], mix_node2.inputs[2])
    link = links.new(mix_node2.outputs[0], bump_node.inputs[2])
    link = links.new(bump_node.outputs[0], node_principled.inputs['Normal'])

  elif style_vals[0] == 'pulver':
    try:
      strength = float( style_vals[1] )
    except:
      strength = 0.08
    try:
      text_scale = float(style_vals[2])
    except:
      text_scale = 1.0
    coordinates_node = nodes.new(type="ShaderNodeTexCoord")
    coordinates_node.location = -1400,-300

    mapping_node = nodes.new(type="ShaderNodeMapping")
    mapping_node.location = -1100,-300
    mapping_node.inputs['Scale'].default_value[0] = 200*text_scale
    mapping_node.inputs['Scale'].default_value[1] = 200*text_scale
    mapping_node.inputs['Scale'].default_value[2] = 200*text_scale


    noise_node = nodes.new(type="ShaderNodeTexNoise")
    noise_node.location = -700,-300
    noise_node.inputs[1].default_value = 5.0
    noise_node.inputs[2].default_value = 2.0
    noise_node.inputs[3].default_value = 0.0

    bump_node = nodes.new(type="ShaderNodeBump")
    bump_node.location = 0,-300
    bump_node.inputs[0].default_value = strength
    bump_node.inputs[1].default_value = 1.0

    links = mat.node_tree.links
    link = links.new(coordinates_node.outputs[3], mapping_node.inputs[0])
    link = links.new(mapping_node.outputs[0], noise_node.inputs[0])
    link = links.new(noise_node.outputs[0], bump_node.inputs[2])
    link = links.new(bump_node.outputs[0], node_principled.inputs['Normal'])
  #
  # Link the nodes together
  #
  links = mat.node_tree.links
  if node_texture:
    link = links.new(node_texture.outputs[0], node_principled.inputs['Base Color'])
  if node_normalmap:
    link = links.new(node_normalmap.outputs[0], node_normalvector.inputs[1])
    link = links.new(node_normalvector.outputs[0], node_principled.inputs['Normal']) #needs to find the link by name, doesn't connect otherwise??
  link = links.new(node_principled.outputs[0], node_output.inputs[0])
  if node_noise and node_math:
    link = links.new(node_noise.outputs[1], node_math.inputs[0])
    link = links.new(node_math.outputs[0], node_output.inputs[2])
  return mat


def setup_transparent_shader(mat, col):
  nodes = mat.node_tree.nodes
  for node in nodes:
    nodes.remove(node)
  node_transparent = nodes.new(type="ShaderNodeBsdfTransparent")
  node_transparent.location = 200,0
  col = [x*0.2 + 0.8 for x in col]
  if len(col) == 3:
    ccolor = [0,0,0,1]
    ccolor[:3] = col
    col = tuple(ccolor)
  col = [x**2.2 for x in col] # gamma correction
  node_transparent.inputs[0].default_value = col
  node_output = nodes.new(type='ShaderNodeOutputMaterial')   
  node_output.location = 600,0
  links = mat.node_tree.links
  link = links.new(node_transparent.outputs[0], node_output.inputs[0])
  return mat

def setupShadowCatcher(mat_name, color):
  # Create EEVEE shadow catcher material
  mat = bpy.data.materials.new(name="EEVEE_Shadow_Catcher")
  mat.use_nodes = True
  
  # Set material properties
  mat.alpha_threshold = 0.5
  mat.blend_method = 'BLEND'
  mat.displacement_method = 'BUMP'
  mat.preview_render_type = 'SPHERE'
  if hasattr(mat, 'surface_render_method'):
    mat.surface_render_method = 'BLENDED'
  mat.show_transparent_back = True
  if hasattr(mat, 'use_transparency_overlap'):
    mat.use_transparency_overlap = True
  if hasattr(mat, 'use_transparent_shadow'):
    mat.use_transparent_shadow = True
  
  # Setup node tree
  shader_nodetree = mat.node_tree
  
  # Clear existing nodes
  for node in shader_nodetree.nodes:
    shader_nodetree.nodes.remove(node)
  
  # Create nodes
  material_output = shader_nodetree.nodes.new("ShaderNodeOutputMaterial")
  material_output.name = "Material Output"
  material_output.location = (645.79248046875, 323.4210205078125)
  material_output.is_active_output = True
  material_output.target = 'ALL'
  
  transparent_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfTransparent")
  transparent_bsdf.name = "Transparent BSDF"
  transparent_bsdf.location = (-114.39779663085938, 133.02207946777344)
  transparent_bsdf.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
  
  emission = shader_nodetree.nodes.new("ShaderNodeEmission")
  emission.name = "Emission"
  emission.location = (-105.24452209472656, 245.03561401367188)
  emission.inputs[0].default_value = (0.0, 0.0, 0.0, 1.0)
  emission.inputs[1].default_value = 1.0
  
  diffuse_bsdf = shader_nodetree.nodes.new("ShaderNodeBsdfDiffuse")
  diffuse_bsdf.name = "Diffuse BSDF"
  diffuse_bsdf.location = (-447.9857482910156, 342.8215026855469)
  diffuse_bsdf.inputs[0].default_value = (0.800000011920929, 0.800000011920929, 0.800000011920929, 1.0)
  diffuse_bsdf.inputs[1].default_value = 0.0
  
  shader_to_rgb = shader_nodetree.nodes.new("ShaderNodeShaderToRGB")
  shader_to_rgb.name = "Shader to RGB"
  shader_to_rgb.location = (-225.2999267578125, 353.6590576171875)
  
  color_ramp = shader_nodetree.nodes.new("ShaderNodeValToRGB")
  color_ramp.name = "Color Ramp"
  color_ramp.location = (-29.011865615844727, 481.9655456542969)
  color_ramp.color_ramp.color_mode = 'RGB'
  color_ramp.color_ramp.hue_interpolation = 'NEAR'
  color_ramp.color_ramp.interpolation = 'LINEAR'
  
  # Setup color ramp elements
  color_ramp.color_ramp.elements.remove(color_ramp.color_ramp.elements[0])
  color_ramp_cre_0 = color_ramp.color_ramp.elements[0]
  color_ramp_cre_0.position = 0.0
  color_ramp_cre_0.alpha = 1.0
  color_ramp_cre_0.color = (0.0, 0.0, 0.0, 1.0)
  
  color_ramp_cre_1 = color_ramp.color_ramp.elements.new(0.8454546928405762)
  color_ramp_cre_1.alpha = 1.0
  color_ramp_cre_1.color = (1.0, 1.0, 1.0, 1.0)
  
  mix_shader = shader_nodetree.nodes.new("ShaderNodeMixShader")
  mix_shader.name = "Mix Shader"
  mix_shader.location = (304.4345703125, 282.4414978027344)
  
  # Create links
  shader_nodetree.links.new(diffuse_bsdf.outputs[0], shader_to_rgb.inputs[0])
  shader_nodetree.links.new(shader_to_rgb.outputs[0], color_ramp.inputs[0])
  shader_nodetree.links.new(color_ramp.outputs[0], mix_shader.inputs[0])
  shader_nodetree.links.new(mix_shader.outputs[0], material_output.inputs[0])
  shader_nodetree.links.new(emission.outputs[0], mix_shader.inputs[1])
  shader_nodetree.links.new(transparent_bsdf.outputs[0], mix_shader.inputs[2])
  
  return mat

def setupAlphaOverCompositor(scene=None):
  """Setup Alpha Over compositor node tree for when environment is not visible"""
  if scene is None:
    scene = bpy.context.scene
  
  # Enable compositing
  scene.use_nodes = True
  
  # Get compositor node tree
  if bpy.app.version < (5, 0, 0):
    compositor_nodes = scene.node_tree
  else:
    scene.compositing_node_group = bpy.data.node_groups.new(type='CompositorNodeTree', name="Compositor Nodes")
    compositor_nodes = scene.compositing_node_group
  
  # Clear existing nodes
  for node in compositor_nodes.nodes:
    compositor_nodes.nodes.remove(node)
  
  compositor_nodes.color_tag = 'NONE'
  compositor_nodes.description = ""
  compositor_nodes.default_group_node_width = 140
  
  # Create interface sockets for Blender 5.0+
  if bpy.app.version >= (5, 0, 0):
    # Output socket
    image_socket = compositor_nodes.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'
    
    # Input socket
    image_socket_1 = compositor_nodes.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.default_input = 'VALUE'
    image_socket_1.structure_type = 'AUTO'
  
  # Create nodes
  
  # Group Output (for Blender 5.0+) or Composite Output (for older versions)
  if bpy.app.version >= (5, 0, 0):
    group_output = compositor_nodes.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True
    group_output.location = (200.0, 0.0)
    group_output.width = 140.0
    group_output.height = 100.0
    output_node = group_output
  else:
    composite = compositor_nodes.nodes.new("CompositorNodeComposite")
    composite.name = "Composite"
    composite.location = (200.0, 0.0)
    composite.width = 140.0
    composite.height = 100.0
    output_node = composite
  
  # Render Layers
  render_layers = compositor_nodes.nodes.new("CompositorNodeRLayers")
  render_layers.name = "Render Layers"
  render_layers.layer = 'ViewLayer'
  render_layers.location = (-529.6492919921875, -2.9944028854370117)
  render_layers.width = 240.0
  render_layers.height = 100.0
  
  # Reroute
  reroute = compositor_nodes.nodes.new("NodeReroute")
  reroute.name = "Reroute"
  reroute.socket_idname = "NodeSocketColor"
  reroute.location = (100.0, -35.0)
  reroute.width = 10.0
  reroute.height = 100.0
  
  # Viewer
  viewer = compositor_nodes.nodes.new("CompositorNodeViewer")
  viewer.name = "Viewer"
  viewer.ui_shortcut = 0
  viewer.location = (200.0, -80.0)
  viewer.width = 140.0
  viewer.height = 100.0
  
  # Alpha Over
  alpha_over = compositor_nodes.nodes.new("CompositorNodeAlphaOver")
  alpha_over.name = "Alpha Over"
  alpha_over.location = (-172.06793212890625, 3.49346923828125)
  alpha_over.width = 140.0
  alpha_over.height = 100.0
  
  # Set Alpha Over properties
  alpha_over.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)  # Background
  alpha_over.inputs[2].default_value = 1.0  # Fac
  if bpy.app.version >= (5, 0, 0):
    alpha_over.inputs[3].default_value = 'Over'  # Type
    alpha_over.inputs[4].default_value = False  # Straight Alpha
  
  # Create links
  
  # reroute -> output
  if bpy.app.version >= (5, 0, 0):
    compositor_nodes.links.new(reroute.outputs[0], output_node.inputs[0])
  else:
    compositor_nodes.links.new(reroute.outputs[0], output_node.inputs[0])
  
  # reroute -> viewer
  compositor_nodes.links.new(reroute.outputs[0], viewer.inputs[0])
  
  # render_layers -> alpha_over (Image to Foreground)
  compositor_nodes.links.new(render_layers.outputs[0], alpha_over.inputs[1])
  
  # alpha_over -> reroute
  compositor_nodes.links.new(alpha_over.outputs[0], reroute.inputs[0])
  
  return compositor_nodes