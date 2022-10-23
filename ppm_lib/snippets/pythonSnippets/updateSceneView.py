import hou

def update_scene_view():
    panes = hou.ui.panes()
    scene_viewer = None
    scene_viewer_pane = None
    
    for pane in panes:
        for tab in pane.tabs():            
            if tab.type() == hou.paneTabType.SceneViewer:
                scene_viewer = tab
                scene_viewer_pane = pane
    
    
    if scene_viewer:
        scene_viewer.close()
    else:
        hou.ui.displayMessage("No Scene View present")
        
    if scene_viewer_pane:
        scene_viewer_pane.createTab(hou.paneTabType.SceneViewer)    
    

    
update_scene_view()