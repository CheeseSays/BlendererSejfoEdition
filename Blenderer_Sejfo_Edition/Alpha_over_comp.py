import bpy
import mathutils
import os
import typing


# Generate unique scene name
base_name = "Scene"
end_name = base_name
if bpy.data.scenes.get(end_name) is not None:
    i = 1
    end_name = base_name + f".{i:03d}"
    while bpy.data.scenes.get(end_name) is not None:
        end_name = base_name + f".{i:03d}"
        i += 1

bpy.ops.scene.new(type='NEW')
scene = bpy.context.scene
scene.name = end_name
scene.use_fake_user = True
bpy.context.window.scene = scene
if bpy.app.version < (5, 0, 0):
    scene.use_nodes = True
scene.audio_doppler_factor = 1.0
scene.audio_doppler_speed = 343.29998779296875
scene.audio_volume = 1.0
scene.use_audio = True
scene.use_audio_scrub = False
scene.use_gravity = True
scene.audio_distance_model = 'INVERSE_CLAMPED'
scene.sync_mode = 'NONE'
scene.gravity = (0.0, 0.0, -9.8100004196167)
scene.use_stamp_note = ""

def compositor_nodes_node_group(node_tree_names: dict[typing.Callable, str]):
    """Initialize Compositor Nodes node group"""
    if bpy.app.version < (5, 0, 0):
        compositor_nodes = scene.node_tree
    else:
        scene.compositing_node_group = bpy.data.node_groups.new(type = 'CompositorNodeTree', name = "Compositor Nodes")
        compositor_nodes = scene.compositing_node_group

    # Start with a clean node tree
    for node in compositor_nodes.nodes:
        compositor_nodes.nodes.remove(node)
    compositor_nodes.color_tag = 'NONE'
    compositor_nodes.description = ""
    compositor_nodes.default_group_node_width = 140
    # compositor_nodes interface

    # Socket Image
    image_socket = compositor_nodes.interface.new_socket(name="Image", in_out='OUTPUT', socket_type='NodeSocketColor')
    image_socket.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket.attribute_domain = 'POINT'
    image_socket.default_input = 'VALUE'
    image_socket.structure_type = 'AUTO'

    # Socket Image
    image_socket_1 = compositor_nodes.interface.new_socket(name="Image", in_out='INPUT', socket_type='NodeSocketColor')
    image_socket_1.default_value = (0.0, 0.0, 0.0, 1.0)
    image_socket_1.attribute_domain = 'POINT'
    image_socket_1.default_input = 'VALUE'
    image_socket_1.structure_type = 'AUTO'

    # Initialize compositor_nodes nodes

    # Node Group Output
    group_output = compositor_nodes.nodes.new("NodeGroupOutput")
    group_output.name = "Group Output"
    group_output.is_active_output = True

    # Node Render Layers
    render_layers = compositor_nodes.nodes.new("CompositorNodeRLayers")
    render_layers.name = "Render Layers"
    render_layers.layer = 'ViewLayer'

    # Node Reroute
    reroute = compositor_nodes.nodes.new("NodeReroute")
    reroute.name = "Reroute"
    reroute.socket_idname = "NodeSocketColor"
    # Node Viewer
    viewer = compositor_nodes.nodes.new("CompositorNodeViewer")
    viewer.name = "Viewer"
    viewer.ui_shortcut = 0

    # Node Alpha Over
    alpha_over = compositor_nodes.nodes.new("CompositorNodeAlphaOver")
    alpha_over.name = "Alpha Over"
    # Background
    alpha_over.inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    # Fac
    alpha_over.inputs[2].default_value = 1.0
    # Type
    alpha_over.inputs[3].default_value = 'Over'
    # Straight Alpha
    alpha_over.inputs[4].default_value = False

    # Set locations
    compositor_nodes.nodes["Group Output"].location = (200.0, 0.0)
    compositor_nodes.nodes["Render Layers"].location = (-529.6492919921875, -2.9944028854370117)
    compositor_nodes.nodes["Reroute"].location = (100.0, -35.0)
    compositor_nodes.nodes["Viewer"].location = (200.0, -80.0)
    compositor_nodes.nodes["Alpha Over"].location = (-172.06793212890625, 3.49346923828125)

    # Set dimensions
    compositor_nodes.nodes["Group Output"].width  = 140.0
    compositor_nodes.nodes["Group Output"].height = 100.0

    compositor_nodes.nodes["Render Layers"].width  = 240.0
    compositor_nodes.nodes["Render Layers"].height = 100.0

    compositor_nodes.nodes["Reroute"].width  = 10.0
    compositor_nodes.nodes["Reroute"].height = 100.0

    compositor_nodes.nodes["Viewer"].width  = 140.0
    compositor_nodes.nodes["Viewer"].height = 100.0

    compositor_nodes.nodes["Alpha Over"].width  = 140.0
    compositor_nodes.nodes["Alpha Over"].height = 100.0


    # Initialize compositor_nodes links

    # reroute.Output -> group_output.Image
    compositor_nodes.links.new(
        compositor_nodes.nodes["Reroute"].outputs[0],
        compositor_nodes.nodes["Group Output"].inputs[0]
    )
    # reroute.Output -> viewer.Image
    compositor_nodes.links.new(
        compositor_nodes.nodes["Reroute"].outputs[0],
        compositor_nodes.nodes["Viewer"].inputs[0]
    )
    # render_layers.Image -> alpha_over.Foreground
    compositor_nodes.links.new(
        compositor_nodes.nodes["Render Layers"].outputs[0],
        compositor_nodes.nodes["Alpha Over"].inputs[1]
    )
    # alpha_over.Image -> reroute.Input
    compositor_nodes.links.new(
        compositor_nodes.nodes["Alpha Over"].outputs[0],
        compositor_nodes.nodes["Reroute"].inputs[0]
    )

    return compositor_nodes


if __name__ == "__main__":
    # Maps node tree creation functions to the node tree 
    # name, such that we don't recreate node trees unnecessarily
    node_tree_names : dict[typing.Callable, str] = {}

    compositor_nodes = compositor_nodes_node_group(node_tree_names)
    node_tree_names[compositor_nodes_node_group] = compositor_nodes.name

