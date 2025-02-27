bl_info = {
    "name": "Blend File Auto Renamer - Irgalle",
    "blender": (3, 3, 19),
    "category": "Render",
    "description": "Automatisasi rename dan save file .blend dengan versi yang bertambah",
    "author": "Irgalle",
    "version": (1, 0, 0),
    "location": "View3D > Sidebar > AutoRenamer",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
}

import bpy
import os
import re
from bpy.props import CollectionProperty, StringProperty
from bpy_extras.io_utils import ImportHelper

# Fungsi untuk mendapatkan versi berikutnya
def get_next_version(filepath):
    base, ext = os.path.splitext(filepath)
    match = re.search(r"_RENDER_V(\d+)$", base)
    if match:
        version = int(match.group(1)) + 1
        new_name = re.sub(r"_RENDER_V\d+$", f"_RENDER_V{version:03d}", base) + ext
    else:
        new_name = base + "_RENDER_V001" + ext
    return new_name

# Fungsi untuk membuka, save as, dan rename file .blend
def process_blend_file(filepath):
    if not os.path.exists(filepath):
        print(f"File tidak ditemukan: {filepath}")
        return
    
    new_filepath = get_next_version(filepath)
    bpy.ops.wm.open_mainfile(filepath=filepath)
    bpy.ops.wm.save_as_mainfile(filepath=new_filepath)
    print(f"File tersimpan: {new_filepath}")

# Operator untuk memilih subfolder
class OT_SelectFolders(bpy.types.Operator, ImportHelper):
    bl_idname = "wm.select_folders"
    bl_label = "Pilih Folder"
    filter_glob: StringProperty(default="*.blend", options={'HIDDEN'})
    files: CollectionProperty(type=bpy.types.PropertyGroup)
    directory: StringProperty(subtype="DIR_PATH")
    
    def execute(self, context):
        selected_folders = [os.path.join(self.directory, f.name) for f in self.files]
        
        for folder in selected_folders:
            for root, _, files in os.walk(folder):
                for file in files:
                    if file.endswith(".blend"):
                        process_blend_file(os.path.join(root, file))
        return {'FINISHED'}

# Panel UI di Blender
class PT_BlendRenamerPanel(bpy.types.Panel):
    bl_label = "Blend File Auto Renamer"
    bl_idname = "PT_BlendRenamerPanel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "AutoRenamer"

    def draw(self, context):
        layout = self.layout
        layout.operator("wm.select_folders", text="Pilih Folder")

# Registrasi addon
def register():
    bpy.utils.register_class(OT_SelectFolders)
    bpy.utils.register_class(PT_BlendRenamerPanel)

def unregister():
    bpy.utils.unregister_class(OT_SelectFolders)
    bpy.utils.unregister_class(PT_BlendRenamerPanel)

if __name__ == "__main__":
    register()
