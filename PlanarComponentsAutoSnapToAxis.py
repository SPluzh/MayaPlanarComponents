# -----------------------------------------------------------------------------------
# Planarizes selected components to their best-fit plane.
# Version: 1.2
# 
# Changes in v1.2:
# - Only moves vertices that are OFF the plane (selective displacement)
# - Detects vertices already on plane and uses them to define it (preserves majority)
# - Shows in-viewport notification with moved vertex count and plane orientation
# - Distance threshold (1e-3) determines which vertices need alignment
# - Fixed selectType flag error when object is selected
#
# Changes in v1.1:
# - Added snap_normal_to_axis: snaps plane normal to X/Y/Z if within 0.1° threshold
# - Preserves original selection mode (vertex/edge/face/object) after operation
# - Added error handling for selection type detection
# - Improved performance: Vtx3DtoNpArray uses list comprehension instead of np.append
# -----------------------------------------------------------------------------------



import maya.cmds as cmds
import maya.mel as mel
import numpy as np

# -----------------------------------------------------------------------------------
# Linear algebra utilities
# -----------------------------------------------------------------------------------

def Vtx3DtoNpArray(S):
    """Returns vertex coordinates as a numpy array of shape [n, 3]"""
    return np.array([cmds.xform(vtx, q=True, ws=True, t=True) for vtx in S])

def normalized(v):
    """Returns the normalized version of a vector"""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def fitPlaneEigen(M):
    """Returns the normal of the best-fit plane for a set of points"""
    cov = np.cov(M.T)
    eigvals, eigvecs = np.linalg.eig(cov)
    idx = np.argmin(eigvals)
    return eigvecs[:, idx]

def average(M):
    """Returns the average point (centroid) of a set of points"""
    return np.mean(M, axis=0)

def snap_normal_to_axis(normal, threshold_deg=0.1):
    """
    If the normal is within threshold_deg of a world axis (X/Y/Z),
    snaps it to that axis.
    """
    threshold_rad = np.deg2rad(threshold_deg)
    world_axes = [
        np.array([1.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0]),
        np.array([0.0, 0.0, 1.0])
    ]
    
    n = normalized(normal)
    for axis in world_axes:
        dot = np.dot(n, axis)
        angle = np.arccos(np.clip(abs(dot), -1.0, 1.0))
        if angle < threshold_rad:
            return axis * np.sign(dot)
    return n

# -----------------------------------------------------------------------------------
# Main Function: Align vertices to a best-fit plane
# -----------------------------------------------------------------------------------

def alignVtxToPlane():
    selCom = cmds.ls(sl=True, fl=True)
    if not selCom:
        cmds.error("Nothing selected.")
        return

    # Detect original selection type
    sel_mode = {
        "vertex": bool(cmds.filterExpand(selCom, sm=31)),
        "edge": bool(cmds.filterExpand(selCom, sm=32)),
        "face": bool(cmds.filterExpand(selCom, sm=34)),
        "object": all("." not in s and "Shape" not in s for s in selCom)
    }

    mesh = selCom[0].split('.')[0]

    # Convert to vertices
    cmds.select(selCom)
    try:
        cmds.ConvertSelectionToVertices()
    except:
        cmds.error("Failed to convert selection to vertices.")
        return

    selVtx = cmds.ls(sl=True, fl=True)
    if len(selVtx) < 3:
        cmds.error("Select at least 3 vertices, 2 edges, or 1 face.")
        return

    # Compute initial best-fit plane
    vtxCoor = Vtx3DtoNpArray(selVtx)
    avg = average(vtxCoor)
    normal = fitPlaneEigen(vtxCoor)
    normal = snap_normal_to_axis(normal)
    
    # Find vertices already on the plane
    distance_threshold = 1e-3
    distances = [abs(np.dot(vtxCoor[i] - avg, normal)) for i in range(len(selVtx))]
    on_plane_indices = [i for i, d in enumerate(distances) if d <= distance_threshold]
    
    # If most vertices are already on a plane, use them to define the plane
    if len(on_plane_indices) >= 3:
        plane_points = vtxCoor[on_plane_indices]
        avg = average(plane_points)
        normal = fitPlaneEigen(plane_points)
        normal = snap_normal_to_axis(normal)

    # Move only vertices that are off the plane
    moved_count = 0
    for i in range(len(selVtx)):
        vec = vtxCoor[i] - avg
        distance_to_plane = abs(np.dot(vec, normal))
        
        if distance_to_plane > distance_threshold:
            proj = np.dot(vec, normal) * normal
            new_pos = vtxCoor[i] - proj
            cmds.move(new_pos[0], new_pos[1], new_pos[2], selVtx[i], absolute=True)
            moved_count += 1

    # Restore original selection
    cmds.select(cl=True)
    cmds.select(selCom)

    # Restore original component selection mode
    if sel_mode["vertex"]:
        mel.eval('doMenuComponentSelectionExt("%s", "vertex", 0);' % mesh)
    elif sel_mode["edge"]:
        mel.eval('doMenuComponentSelectionExt("%s", "edge", 0);' % mesh)
    elif sel_mode["face"]:
        mel.eval('doMenuComponentSelectionExt("%s", "facet", 0);' % mesh)
    elif sel_mode["object"]:
        cmds.selectType(allObjects=True)
    
    # Show success notification
    axis_names = {
        (1.0, 0.0, 0.0): "X", (-1.0, 0.0, 0.0): "X",
        (0.0, 1.0, 0.0): "Y", (0.0, -1.0, 0.0): "Y",
        (0.0, 0.0, 1.0): "Z", (0.0, 0.0, -1.0): "Z"
    }
    normal_tuple = tuple(normal)
    axis_info = axis_names.get(normal_tuple, "custom")

    message = '<hl>Aligned {count} vertices</hl> to plane (normal: <hl>{axis}</hl>)'.format(
        count=moved_count,
        axis=axis_info
    )
    cmds.inViewMessage(
        amg=message,
        pos='topCenter',
        fade=True,
        fadeInTime=200,
        fadeStayTime=1500,
        fadeOutTime=500
    )

# Run the function
alignVtxToPlane()