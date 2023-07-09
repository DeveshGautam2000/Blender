import bpy
import math

# Clear existing scene
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.object.select_by_type(type='MESH')
bpy.ops.object.delete()

# Create a new scene
scene = bpy.context.scene

# Set up camera
camera = bpy.data.objects.new('Camera', bpy.data.cameras.new('Camera'))
scene.collection.objects.link(camera)
scene.camera = camera

# Create glasses mesh
vertices = [
    (-1, 1, 0),
    (1, 1, 0),
    (-1, -1, 0),
    (1, -1, 0)
]

faces = [
    (0, 1, 3, 2)
]

glasses_mesh = bpy.data.meshes.new('GlassesMesh')
glasses_mesh.from_pydata(vertices, [], faces)

glasses_obj = bpy.data.objects.new('GlassesObject', glasses_mesh)
scene.collection.objects.link(glasses_obj)

# Set up glass material
glass_material = bpy.data.materials.new('GlassMaterial')
glass_material.use_nodes = True
glass_material.node_tree.nodes.clear()
glass_material_output = glass_material.node_tree.nodes.new(
    'ShaderNodeOutputMaterial')
glass_material_bsdf = glass_material.node_tree.nodes.new(
    'ShaderNodeBsdfPrincipled')
glass_material.node_tree.links.new(
    glass_material_bsdf.outputs['BSDF'], glass_material_output.inputs['Surface'])
glass_material_bsdf.inputs['Base Color'].default_value = (
    0.2, 0.4, 0.8, 1.0)  # Adjust the RGB values as desired
glass_material_bsdf.inputs['Transmission'].default_value = 1.0
glass_material_bsdf.inputs['Transmission Roughness'].default_value = 0.0
glasses_obj.data.materials.append(glass_material)

# Set up the render settings
scene.render.image_settings.file_format = 'PNG'

# Set the panoramic camera properties
camera.data.type = 'PANO'
camera.data.cycles.panorama_type = 'EQUIRECTANGULAR'

# Define the number of steps to capture the panoramic view
num_steps = 36  # Adjust this value to control the level of detail

# Set the render output path and base filename
output_path = '/path/to/save/panoramic_view_'
output_file_extension = '.png'

# Capture the panoramic view by rotating the camera
for step in range(num_steps):
    angle = 2 * math.pi * (step / num_steps)
    camera.rotation_euler[2] = angle

    # Set the output filename for the current step
    scene.render.filepath = output_path + \
        str(step).zfill(3) + output_file_extension

    # Render the current step
    bpy.ops.render.render(write_still=True)
