# BlenderProps.py
# Visual Components 4.10 — Python Command (IronPython 2.7 compatible)
# Adds a button in the Wizards menu to generate predefined properties to be used in conjunction with the Blenderer Add-on

from vcCommand import *

# --- selection helpers (tolerant across 4.x variations) ---
try:
    # Newer helper layout
    from vcHelpers.Selection import getSelectedFeatures, getSelectedNodesFeatures
except:
    # Older layout fallback
    try:
        from vcHelpers import Selection
        def getSelectedFeatures():
            return Selection.getSelectedFeatures()
        def getSelectedNodesFeatures():
            try:
                return Selection.getSelectedNodesFeatures()
            except:
                return []
    except:
        def getSelectedFeatures():
            return []
        def getSelectedNodesFeatures():
            return []

try:
    from vcHelpers.SelectionManager import SelectionManager
except:
    SelectionManager = None
        
APP = getApplication()
cmd = getCommand()
sim = getSimulation()


# --- Pre-defined Property Sets ---
# Add your property definitions here using the following format:
# Each property is a tuple: (name, type, value)
# Supported types: VC_BOOLEAN, VC_INTEGER, VC_REAL, VC_STRING

# IMPORTANT: Specify the component name here (leave empty to be prompted)
COMPONENT_NAME = ""  # e.g., "MyComponent" or leave empty

COMPONENT_PROPERTIES = [
    # Example: ("MyBoolProperty", VC_BOOLEAN, True),
    # Example: ("MyIntProperty", VC_INTEGER, 0),
    # Example: ("MyRealProperty", VC_REAL, 0.0),
    # Example: ("MyStringProperty", VC_STRING, ""),
    ("Blender::Cast Shadow", VC_BOOLEAN, True),
    ("Blender::Visible in Camera", VC_BOOLEAN, True),
    ("Blender::Holdout Mask", VC_BOOLEAN, False),
    ("Blender::Collection", VC_STRING, "Collection")
    
]


def addPropertiesToComponent(comp, properties):
    """
    Add a list of properties to a component.
    
    Args:
        comp: The component to add properties to
        properties: List of tuples (name, type, default_value)
    """
    if not comp:
        return
    
    for prop_name, prop_type, default_value in properties:
        # Check if property already exists
        existing_prop = comp.getProperty(prop_name)
        if existing_prop:
            print("  Property '%s' already exists on component '%s', skipping." % (prop_name, comp.Name))
            continue
        
        # Create new property
        new_prop = comp.createProperty(prop_type, prop_name)
        if new_prop:
            new_prop.Value = default_value
            print("  Added property '%s' to component '%s'" % (prop_name, comp.Name))
        else:
            print("  Failed to create property '%s' on component '%s'" % (prop_name, comp.Name))


def OnStart():
    """Main function to add properties to selected component and its links."""
    comp = None
    
    # Method 1: Try SelectionManager with VC_SELECTION_COMPONENT (same as RobotWizard)
    try:
        comps = APP.SelectionManager.getSelection(VC_SELECTION_COMPONENT)
        if comps:
            comp = comps[0]
            print("Found component from SelectionManager: %s" % comp.Name)
    except Exception as e:
        print("Method 1 (SelectionManager) debug: %s" % str(e))
    
    # Method 2: Try getting from selected features
    if not comp:
        try:
            selected_features = getSelectedFeatures()
            if selected_features:
                comp = selected_features[0].Component
                print("Found component from selected features: %s" % comp.Name)
        except:
            pass
    
    # Method 3: Try getting from selected nodes
    if not comp:
        try:
            selected_nodes = getSelectedNodesFeatures()
            if selected_nodes:
                comp = selected_nodes[0].Component
                print("Found component from selected nodes: %s" % comp.Name)
        except:
            pass
    
    # Method 4: Use component name from configuration
    if not comp and COMPONENT_NAME:
        comp = APP.findComponent(COMPONENT_NAME)
        if comp:
            print("Found component by configured name: %s" % comp.Name)
        else:
            print("ERROR: Component '%s' not found." % COMPONENT_NAME)
            return
    
    # Method 5: If still no component, try to get a list of all components
    if not comp:
        print("")
        print("Searching for components in the world...")
        all_comps = []
        try:
            # Try to find components by common naming patterns
            # We'll try numbers and common names
            test_names = ["World", "Ground", "Component", "Model", "Robot", "Part"]
            for i in range(1, 100):  # Try up to 100 component indices
                try:
                    test_comp = APP.findComponent(str(i))
                    if test_comp and test_comp not in all_comps:
                        all_comps.append(test_comp)
                except:
                    pass
            
            # Try finding by common prefixes
            for prefix in test_names:
                for i in range(1, 20):
                    for suffix in ["", str(i), " " + str(i)]:
                        try:
                            test_comp = APP.findComponent(prefix + suffix)
                            if test_comp and test_comp not in all_comps:
                                all_comps.append(test_comp)
                        except:
                            pass
        except:
            pass
        
        if all_comps:
            print("")
            print("=" * 60)
            print("FOUND %s COMPONENT(S) IN THE WORLD:" % len(all_comps))
            print("=" * 60)
            for i, c in enumerate(all_comps, 1):
                print("%s. %s" % (i, c.Name))
            print("=" * 60)
            print("")
            print("Please set COMPONENT_NAME to one of the above names.")
            print("Example: COMPONENT_NAME = \"%s\"" % all_comps[0].Name)
            print("=" * 60)
            return
    
    # Method 6: Prompt user to set component name
    if not comp:
        print("")
        print("=" * 60)
        print("NO COMPONENT FOUND")
        print("=" * 60)
        print("Please set COMPONENT_NAME at the top of the script.")
        print("Example: COMPONENT_NAME = \"MyComponent\"")
        print("")
        print("To find your component name:")
        print("1. Look at the Component Browser tree")
        print("2. Or check the title bar when in modeling tab")
        print("=" * 60)
        return
    
    if not comp:
        print("ERROR: No component selected or active.")
        print("Please select a component in the 3D world or component tree and try again.")
        return
    
    print("Adding properties to component: %s" % comp.Name)
    print("")
    
    # Add properties to component
    if COMPONENT_PROPERTIES:
        print("Adding component properties...")
        addPropertiesToComponent(comp, COMPONENT_PROPERTIES)
    else:
        print("No component properties defined in COMPONENT_PROPERTIES list.")
    
    print("")
    print("Done!")


