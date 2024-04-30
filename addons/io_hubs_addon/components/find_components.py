import bpy
from bpy.props import EnumProperty, BoolProperty
from bpy.types import Operator
from os.path import join, isfile, isdir, dirname, realpath
from . import components_registry

COMPONENT_TYPE_ITEMS = None # collect 

def get_component_definitions():
    global COMPONENT_TYPE_ITEMS
    if COMPONENT_TYPE_ITEMS is None: 
        components_dir = join(dirname(realpath(__file__)), "definitions")
        component_names = components_registry.get_components_in_dir(components_dir)
        print ("Component names:\n",component_names)
        COMPONENT_TYPE_ITEMS = [("All", "Search for all hubs components", 'ALL')]
        # for c in component_names:
        #     COMPONENT_TYPE_ITEMS.append(get_item_from_name(c))

    return COMPONENT_TYPE_ITEMS

def get_item_from_name(name):
    label = name.replace('-', ' ').title()
    description = "Look for " + label + " component "
    id = name.replace('-','_')
    return (label, description, id)

class FindHubsComponents(Operator):
    bl_idname = "object.find_hubs_component"
    bl_label = "Find Hubs Components in Scene"
    bl_options = {'REGISTER'}

    component_type: EnumProperty(
        name="Type", 
        description="Select Type",
        items=get_component_definitions()
    )
    select_objects: BoolProperty(
        name="Select Objects",
        description="Select the objects with the desired component(s)",
        default=True
    )
    def execute(self, context):
        print("Finding objects", self.component_type)
        objects_with_component = self.collect_all_components() if self.component_type == 'All' else self.collect_components() 
        self.print_report_all(objects_with_component)
        return {'FINISHED'}

    def collect_components(self):
        name = self.component_type
        all_objects = bpy.data.objects
        objects_with_component = []
        for ob in all_objects:
            if ob.get(name) is not None:
                objects_with_component.append(ob)

        return objects_with_component

    def collect_all_components(self):
        all_objects = bpy.data.objects
        objects_with_component = []
        for ob in all_objects:
            try:
                components = ob['hubs_component_list']
                if len(components) > 0:
                    objects_with_component.append(ob)
            except:
                pass
        return objects_with_component

    # def print_report(self, objects):
    #     print("Looking for component", self.component_name)
    #     if len(objects) == 0:
    #         print("Did not find any")
    #         return
    #     for ob in objects:
    #         print("Found:", ob.name)
    #         if self.select_objects:
    #             ob.select_set(True)

    def print_report_all(self, objects):
        if len(objects) == 0:
            print("There are no objects with hubs components in the scene")
            return
        print("All objects with a hubs component:")
        for ob in objects:
            print("Found:", ob.name, "with")
            for component in ob['hubs_component_list']['items']:
                for entry in component.to_dict():
                    name = component['name'].replace('-', ' ')
                    print("\t" + name.title())
            if self.select_objects:
                ob.select_set(True)



def register():
    print("Registering FindHubsComponents") 
    bpy.utils.register_class(FindHubsComponents)
def unregister():
    bpy.utils.unregister_class(FindHubsComponents)
