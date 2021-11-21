from __future__ import print_function

import hou

# A minimal state handler implementation. 
class MyState(object):
    """
    state_name: The state name string this state is registered under

    scene_viewer: A hou.SceneViewer object representing the scene viewer
    the tool is operating in, this object has many useful methods you can 
    use to implement your state, for example:
    hou.SceneViewer.currentGeometrySelection()
    hou.SceneViewer.setCurrentGeometrySelection()
    """
    def __init__(self, state_name, scene_viewer):
        """
        Storing the arguments in attributes so we can use them in other methods
        """
        self.state_name = state_name
        self.scene_viewer = scene_viewer

    # Handler methods go here
    def onMouseEvent(self, kwargs):
        dev = kwargs["ui_event"].device()
        print("Mouse:", dev.mouseX(), dev.mouseY(), dev.isLeftButton())

# A registration entry-point
def createViewerStateTemplate():
    # Choose a name and label 
    state_name = "mystate"
    state_label = "My New State"
    category = hou.sopNodeTypeCategory()

    # Create the template
    template = hou.ViewerStateTemplate(state_name, state_label, category)
    template.bindFactory(MyState)

    # Other optional bindings will go here...

    # returns the 'mystate' template
    return template