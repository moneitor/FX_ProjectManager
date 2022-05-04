import viewerstate.utils as su

node = hou.pwd()
geo = node.geometry()
geo.addAttrib(hou.attribType.Point, "N", hou.Vector3())
geo.addAttrib(hou.attribType.Global, "info", "")

scene_view = hou.ui.curDesktop().paneTabOfType(hou.paneTabType.SceneViewer)
viewport = scene_viewer.viewports()[-1]
if(viewport.isActive3D()):    
    lookup = [node.parm("x").eval(), node.parm("y").eval()]
    lookup[0] *= viewport.size()[2]
    lookup[1] *= viewport.size()[3]    
    
    collisionNode = viewport.queryNodeAtPixel( int(lookup[0]), int(lookup[1]))   
    objs = hou.objNodeTypeCategory()    
    if(collisionNode.type().category() == objs):
        collision = collisionNode.displayNode().geometry()
    else:
        collision = collisionNode.geometry()
        
    ray = viewport.mapToWorld(int(lookup[0]), int(lookup[1]))
    geo_intersector = su.GeometryIntersector(collision, scene_view)
    geo_intersector.intersect(ray[1], ray[0])
    print(geo_intersector.intersected)
    
    if (geo_intersector.intersected):        
        pt = geo.createPoint()
        pt.setPosition(geo_intersector.position)
        pt.setAttribValue("N", geo_intersector.normal)
        geo.setGlobalAttribValue("info", "Hit " + str(collision.sopNode().path()) + "\nP:" + str(geo_intersector.position) + "\nN:" + str(geo_intersector.normal))
    
