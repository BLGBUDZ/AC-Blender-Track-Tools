bl_info = {
    "name": "AC Track Tools",
    "author": "BLGBUDZ",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > AC Track Tools",
    "description": "Tools for AC Track creation",
    "warning": "",
    "category": "3D View"
}

import bpy

class SetObjectTypeOperator(bpy.types.Operator):
    """Set the custom property for Assetto Corsa object type"""
    bl_idname = "object.set_ac_type"
    bl_label = "Set AC Object Type"
    
    ac_type: bpy.props.StringProperty()
    
    def create_material_with_null_texture(self, name):
        # Create new material if it doesn't exist
        mat = bpy.data.materials.get(name)
        if mat is None:
            mat = bpy.data.materials.new(name=name)
        
        # Enable nodes
        mat.use_nodes = True
        nodes = mat.node_tree.nodes
        
        # Clear existing nodes
        nodes.clear()
        
        # Create nodes
        principled = nodes.new('ShaderNodeBsdfPrincipled')
        output = nodes.new('ShaderNodeOutputMaterial')
        tex_image = nodes.new('ShaderNodeTexImage')
        
        # Set null.dds texture
        if "null.dds" not in bpy.data.images:
            null_img = bpy.data.images.new("null.dds", 1, 1)
            null_img.source = 'FILE'
            null_img.filepath = "null.dds"
        else:
            null_img = bpy.data.images["null.dds"]
        
        tex_image.image = null_img
        
        # Link nodes
        links = mat.node_tree.links
        links.new(tex_image.outputs['Color'], principled.inputs['Base Color'])
        links.new(principled.outputs['BSDF'], output.inputs['Surface'])
        
        return mat
    
    def execute(self, context):
        selected_objects = bpy.context.selected_objects
        
        if not selected_objects:
            self.report({'WARNING'}, "No objects selected")
            return {'CANCELLED'}
            
        for obj in selected_objects:
            # Set the custom property
            obj["ac_type"] = self.ac_type
            
            # Create and assign material
            mat_name = f"{self.ac_type}_material"
            mat = self.create_material_with_null_texture(mat_name)
            
            # Assign material to object
            if obj.data:  # Check if object has data (mesh, curve, etc)
                if len(obj.material_slots) == 0:
                    obj.data.materials.append(mat)
                else:
                    obj.material_slots[0].material = mat
            
            # Rename the object
            obj.name = f"{self.ac_type}_{obj.name.split('_')[-1]}" if '_' in obj.name else f"{self.ac_type}"
            
        self.report({'INFO'}, f"Set {len(selected_objects)} objects to {self.ac_type} with null.dds material")
        return {'FINISHED'}



class MyCustomPanel(bpy.types.Panel):
    """Creates a custom panel in Blender's UI"""
    bl_label = "AC Track Tools"
    bl_idname = "VIEW3D_PT_ac_track_tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'AC Track Tools'

    def draw(self, context):
        layout = self.layout
        
        # Track Elements Section
        box = layout.box()
        box.label(text="MATERIAL PHYSICS")
        
        col = box.column(align=True)
        col.operator("object.set_ac_type", text="ROAD").ac_type = "1ROAD"
        col.operator("object.set_ac_type", text="Grass").ac_type = "1GRASS"
        col.operator("object.set_ac_type", text="Curb").ac_type = "1KERB"
        col.operator("object.set_ac_type", text="Gravel").ac_type = "1GRAVEL"
        col.operator("object.set_ac_type", text="Wall").ac_type = "1WALL"
        
        # Track Details Section
        box = layout.box()
        box.label(text="TRACK REQUIREMENTS (add these or no worky)")
        
        col = box.column(align=True)
        col.operator("object.set_ac_type", text="START 0").ac_type = "AC_START_0"
        col.operator("object.set_ac_type", text="START 1").ac_type = "AC_START_1"
        col.operator("object.set_ac_type", text="PIT 0").ac_type = "AC_PIT_0"
        col.operator("object.set_ac_type", text="PIT 1").ac_type = "AC_PIT_1"
        col.operator("object.set_ac_type", text="HL START 0").ac_type = "AC_HOTLAP_START_0"
        col.operator("object.set_ac_type", text="TIME 0 L").ac_type = "AC_TIME_0_L"
        col.operator("object.set_ac_type", text="TIME 0 R").ac_type = "AC_TIME_0_R"
        col.operator("object.set_ac_type", text="AC_TIME_1_L").ac_type = "AC_TIME_1_L"
        col.operator("object.set_ac_type", text="AC_TIME_1_R").ac_type = "AC_TIME_1_R"

def register():
    bpy.utils.register_class(SetObjectTypeOperator)
    bpy.utils.register_class(MyCustomPanel)

def unregister():
    bpy.utils.unregister_class(SetObjectTypeOperator)
    bpy.utils.unregister_class(MyCustomPanel)

if __name__ == "__main__":
    register()
