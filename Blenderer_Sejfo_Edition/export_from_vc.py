# This Python file uses the following encoding: utf-8
from __future__ import with_statement 
import math, vcVector, vcMatrix
import os.path
import datetime
import json
from PIL import Image
try:from vcScript import *
except:pass
try:from vcCommand import *
except:pass
from collections import defaultdict, deque

LINECHANGE = '\n'

def sanitizefilename(fname):
  if type(fname) == unicode:
    fname = str(fname)
  suspiciouscharacters = [r'/', '\\' ,'#',':',';','!','�','%','&','?','^','*',' ','\t']
  for c in suspiciouscharacters:
    fname = fname.replace(c,'_')
  return fname



def isRobotMaterial(app, material_name, node):
  controllers = node.Component.findBehavioursByType(VC_ROBOTCONTROLLER)
  if not controllers: return material_name # not a robot
  controller = controllers[0]
  if not controller.FlangeNode or node in [controller.FlangeNode, controller.FlangeNode.Parent]:
    return material_name # skip flange 
  mat = app.findMaterial(material_name)
  diffuse = mat.Diffuse
  avg = (diffuse.X + diffuse.Y + diffuse.Z)/3.0
  dispersion = max([diffuse.X, diffuse.Y, diffuse.Z])-min([diffuse.X, diffuse.Y, diffuse.Z])
  style = ''
  if controller.Name == 'CB3':
    if mat.Opacity > 0.95:
      style = '_pulver'
  else:
    if dispersion > 0.4 or avg > .6 and mat.Opacity > 0.95:
      style = '_cast_metal'
  material_name = material_name + style
  return material_name


def export_obj( app, 
                node, 
                materials, 
                material_file, 
                scale, 
                filename, 
                mat_mode, 
                mat_csv, 
                mat_dict, 
                SEP, 
                re_render,
                use_robot_materials):
  new_materials = {}
  dirM = vcMatrix.new()
  #filename = sanitizefilename(filename)
  # Ensure filename is unicode to prevent encoding errors
  if type(filename) != unicode:
    filename = filename.decode('utf8')
  basename, extension = os.path.splitext(os.path.basename(filename))
  dirname = os.path.dirname(filename)
  if not material_file:
    mtlfilename = dirname +u'\\'+ u"VC_to_Blender_materials.mtl"
  ii = 1
  hasgeometry = False
  for gs in node.Geometry.GeometrySets:
    if gs.Type == VC_TRIANGLESET:
      if gs.PointCount > 0:
        hasgeometry = True
        break
  else:
    # nothing to export return
    return None, materials, material_file

  ##
  geosets_by_material = defaultdict(list)
  for gs in node.Geometry.GeometrySets:
    if gs.Type == VC_TRIANGLESET:
      if gs.Feature and not gs.Feature.Visible:
        continue
      if not gs.Material:
        material_name = 'orange'
        material = app.findMaterial(material_name)
      else:
        material_name = gs.Material.Name
        material = gs.Material
      using_styles = [material_name.endswith(x) for x in ['_pulver', '_cast_metal']]
      if use_robot_materials and not any(using_styles):
        material_name = isRobotMaterial(app, material_name, node)
      geosets_by_material[material_name].append(gs)
      new_materials[material_name] = material
  ##
  if not re_render:
    try:
      out = open(filename,"w")
    except IOError:
      print 'cannot open file %s' % filename
      return None, materials, material_file
    with out:
      out.write("# Visual Components OBJ Exporter v0.1c - (c)2018 Visual Components\n")
      out.write("# File Created: %s\n\n" % datetime.datetime.now().isoformat())
      out.write("mtllib %s\n\n" % ("VC_to_Blender_materials.mtl"))
      ii = 1
      mp = vcMatrix.new()#n.WorldPositionMatrix
      mo = vcMatrix.new(mp)
      mo.P = vcVector.new()
      aaa = 0

      for material_name, geoset_list in geosets_by_material.iteritems():
        #if gs.Material and gs.Material.Name == 'cyan':
        #  continue
        aaa += 1


        out.write("#\n# object %s <%i geosets>\n#\n\n" % (material_name,len(geoset_list)))
        # vertex_string = ''
        # text_coord_string = ''
        # face_string = ''
        vertex_string = deque()
        text_coord_string = deque()
        face_string = deque()
        vertex_indexer = 0
        for gs in geoset_list:
          for vec in zip(gs.PositionTable[::3],gs.PositionTable[1::3],gs.PositionTable[2::3]):
            v = mp*vcVector.new(vec[0]*scale,vec[1]*scale,vec[2]*scale)
            vertex_string.append("v %.4f %.4f %.4f" % (v.X,v.Y,v.Z) )
          #out.write("# %d vertices\n\n" % gs.PointCount )
          if len(gs.TextureCoordinateTable) > 0:
            for vec in zip(gs.TextureCoordinateTable[::2],gs.TextureCoordinateTable[1::2]):
              text_coord_string.append("vt %.4f %.4f 0.0000" % vec)
          else:
            for i in range(gs.PointCount):
              text_coord_string.append("vt 0.0000 0.0000 0.0000")
          #out.write("# %d texture coords\n\n" % gs.PointCount )
          tt = gs.TriangleTable
          for v in zip(tt[::3],tt[1::3],tt[2::3]):
            face_string.append("f %d/%d/%d %d/%d/%d %d/%d/%d" % (v[0]+ii,v[0]+ii,v[0]+ii,v[1]+ii,v[1]+ii,v[1]+ii,v[2]+ii,v[2]+ii,v[2]+ii))
          #out.write("# %d polygons\n\n" % gs.TriangleCount )
          ii += gs.PointCount
        vertex_string = '\n'.join(vertex_string)
        text_coord_string = '\n'.join(text_coord_string)
        face_string = '\n'.join(face_string)
        out.write('\n')
        out.write(vertex_string)
        out.write('\n')
        out.write(text_coord_string)
        out.write('\n')
        out.write("g %s_%i\n" % ('geo_'+material_name, aaa))
        #out.write("usemtl %s\n" % sanitizefilename(material_name))
        out.write("usemtl %s\n" % material_name)
        out.write(face_string)
        out.write('\n')


  # # # # # # # # # # # # # # # # # # # # #
  try:
    if material_file:
      out = open(material_file.name, 'a')
    else:
      out = open(mtlfilename,"w")
      out.write("# Visual Components OBJ like material exporter - (c)2018 Visual Components\n")
      out.write("# File Created: %s\n\n" % datetime.datetime.now().isoformat())
  except IOError:
    print 'cannot open file %s' % filename
    return None, materials, material_file
  with out:
    # # # # # # # # # # # # # # # # # # # # 
    # # # # # # # Materials # # # # # # # # 
    # # # # # # # # # # # # # # # # # # # # 

    for material_name, mat in new_materials.iteritems():
      if material_name in materials:
        # the material is already written to the mat file
        continue
      table_material = False
      if mat_mode == 'Read From Table' and mat.Name in mat_dict:
        table_material = True
        R = float(mat_dict[mat.Name]['R'])**2.2 #to be gamma corrected 
        G = float(mat_dict[mat.Name]['G'])**2.2 #to be gamma corrected 
        B = float(mat_dict[mat.Name]['B'])**2.2 #to be gamma corrected 
        metallic = float(mat_dict[mat.Name]['metallic'])
        roughness = float(mat_dict[mat.Name]['roughness'])
        bumpiness = float(mat_dict[mat.Name]['bumpiness'])
        clearcoat = float(mat_dict[mat.Name]['clearcoat'])
        clearcoat_rouhness = mat_dict[mat.Name]['clearcoat_rouhness'] # not implemented
        opacity = float(mat_dict[mat.Name]['opacity'])
        style = mat_dict[mat.Name]['style']
        #procedural_displacement = mat_dict[mat.Name]['procedural_displacement']
        #displacement_value = float(mat_dict[mat.Name]['displacement_value'])
        #displacement_scale = float(mat_dict[mat.Name]['displacement_scale'])
        color_map = mat_dict[mat.Name]['color_map']
        normal_map = mat_dict[mat.Name]['normal_map']
      new_line = "newmtl %s\n" % material_name
      new_line = new_line.encode('utf-8')
      out.write(new_line)
      if table_material:
        out.write("\td %.4f\n" % opacity)
      elif mat.OpacityType == VC_MATERIAL_TRANSPARENCY_CONSTANT:
          out.write("\td %.4f\n" % mat.Opacity)
          opacity = mat.Opacity
      elif mat.OpacityType == VC_MATERIAL_TRANSPARENCY_NONE:
        out.write("\td 1.0000\n")
        opacity = 1.0
      out.write("\tKa %.4f %.4f %.4f\n" % (mat.Ambient.X,mat.Ambient.Y,mat.Ambient.Z))
      if table_material:
        out.write("\tKd %.4f %.4f %.4f\n" % (R**(1/2.2),G**(1/2.2),B**(1/2.2))) # HUOM! DOUBLE CHECK THE GAMMA CORRECTION
      else:
        try:
          out.write("\tKd %.4f %.4f %.4f\n" % (mat.BaseColor.X,mat.BaseColor.Y,mat.BaseColor.Z))
        except:
          out.write("\tKd %.4f %.4f %.4f\n" % (mat.Diffuse.X,mat.Diffuse.Y,mat.Diffuse.Z))
      out.write("\tKs %.4f %.4f %.4f\n" % (mat.Specular.X,mat.Specular.Y,mat.Specular.Z))
      out.write("\tillum 3\n")
      texturefilename = ''
      if False and table_material and color_map: #FALSE FORCED TO DISABLE 
        out.write("\tmap_Kd %s\n" % sanitizefilename(color_map))
        # MAP NEEDS TO BE COPIEND INT HE TEMPDATA FOLDER  !! NOT IMPLEMENTED YET HUOM!!
      elif mat.Texture:
        tname = basename + u'_' + material_name + u".png"
        tname = sanitizefilename(tname)
        texturefilename = u"file:///" + dirname + u'\\' + tname
        app.saveBitmap(mat.Texture, texturefilename)
        out.write("\tmap_Kd %s\n" % tname)
      #
      if False and table_material and normal_map: #FALSE FORCED TO DISABLE 
        out.write("\tmap_bump %s\n" % sanitizefilename(normal_map))
        # MAP NEEDS TO BE COPIEND INT HE TEMPDATA FOLDER  !! NOT IMPLEMENTED YET HUOM!!
      else:
        try:
          mat.BumpMap
          bumpmapAvailable = True
        except:
          bumpmapAvailable = False
        bumptexturefilename = ''
        if bumpmapAvailable:
          tname = basename + u'_' + material_name + u'_BUMP' + u".png"
          tname = sanitizefilename(tname)
          bumptexturefilename = u"file:///" + dirname + u'\\' + tname
          app.saveBitmap(mat.BumpMap, bumptexturefilename)
          #
          out.write("\tmap_bump %s\n" % tname)
      #
      if table_material:
        out.write("\tbumpiness %f\n" % bumpiness)
      else:
        try:
          bumpiness = mat.Bumbiness #typo in API should be bumpiness
        except:
          bumpiness = 0.0
        out.write("\tbumpiness %f\n" % bumpiness)
      #
      if table_material:
        out.write("\tmetallic %f\n" % metallic)
      else:
        try:
          metallic = mat.Metallic
        except:
          metallic = 0.0
        out.write("\tmetallic %f\n" % metallic)
      # clearcoat
      if table_material:
        out.write("\tclearcoat %f\n" % clearcoat)
      else:
        try:
          clearcoat = mat.Clearcoat
        except:
          clearcoat = 0.0
        out.write("\tclearcoat %f\n" % clearcoat)
      # style
      if table_material:
        out.write("\tstyle %s\n" % style)
      else:
        try:
          style = mat.Style
        except:
          style = 'N/A'
        out.write("\tstyle %s\n" % style)
      #
      if table_material:
        out.write("\troughness %f\n" % roughness)
      else:
        try:
          roughness = mat.Roughness
        except:
          roughness = 0.0
        out.write("\troughness %f\n" % roughness)
      out.write("\n")
      if mat_mode == 'Write To Table' and mat_csv and mat.Name not in materials:
        mat_csv.write(mat.Name + SEP)
        mat_csv.write(str(mat.Diffuse.X) + SEP)
        mat_csv.write(str(mat.Diffuse.Y) + SEP)
        mat_csv.write(str(mat.Diffuse.Z) + SEP)
        mat_csv.write(str(metallic) + SEP)
        mat_csv.write(str(roughness) + SEP)
        mat_csv.write(str(bumpiness) + SEP)
        mat_csv.write(str(clearcoat) + SEP)
        mat_csv.write('' + SEP)
        mat_csv.write(str(opacity) + SEP)
        mat_csv.write(style + SEP)
        #mat_csv.write(procedural_displacement + SEP)
        #mat_csv.write(str(displacement_value) + SEP)
        #mat_csv.write(str(displacement_scale) + SEP)
        mat_csv.write(texturefilename + SEP)
        mat_csv.write(bumptexturefilename + LINECHANGE)
        #material_table_csv.close()
      #materials[mat.Name] = mat
      materials[material_name] = mat
  return True, materials, out

def export_metadata(node, output_path):
  """Extract and save node metadata"""
  metadata = {}

  # Get node properties
  metadata['name'] = node.Name
  
  # Build path by traversing node hierarchy
  path_parts = []
  current = node
  while current:
    path_parts.insert(0, current.Name)
    current = getattr(current, 'Parent', None)
  metadata['path'] = '/'.join(path_parts) if path_parts else node.Name

  # Extract custom properties
  properties = {}
  try:
    if hasattr(node, 'Properties'):
      for prop in node.Properties:
        try:
          prop_name = prop.Name
          prop_value = str(prop.Value)
          properties[prop_name] = prop_value
        except:
          pass
  except:
    pass

  metadata['properties'] = properties

  # Get component metadata
  if node.Component:
    metadata['component_name'] = node.Component.Name
    metadata['component_type'] = node.Component.Type

  return metadata