"""
State:          "ppm::inspector::1.0"
State type:     "ppm::inspector::1.0"
Description:    "ppm::inspector::1.0"
Author:         hernan
Date Created:   March 25, 2022 - 15:43:32
"""

"""
import hou

viewer = hou.ui.paneTabOfType(hou.paneTabType.SceneViewer)

viewport = viewer.selectedViewport()
is_cam = viewport.camera()
name = viewport.name()
node = viewport.queryNodeAtPixel()

print (is_cam, name)
"""
import hou
import viewerstate.utils as su

class State(object):
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer

    def onGenerate(self, kwargs):
        # Show a prompt to the user
        self.scene_viewer.setPromptMessage("Hover over primitives to show info")

        # Make the group selection box visible
        self.scene_viewer.setGroupListVisible(True)
        self.log("Entered Inspector")

    def onInterrupt(self, kwargs):
        """ Called when the state is interrupted e.g when the mouse 
        moves outside the viewport
        """
        pass

    def onResume(self, kwargs):
        """ Called when an interrupted state resumes
        """
        pass

    def onMouseEvent(self, kwargs):
        """ Process mouse events
        """
        ui_event = kwargs["ui_event"]
        dev = ui_event.device()
        self.log("Mouse:", dev.mouseX(), dev.mouseY(), dev.isLeftButton())

        # Must return True to consume the event
        return False

    def onMouseWheelEvent(self, kwargs):
        """ Process a mouse wheel event
        """

        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]

        # Must return True to consume the event
        return False

    def onMenuAction(self, kwargs):
        """ Callback implementing the actions of a bound menu. Called 
        when a menu item has been selected. 
        """

        menu_item = kwargs["menu_item"]
        state_parms = kwargs["state_parms"]



    def onKeyEvent(self, kwargs):
        """ Called for processing a keyboard event
        """
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]

        # Must returns True to consume the event
        return False
    
    def onDraw(self, kwargs):
        """ Called for rendering a state e.g. required for 
        hou.AdvancedDrawable objects
        """
        draw_handle = kwargs["draw_handle"]


def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = "ppm::inspector::1.0"
    state_label = "1 ppm - inspector"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon("MISC_python")




    return template
