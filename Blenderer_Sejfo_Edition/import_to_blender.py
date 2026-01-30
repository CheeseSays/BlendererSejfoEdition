import json
import sys, os
sys.path.append('')
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
import bpy, mathutils, glob, re, random
import time, subprocess, importlib
from math import radians
import xml.etree.ElementTree as ET
import material_helper


# read arguments given on the command line
sys_argv = sys.argv
sys_argv = sys_argv[sys_argv.index("--") + 1:]  
uri_root = sys_argv[0]

video_container = 'AVI' # <'AVI', 'MP4'>
importlib.reload(material_helper)
random.seed(1)

def auto_increment_filename(filename):
    if not os.path.isfile(filename):
        return filename
    filepathroot, file_extension = os.path.splitext(filename)
    search_name = filepathroot + '*' + file_extension
    current_pics = glob.glob(search_name)
    list_of_numbers = [0]
    for pic in current_pics:
        fname = os.path.splitext(pic)[0]
        try:
            number = re.findall('[0-9]+$', fname)[0]
            list_of_numbers.append(int(number))
        except IndexError:
            pass
    list_of_numbers = sorted(list_of_numbers)
    new_number = list_of_numbers[-1]+1
    filename = '%s %d%s' % (filepathroot, new_number , file_extension)
    return filename


def do_import_vc():
    '''
    ------------------------------------------------------------------------
    one function wonder:
        read scene settings from xml file and set blender properties accordingly
        read scene structure from .vcbx file: lights, camera, nodes
        generate geometry based on the obj data and keyframe it
        add lights and camera
        and bunch of other things
    ------------------------------------------------------------------------
    '''
    global video_container
    #
    # parse recording.vcbx keyframe data into list of lists
    #
    rec_file_uri = os.path.join(uri_root, 'recording.vcbx' ) 
    rec_file = open(rec_file_uri, 'r', encoding='utf8')
    mydata = rec_file.read()
    rec_file.close()
    rec_data = eval(mydata) #convert string to list (data is saved as data=str(list) so it can be evalued back to list)
    #
    # parse config.xml into a dictionary
    #
    config_file_uri = os.path.join(uri_root, 'render_config.xml' )
    tree = ET.parse(config_file_uri)
    root = tree.getroot()
    config_dict = {}
    for kid in root:
        config_dict[kid.tag] = kid.text
    #
    # set some render setting 
    # 
    bpy.context.scene.render.engine = config_dict['engine']
    bpy.context.scene.render.resolution_x = int(config_dict['resolution_x'])
    bpy.context.scene.render.resolution_y = int(config_dict['resolution_y'])
    bpy.context.scene.render.resolution_percentage = int(config_dict['resolution_percentage'])
    bpy.context.scene.render.use_border = False
    bpy.context.scene.eevee.taa_render_samples = int(config_dict['samples'])
    bpy.context.scene.frame_start = frameS = int(config_dict['frame_start'])
    bpy.context.scene.frame_end = frameE = int(config_dict['frame_end'])
    bpy.context.scene.render.fps = int(config_dict['anim_fps'])
    bpy.context.scene.render.filepath = config_dict['filepath']
    video_container = config_dict['video_container']
    bpy.context.scene.view_settings.exposure = envstrength = float(config_dict['exposure'])
    bpy.context.scene.eevee.use_soft_shadows = True
    bpy.context.scene.eevee.use_gtao = True #ambient occlusion
    bpy.context.scene.eevee.gtao_distance = 0.5
    bpy.context.scene.eevee.gtao_factor = 2
    bpy.context.scene.eevee.use_ssr = True
    bpy.context.scene.render.filter_size = 2 # smoother edges
    bpy.context.scene.view_settings.view_transform = 'Standard'
    bpy.context.scene.view_settings.look = 'Medium High Contrast'

    # bpy.context.scene.eevee.use_motion_blur = True
    # bpy.context.scene.eevee.motion_blur_samples = 8
    # bpy.context.scene.eevee.motion_blur_shutter = 0.5

    # Bloom
    use_bloom = config_dict['bloom'] == 'True'
    bpy.context.scene.eevee.use_bloom = use_bloom
    bpy.context.scene.eevee.bloom_intensity = float(config_dict['bloomintensity'])
    # Edge rendering i.e. freestyle
    bpy.context.scene.render.use_freestyle = config_dict['use_renderedges'] == 'True'
    if bpy.context.scene.render.use_freestyle:
        bpy.data.linestyles["LineStyle"].thickness = int(config_dict['edge_line_thickness'])
    
    #
    # read rest of the settings to variables
    #
    depthOFnode = config_dict['depthOFnode']
    depthOfFieldObject = None
    depth_fstop = float(config_dict['depth_fstop'])
    re_render = config_dict['re_render'] == 'True'
    openinblender = config_dict['openinblender'] == 'True'
    if config_dict['envimage']:
        envimage = config_dict['envimage'].replace('file:///' , '')
    else:
        envimage = None
    envstrength = float(config_dict['envstrength'])
    envrotation = float(config_dict['envrotation'])
    envtype = config_dict['envtype']
    envcolorgb = [float(x) for x in config_dict['envcolor'].split(';')]
    envvisible = config_dict['envvisible'] == 'True'
    floorvisible = config_dict['floorvisible']
    floorsize = config_dict['floorsize']
    floortype = config_dict['floortype']
    if config_dict.get('floorcolorimage'):
        floorcolorimage = config_dict.get('floorcolorimage').replace('file:///' , '')
    else:
        floorcolorimage = ''
    if config_dict.get('floorbumpimage'):
        floorbumpimage = config_dict.get('floorbumpimage').replace('file:///' , '')
    else:
        floorbumpimage = ''
    floorbumpstrength = float(config_dict.get('floorbumpstrength'))
    floortexturesize = float(config_dict['floortexturesize'])
    floorcolor = [float(x) for x in config_dict['floorcolor'].split(';')]
    scene_bound = eval(config_dict['scene_bound'])
    floor_overshoot = float(config_dict['floor_overshoot'])
    floor_corners = scene_bound[:] # [-X, +X, -Y, +Y, -Z, +Z]
    floor_corners[0] -= floor_overshoot
    floor_corners[1] += floor_overshoot
    floor_corners[2] -= floor_overshoot
    floor_corners[3] += floor_overshoot
    floor_corners[4] -= floor_overshoot
    floor_corners[5] += floor_overshoot
    CameraFOV = float(config_dict['CameraFOV'])
    #
    # init scene
    #
    clearScene(re_render)
    #
    # Collections
    #
    if re_render: # find existing collections
        collection_utils = bpy.data.collections['Utils']
        collection_comps = bpy.data.collections['Components']
    else: # create new collections
        collection_utils = bpy.data.collections.new('Utils')
        bpy.context.scene.collection.children.link(collection_utils)
        collection_comps = bpy.data.collections.new('Components')
        bpy.context.scene.collection.children.link(collection_comps)
    #
    # Set HDRI (env map)
    #
    print('Setting Environment HDRI map...')
    scn = bpy.context.scene
    scn.world.use_nodes = True
    wd = scn.world
    nt = bpy.data.worlds[wd.name].node_tree
    env_strength_node = None
    for node in nt.nodes:
        nt.nodes.remove(node) # clear if there's any pre-existing nodes
    backNode = nt.nodes.new(type="ShaderNodeBackground")
    outputNode = nt.nodes.new(type="ShaderNodeOutputWorld")
    if envtype == 'Image' and envimage:
        envNode = nt.nodes.new(type="ShaderNodeTexEnvironment")
        envTexture_img = bpy.data.images.load(envimage)
        envNode.image = envTexture_img
        envNode.location.x = backNode.location.x-300
        outputNode.location.x = backNode.location.x+200
        envNode.location.y = backNode.location.y
        envNodeOut = envNode.outputs['Color']
        backColIn = backNode.inputs['Color']
        backNode.inputs[1].default_value = envstrength
        env_strength_node = backNode
        textcoordNode = nt.nodes.new(type="ShaderNodeTexCoord")
        textcoordNode.location.x = backNode.location.x-900
        mappingNode = nt.nodes.new(type="ShaderNodeMapping")
        mappingNode.location.x = backNode.location.x-700
        mappingNode.inputs['Rotation'].default_value[2] = -radians(envrotation)
        nt.links.new(envNodeOut, backColIn)
        nt.links.new(textcoordNode.outputs[0], mappingNode.inputs[0])
        nt.links.new(mappingNode.outputs[0], envNode.inputs[0])
        nt.links.new(backNode.outputs[0], outputNode.inputs[0])
    else: #color RGB
        backNode = nt.nodes['Background']
        backColIn = backNode.inputs['Color']
        if len(envcolorgb) == 3:
            ccolor = [0,0,0,1]
            ccolor[:3] = envcolorgb
            envcolorgb = tuple(ccolor)
        envcolorgb = [x**2.2 for x in envcolorgb] # gamma correction
        backColIn.default_value = envcolorgb
        backNode.inputs[1].default_value = envstrength
        env_strength_node = backNode
        nt.links.new(backNode.outputs[0], outputNode.inputs[0])
    if envvisible:
        bpy.context.scene.world.cycles_visibility.camera = True
        bpy.context.scene.render.film_transparent = False

    else:
        bpy.context.scene.world.cycles_visibility.camera = False
        bpy.context.scene.render.film_transparent = True
        material_helper.setupAlphaOverCompositor()
        set_up_backdrop( config_dict )
    #
    # Load materials
    #
    matData = loadMAT(os.path.join(uri_root,'VC_to_Blender_materials.mtl'))
    blender_materials = {}
    monochrome = config_dict['monochrome']
    simple_transparents = config_dict['use_simple_transparent'] == 'True'
    for materialname in matData:
            mObj = matData[materialname]
            mat = material_helper.setupMaterial(materialname,
                                mObj.Color,
                                mObj.ColorMap,
                                mObj.Metallic,
                                mObj.Roughness,
                                mObj.NormalMap,
                                mObj.Bumpiness,
                                mObj.Clearcoat,
                                mObj.ClearcoatRougness,
                                mObj.Opacity,
                                mObj.Style,
                                monochrome,
                                simple_transparents)
            blender_materials[materialname] = mat
    #
    # Loop rec_data to create objects and set the keyframe data
    #
    mycounter = 0
    allcount = len(rec_data)
    lamps = []
    sparks_on_off = []
    for item in rec_data:
        mycounter += 1 
        name = item[0]
        name = name.encode('raw-unicode-escape')
        name = name.decode('utf-8')
        item_type = item[1]
        object_data = item[2]
        position_data_list = item[3]
        inipos = position_data_list[0]
        if re_render:
            print('Updating %i/%i: "%s"' % (mycounter, allcount, name) )
        else:
            print('Generating %i/%i: "%s"' % (mycounter, allcount, name) )
        if item_type == 'CAMERA':
            new_camera= bpy.ops.object.add(type='CAMERA', location=inipos[1:4])
            camera_object = bpy.context.selected_objects[0]
            camera_object.name = name
            collection_utils.objects.link(camera_object)
            point = mathutils.Vector((inipos[4], inipos[5], inipos[6]))
            look_at(camera_object, point)
            camera_object.data.clip_start = 0.01
            camera_object.data.clip_end = 150000
            camera_object.data.lens_unit = 'FOV'
            camera_object.data.angle = radians(CameraFOV)
            bpy.context.scene.camera = camera_object
            obj_object = camera_object
        elif '_LIGHT' in item_type:
            lamp_object = createLampEevee(name, inipos, item_type.replace('_LIGHT', ''), object_data)
            collection_utils.objects.link(lamp_object)
            obj_object = lamp_object
            lamps.append( [lamp_object, object_data] )
        elif item_type == 'NODE':
            if re_render:
                # find existing object in the opened  *.blend file
                geometry_object = bpy.data.objects[name] 
            else:
                # fresh scene. create new content
                uri = os.path.join(uri_root, name)
                uri += '.obj'
                geometry_object = loadmodel(uri, name, blender_materials, collection_comps)
            geometry_object.location = inipos[1:4]
            geometry_object.rotation_euler = inipos[4:7]
            geometry_object.scale = inipos[7:]
            obj_object = geometry_object
            if depthOFnode and depthOFnode == name:
                depthOfFieldObject = geometry_object
        elif item_type == 'SPARKS':
            #
            # SPARKS
            #
            if re_render:
                # find existing object in the opened  *.blend file
                geometry_object = bpy.data.objects[name] 
            else:
                # fresh scene. create new content
                uri = os.path.join(uri_root, name)
                uri += '.obj'
                geometry_object = loadmodel(uri, name, blender_materials, collection_comps)
            geometry_object.location = inipos[1:4]
            geometry_object.rotation_euler = inipos[4:7]
            geometry_object.scale = inipos[7:10]
            obj_object = geometry_object
            if depthOFnode and depthOFnode == name:
                depthOfFieldObject = geometry_object
            spark_geo = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, enter_editmode=False, location=(200, 0, 0))
            spark_geo = bpy.context.selected_objects[0]
            spark_geo.scale[0] = 0.3
            spark_geo.scale[1] = 7
            spark_geo.scale[2] = 0.3
            spark_geo.name = 'VC_TO_BLENDER_SPARK_GEO'
            #spark_color1 = (0.3, 0.6, 1.0, 0.0)
            spark_color1 = object_data[0]
            sparks_material = material_helper.setupSparks('SparksEmission', spark_color1)
            spark_geo.data.materials.append( sparks_material )
            #2
            spark_geo = bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1, enter_editmode=False, location=(200, 0, 0))
            spark_geo = bpy.context.selected_objects[0]
            spark_geo.scale[0] = 0.5
            spark_geo.scale[1] = 5
            spark_geo.scale[2] = 0.5
            spark_geo.name = 'VC_TO_BLENDER_SPARK_GEO2'
            #spark_color2 = (0.15, 0.3, 1.0, 0.0)
            spark_color2 = object_data[0]
            sparks_material2 = material_helper.setupSparks('SparksEmission2', spark_color2)
            spark_geo.data.materials.append( sparks_material2 ) 
        else:
            continue
        t=0
        prev_spark_on = 0.0
        spark_lamp = None
        for i,L in enumerate(position_data_list):
            keyframe_index = L[0]
            new_loc = mathutils.Vector((L[1], L[2], L[3]))
            obj_object.location = new_loc
            if item_type in ['CAMERA', 'AREA_LIGHT', 'SPOT_LIGHT', 'POINT_LIGHT', 'SUN_LIGHT']:
                point = mathutils.Vector((L[4], L[5], L[6]))
                look_at(obj_object, point)
                if '_LIGHT' in item_type and len(L) > 7:
                    obj_object.data.energy = L[7]
                    obj_object.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
            else:
                obj_object.rotation_euler = L[4], L[5], L[6]
            if item_type == 'NODE':
                obj_object.scale = L[7], L[8], L[9]
            if item_type == 'SPARKS':
                spark_on = L[10]
                if spark_on and not prev_spark_on:
                    # create new spark lamp and particle system
                    # lamp1
                    lamp_data = ([x*255 for x in spark_color1[0:3]], 0, 0.1)
                    lamp_loc = list(new_loc[:])
                    lamp_loc.insert(0,0)
                    lamp_loc.extend([0,0,0])
                    lamp_loc = tuple(lamp_loc)
                    spark_lamp = createLampEevee(obj_object.name+'_lamp', lamp_loc, 'POINT', lamp_data )
                    spark_lamp.data.energy = 3.14
                    collection_utils.objects.link(spark_lamp)
                    spark_lamp.keyframe_insert( data_path = 'location', frame = keyframe_index )
                    spark_lamp.data.energy = 0.0
                    spark_lamp.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                    spark_lamp.data.use_custom_distance = False
                    spark_lamp.data.cutoff_distance = 0.1
                    spark_lamp.data.use_shadow = True
                    spark_lamp.data.use_contact_shadow = False
                    # lamp2
                    lamp_data = ([x*255 for x in spark_color2[0:3]], 0, 0.1)
                    spark_lamp2 = createLampEevee(obj_object.name+'_lamp', lamp_loc, 'POINT', lamp_data )
                    spark_lamp2.data.energy = 3.14
                    collection_utils.objects.link(spark_lamp2)
                    spark_lamp2.keyframe_insert( data_path = 'location', frame = keyframe_index )
                    spark_lamp2.data.energy = 0.0
                    spark_lamp2.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                    spark_lamp2.data.use_custom_distance = True
                    spark_lamp2.data.cutoff_distance = 0.1
                    spark_lamp2.data.use_shadow = False
                    spark_lamp2.data.use_contact_shadow = False

                    children = getChildren(obj_object)
                    for child_mesh in children:
                        child_mesh.modifiers.new("part", type='PARTICLE_SYSTEM')
                        particles = child_mesh.particle_systems[-1]
                        particle_settings = particles.settings
                        particle_settings.frame_end = bpy.context.scene.frame_end
                        particle_settings.frame_start = keyframe_index
                        particle_settings.lifetime = 2 # edit this for intensity (integer)
                        particle_settings.lifetime_random = 1.0
                        particle_settings.normal_factor = 3.0
                        particle_settings.normal_factor = 6.0
                        particle_settings.factor_random = 0.4
                        particle_settings.emit_from = 'FACE'
                        particle_settings.distribution = 'RAND'
                        particle_settings.render_type = 'OBJECT'
                        particle_settings.instance_object = bpy.data.objects["VC_TO_BLENDER_SPARK_GEO"]
                        particle_settings.particle_size = 0.002
                        particle_settings.size_random = 0.99
                        particle_settings.use_rotations = True
                        #2
                        child_mesh.modifiers.new("part2", type='PARTICLE_SYSTEM')
                        particles = child_mesh.particle_systems[-1]
                        particle_settings2 = particles.settings
                        particle_settings2.frame_end = bpy.context.scene.frame_end
                        particle_settings2.frame_start = keyframe_index
                        particle_settings2.lifetime = 1 # edit this for intensity (integer)
                        particle_settings2.lifetime_random = 1.0
                        particle_settings2.normal_factor = 1.5
                        particle_settings2.factor_random = 0.6
                        particle_settings2.emit_from = 'FACE'
                        particle_settings2.distribution = 'RAND'
                        particle_settings2.render_type = 'OBJECT'
                        particle_settings2.instance_object = bpy.data.objects["VC_TO_BLENDER_SPARK_GEO2"]
                        particle_settings2.particle_size = 0.002
                        particle_settings2.size_random = 0.99
                        particle_settings2.use_rotations = True
                    # turn off env map light
                    sparks_on_off.append( [True,object_data[1], keyframe_index] )
                elif spark_on and prev_spark_on:
                    # keep particle system going and flicker the lights
                    if spark_lamp:
                        spark_lamp.location = new_loc
                        spark_lamp2.location = new_loc
                        spark_lamp.keyframe_insert( data_path = 'location', frame = keyframe_index )
                        spark_lamp2.keyframe_insert( data_path = 'location', frame = keyframe_index )
                        R = random.random()
                        if R < .4:
                            R=0
                        spark_lamp.data.energy = R*50.0#(R*50.0+spark_lamp.data.energy)/2
                        spark_lamp2.data.energy = R*250.0#(R*250.0+spark_lamp.data.energy)/2
                        spark_lamp.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                        spark_lamp2.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                elif not spark_on and prev_spark_on:
                    # turn particle system down
                    spark_lamp.data.energy = 0.0
                    spark_lamp.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                    spark_lamp2.data.energy = 0.0
                    spark_lamp2.data.keyframe_insert( data_path = 'energy', frame = keyframe_index )
                    children = getChildren(obj_object)
                    # for child_mesh in children:
                    #     for i, particles in enumerate(child_mesh.particle_systems):
                    #         particle_settings = particles.settings
                    particle_settings.frame_end = keyframe_index
                    duration = particle_settings.frame_end - particle_settings.frame_start
                    particle_settings.count = int(100 * duration)
                    particle_settings2.frame_end = keyframe_index
                    duration = particle_settings2.frame_end - particle_settings2.frame_start
                    particle_settings2.count = int(200 * duration)
                    sparks_on_off.append( [False, object_data[1], keyframe_index] )
                prev_spark_on = spark_on
            obj_object.keyframe_insert( data_path = 'location', frame = keyframe_index )
            obj_object.keyframe_insert( data_path = 'rotation_euler', frame = keyframe_index )
            obj_object.keyframe_insert( data_path = 'scale', frame = keyframe_index )
            t+=1
    
    # Load metadata
    metadata_file = os.path.join(uri_root, 'object_metadata.json')
    if os.path.exists(metadata_file):
        with open(metadata_file, 'r') as mf:
            metadata_collection = json.load(mf)

        # Apply to objects
        for obj_name, metadata in metadata_collection.items():
            if obj_name in bpy.data.objects:
                obj = bpy.data.objects[obj_name]
                
                # Add custom properties
                for prop_name, prop_value in metadata.get('properties', {}).items():
                    obj[prop_name] = prop_value

                # Add component info
                if 'component_name' in metadata:
                    obj['component_name'] = metadata['component_name']
                if 'path' in metadata:
                    obj['vc_path'] = metadata['path']

    # Kill actions with less than 3 keyframes to free up memory
    min_frames = 3
    actions_to_remove = [action for action in bpy.data.actions if all(len(fcurve.keyframe_points) < min_frames for fcurve in action.fcurves)]

    for action in actions_to_remove:
        if action.users > 0:
            for obj in bpy.data.objects:
                if obj.animation_data and obj.animation_data.action == action:
                    obj.animation_data_clear()
        bpy.data.actions.remove(action)

    #
    # Turn other lighting on/off while sparks
    #
    for on_off,dim_rate, keyframe in sparks_on_off:
        strength_input = env_strength_node.inputs[1]
        strength_input.default_value = envstrength if on_off else dim_rate*envstrength
        strength_input.keyframe_insert('default_value', frame=keyframe)
        strength_input.default_value = dim_rate*envstrength if on_off else envstrength
        strength_input.keyframe_insert('default_value', frame=keyframe+3)
        for lamp, object_data in lamps:
            default_energy = object_data[1]
            lamp.data.energy = default_energy if on_off else dim_rate*default_energy
            lamp.data.keyframe_insert('energy', frame=keyframe)
            lamp.data.energy = dim_rate*default_energy if on_off else default_energy
            lamp.data.keyframe_insert('energy', frame=keyframe+3)
    #
    # Depth Of Field
    #
    if depthOfFieldObject:
        # depthOfFieldObject was cached during recdata loop (if defined by user)
        camera_object.data.dof.use_dof = True
        camera_object.data.dof.focus_object = depthOfFieldObject
        camera_object.data.dof.aperture_fstop = float(depth_fstop)
    else:
        camera_object.data.dof.use_dof = False
    #
    # Floor
    #
    Lx = floor_corners[1]-floor_corners[0]
    Ly = floor_corners[3]-floor_corners[2]
    Lz = floor_corners[5]-floor_corners[4]
    MidX = (floor_corners[0]+floor_corners[1])/2.0
    MidY = (floor_corners[2]+floor_corners[3])/2.0
    MidZ = (floor_corners[4]+floor_corners[5])/2.0
    if re_render:
        bpy.ops.object.select_all(action='DESELECT')
        if 'VC_TO_BLENDER_FLOOR_OBJECT' in bpy.data.objects:
            bpy.data.objects['VC_TO_BLENDER_FLOOR_OBJECT'].select_set(True) # Blender 2.8x
            bpy.ops.object.delete()
    if floorvisible == 'True':
        plane = bpy.ops.mesh.primitive_plane_add(location=(MidX,MidY,-0.001), size = .5)
        plane_object = bpy.context.selected_objects[0]
        plane_object.name = 'VC_TO_BLENDER_FLOOR_OBJECT'
        bpy.context.object.dimensions = (Lx,Ly,0)
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
        bpy.ops.object.editmode_toggle()
        bpy.ops.uv.unwrap(method='ANGLE_BASED', margin=0.001)
        bpy.ops.object.editmode_toggle()

        scale = floortexturesize
        uvs = [(0,0),(Lx/scale,0),(Lx/scale,Ly/scale),(0,Ly/scale)]
        for loop, coords in zip(plane_object.data.loops, uvs):
            uv_coords = plane_object.data.uv_layers.active.data[loop.index].uv
            uv_coords[0] = coords[0]
            uv_coords[1] = coords[1]
        ob = bpy.context.active_object
        if len(floorcolor) == 3:
            ccolor = [0,0,0,1]
            ccolor[:3] = floorcolor
            floorcolor = tuple(ccolor)
        floorcolor = [x**2.2 for x in floorcolor] # gamma correction
        metallic = 0.0
        roughness = 0.6
        clearcoat = 0.0
        clearcoat_rouhness = 0.0
        bumpiness = 1.0
        opacity = 1.0
        style = ''
        simple_transparents = config_dict['use_simple_transparent'] == 'True'
        materialname = "FLOORMATERIAL_BlenderToVC_X"
        if floortype == '<ShadowCatcher>':
            mat = material_helper.setupShadowCatcher(materialname, floorcolor)
        else:
            mat = material_helper.setupMaterial(materialname,
                                floorcolor,
                                floorcolorimage,
                                metallic,
                                roughness,
                                floorbumpimage,
                                floorbumpstrength,
                                clearcoat,
                                clearcoat_rouhness,
                                opacity,
                                style,
                                monochrome,
                                simple_transparents)
        ob.data.materials.append(mat)


    #
    # indirect_lighting
    #
    if config_dict['indirect_lighting'] != 'Off' :
        print('Baking indirect lighting.')
        iLx = scene_bound[1]-scene_bound[0]
        iLy = scene_bound[3]-scene_bound[2]
        iLz = scene_bound[5]-scene_bound[4]
        iMidX = (scene_bound[0]+scene_bound[1])/2.0
        iMidY = (scene_bound[2]+scene_bound[3])/2.0
        iMidZ = (scene_bound[4]+scene_bound[5])/2.0
        bpy.ops.object.lightprobe_add(type='GRID', enter_editmode=False, location=(iMidX,iMidY,iMidZ))
        bpy.context.object.scale[0] = iLx*.5
        bpy.context.object.scale[1] = iLy*.5
        bpy.context.object.scale[2] = iLz*.5
        desired_dist = {'Fast':5,'Normal':2,'HQ':0.5}[ config_dict['indirect_lighting'] ]
        bpy.context.object.data.grid_resolution_x = max(2, int(iLx/desired_dist))
        bpy.context.object.data.grid_resolution_y = max(2, int(iLy/desired_dist))
        bpy.context.object.data.grid_resolution_z = max(2, int(iLz/desired_dist))
        bpy.ops.scene.light_cache_bake()
    #
    # done
    #
    print('Finishing scene...')
    return openinblender, config_dict


def set_up_backdrop( config_dict ):
    backdroptype = config_dict['backdroptype']
    if backdroptype == 'None':
        return
    if config_dict['backdropimage']:
        backdropimage = config_dict['backdropimage'].replace('file:///' , '')
    else:
        backdropimage = None
    backdropcolor = [float(x) for x in config_dict['backdropcolor'].split(';')]
    while len(backdropcolor) < 4:
        backdropcolor.append(1.0)

    # get compositor and clear defaults
    bpy.context.scene.use_nodes = True
    node_tree = bpy.context.scene.node_tree
    for node in node_tree.nodes:
        node_tree.nodes.remove(node)
    # create nodes
    render_node = node_tree.nodes.new(type='CompositorNodeRLayers')
    render_node.location = 0,-100
    output_node = node_tree.nodes.new('CompositorNodeComposite')   
    output_node.location = 800,0
    alpha_node = node_tree.nodes.new('CompositorNodeAlphaOver')   
    alpha_node.location = 400,0
    if backdroptype == 'ColorRGB':
        color_node = node_tree.nodes.new('CompositorNodeRGB')   
        color_node.outputs[0].default_value = backdropcolor
        color_node.location = 0,100
    elif backdroptype == 'Image':
        color_node = node_tree.nodes.new(type='CompositorNodeImage')
        color_node.location = 0,200
        if backdropimage and os.path.exists(backdropimage):
            texture_img = bpy.data.images.load(backdropimage)
            color_node.image = texture_img
    scale_node = node_tree.nodes.new(type='CompositorNodeScale')
    scale_node.space = 'RENDER_SIZE'
    scale_node.frame_method = 'FIT'



    # connect nodes with links
    links = node_tree.links
    link = links.new(color_node.outputs[0], scale_node.inputs[0]) #scale color (rgb or image)
    link = links.new(scale_node.outputs[0], alpha_node.inputs[1]) #color through scale to 1st alpha image input
    link = links.new(render_node.outputs[0], alpha_node.inputs[2]) #render to 2nd alpha image input
    link = links.new(render_node.outputs[1], alpha_node.inputs[0]) #render alpha to alpha factor
    link = links.new(alpha_node.outputs[0], output_node.inputs[0]) #alpha result to composite output


def getChildren(myObject): 
    children = [] 
    for ob in bpy.data.objects: 
        if ob.parent == myObject: 
            children.append(ob) 
    return children 


def look_at(object_, point):
    loc_object_ = object_.location
    direction = point - loc_object_
    rot_quat = direction.to_track_quat('-Z', 'Y') # point camera -Z axis (Y-vec up)
    rotation_euler = rot_quat.to_euler()
    object_.rotation_euler = rotation_euler


def createLampEevee(lampname, location, lamptype, object_data):
    scene = bpy.context.scene
    lamp_data = bpy.data.lights.new(name=lampname, type=lamptype)
    rgb = object_data[0]
    strength = object_data[1]
    rgb = tuple([x/255.0 for x in rgb])
    lamp_data.color = rgb
    lamp_data.energy = strength
    lamp_data.use_contact_shadow = True
    lamp_data.contact_shadow_distance = 0.1
    lamp_data.contact_shadow_bias = 0.1
    lamp_data.contact_shadow_thickness = 0.1
    lamp_data.shadow_buffer_bias = 1.0

    if lamptype == 'AREA':
        lamp_data.shape = 'RECTANGLE'
        lamp_data.size = object_data[2]
        lamp_data.size_y = object_data[3]
    elif lamptype in ['SPOT']:
        size = object_data[2]
        lamp_data.spot_size = radians(object_data[3])
    elif lamptype in ['POINT']:
        size = object_data[2]
        lamp_data.shadow_soft_size = float(size)
        lamp_data.use_shadow = True
    else: #SUN
        size = object_data[2]
    lamp_object = bpy.data.objects.new(name=lampname, object_data=lamp_data)
    lamp_object.location = location[1:4]
    point = mathutils.Vector((location[4], location[5], location[6]))
    look_at(lamp_object, point)
    return lamp_object




def clearScene(re_render):
    if re_render:
        # CLEAR just lights and camera
        for bpy_data_iter in (
                bpy.data.lights,
                bpy.data.cameras,
                            ):
            for id_data in bpy_data_iter:
                bpy_data_iter.remove(id_data)
    else:
        # CLEAR complete scene
        for bpy_data_iter in (
                bpy.data.objects,
                bpy.data.meshes,
                bpy.data.lights,
                bpy.data.collections,
                bpy.data.cameras,
                            ):
            for id_data in bpy_data_iter:
                bpy_data_iter.remove(id_data)


##########################################
############# OBJ IMPORTING ##############
##########################################
import bpy, os
class ObjGroup:
    def __init__(self,name):
        self.Name = name
        self.MaterialName = ""
        self.Faces = []
        self.TextureCoords = []
        self.TextureCoordsFlat = []
        self.Verts = []

class ObjMaterial:
    def __init__(self,name):
        self.Name = name
        self.Opacity = 1.0
        self.Color = 0.0, 0.0, 0.0
        self.ColorMap = ''
        self.Emission = 0.0
        self.Metallic = 0.0
        self.Roughness = 0.0
        self.NormalMap = ''
        self.Bumpiness = 0.0
        self.Clearcoat = 0.0
        self.ClearcoatRougness = 0.0
        self.Style = 'N/A'
        #self.ProceduralDisplacement = 'N/A'
        #self.DisplacementValue = 5.0
        #self.DisplacementScale = 5.0

def stripNonAscii(s):
    ss = ""
    for c in s:
        if ord(c) <128:
            ss += c
    return ss


def loadMAT(filename):
    materials = {}
    DIR = os.path.dirname(filename)
    material_name = 'OBJ_import_material'
    current_mat = None
    with open(filename, "r", encoding='utf8') as mtlfile:
        for line in mtlfile:
            #line = stripNonAscii(line.strip())
            line = line.strip()
            if not line or line[0] == '#':
                # skip empty or comment lines
                continue
            vals = line.split()
            line_id = vals[0].lower()
            if line_id == "newmtl":
                material_name = ' '.join(vals[1:]).strip(',.-#')
                if material_name not in materials:
                    materials[material_name] = ObjMaterial(material_name)
                current_mat = materials[material_name]
            elif line_id == 'kd':
                current_mat.Color = (float(vals[1]), float(vals[2]), float(vals[3]))
            elif line_id == 'ks':
                col_specular = (float(vals[1]), float(vals[2]), float(vals[3]))
            elif line_id == 'ke':
                current_mat.Emission = float(vals[1])
            elif line_id == 'd':  # dissolve (transparency)
                current_mat.Opacity = float(vals[1])
            elif line_id == 'bumpiness':  
                current_mat.Bumpiness = float(vals[1])
            elif line_id == 'clearcoat': 
                current_mat.Clearcoat = float(vals[1])
            elif line_id == 'roughness':  
                current_mat.Roughness = float(vals[1])
            elif line_id == 'metallic':  
                current_mat.Metallic = float(vals[1])
            elif line_id == 'map_kd':
                current_mat.ColorMap = os.path.join(str(DIR), vals[1] )
            elif line_id == 'map_bump':
                current_mat.NormalMap = os.path.join(str(DIR), vals[1] )
            elif line_id == 'style':
                current_mat.Style = vals[1]
    return materials


def loadOBJ(filename):
    global matData
    groups = {}
    group_name = os.path.splitext(os.path.basename(filename))[0]
    verts = []  
    texts = []
    vindex = 0
    mtllib = ""
    base_group_name = group_name
    currentline = 0
    prev_verts_count = 0
    #with open(filename, "r", encoding='latin-1') as objfile:
    with open(filename, "r", encoding='utf8') as objfile:
        for line in objfile:
            currentline+=1
            #line = stripNonAscii(line.strip())
            line = line.strip()
            if not line or line[0] == '#':
                # skip empty or comment lines
                continue
            vals = line.split() 
            if vals[0] == "mtllib":
                mtllib = ' '.join(vals[1:])
            if vals[0] == "v":
                # vertices
                v = tuple(map(float, vals[1:4]))
                verts.append(v)
            if vals[0] == "vt":
                # vertex texture coordinates
                t = tuple(map(float, vals[1:3])) # use only 2 coordinates (u,v)
                texts.append(t) #e.g. texts.append( (0.175, 0.791) )
            if vals[0] == "g":
                group_name = ' '.join(vals[1:])
                if group_name not in groups:
                    groups[group_name] = ObjGroup(group_name) 
                groups[group_name].Verts = verts[:]
                groups[group_name].TextureCoords = texts[:]
                vindex += prev_verts_count
                prev_verts_count = len(verts[:])
                verts = []
                texts = []
                base_group_name = group_name
            if vals[0] == "usemtl":
                matname = ' '.join(vals[1:]).strip(',.-#')
                #group_name = base_group_name + '_' + matname
                #if group_name not in groups:
                #    groups[group_name] = ObjGroup(group_name) 
                groups[group_name].MaterialName = matname
            if vals[0] == "f":
                face = []
                text = []
                # FACE
                for f in vals[1:]:  
                    w = f.split("/")  
                    # FACE VERTEX
                    try:face.append( int(w[0])-1-vindex ) # obj indexing starts from 1
                    except:
                        print(currentline,'<= on line. Error: vertex indexing', len(verts), [int(w[0])-1-vindex])
                        return
                    # FACE TEXTURE COORDINATE
                    # try:     text.append( texts[int(w[1])-1-tindex] )
                    # try:     groups[group_name].TextureCoordsFlat.extend( groups[group_name].TextureCoords[int(w[1])-1] )
                    # except:  groups[group_name].TextureCoordsFlat.extend( [0,0] )
                    try:text.extend( groups[group_name].TextureCoords[int(w[1])-1-vindex] )
                    except:
                        print(currentline,'<= on line. Error: vertex indexing', len(verts), [int(w[0])-1-vindex])
                        return
                # ADD FACE TO THIS GROUP 
                groups[group_name].Faces.append(face)  #(groups ~ dictionary)
                groups[group_name].TextureCoordsFlat.extend(text)
    if verts and group_name in groups:
        # store previous group's verts
        groups[group_name].Verts = verts[:]
        verts = []
    # remove if there are any empty groups
    emptygroups = []
    for g in groups.keys():
        if not groups[g].Faces:
            emptygroups.append(g)
    for e in emptygroups:
        del groups[e]
    return groups#, texts

EMPTY_TYPE = None
import numpy as np
def loadmodel(filename, name, blender_materials, collection):
    #basename, extension = os.path.splitext(os.path.basename(filename))
    items = loadOBJ(filename) 
    empty_object = bpy.data.objects.new( name, EMPTY_TYPE )
    collection.objects.link(empty_object)
    for item_name in items:
        item = items[item_name]
        mat = blender_materials.get(item.MaterialName)
        read_mesh(  empty_object,
                        collection,
                        item_name, 
                        item.Verts, 
                        item.Faces, 
                        item.TextureCoordsFlat,
                        mat)
    return empty_object


def read_mesh(  parent_object,
                collection,
                item_name, 
                vertices, 
                faces, 
                text_coords,
                material):
    # rint('-'*99)
    # rint(item_name)
    # rint('vertices',len(vertices),vertices)
    # rint('text_coords',len(text_coords),text_coords)
    mesh_data = bpy.data.meshes.new(item_name)
    mesh_data.from_pydata(vertices, [], faces)
    mesh_data.update(calc_edges=True)
    scene_object = bpy.data.objects.new(item_name, mesh_data)
    scene_object.parent = parent_object
    collection.objects.link(scene_object)
    scene_object.data.materials.append(material)
    scene_object.data.polygons.foreach_set("use_smooth", [True]*len(scene_object.data.polygons))
    # UV
    uv = scene_object.data.uv_layers.active
    if uv is None:
        uv = scene_object.data.uv_layers.new(name="UVMap")
    uv.data.foreach_set("uv", text_coords)

##########################################
############# OBJ IMPORTING funcs end ####
##########################################
def convertToVideo(file_sequence, filepathroot, config_dict):
    for i, uri in enumerate( file_sequence ):
        bpy.context.scene.sequence_editor.sequences.new_image(  'image_sequence', uri, 2, i )
    bpy.context.scene.frame_start = 0
    bpy.context.scene.frame_end = i
    bpy.context.scene.render.resolution_x = int(config_dict['resolution_x'])
    bpy.context.scene.render.resolution_y = int(config_dict['resolution_y'])
    bpy.context.scene.render.resolution_percentage = 100
    if video_container == 'MP4':
        bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
        bpy.context.scene.render.ffmpeg.format = "MPEG4"
        bpy.context.scene.render.ffmpeg.codec = "H264"
        bpy.context.scene.render.ffmpeg.constant_rate_factor = "HIGH"
        bpy.context.scene.render.ffmpeg.ffmpeg_preset = "GOOD"
        video_uri = filepathroot + '.mp4'
    else:
        bpy.context.scene.render.image_settings.file_format = 'AVI_JPEG'
        video_uri = filepathroot + '.avi'
    video_uri = auto_increment_filename(video_uri)
    bpy.context.scene.render.filepath = video_uri
    bpy.ops.render.render( animation=True )


import webbrowser
def main():
    profiler_in = time.perf_counter()
    openinblender, config_dict = do_import_vc()
    frameCount = bpy.context.scene.frame_end - bpy.context.scene.frame_start
    filepathroot, file_extension = os.path.splitext(bpy.context.scene.render.filepath)
    save_file_uri = os.path.join(uri_root, 'blender_scene.blend' ) 
    # Pack all external resources into the .blend file
    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=save_file_uri)
    if not openinblender:
        if frameCount == 0:
            bpy.context.scene.frame_set( 0 )
            bpy.context.scene.render.filepath = auto_increment_filename(bpy.context.scene.render.filepath)
            bpy.ops.render.render( write_still=True )
            time.sleep(0.2)
            webbrowser.open(bpy.context.scene.render.filepath)
        else:
            file_sequence = []
            froot, fname = os.path.split(filepathroot)
            #try:os.path.makedir(filepathroot+'_frames')
            #except:pass
            for i in range(frameCount):
                bpy.context.scene.frame_set( i )
                i_filename = os.path.join(filepathroot+'_frames', fname+str(i)+file_extension)
                file_sequence.append( i_filename )
                bpy.context.scene.render.filepath = i_filename
                bpy.ops.render.render( write_still=True )
            bpy.context.scene.view_settings.exposure = 0.0
            convertToVideo(file_sequence, filepathroot, config_dict)
    profiler_out = time.perf_counter()
    print('Total Blender time:', round((profiler_out - profiler_in), 3), "s")

 
if __name__ == "__main__":
    main()



