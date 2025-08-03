# -----------------------------------------------------------------------------------
# Planarizes selected components to their best-fit plane,
# preserving most vertex positions. If the plane is nearly aligned
# with a world axis, it snaps to the closest world axis (X, Y, or Z).
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
        "edge":   bool(cmds.filterExpand(selCom, sm=32)),
        "face":   bool(cmds.filterExpand(selCom, sm=34)),
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

    # Compute best-fit plane and average point
    vtxCoor = Vtx3DtoNpArray(selVtx)
    avg = average(vtxCoor)
    normal = fitPlaneEigen(vtxCoor)
    normal = snap_normal_to_axis(normal)

    # Project all vertices onto the plane
    for i in range(len(selVtx)):
        vec = vtxCoor[i] - avg
        proj = np.dot(vec, normal) * normal
        new_pos = vtxCoor[i] - proj
        cmds.move(new_pos[0], new_pos[1], new_pos[2], selVtx[i], absolute=True)

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
        cmds.selectType(o=True)

# Run the function
alignVtxToPlane()
