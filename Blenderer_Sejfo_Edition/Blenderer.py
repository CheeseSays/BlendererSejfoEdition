#
# Blenderer Addon version 2023-06-16 v2.3.X 
# Blenderer Modification version 2026-01-26 v1.1-Blender5 by andreas.wetter@sejfo.se
# - Added prototype for exporting properties and metadata to Blender
# - Made the addon Blender 5.0 compatible (Might still work with 3.6+)
# - On import to Blender, animation data on static objects is removed to avoid bloating the file.
# - External resources are now packed into the .blend file on export
#
from vcCommand import *
import vcHelpers.Selection as selection
from collections import defaultdict
import vcMatrix, vcVector
import os, sys, os.path, csv
import json
import math
import subprocess
import time
import sys
import xml.etree.cElementTree as ET
import export_from_vc
import tempfile, shutil
from pprint import pprint
reload(export_from_vc)


DEG2RAD = math.radians(1)
RAD2DEG = math.degrees(1)
LINECHANGE = '\n'
cmd = getCommand()
app = getApplication()
app2 = getApplication() #two app objects for two separate OnRender events
camera = app.findCamera()


sim = getSimulation()
SCALE = 0.001
rec_file = False


def OnStart():
  global blender_exe_uri, blender_exe_uri_prop, prop_defaults_xml_uri, prop_defaults_xml_tree, prop_defaults_dict
  reload( export_from_vc )
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  thefolder = thefolder.decode('utf8')
  # clear possible render limit frame
  geocont = sim.World.UserGeometry
  geocont.clear()
  app.render()
  #
  # read default settings
  #
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  prop_defaults_xml_uri = os.path.join(thefolder,'defaults.xml')
  prop_defaults_xml_uri = prop_defaults_xml_uri.decode('utf8')
  prop_defaults_xml_tree = ET.parse(prop_defaults_xml_uri)
  prop_defaults_dict = {}
  for child in prop_defaults_xml_tree.getroot():
    prop_defaults_dict[child.attrib['name']] = child.attrib['value']
  #
  # # DEFAULT TAB
  #
  global openinblenderProp, filepathProp, tempuriProp, samplesProp, resProp, resXProp, resYProp, portraitProp, reRender_prop, renderstill_prop, presetProp, preset_tree, temproot_uri
  try:
    # Try using windows user's Pictures folder as default
    pictures = os.path.join(os.environ["USERPROFILE"], "Pictures")
    renderuri = os.path.join(pictures, 'Blenderer', 'Picture.png')
  except:
    # if fails, use output fodler in the command folder as default
    renderuri = os.path.join('file///:', thefolder, 'Output', 'Picture.png')
  renderuri = renderuri.decode('utf8')
  filepathProp = getProp(VC_URI, 'Output file', str(renderuri), visible = True, overwrite = False)
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  temp_dir = tempfile.gettempdir()
  temproot_uri = os.path.join(temp_dir,'blenderer_temp')
  if not os.path.exists(temproot_uri):
    os.makedirs(temproot_uri)
  tempdata_uri = os.path.join(temproot_uri, 'TEMPDATA')
  if not os.path.exists(tempdata_uri):
    os.makedirs(tempdata_uri)
  #tempdata_uri = 'file///:' + tempdata_uri
  tempdata_uri = tempdata_uri.decode('utf8')
  tempuriProp = getProp(VC_URI, 'TEMPDATA_URI', str(tempdata_uri), visible = False, overwrite = False)
  samplesProp = getProp(VC_INTEGER, 'Samples', 16, visible = True, overwrite = False)
  #
  res_list = ['<Custom>', '300x300', '384x216', '640x360', '640x640' ,'1280x720', '1920x1080', '3840x2160']
  resProp = getProp(VC_STRING, 'Resolution', '1920x1080', steps = res_list, limits = [], visible = True, overwrite = False)
  resXProp = getProp(VC_INTEGER, 'ResX', 1920, visible = True, overwrite = False)
  resYProp = getProp(VC_INTEGER, 'ResY', 1080, visible = True, overwrite = False)
  resXProp.OnChanged = showBorderChangedEvent
  resYProp.OnChanged = showBorderChangedEvent
  resXProp.WritableWhenConnected = False
  resXProp.WritableWhenDisconnected = False
  resYProp.WritableWhenConnected = False
  resYProp.WritableWhenDisconnected = False
  portraitProp = getProp(VC_STRING, 'Page', 'Landscape', steps = ['Landscape', 'Portrait'], visible = True, overwrite = False)
  portraitProp.OnChanged = fovChangedEvent
  resProp.OnChanged = resChanged
  tree = getPresetTree()
  preset_tree = tree.getroot()
  preset_names = [x.get('name') for x in preset_tree]
  stepvals = preset_names
  #stepvals.sort()
  presetProp = getProp(VC_STRING, 'Lighting Preset', stepvals[0], steps = stepvals, visible = True, overwrite = False)
  if stepvals != presetProp.StepValues:
    presetProp.StepValues = stepvals

  presetProp.OnChanged = setEnvHDRI
  renderstill_prop = getProp(VC_BUTTON, 'Render', True, visible = True, overwrite = False)
  reRender_prop = getProp(VC_BOOLEAN, 'Reuse Previous Scene', False, visible = True, overwrite = False)
  openinblenderProp = getProp(VC_BOOLEAN, 'Open in Blender', False, visible = True, overwrite = False)
  renderstill_prop.OnChanged = CallStill
  #   
  # LIGHTS TAB
  global addPointLightProp, addAreaLightProp, addSpotLightProp, addSunLightProp, lightStrengthProp, addSparksProp
  addPointLightProp = getProp(VC_BUTTON, 'Lights::Add Point Light', False, visible = True, overwrite = False)
  addPointLightProp.OnChanged = addLamp
  addAreaLightProp = getProp(VC_BUTTON, 'Lights::Add Area Light', False, visible = True, overwrite = False)
  addAreaLightProp.OnChanged = addLamp
  addSpotLightProp = getProp(VC_BUTTON, 'Lights::Add Spot Light', False, visible = True, overwrite = False)
  addSpotLightProp.OnChanged = addLamp
  addSunLightProp = getProp(VC_BUTTON, 'Lights::Add Sun Light', False, visible = True, overwrite = False)
  addSunLightProp.OnChanged = addLamp
  lightStrengthProp = getProp(VC_REAL, 'Lights::Default Strength', 500, visible = True, overwrite = False)
  addSparksProp = getProp(VC_BUTTON, 'Lights::Add Sparks Emitter', False, visible = True, overwrite = False)
  addSparksProp.OnChanged = addSparks
  #
  # ADVANCED TAB
  global indirectLightProp, renderedgesProp, engeThicknessProp, fovProp, showBorderProp, exposureProp, bloomProp, bloomIntensityProp
  global deviceProp, exportComponentsProp
  global depthOFnodeProp, depthOfFstopProp, cameraProp, viewProp, reset_props_prop
  fovProp = getProp(VC_REAL, 'Advanced::CameraFov', 33.0, visible = True, overwrite = False, unit = 'Angle', magnitude = 1.0)
  showBorderProp = getProp(VC_BOOLEAN, 'Advanced::Show Border', False, visible = True, overwrite = False)
  fovProp.OnChanged = fovChangedEvent
  showBorderProp.OnChanged = showBorderChangedEvent
  exposureProp = getProp(VC_REAL, 'Advanced::Exposure', 0.0, visible = True, overwrite = False)
  bloomProp = getProp(VC_BOOLEAN, 'Advanced::Bloom', False, visible = True, overwrite = False)
  bloomIntensityProp = getProp(VC_REAL, 'Advanced::Bloom Intensity', 0.1, visible = True, overwrite = False)
  #openinblenderProp = getProp(VC_BOOLEAN, 'Advanced::Open in Blender', False, visible = True, overwrite = False)
  deviceProp = getProp(VC_STRING, 'Advanced::RenderDevice', 'GPU', steps = ['CPU', 'GPU'], visible = True, overwrite = False)
  renderedgesProp = getProp(VC_BOOLEAN, 'Advanced::Render Edges', False, visible = True, overwrite = False)
  engeThicknessProp = getProp(VC_INTEGER, 'Advanced::Edge Thickness', 3, visible = True, overwrite = False)
  depthOFnodeProp = getProp('Ref<Node>', 'Advanced::DepthOfFieldNode', None, visible = True, overwrite = False)
  depthOfFstopProp = getProp(VC_REAL, 'Advanced::Depth F-Stop', 2.8, visible = True, overwrite = False) 
  indirectLightProp = getProp(VC_STRING, 'Advanced::Indirect Lighting', 'Off', steps = ['Off', 'Fast', 'Normal', 'HQ'], visible = True, overwrite = False)
  blender_exe_uri_prop = getProp(VC_URI, 'Advanced::Blender Executable', '', visible = True, overwrite = False)
  exportComponentsProp = getProp('List<Ref<Component>>', 'Advanced::Export Components', [], visible = True, overwrite = False)
  reset_props_prop = getProp(VC_BUTTON, 'Advanced::Reset All Properties', True, visible = True, overwrite = False)
  reset_props_prop.OnChanged = reset_all_props
  #
  # MATERIALS TAB
  global materialTableProp, tableSeparatorProp, robotMaterials, monochromeProp, simpleTransparentProp, glassVersionProp
  materialTableProp = getProp(VC_STRING, 'Materials::Mode', 'Default', steps = ['Default','Read From Table', 'Write To Table'], visible = True, overwrite = False)
  tableSeparatorProp = getProp(VC_STRING, 'Materials::Table Delimiter', ';', steps = [';', ','], visible = True, overwrite = False)
  robotMaterials = getProp(VC_STRING, 'Materials::Robot Materials', 'Smart Materials', steps = ['Default', 'Smart Materials'], visible = True, overwrite = False)
  monochromeProp = getProp('Ref<Material>', 'Materials::Monochrome Override', None, visible = True, overwrite = False)
  simpleTransparentProp = getProp(VC_BOOLEAN, 'Materials::UseSimpleTransparent', False, visible = True, overwrite = False)
  glassVersionProp = getProp(VC_INTEGER, 'Materials::Glass Version', 1, steps=[0,1], visible=True, overwrite=False)
  # 
  # ANIMATION TAB
  global recanim_prop, startanim_prop, endanim_prop, stepanim_prop, fpsanim_prop, videocontainer_prop, renderanim_prop
  recanim_prop = getProp(VC_BOOLEAN, 'Animation::RecAnimation', False, visible = True, overwrite = True)
  recanim_prop.OnChanged = InitAnim
  startanim_prop = getProp(VC_REAL, 'Animation::Start', 5.0, visible = True, overwrite = False, unit = 'Time', magnitude = 1.0)
  endanim_prop = getProp(VC_REAL, 'Animation::End', 10.0, visible = True, overwrite = False, unit = 'Time', magnitude = 1.0)
  stepanim_prop = getProp(VC_REAL, 'Animation::Rec step', 1.0/25.0, visible = True, overwrite = False, unit = 'Time', magnitude = 1.0)
  stepanim_prop.OnChanged = InitAnim
  fpsanim_prop = getProp(VC_INTEGER, 'Animation::FPS', 25, visible = True, overwrite = False)
  videocontainer_prop = getProp(VC_STRING, 'Animation::Container', 'MP4', steps = ['MP4'], visible = True, overwrite = False)
  renderanim_prop = getProp(VC_BUTTON, 'Animation::RenderAnimation', True, visible = True, overwrite = False)
  renderanim_prop.OnChanged = CallAnim
  #
  # ENV TAB
  global envtypeProp, envimageProp, envcolorProp, envstrengthProp, envRotationProp, envvisibleProp
  global backdropTypeProp, backdropImageProp, backdropRgbProp
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  envmapuri = ''
  hdri_strength = 0
  current_preset = [x for x in preset_tree if x.get("name") == presetProp.Value]
  if current_preset:
    current_preset = current_preset[0]
    hdri_element = current_preset.find('hdri')
    if hdri_element!=None: # must compare to none
      hdri_uri = hdri_element.get('file')
      hdri_uri = hdri_uri.decode('utf8')
      hdri_strength = hdri_element.get('strength')
      envmapuri = os.path.join('file:///', thefolder , 'Lights\\Presets' , hdri_uri)
  envtypeProp = getProp(VC_STRING, 'Env::Background', 'Image', steps = ['Image', 'ColorRGB'], visible = True, overwrite = False)
  envtypeProp.OnChanged = envtypeChanged
  envimageProp = getProp(VC_URI, 'Env::Image', envmapuri, visible = True, overwrite = False)
  envcolorProp = getProp(VC_VECTOR, 'Env::ColorRGB', vcVector.new(1,1,1), visible = False, overwrite = False)
  envstrengthProp = getProp(VC_REAL, 'Env::Strength', 2.0, visible = True, overwrite = False)
  envstrengthProp.Value = float(hdri_strength)
  envRotationProp = getProp(VC_REAL, 'Env::Rotation', 0.0, visible = True, overwrite = False)
  envvisibleProp = getProp(VC_BOOLEAN, 'Env::Visible', True, visible = True, overwrite = False)
  envvisibleProp.OnChanged = backdrop_props_visibility
  backdropTypeProp = getProp(VC_STRING, 'Env::BackdropType', 'None', steps = ['None', 'Image', 'ColorRGB'], visible = True, overwrite = False)
  backdropTypeProp.OnChanged = backdrop_props_visibility
  backdropImageProp = getProp(VC_URI, 'Env::BackdropImage', envmapuri, visible = True, overwrite = False)
  backdropRgbProp = getProp(VC_VECTOR, 'Env::BackdropColorRGB', vcVector.new(1,1,1), visible = True, overwrite = False)
  backdrop_props_visibility('void')

  #
  # FLOOR TAB
  global floorvisibleProp, floorsizeProp, floortypeProp, floorcolorimageProp, floorbumpimageProp, floortexturesizeProp, floorcolorProp, floorbumpstrengthProp
  floorvisibleProp = getProp(VC_BOOLEAN, 'Floor::Visible', True, visible = True, overwrite = False)
  floorsizeProp = getProp(VC_REAL, 'Floor::BorderSize', 6000, visible = True, overwrite = False, unit = 'Distance', magnitude = 1.0)
  floortypes_list = sorted(floortextures.keys())
  floortypeProp = getProp(VC_STRING, 'Floor::Style', '<ShadowCatcher>', steps = floortypes_list, visible = True, overwrite = False)
  floorcolorimageProp = getProp(VC_URI, 'Floor::ColorTexture', '', visible = True, overwrite = False)
  floorbumpimageProp = getProp(VC_URI, 'Floor::BumpTexture', '', visible = True, overwrite = False)
  floorbumpstrengthProp = getProp(VC_REAL, 'Floor::BumpStrength', 1.0, visible = True, overwrite = False)
  floortexturesizeProp = getProp(VC_REAL, 'Floor::TextureSize', 1200, visible = True, overwrite = False)
  floorcolorProp = getProp(VC_VECTOR, 'Floor::ColorRGB', vcVector.new(.8,.8,.8), visible = True, overwrite = False)
  floortypeChanged(floortypeProp)
  floortypeProp.OnChanged = floortypeChanged 
  executeInActionPanel()
  #


def backdrop_props_visibility(arg):
  if envvisibleProp.Value == True:
    backdropTypeProp.IsVisible = False
    backdropRgbProp.IsVisible = False
    backdropImageProp.IsVisible = False
  else:
    backdropTypeProp.IsVisible = True
    backdropRgbProp.IsVisible = False
    backdropImageProp.IsVisible = False
    if backdropTypeProp.Value == 'Image':
      backdropImageProp.IsVisible = True
    if backdropTypeProp.Value == 'ColorRGB':
      backdropRgbProp.IsVisible = True



def reset_all_props(arg=None):
  for prop in cmd.Properties:
    cmd.deleteProperty(prop)
  cmd.execute()


def etree_to_dict(t):
  d = {t.tag: {} if t.attrib else None}
  children = list(t)
  if children:
    dd = defaultdict(list)
    for dc in map(etree_to_dict, children):
      for k, v in dc.items():
        dd[k].append(v)
    d = {t.tag: {k:v[0] if len(v) == 1 else v for k, v in dd.items()}}
  if t.attrib:
    d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
  if t.text:
    text = t.text.strip()
    if children or t.attrib:
      if text:
        d[t.tag]['#text'] = text
    else:
      d[t.tag] = text
  return d

def getDefaultValue(pname, ptype):
  value = None
  ok = False
  if pname in prop_defaults_dict:
    raw_value = prop_defaults_dict[pname]
    if ptype == VC_BOOLEAN:
      if raw_value.strip().lower() in ['false', 0]:
        value = False
      else:
        value = True
      ok = True
    elif ptype == VC_INTEGER:
      try:
        value = int(raw_value)
        ok = True
      except Exception, e:
        pass
    elif ptype == VC_REAL:
      try:
        value = float(raw_value)
        ok = True
      except Exception, e:
        pass
    elif ptype == VC_VECTOR:
      try:
        vals = [float(x) for x in raw_value.split('|')]
        value = vcVector.new(*vals)
        ok = True
      except Exception, e:
        pass
    elif ptype == VC_STRING:
      value = raw_value.strip()
      ok = True
    elif ptype == VC_URI:
      value = raw_value.strip()
      ok = True
    else:
      print 'Blenderer: non supported value type in defaults.xml:',ptype,'|', raw_value
    # VC_DISTRIBUTION
    # VC_VECTOR
    # VC_MATRIX
    # VC_EXPRESSION
    # VC_BUTTON
    # List<Ref<Behaviour>>
    # List<Ref<Component>>
    # List<Ref<Feature>>
    # List<Ref<Node>>
    # List<Ref<Parameter>>
    # Ref<Behaviour>
    # Ref<Component>
    # Ref<Feature>
    # Ref<Material>
    # Ref<Node>
    # Ref<Parameter>
  return ok, value


def getProp(ptype, pname, pval, steps = [], limits = [], visible = True, overwrite = False, unit = '', magnitude = 1.0):
  default_available, default_value = False, ''
  owner = cmd
  p = owner.getProperty(pname)
  if not p:
    default_available, default_value = getDefaultValue(pname, ptype)
  if p and overwrite:
    owner.deleteProperty(p)
  elif p:
    if default_available:
      p.Value = default_value
    return p
  if steps:
    p = owner.createProperty(ptype,pname,VC_PROPERTY_STEP)
    p.StepValues = steps
  elif limits:
    p = owner.createProperty(ptype,pname,VC_PROPERTY_LIMIT)
    p.MinLimits = limits[0]
    p.MaxLimits = limits[1]
  else:
    p = owner.createProperty(ptype,pname)
  if ptype != VC_BUTTON:
    if default_available:
      pval = default_value
    if type(pval)==unicode:
      pval = str(pval)
    p.Value = pval
  p.IsVisible = visible
  if unit:
    p.Quantity = unit
    p.Magnitude = magnitude
  return p


def sanitizefilename(fname):
  suspiciouscharacters = [r'/', '\\' ,'#',':',';','!','¤','%','&','?','^','*',' ','\t']
  for c in suspiciouscharacters:
    fname = fname.replace(c,'_')
  return fname


def resChanged(arg):
  if resProp.Value == '<Custom>':
    resXProp.WritableWhenConnected = True
    resXProp.WritableWhenDisconnected = True
    resYProp.WritableWhenConnected = True
    resYProp.WritableWhenDisconnected = True
  else:
    resXProp.WritableWhenConnected = False
    resXProp.WritableWhenDisconnected = False
    resYProp.WritableWhenConnected = False
    resYProp.WritableWhenDisconnected = False
    vals = [int(x) for x in resProp.Value.split('x')]
    resXProp.Value = vals[0]
    resYProp.Value = vals[1]


def create_config_XML(uri, framecount):
  uri = uri.decode('utf8')
  settings_dict = {}
  settings_dict['engine'] = 'BLENDER_EEVEE'
  settings_dict['re_render'] = str(reRender_prop.Value)
  res = [resXProp.Value, resYProp.Value]
  portrait = portraitProp.Value == 'Portrait'
  res = res[::-1] if portrait else res
  settings_dict['resolution_x'] = res[0]
  settings_dict['resolution_y'] = res[1]
  settings_dict['samples'] = samplesProp.Value
  settings_dict['filepath'] = str(filepathProp.Value).replace(r'file:///','')
  #
  settings_dict['resolution_percentage'] = 100
  settings_dict['openinblender'] = openinblenderProp.Value
  settings_dict['frame_start'] = 0
  settings_dict['frame_end'] = framecount
  settings_dict['anim_fps'] = fpsanim_prop.Value
  settings_dict['video_container'] = videocontainer_prop.Value
  if framecount:
    print 'Animation rendering: %i frames' % framecount
  portrait = portraitProp.Value == 'Portrait'
  xRes = resYProp.Value if portrait else resXProp.Value
  yRes = resXProp.Value if portrait else resYProp.Value
  dist = (yRes/2.0)/(math.tan(fovProp.Value/2.0*DEG2RAD))
  fov = fovProp.Value if portrait else math.atan(xRes/2.0/dist)*2*RAD2DEG # convert vertical res to horizontal in non portrait
  settings_dict['CameraFOV'] = fov
  settings_dict['device'] = deviceProp.Value
  settings_dict['use_renderedges'] = renderedgesProp.Value
  if monochromeProp.Value:
    monochrome_material = monochromeProp.Value
    mono_r = monochrome_material.Diffuse.X
    mono_g = monochrome_material.Diffuse.Y
    mono_b = monochrome_material.Diffuse.Z
    settings_dict['monochrome'] = '|'.join([str(mono_r), str(mono_g), str(mono_b)])
  else:
    settings_dict['monochrome'] = ''

  settings_dict['use_simple_transparent'] = simpleTransparentProp.Value
  settings_dict['edge_line_thickness'] = engeThicknessProp.Value
  settings_dict['depth_fstop'] = depthOfFstopProp.Value
  settings_dict['indirect_lighting'] = indirectLightProp.Value
  if depthOFnodeProp.Value:
    node = depthOFnodeProp.Value
    node_name = get_node_name(node)
  else:
    node_name = ''
  settings_dict['depthOFnode'] = node_name
  settings_dict['exposure'] = exposureProp.Value
  settings_dict['bloom'] = bloomProp.Value
  settings_dict['bloomintensity'] = bloomIntensityProp.Value
  #
  settings_dict['envimage'] = envimageProp.Value.replace('file:///','')
  settings_dict['envstrength'] = envstrengthProp.Value
  settings_dict['envrotation'] = envRotationProp.Value
  settings_dict['envtype'] = envtypeProp.Value
  rgb_vec = envcolorProp.Value
  settings_dict['envcolor'] = '%s;%s;%s' % (rgb_vec.X, rgb_vec.Y, rgb_vec.Z)
  settings_dict['envvisible'] = envvisibleProp.Value

  settings_dict['backdroptype'] = backdropTypeProp.Value
  backdrop_rgb_vec = backdropRgbProp.Value
  settings_dict['backdropcolor'] = '%s;%s;%s' % (backdrop_rgb_vec.X, backdrop_rgb_vec.Y, backdrop_rgb_vec.Z)
  settings_dict['backdropimage'] = backdropImageProp.Value.replace('file:///','')
  #
  settings_dict['floorvisible'] = floorvisibleProp.Value
  settings_dict['floorsize'] = floorsizeProp.Value
  settings_dict['floortype'] = floortypeProp.Value
  settings_dict['floorcolorimage'] = floorcolorimageProp.Value.replace(r'file:///','')
  settings_dict['floorbumpimage'] = floorbumpimageProp.Value.replace(r'file:///','')
  settings_dict['floorbumpstrength'] = str(floorbumpstrengthProp.Value)
  rgb_vec = floorcolorProp.Value
  settings_dict['floorcolor'] = '%s;%s;%s' % (rgb_vec.X, rgb_vec.Y, rgb_vec.Z)
  settings_dict['floortexturesize'] = floortexturesizeProp.Value*SCALE
  settings_dict['scene_bound'] = str([x*SCALE for x in threeD_bound])
  settings_dict['floor_overshoot'] = str(floorsizeProp.Value*SCALE)

  root = ET.Element("RenderSettings")
  for key, item in settings_dict.iteritems():
    ET.SubElement(root, key).text = str(item)
  settings_tree = ET.ElementTree(root)
  settings_tree.write(uri, 'UTF-8')


def parentVisible(n):
  if not n.Visible:
    return False
  if n.Parent and not parentVisible(n.Parent):
    return False
  return True


def hasgeometry(n, rebuild_flag = False):
  hasgeometry = False
  if rebuild_flag:
    n.rebuild()
  if n.Component.getProperty('ShowWhenSimulating') and not n.Component.getProperty('ShowWhenSimulating').Value:
    return False
  if not parentVisible(n):
    return False
  for gs in n.Geometry.GeometrySets:
    if gs.Type == VC_TRIANGLESET:
      if gs.PointCount > 0:
        hasgeometry = True
        return True
  return False


def exportType(x):
  if x.Type in [VC_NODE]: # comp fails this test
    if x.Parent.Type == VC_COMPONENT and x.Parent.getProperty('BLENDER_OBJECT_TYPE') and x.Parent.getProperty('BLENDER_OBJECT_TYPE').Value == 'SPARKS':
      return 'SPARKS_VISUAL'
    return 'NODE'
  type_prop = x.getProperty('BLENDER_OBJECT_TYPE')
  if type_prop:
    return type_prop.Value
  else:
    return 'NODE'


def findAllNodes():
  nodes = []
  # Check if specific components were selected
  if exportComponentsProp.Value and len(exportComponentsProp.Value) > 0:
    selected_comps = list(exportComponentsProp.Value)
    
    print '--- Export Specific Components is ENABLED ---'
    print 'SUCCESS: Exporting %d selected component(s):' % len(selected_comps)
    for comp in selected_comps:
      print '  - %s' % comp.Name
    
    components_to_export = selected_comps
  else:
    components_to_export = app.Components
    print 'Export Components is empty. Exporting all %d components.' % len(list(app.Components))
  
  for c in components_to_export:
    nodes.append(c)
    kids = [x for x in c.Children if x.Type == VC_NODE]
    while kids:
      k = kids.pop(0)
      nodes.append(k)
      kids.extend([x for x in k.Children if x.Type == VC_NODE])
  return nodes


def setCustomDataProps(material_name, custom_data_val):
  m = app.findMaterial(material_name)
  if m:
    p = m.createProperty(VC_STRING, 'CustomData')
    p.Value = custom_data_val
  return m


def setBound(node,threeD_bound):
  bd = node.BoundDiagonal
  bc = node.BoundCenter
  V = vcVector.new
  wp = node.WorldPositionMatrix
  corners = [V(bd.X,bd.Y,bd.Z), 
             V(bd.X,-bd.Y,bd.Z), 
             V(-bd.X,-bd.Y,bd.Z), 
             V(-bd.X,bd.Y,bd.Z),
             V(bd.X,bd.Y,-bd.Z), 
             V(bd.X,-bd.Y,-bd.Z), 
             V(-bd.X,-bd.Y,-bd.Z), 
             V(-bd.X,bd.Y,-bd.Z)]
  corners = [wp * (bc+x) for x in corners]
  minX = min([x.X for x in corners])
  maxX = max([x.X for x in corners])
  minY = min([x.Y for x in corners])
  maxY = max([x.Y for x in corners])
  minZ = min([x.Z for x in corners])
  maxZ = max([x.Z for x in corners])
  if minX < threeD_bound[0]:
    threeD_bound[0] = minX
  if maxX > threeD_bound[1]:
    threeD_bound[1] = maxX
  if minY < threeD_bound[2]:
    threeD_bound[2] = minY
  if maxY > threeD_bound[3]:
    threeD_bound[3] = maxY
  if minZ < threeD_bound[4]:
    threeD_bound[4] = minZ
  if maxZ > threeD_bound[5]:
    threeD_bound[5] = maxZ


def get_render_items():
  nodes = findAllNodes()
  all_them_items = [[x, exportType(x)] for x in nodes if hasgeometry(x)]
  camera = app.findCamera()
  all_them_items.insert(0,[camera, 'CAMERA'])
  return all_them_items


def getMaterialFiles():
  global threeD_bound
  materials = {}
  mtl_file = None
  uri_root = cmd.TEMPDATA_URI
  uri_root = uri_root.decode('utf8')
  for root, folders, files in os.walk(uri_root):
    for f in files:
      thisuri = os.path.join( root, f )
      thisuri = thisuri.decode('utf8')
      body, extension = os.path.splitext( f )
      if reRender_prop.Value and extension == '.blend':
        # do not delete the blend file as it is used for re-rendering same scene
        continue
      os.remove(thisuri)
  threeD_bound = [9999999,-9999999,9999999,-9999999,9999999,-999999]
  material_table_csv = None
  material_data_dict = {}
  if materialTableProp.Value == 'Write To Table':
    thefolder, commandfilename = os.path.split(getCommandPath()[8:])
    material_table_csv_uri = os.path.join(thefolder, 'materials.csv')
    material_table_csv_uri = material_table_csv_uri.decode('utf8')
    try:
      material_table_csv = open(material_table_csv_uri, 'w')
      SEP = tableSeparatorProp.Value
      material_table_csv.write(SEP.join(material_columns)+LINECHANGE)
    except:
      material_table_csv = None
      print 'Unable to open table file for writing "%s"' % material_table_csv_uri
      print 'Make sure it is not open in another software.'
  elif materialTableProp.Value == 'Read From Table':
    thefolder, commandfilename = os.path.split(getCommandPath()[8:])
    material_table_csv_uri = os.path.join(thefolder, 'materials.csv')
    material_table_csv_uri = material_table_csv_uri.decode('utf8')
    with open(material_table_csv_uri, 'r') as material_table_csv:
      SEP = tableSeparatorProp.Value
      tablereader = csv.reader(material_table_csv, delimiter=SEP)
      tablereader.next() #skip header
      for csvline in tablereader:
        csvline = list(csvline)
        material_data_dict[csvline[0]] = {}
        for title, csv_value in zip(material_columns, csvline)[1:]:
          material_data_dict[csvline[0]][title] = csv_value
  return materials, mtl_file, material_table_csv, material_data_dict


def getAllMaterials():
  materials = set()
  nodes = sim.World.Children
  i=0
  while nodes:
    i+=1
    node = nodes.pop(0)
    nodes.extend(node.Children)
    materials.update([x.Material.Name for x in node.Geometry.GeometrySets if x.Type == VC_TRIANGLESET and x.Material])
  return list(materials)


def exportGeo(items,
              materials, 
              mtl_file, 
              material_table_csv, 
              material_data_dict):
  global threeD_bound
  # loop layout content
  uri_root = cmd.TEMPDATA_URI
  uri_root = uri_root.decode('utf8')
  # Initialize metadata collection
  metadata_collection = {}
  for node, object_type in items:
    try:
      node.Name
      dead = False
    except:
      dead = True
    if dead:
      continue
    if object_type in ['CAMERA', 'RECORDER', 'POINT_LIGHT', 'AREA_LIGHT', 'SUN_LIGHT', 'SPOT_LIGHT', 'SPARKS_VISUAL']:
      # skip abstract components. Geometry not exported
      continue
    if node.Type in [VC_COMPONENT, VC_NODE]:
      setBound(node,threeD_bound)
    node_name = get_node_name(node)
    fileuri = os.path.join(uri_root, node_name+'.obj')
    fileuri = fileuri.decode('utf8')
    SEP = tableSeparatorProp.Value
    ok, materials, mtl_file = export_from_vc.export_obj( app, 
                                                              node, 
                                                              materials, 
                                                              mtl_file, 
                                                              SCALE, 
                                                              fileuri, 
                                                              materialTableProp.Value, 
                                                              material_table_csv, 
                                                              material_data_dict, 
                                                              SEP,
                                                              reRender_prop.Value,
                                                              robotMaterials.Value == 'Smart Materials' )
    # Collect metadata for this node
    metadata_collection[node_name] = export_from_vc.export_metadata(node, temproot_uri)

  metadata_file = os.path.join(uri_root, 'object_metadata.json')
  with open(metadata_file, 'w') as mf:
    json.dump(metadata_collection, mf, indent=2)
  return materials, mtl_file, material_table_csv, material_data_dict


def get_node_name(node):
  if node.Type == VC_COMPONENT:
    #comp name
    node_name = node.Name
    item_component = node
  else:
    #comp name + node name
    node_name = '%s__%s'  % (node.Component.Name, node.Name)
    item_component = node.Component
  if item_component.Product:
    node_name += '_PRD_' + item_component.Product.ProductType.Name
  node_name = sanitizefilename(node_name)
  node_name = node_name.encode('utf-8') # not helping.. assigning to a list screws things up
  return node_name

prev_cam_id = ''

def recKeyFrame(items, rec_data, animation = False):
  global preset_tree, keyframe_index_c, prev_cam_id
  sim.update()
  keyframe_index_c = int(round((sim.SimTime-startanim_prop.Value) / stepanim_prop.Value))
  for i, token in enumerate(items):
    item, item_type = token
    item_component = None #set for node types later
    deadComponent = False
    try:
      item.Name #this fails if a component has disappeared from the layout (dynamic comps during animation)
    except:
      deadComponent = True
    if item_type == 'CAMERA':
      # element is camera
      object_name = 'VC_TO_BLENDER_CAMERA_OBJECT'
      if deadComponent or item is None:
        if keyframe_index == 0:
          object_data = []
          position_data = (keyframe_index_c, 0, 0, 0, 0, 0, 0)
        else:
          position_data = rec_data[i][3][-1]
      else:
        mtx = item.Matrix
        rot = mtx.WPR
        eye = item.Eye
        coi = item.Coi
        position_data = keyframe_index_c, eye.X*SCALE, eye.Y*SCALE, eye.Z*SCALE, coi.X*SCALE, coi.Y*SCALE, coi.Z*SCALE
        title_line = 'addon: t%.2f; ' % (sim.SimTime)
        cam_id = 'x=%.2f; y=%.2f; z=%.2f; mtx.Y=%.2f' % (eye.X*SCALE, eye.Y*SCALE, eye.Z*SCALE, mtx.P.Y)
        if cam_id == prev_cam_id:
          pass
          #print title_line + cam_id, ' <= same'
        else:
          pass
          #print title_line + cam_id
        prev_cam_id = cam_id
        if keyframe_index == 0:
          object_data = []
    elif item_type == 'SPARKS':
      object_name = item.Name
      object_name = sanitizefilename(object_name)
      if keyframe_index == 0:
        rgb = (item.R/255.0, item.G/255.0, item.B/255.0, 1.0)
        object_data = [rgb, item.DimGlobalLighting]
      mtx = item.WorldPositionMatrix
      rot = mtx.WPR
      sx = mtx.N.length()
      sy = mtx.O.length()
      sz = mtx.A.length()
      spark_on = 2.0 if item.findBehaviour('SparksSignal').Value else 0.0
      position_data = keyframe_index_c, mtx.P.X*SCALE, mtx.P.Y*SCALE, mtx.P.Z*SCALE, rot.X*DEG2RAD, rot.Y*DEG2RAD, rot.Z*DEG2RAD, sx,sy,sz, spark_on
    elif item_type in ['AREA_LIGHT', 'POINT_LIGHT', 'SUN_LIGHT', 'SPOT_LIGHT']:
      object_name = item.Name
      object_name = sanitizefilename(object_name)
      rgb = [item.R, item.G, item.B]
      strength = item.Strength
      if keyframe_index == 0 and item_type in ['AREA_LIGHT']:
        sizeX = item.SizeX*SCALE
        sizeY = item.SizeY*SCALE
        falloff = item.Falloff
        object_data = [rgb, strength, sizeX, sizeY, falloff]
      elif keyframe_index == 0 and item_type in ['POINT_LIGHT']:
        size = item.Size*SCALE
        falloff = item.Falloff
        object_data = [rgb, strength, size, falloff]
      elif keyframe_index == 0 and item_type in ['SUN_LIGHT']:
        size = 0.1
        object_data = [rgb, strength, size]
      elif keyframe_index == 0 and item_type in ['SPOT_LIGHT']:
        size = item.Size*SCALE
        angle = item.Angle
        falloff = item.Falloff
        object_data = [rgb, strength, size, angle, falloff]
      p = item.WorldPositionMatrix.P
      coi = vcMatrix.new(item.WorldPositionMatrix)
      coi.translateRel(0,0,-1000)
      coi = coi.P
      position_data = keyframe_index_c, p.X*SCALE, p.Y*SCALE, p.Z*SCALE, coi.X*SCALE, coi.Y*SCALE, coi.Z*SCALE, strength
    elif item_type == 'NODE':
      if deadComponent:
        position_data = rec_data[i][3][-1] #last keyframe
        position_data = list(position_data)
        # SCALE to zero so that the node disappears
        position_data[-1] = 0
        position_data[-2] = 0
        position_data[-3] = 0
        position_data[0] = keyframe_index_c
        position_data = tuple(position_data)
      else:
        object_name = get_node_name(item)
        mtx = item.WorldPositionMatrix
        rot = mtx.WPR
        sx = mtx.N.length()
        sy = mtx.O.length()
        sz = mtx.A.length()
        position_data = keyframe_index_c, mtx.P.X*SCALE, mtx.P.Y*SCALE, mtx.P.Z*SCALE, rot.X*DEG2RAD, rot.Y*DEG2RAD, rot.Z*DEG2RAD, sx,sy,sz
        if keyframe_index == 0:
          object_data = []
    if keyframe_index == 0:
      if item_type == 'NODE':
        object_name = get_node_name(item)
      rec_data.append( [object_name, item_type, object_data, [position_data]] )
    else:
      if keyframe_index > 1 and position_data[1:] == rec_data[i][3][-1][1:] == rec_data[i][3][-2][1:] and item_type != 'SPARKS':
        # node is stationary.. only keyframe index changes.. replace prev positiondata
        rec_data[i][3][-1] = position_data
      else:
        # sparks must be keyframed even if stationary
        rec_data[i][3].append(position_data)
  return rec_data



def setPresetLights(rec_data):
  current_preset = [x for x in preset_tree if x.get("name") == presetProp.Value]
  if current_preset:
    current_preset = current_preset[0]
    sun_lights = current_preset.findall('sun_light')
    for light in sun_lights:
      object_name = 'preset_light'
      item_type = 'SUN_LIGHT'
      rgb = tuple( [float(light.get(x)) for x in ['r','g','b']])
      strength = float(light.get('energy'))
      size = float(light.get('size'))
      object_data = [rgb, strength, size]
      mtx = vcMatrix.new()
      mtx.rotateRelZ( float(light.get('orientation')) + envRotationProp.Value )
      mtx.rotateRelY( 90 - float(light.get('elevation')) )
      if 'auto' in light.get('distance').lower():
        mtx.translateRel(0,0,10000)
      else:
        mtx.translateRel(0,0,eval(light.get('distance')))
      p = mtx.P
      coi = vcMatrix.new(mtx)
      coi.translateRel(0,0,-1000)
      coi = coi.P
      position_data1 = 0,p.X*SCALE, p.Y*SCALE, p.Z*SCALE, coi.X*SCALE, coi.Y*SCALE, coi.Z*SCALE
      position_data2 = keyframe_index,p.X*SCALE, p.Y*SCALE, p.Z*SCALE, coi.X*SCALE, coi.Y*SCALE, coi.Z*SCALE
      object_name = object_name.encode('utf-8')
      rec_data.append( [object_name, item_type, object_data, [position_data1,position_data2]] )
  return rec_data


def getPresetTree():
  import xml.etree.ElementTree as ET
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  thefolder = thefolder.decode('utf8')
  preset_xml_uri = os.path.join(thefolder , 'Lights\\Presets' , 'presets.xml')
  preset_xml_uri = preset_xml_uri.decode('utf8')
  preset_tree = ET.parse(preset_xml_uri)
  return preset_tree


def CallStill(arg):
  global keyframe_index
  profiler_in = time.time()
  showBorderProp.Value = False
  rec_data = []
  new_dynamic_nodes = []
  all_items = get_render_items()
  keyframe_index=0
  recKeyFrame(all_items, rec_data)
  setPresetLights(rec_data)
  materials, mtl_file, material_table_csv, material_data_dict = getMaterialFiles()
  exportGeo(all_items,
            materials, 
            mtl_file, 
            material_table_csv, 
            material_data_dict)

  if material_table_csv:
    material_table_csv.close()
  '''
  overshoot = floorsizeProp.Value
  threeD_bound[0] -= overshoot
  threeD_bound[1] += overshoot
  threeD_bound[2] -= overshoot
  threeD_bound[3] += overshoot'''
  ok = CallBlender(rec_data, animation = False)
  if not ok:
    return
  profiler_out = time.time()
  print 'Export time:', round((profiler_out - profiler_in), 3), "s"



def CallAnim(arg):
  global rec_data, threeD_bound
  showBorderProp.Value = False
  overshoot = floorsizeProp.Value
  try:
    threeD_bound[0] -= overshoot
    threeD_bound[1] += overshoot
    threeD_bound[2] -= overshoot
    threeD_bound[3] += overshoot
    ok = CallBlender(rec_data, animation = True)
  except:
    print '*** Error in animation rendering call. ***'
    print ' - Make sure you first check "RecAnimation" check box'
    print ' - Then run simulation once until "RecAnimation" is automatically unchecked'
    print ' - Then hit "RenderAnimation"'


def OnSimRender(local_sim): #this is used for recording key frames during animation
  global rec_data, new_dynamic_nodes, keyframe_index, cache_material_files, keyframe_index_c
  keyframe_index_c = int(round((sim.SimTime-startanim_prop.Value) / stepanim_prop.Value))
  if showBorderProp.Value: showBorderProp.Value = False
  t = sim.SimTime
  if startanim_prop.Value > endanim_prop.Value:
    app.messageBox('Error: Animation start time is higher than end time.', 'Animation recording error', VC_MESSAGE_TYPE_ERROR, VC_MESSAGE_BUTTONS_OK)
    app.Simulation.reset()
  if t > startanim_prop.Value and t <= endanim_prop.Value:
    app.OnDynamicComponent = MyOnDynamicComponent
    sim.OnReset = MyOnReset
    #if keyframe_index==0:
    if keyframe_index == 0:
      all_items = get_render_items()
      materials, mtl_file, material_table_csv, material_data_dict = getMaterialFiles()
      materials, mtl_file, material_table_csv, material_data_dict = exportGeo(all_items,
                                                                              materials, 
                                                                              mtl_file, 
                                                                              material_table_csv, 
                                                                              material_data_dict)
    else:
      all_items, materials, mtl_file, material_table_csv, material_data_dict = cache_material_files
      if new_dynamic_nodes:
        added_dynamic_nodes = add_new_dynamic_component(new_dynamic_nodes)
        materials, mtl_file, material_table_csv, material_data_dict = exportGeo(added_dynamic_nodes,
                                                                                materials, 
                                                                                mtl_file, 
                                                                                material_table_csv, 
                                                                                material_data_dict)
        all_items.extend( added_dynamic_nodes )

        for i, token in enumerate(added_dynamic_nodes):
          item, item_type = token
          object_name = get_node_name(item)
          mtx = item.WorldPositionMatrix
          rot = mtx.WPR
          sx = 0.0 # force scale to zero. Item will be invisible until this keyframe.
          sy = 0.0
          sz = 0.0
          position_data1 = 0, mtx.P.X*SCALE, mtx.P.Y*SCALE, mtx.P.Z*SCALE, rot.X*DEG2RAD, rot.Y*DEG2RAD, rot.Z*DEG2RAD, sx,sy,sz
          position_data2 = keyframe_index_c-1, mtx.P.X*SCALE, mtx.P.Y*SCALE, mtx.P.Z*SCALE, rot.X*DEG2RAD, rot.Y*DEG2RAD, rot.Z*DEG2RAD, sx,sy,sz
          object_data = []
          rec_data.append( [object_name, item_type, object_data, [position_data1,position_data2]] )
        new_dynamic_nodes = []
    cache_material_files = all_items, materials, mtl_file, material_table_csv, material_data_dict
    rec_data = recKeyFrame(all_items, rec_data)
    keyframe_index += 1
  elif t > endanim_prop.Value:
    all_items = get_render_items()
    setPresetLights(rec_data)
    #exportGeo(all_items)
    app.OnDynamicComponent = None
    app.OnRender = None
    recanim_prop.Value = False


def MyOnDynamicComponent(component, container, added):
  global new_dynamic_nodes
  #rint component.Name, '|',container.Parent.Component.Name, '|', container.Name
  if added:
    new_dynamic_nodes.append(component)



def add_new_dynamic_component(new_components):
  added_dynamic_nodes = []
  added = []
  while new_components:
    new_component = new_components.pop(0)
    new_components.extend(new_component.Children)
    if hasgeometry(new_component) and new_component not in added:
      added.append(new_component)
      added_dynamic_nodes.append( [new_component, exportType(new_component)] )
  return added_dynamic_nodes


def MyOnReset(local_sim):
  sim.OnReset = None
  app.OnDynamicComponent = None


def InitAnim(arg):
  global rec_data, new_dynamic_nodes, keyframe_index, keyframe_index_c
  if recanim_prop.Value:
    rec_data = []
    new_dynamic_nodes = []
    app.RealTimeMode = False
    app.Simulation.SimSpeed = stepanim_prop.Value
    app.OnRender = OnSimRender
    keyframe_index = 0 #this one is purely indexed up per each recorded render step
    keyframe_index_c = 0 #this one is calculated based on the simulation time
  else:
    app.OnRender = None
  fpsanim_prop.Value = int(1.0/stepanim_prop.Value)


def get_blender_exe_uri():
  blender_exe_uri = blender_exe_uri_prop.Value
  blender_exe_uri = blender_exe_uri.decode('utf8')
  if not os.path.isfile(blender_exe_uri):
    # Try to auto-detect Blender in common installation locations
    import glob
    search_paths = [
      'C:\\Program Files\\Blender Foundation\\Blender*\\blender.exe',
      'C:\\Program Files (x86)\\Blender Foundation\\Blender*\\blender.exe',
      'C:\\Blender*\\blender.exe',
      os.path.join(os.environ.get('USERPROFILE', 'C:\\'), 'Desktop\\Blender*\\blender.exe'),
      os.path.join(os.environ.get('USERPROFILE', 'C:\\'), 'Desktop\\blender*\\blender.exe'),
    ]
    
    found_blenders = []
    for search_path in search_paths:
      found_blenders.extend(glob.glob(search_path))
    
    if found_blenders:
      # Sort to get the highest version first (Blender 5.0 before 4.x, etc.)
      found_blenders.sort(reverse=True)
      blender_exe_uri = found_blenders[0]
      print 'Auto-detected Blender at: {}'.format(blender_exe_uri)
      blender_exe_uri_prop.Value = blender_exe_uri
      # Update defaults.xml
      for child in prop_defaults_xml_tree.getroot():
        if child.attrib['name'] == "Advanced::Blender Executable":
          child.attrib['value'] = blender_exe_uri
      prop_defaults_xml_tree.write(prop_defaults_xml_uri)
      return blender_exe_uri
    
    # If auto-detection failed, show the dialog
    msg = 'Is Blender application already installed?\n\n'
    msg += 'Yes:\nOpens a dialog to locate the Blender executable. (blender.exe)\n\n'
    msg += 'No:\nCancels the addon. Please install the Blender and try again.\n'
    dialog_return_value = app.messageBox(msg, 'Failed to locate Blender executable.', VC_MESSAGE_BUTTONS_YESNO)
    if dialog_return_value == VC_MESSAGE_RESULT_YES:
      file_filter = "Executables (*.exe)|*.exe"
      savecmd = app.findCommand("dialogOpen")
      savecmd.execute('',True,file_filter,'Locate Blender executable.')
      if not savecmd.Param_2:
        print "Blender executable not located. Aborting addon."
        return
      uri = savecmd.Param_1
      blender_exe_uri = uri[8:]
      blender_exe_uri_prop.Value = blender_exe_uri
      blender_exe_uri = blender_exe_uri.decode('utf8')
      prop_defaults_xml_tree
      for child in prop_defaults_xml_tree.getroot():
        if child.attrib['name'] == "Advanced::Blender Executable":
          child.attrib['value'] = blender_exe_uri
      prop_defaults_xml_tree.write(prop_defaults_xml_uri)
      #
    else:
      return ''
  return blender_exe_uri


def get_blender_version(blender_exe_uri):
  """
  Check Blender version from the executable path.
  Returns version as float (e.g., 5.0, 4.2, 3.6) or None if cannot determine.
  """
  import re
  # Try to extract version from the path (e.g., "Blender 5.0", "Blender 4.2", etc.)
  version_match = re.search(r'[Bb]lender[\s_-]?(\d+)\.(\d+)', blender_exe_uri)
  if version_match:
    major = int(version_match.group(1))
    minor = int(version_match.group(2))
    return float('{}.{}'.format(major, minor))
  return None


import io
def CallBlender(rec_data, animation = False):
  blender_exe_uri = get_blender_exe_uri()
  if not blender_exe_uri:
    return False
  uri_root = cmd.TEMPDATA_URI
  uri_root = uri_root.decode('utf8')
  rec_file_name = os.path.join(uri_root, 'recording.vcbx')
  rec_file_name = rec_file_name.decode('utf8')
  with io.open(rec_file_name, 'w', encoding = 'utf-8') as rec_file:
    rec_file.write( unicode(rec_data) )
    #rec_file.write( str(rec_data) )
  xml_uri = os.path.join(uri_root, 'render_config.xml')
  xml_uri = xml_uri.decode('utf8')
  framecount = keyframe_index_c if animation else 0
  create_config_XML(xml_uri, framecount)
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  
  # Determine which import script to use based on Blender version
  blender_version = get_blender_version(blender_exe_uri)
  if blender_version and blender_version >= 5.0:
    import_script_name = 'import_to_blender5.py'
    material_helper_name = 'material_helper.py'  # material_helper works for both versions
    print 'Detected Blender version {:.1f}, using {}'.format(blender_version, import_script_name)
  else:
    import_script_name = 'import_to_blender.py'
    material_helper_name = 'material_helper.py'
    if blender_version:
      print 'Detected Blender version {:.1f}, using {}'.format(blender_version, import_script_name)
    else:
      print 'Could not detect Blender version from path, using default {}'.format(import_script_name)
  
  vcimporteruri = os.path.join(thefolder, import_script_name)
  vcimporteruri = vcimporteruri.decode('utf8')
  vcimporteruri_copy = os.path.join(temproot_uri, 'import_to_blender.py')
  vcimporteruri_copy = vcimporteruri_copy.decode('utf8')
  materialhelperuri = os.path.join(thefolder, material_helper_name)
  materialhelperuri = materialhelperuri.decode('utf8')
  materialhelperuri_copy = os.path.join(temproot_uri, 'material_helper.py')
  materialhelperuri_copy = materialhelperuri_copy.decode('utf8')
  materialsuri = os.path.join(thefolder, 'materials.py')
  materialsuri = materialsuri.decode('utf8')
  materialsuri_copy = os.path.join(temproot_uri, 'materials.py')
  materialsuri_copy = materialsuri_copy.decode('utf8')
  shutil.copyfile(vcimporteruri, vcimporteruri_copy)
  shutil.copyfile(materialhelperuri, materialhelperuri_copy)
  shutil.copyfile(materialsuri, materialsuri_copy)
  cli_data = []
  cli_data.append('%s' % blender_exe_uri)
  if reRender_prop.Value:
    previous_scene_uri = os.path.join(uri_root, 'blender_scene.blend' ) 
    #previous_scene_uri = previous_scene_uri.decode('utf8')
    cli_data.append('%s' % previous_scene_uri)
  if not openinblenderProp.Value:
    cli_data.append('--background')
  cli_data.append('--python')
  cli_data.append('%s' % vcimporteruri_copy)
  cli_data.append('--')
  cli_data.append('%s' % uri_root)
  blend_p = subprocess.Popen(cli_data)
  # blend_p = subprocess.Popen(cli_data, stdout=subprocess.PIPE)
  # comm_messages = blend_p.communicate()[0]
  # ret_code = blend_p.returncode
  return True


import locale
def addLamp(arg):
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  thefolder = thefolder.decode('utf8')
  lamp = None
  if 'Sun' in arg.Name:
    lampuri = os.path.join('file///:',thefolder, 'Lights', 'BlenderSunLight.vcmx')
    lamp_strength = lightStrengthProp.Value/20.0
  if 'Spot' in arg.Name:
    lampuri = os.path.join('file///:',thefolder, 'Lights', 'BlenderSpotLight.vcmx')
    lamp_strength = lightStrengthProp.Value
  if 'Area' in arg.Name:
    lampuri = os.path.join('file///:',thefolder, 'Lights', 'BlenderAreaLight.vcmx')
    lamp_strength = lightStrengthProp.Value
  elif 'Point' in arg.Name:
    lampuri = os.path.join('file///:',thefolder, 'Lights', 'BlenderPointLight.vcmx')
    lamp_strength = lightStrengthProp.Value
  lamp = app.load(lampuri)
  c = camera.Coi
  e = camera.Eye
  m = vcMatrix.new()
  m.P = e
  v = e-c
  v.normalize()
  m.setIJK(v.X, v.Y, v.Z)
  m.translateRel(0,0,-1500)
  lamp.PositionMatrix = m
  lamp.Strength = lamp_strength
  lamp.update()
  app.render()


def addSparks(arg):
  selected_comps = app.SelectionManager.getSelection(VC_COMPONENT)
  robot_controller = None
  for selected_comp in selected_comps:
    robot_controllers = selected_comp.findBehavioursByType(VC_ROBOTCONTROLLER)
    robot_executors = selected_comp.findBehavioursByType(VC_ROBOTEXECUTOR)
    if robot_controllers and robot_executors:
      robot = robot_controllers[0]
  #if robot_controller:
  #  target = robot_controller.createTarget()
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  thefolder = thefolder.decode('utf8')
  emitter = None
  emitter_uri = os.path.join('file///:',thefolder, 'Lights', 'SparksEmitter.vcmx')
  emitter = app.load(emitter_uri)
  c = camera.Coi
  e = camera.Eye
  m = vcMatrix.new()
  m.P = e
  v = e-c
  v.normalize()
  m.setIJK(v.X, v.Y, v.Z)
  m.translateRel(0,0,-500)
  emitter.PositionMatrix = m
  emitter.update()
  app.render()


def setEnvHDRI(arg):
  thefolder, commandfilename = os.path.split(getCommandPath()[8:])
  thefolder = thefolder.decode('utf8')
  envmapuri = ''
  hdri_strength = 1
  current_preset = [x for x in preset_tree if x.get("name") == presetProp.Value]
  if current_preset:
    current_preset = current_preset[0]
    hdri_element = current_preset.find('hdri')
    if hdri_element!=None: # must compare to none
      hdri_uri = hdri_element.get('file')
      hdri_uri = hdri_uri.decode('utf8')
      hdri_strength = hdri_element.get('strength')
      envmapuri = os.path.join('file:///', thefolder , 'Lights\\Presets' , hdri_uri)
      envtypeProp.Value = 'Image'
    else:
      envtypeProp.Value = 'ColorRGB'
      hdri_strength = 0
  envimageProp.Value = str(envmapuri)
  envstrengthProp.Value = float(hdri_strength)


def fovChangedEvent(arg):
  portrait = portraitProp.Value == 'Portrait'
  xRes = resYProp.Value if portrait else resXProp.Value
  yRes = resXProp.Value if portrait else resYProp.Value
  overshoot = 2
  temp_view = app.createView('TemporaryBlenderer__VIEW')
  cam = app.findCamera()
  mtx = cam.Matrix
  temp_view.CameraMatrix = mtx
  temp_view.CameraFovy = fovProp.Value + overshoot
  app.useView('TemporaryBlenderer__VIEW')
  app.render()
  app.deleteView('TemporaryBlenderer__VIEW')
  renderBorder('foo')
  app.render()


def showBorderChangedEvent(arg):
  if showBorderProp.Value:
    app2.OnRender = renderBorder
    renderBorder('foo')
  else:
    app2.OnRender = None
    renderBorder('foo')
  app.render()


def renderBorder(foo):
  portrait = portraitProp.Value == 'Portrait'
  xRes = resYProp.Value if portrait else resXProp.Value
  yRes = resXProp.Value if portrait else resYProp.Value
  red = app.findMaterial('red')
  if showBorderProp.Value:
    cam = app.findCamera()
    cont = sim.World.UserGeometry
    cont.clear()
    lset = cont.createGeometrySet(VC_COMPACTLINESET)
    dist_offset = 10.0
    for i in range(5):
      vertical = math.tan(fovProp.Value*DEG2RAD/2)*dist_offset
      horizontal = float(xRes)/float(yRes)*vertical
      v1 = vcVector.new(horizontal,-vertical,0)
      v2 = vcVector.new(horizontal,vertical,0)
      v3 = vcVector.new(-horizontal,vertical,0)
      v4 = vcVector.new(-horizontal,-vertical,0)
      mtx = cam.Matrix
      mtx.invert()
      mtx.translateRel(0,0,-dist_offset)
      line1 = [v1,v2,v3,v4,v1]
      line2 = [v2,v2 + (v4-v2)*0.2]
      line3 = [v4,v4 + (v2-v4)*0.2]
      line4 = [v3,v3 + (v1-v3)*0.2]
      line5 = [v1,v1 + (v3-v1)*0.2]
      for line in [line1, line2, line3, line4, line5]:
        line = [mtx*x for x in line]
        lset.addLine(line)
      dist_offset *= 10.0
    lset.LineWidth = 2
    lset.Material = red
  else:
    cont = sim.World.UserGeometry
    cont.clear()


def envtypeChanged(arg):
  if arg.Value == 'Image':
    envimageProp.IsVisible = True
    envcolorProp.IsVisible = False
  else:
    envimageProp.IsVisible = False
    envcolorProp.IsVisible = True


def floortypeChanged(arg):
  floorcolorimageProp.Value = str(floortextures[arg.Value][0])
  floorbumpimageProp.Value = str(floortextures[arg.Value][1])
  floorbumpstrengthProp.Value = floortextures[arg.Value][2]
  floortexturesizeProp.Value = floortextures[arg.Value][3]


thefolder, commandfilename = os.path.split(getCommandPath()[8:])
thefolder = thefolder.decode('utf8')
asphalt_uri = os.path.join('file:///'+thefolder, 'Textures', 'AsphaltOld.jpg')
asphaltnormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'AsphaltNormal.jpg')
alu_uri = os.path.join('file:///'+thefolder, 'Textures', 'BrushedAlu.jpg')
alunormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'BrushedAluNormal.jpg')
concretelight_uri = os.path.join('file:///'+thefolder, 'Textures', 'ConcreteLight.jpg')
concretewhite_uri = os.path.join('file:///'+thefolder, 'Textures', 'ConcreteWhite.jpg')
concretedark_uri = os.path.join('file:///'+thefolder, 'Textures', 'ConcreteDark.jpg')
metallic_uri = os.path.join('file:///'+thefolder, 'Textures', 'Metallic.jpg')
concretenormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'ConcreteNormal.jpg')
brownslate_uri = os.path.join('file:///'+thefolder, 'Textures', 'FlooringSlateBrown.jpg')
greyslate_uri = os.path.join('file:///'+thefolder, 'Textures', 'FlooringSlateGrey.jpg')
lightslate_uri = os.path.join('file:///'+thefolder, 'Textures', 'FlooringSlateLight.jpg')
slatenormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'FlooringSlateNormal.jpg')
oak_uri = os.path.join('file:///'+thefolder, 'Textures', 'WoodOakTexture.jpg')
metallicnormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'MetallicNormal.jpg')
oaknormal_uri = os.path.join('file:///'+thefolder, 'Textures', 'WoodOakNormal.jpg')
grey_plaster_uri = os.path.join('file:///'+thefolder, 'Textures', 'grey_plaster_diff_2k.jpg')
grey_plaster_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'grey_plaster_nor_dx_2k.jpg')
brushed_concrete_uri = os.path.join('file:///'+thefolder, 'Textures', 'brushed_concrete_03_diff_2k.jpg')
brushed_concrete_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'brushed_concrete_03_nor_dx_2k.jpg')
square_floor_uri = os.path.join('file:///'+thefolder, 'Textures', 'square_floor_diff_2k.jpg')
square_floor_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'square_floor_nor_dx_2k.jpg')
gravel_uri = os.path.join('file:///'+thefolder, 'Textures', 'gravel_embedded_concrete_diff_2k.jpg')
gravel_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'gravel_embedded_concrete_nor_dx_2k.jpg')
garage_floor_uri = os.path.join('file:///'+thefolder, 'Textures', 'garage_floor_diff_2k.jpg')
garage_floor_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'garage_floor_nor_dx_2k.jpg')
pavement_uri = os.path.join('file:///'+thefolder, 'Textures', 'pavement_04_diff_2k.jpg')
pavement_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'pavement_04_nor_dx_2k.jpg')
pavement_multicolor_uri = os.path.join('file:///'+thefolder, 'Textures', 'pavement_03_diff_2k.jpg')
pavement_multicolor_normal_uri = os.path.join('file:///'+thefolder, 'Textures', 'pavement_03_nor_dx_2k.jpg')

# floorcolorimageProp : 0
# floorbumpimageProp : 1
# floorbumpstrengthProp : 2
# floortexturesizeProp : 3

floortextures = {
'ConcreteLight':(concretelight_uri,concretenormal_uri, 1.0, 500),
'ConcreteWhite':(concretewhite_uri,concretenormal_uri, 1.0, 500),
'ConcreteDark':(concretedark_uri,concretenormal_uri, 1.0, 500),
'SlateBrown':(brownslate_uri,slatenormal_uri, 1.0, 1000),
'SlateGrey':(greyslate_uri,slatenormal_uri, 1.0, 1000),
'SlateLight':(lightslate_uri,slatenormal_uri, 1.0, 1000),
'Oak':(oak_uri,oaknormal_uri, 0.3, 1000),
'Asphalt':(asphalt_uri,asphaltnormal_uri, 1.0, 1000),
'Alu':(alu_uri,alunormal_uri, 1.0, 1000),
'GreyPlaster':(grey_plaster_uri,grey_plaster_normal_uri, 1.0, 2000),
'SquareFloor':(square_floor_uri,square_floor_normal_uri, 1.0, 2000),
'BrushedConcrete':(brushed_concrete_uri,brushed_concrete_normal_uri, 1.0, 2000),
'Gravel':(gravel_uri,gravel_normal_uri, 1.0, 2000),
'Pavement Dark':(pavement_uri,pavement_normal_uri, 1.0, 2000),
'Pavement Multi Color':(pavement_multicolor_uri,pavement_multicolor_normal_uri, 1.0, 2000),
'Garage floor':(garage_floor_uri,garage_floor_normal_uri, 1.0, 2000),
#'Metallic':(metallic_uri,metallicnormal_uri, 1.0, 1000),
'<ShadowCatcher>':('','', 1.0, 1000)
}


material_columns = ['Name',
'R', 'G', 'B',
'metallic',
'roughness',
'bumpiness',
'clearcoat',
'clearcoat_rouhness',
'opacity',
'style',
'color_map',
'normal_map']


#
# tooltips
#
net_command = app.findCommand('netCommand')
# Default tab
outputfile_tip = '''File path where the render result is stored. This is also used for animation rendering.'''
samples_tip = '''More samples improve the rendering quality with less noise and smoother lighting, but requires longer rendering time.'''
presets_tip = '''Predefined lighting presets. Preset includes an environment map which can be edited on Env-tab and may also include actual light sources.'''
reuse_scene_tip = '''Use this option to render the same scene again. Saves a lot of time as the scene is not exported/imported again. Simulation scene must include all the same components and nodes for this to work. Disable this if rendering is not working properly.'''
openinblender_tip = '''When enabled "Render" and "Render Animation" buttons will not render the scene. Instead the scene is converted and opened in Blender for further editing.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Output file', 'Description', outputfile_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Samples', 'Description', samples_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lighting Preset', 'Description', presets_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Reuse Previous Scene', 'Description', reuse_scene_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Open in Blender', 'Description', openinblender_tip)
# Lights tab
addpoint_tip = '''Add a point light to the scene. Light is located to the current location of the camera. Select the light component in the scene to edit its properties.'''
addarea_tip = '''Add an area light to the scene. Light is located to the current location of the camera. Select the light component in the scene to edit its properties.'''
addspot_tip = '''Add a spot light to the scene. Light is located to the current location of the camera. Select the light component in the scene to edit its properties.'''
addsun_tip = '''Add a sun light to the scene. Light is located to the current location of the camera. Select the light component in the scene to edit its properties.'''
defaultstrength_tip = '''Default strength given to a newly created light. Strength can be later edited in the properties of the light component.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lights::Add Point Light', 'Description', addpoint_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lights::Add Area Light', 'Description', addarea_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lights::Add Spot Light', 'Description', addspot_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lights::Add Sun Light', 'Description', addsun_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Lights::Default Strength', 'Description', defaultstrength_tip)
# Advanced tab
camerafov_tip = '''Vertical field of view of the camera.'''
showborder_tip = '''Visualize the camera framing in 3d. Change CameraFov for desired result. Resize panels to fit the frame in 3d window horizontally.'''
exposure_tip = '''Camera exposure. Smaller values result darker image. Does not change the depth of field.'''
bloom_tip = '''Enable light bloom effect. Brighter areas in the image bloom creating a glowing effect.'''
bloomintesity_tip = '''Strength of the bloom effect when Bloom is enabled.'''
renderedges_tip = '''Enable to add black edges to the render. Also flattens the materials a little for toon shading style.'''
edgethickness_tip = '''Defines the edge thickness for edge rendering. Enable also the "Render Edges" property.'''
renderdevice_tip = '''Choose GPU or CPU device for rendering. GPU may be faster but CPU may support larger scenes. Enable GPU rendering inside the Blender application preferences.'''
depthoffieldnode_tip = '''Choose a node in the 3d scene to adjust camera lense focus to that specific object.'''
depthFstop_tip = '''F Stop value of the lense. Smaller value result blurrier image outside the focus area.'''
indirect_tip = '''Enabling indirect lighting results more realistic lighting but requires longer rendering and prep time.'''
exportcomponents_tip = '''Click [...] to choose one or more components to export and render. Only the selected components will be included in the scene. Leave empty to export all components.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::CameraFov', 'Description', camerafov_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Show Border', 'Description', showborder_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Exposure', 'Description', exposure_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Bloom', 'Description', bloom_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Bloom Intensity', 'Description', bloomintesity_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Render Edges', 'Description', renderedges_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Edge Thickness', 'Description', edgethickness_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::RenderDevice', 'Description', renderdevice_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::DepthOfFieldNode', 'Description', depthoffieldnode_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Depth F-Stop', 'Description', depthFstop_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Indirect Lighting', 'Description', indirect_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Advanced::Export Components', 'Description', exportcomponents_tip)

# Materials tab
materialmode_tip = '''Default: 
Use scene materials as they are in the VC model.

Read From Table: 
Read material definitions from the materials.csv file inside the command folder.

Write To Table: 
Write scene material definitions to the materials.csv file inside the command folder.

Hint: Use first Write To Table mode and render. Then edit the csv and then render again using the Read From Table mode.'''
delimiter_tip = '''Choose the delimiter that MS Excel is using in your region.'''
robotmaterials_tip = '''Default:
Use materials of the robots as they are in the VC model.

Smart Materials:
Some shading effects are automatically applied to the materials in the components including robot controller behavior.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Materials::Mode', 'Description', materialmode_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Materials::Table Delimiter', 'Description', delimiter_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Materials::Robot Materials', 'Description', robotmaterials_tip)
# Animation tab
rec_animation_tip = '''To record the animation for rendering enable this property. Then run the simulation until this property is automatically disabled and then call RenderAnimation.'''
start_animation_tip = '''Animation recording start time in seconds.'''
end_animation_tip = '''Animation recording end time in seconds.'''
recstep_animation_tip = '''Animation recording step in seconds. Example: 0.04s would result in 25 key frames per second.'''
fps_animation_tip = '''Frames per second of the result video. This value can be different than what the Rec step property defines to speed up or slow down the resulting video.'''
container_animation_tip = '''Choose the video file container format. Choose MP4 for portability (smaller file) OR choose AVI for reliability (better compatibility in some cases).'''
render_animation_tip = '''Make sure to record the animation first before calling rendering. Use RecAnimation preperty for recording the animation.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::RecAnimation', 'Description', rec_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::Start', 'Description', start_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::End', 'Description', end_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::Rec step', 'Description', recstep_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::FPS', 'Description', fps_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::Container', 'Description', container_animation_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Animation::RenderAnimation', 'Description', render_animation_tip)
# Env tab
background_tip = '''Background can be an hdr environment image or a plain solid color.'''
image_tip = '''Background image file. Use spherical projection *.hdr files.'''
colorrgb_tip = '''Background color defined as RGB values between 0...1'''
strength_tip = '''Strength of the light that the background adds to the scene.'''
roration_tip = '''Rotates the background image around the Z axis.'''
visible_tip = '''Show or hide the background. Even if the background is hidden, it can add light to the scene and will show up in reflections.'''
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::Background', 'Description', background_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::Image', 'Description', image_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::ColorRGB', 'Description', colorrgb_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::Strength', 'Description', strength_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::Rotation', 'Description', roration_tip)
net_command.execute('SetLocalizationCommand', 'English', 'Python', 'cmdBlenderer2.Env::Visible', 'Description', visible_tip)


addState(None)

