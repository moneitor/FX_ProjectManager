"""
State:          Sample Scripts
State type:     ppm::sampleScripts
Description:    Ppm::sampleScripts
Author:         hernan
Date Created:   March 10, 2022 - 02:06:47
"""


import hou
import viewerstate.utils as su

class State(object):
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer

    def onEnter(self,kwargs):
        """ Called on node bound states when it starts
        """
        node = kwargs["node"]
        state_parms = kwargs["state_parms"]

        # print kwargs in the viewer state console if "Debug log" is 
        # enabled
        self.log("onEnter=",kwargs)

    def onExit(self,kwargs):
        """ Called when the state terminates
        """
        state_parms = kwargs["state_parms"]

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



    def onMenuPreOpen(self, kwargs):
        """ Implement this callback to update the menu content before 
        it is drawn. 
        """
        menu_states = kwargs["menu_states"]
        menu_item_states = kwargs["menu_item_states"]



    def onParmChangeEvent(self, kwargs):
        """ Implement this callback to react to state parameter changes. 
        """
        parm_name = kwargs["parm_name"]
        parm_value = kwargs["parm_value"]
        state_parms = kwargs["state_parms"]
        ui_event = kwargs["ui_event"]

    def onHandleToState(self, kwargs):
        """ Used with bound dynamic handles to implement the state 
        action when a handle is modified.
        """

        handle = kwargs["handle"]
        parms = kwargs["parms"]
        mod_parms = kwargs["mod_parms"]
        prev_parms = kwargs["prev_parms"]
        ui_event = kwargs["ui_event"]

    def onStateToHandle(self, kwargs):
        """ Used with bound dynamic handles to implement the handle 
        action when a state node parm is modified.
        """

        handle = kwargs["handle"]
        parms = kwargs["parms"]

    def onBeginHandleToState(self, kwargs):
        """ Used with bound dynamic handles to implement the state 
        action when a handle modification has started.
        """

        handle = kwargs["handle"]
        ui_event = kwargs["ui_event"]

    def onEndHandleToState(self, kwargs):
        """ Used with bound dynamic handles to implement the state 
        action when a handle modification has ended.
        """

        handle = kwargs["handle"]
        ui_event = kwargs["ui_event"]

    def onKeyEvent(self, kwargs):
        """ Called for processing a keyboard event
        """
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]

        # Must returns True to consume the event
        return False

    def onKeyTransitEvent(self, kwargs):
        """ Called for processing a transitory key event
        """
        ui_event = kwargs["ui_event"]
        state_parms = kwargs["state_parms"]

        # Must returns True to consume the event
        return False

    def onCommand(self, kwargs):
        """ Use this callback to implement custom commands. 
        """
        command_name = kwargs["command_name"]
        command_args = kwargs["command_args"]
    
    def onDraw(self, kwargs):
        """ Called for rendering a state e.g. required for 
        hou.AdvancedDrawable objects
        """
        draw_handle = kwargs["draw_handle"]

    def onDrawInterrupt(self, kwargs):
        """ Called for rendering an interrupted state e.g. required for 
        hou.AdvancedDrawable objects
        """
        draw_handle = kwargs["draw_handle"]

    def onSelection(self, kwargs):
        """ Called when a selector has selected something
        """        
        selection = kwargs["selection"]
        state_parms = kwargs["state_parms"]

        self.log(selection)

        # Must return True to accept the selection
        return False

    def onStartSelection(self, kwargs):
        """ Called when a bound selector has been started
        """
        state_parms = kwargs["state_parms"]

        self.log(state_parms)

    def onStopSelection(self, kwargs):
        """ Called when a bound selector has been terminated
        """
        state_parms = kwargs["state_parms"]

        self.log(state_parms)

    def onDragTest( self, kwargs ):
        """ Implement this callback to handle drag and drop. 
        """
        
        # DnD text file demo
        if not hou.ui.hasDragSourceData("text/plain"):
            self.scene_viewer.setPromptMessage( "Invalid drag drop source", 
                hou.promptMessageType.Error )
            return False

        su.log(su.dragSourceFilepath())
            
        return True

    def onDropGetOptions( self, kwargs ):
        """ Implement this callback to build a list of drop options. 
        """
        
        kwargs["drop_options"]["ids"] = ("option1", "option2", "option3")
        kwargs["drop_options"]["labels"] = ("Option 1", "Option 2", "Option 3")

    def onDropAccept( self, kwargs ):
        """ Implement this callback to process the event from the 
        selected menu item. 
        """
        
        su.log( kwargs["drop_selection"] )

        return True

    def onGenerate(self, kwargs):
        """ Called when a nodeless state starts
        """
        state_parms = kwargs["state_parms"]


def createViewerStateTemplate():
    """ Mandatory entry point to create and return the viewer state 
        template to register. """

    state_typename = "ppm::sampleScripts"
    state_label = "1 Sample Scripts"
    state_cat = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_typename, state_label, state_cat)
    template.bindFactory(State)
    template.bindIcon("MISC_python")




    return template
