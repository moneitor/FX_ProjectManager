from __future__ import print_function

import hou

import stateutils


class DrawPoints(object):    
    def __init__(self, state_name, scene_viewer):
        self.state_name = state_name
        self.scene_viewer = scene_viewer

        self._node = None
        self._pressed = False
        self._index = 0    

    def _point_count(self):
        multiparm = self._node.parm("points")
        # This is how you get the number of instances in a multiparm
        return multiparm.evalAsInt()

    def _insert_point(self):
        index = self._point_count()
        multiparm = self._node.parm("points")
        multiparm.insertMultiParmInstance(index)
        return index

    def _set(self, index, position):
        self._node.parm("usept%d" % index).set(1)
        self._node.parmTuple("pt%d" % index).set(position)

    def _start(self):
        if not self._pressed:
            self.scene_viewer.beginStateUndo("Add point")
            self._index = self._insert_point()
        self._pressed = True

    def _finish(self):
        if self._pressed:
            self.scene_viewer.endStateUndo()
        self._pressed = False

    def onMouseEvent(self, kwargs):
        node = self._node = kwargs["node"]
        ui_event = kwargs["ui_event"]
        device = ui_event.device()
        origin, direction = ui_event.ray()

        # Find intersection with geometry or ground
        intersected = -1
        inputs = node.inputs()
        # Only try intersecting geometry if this node has input
        if inputs and inputs[0]:
            geometry = inputs[0].geometry()
            intersected, position, _, _ = stateutils.sopGeometryIntersection(geometry, origin, direction)
        if intersected < 0:
            position = stateutils.cplaneIntersection(self.scene_viewer, origin, direction)

        # Create/move point if LMB is down
        if device.isLeftButton():
            self._start()
            self._set(self._index, position)
        else:
            self._finish()

    def onInterrupt(self, kwargs):
        self._finish()


def createViewerStateTemplate():
    # Choose a name and label 
    state_name = "drawpoints.pystate"
    state_label = "Draw Points"
    category = hou.sopNodeTypeCategory()

    template = hou.ViewerStateTemplate(state_name, state_label, category)
    template.bindFactory(DrawPoints)


    return template