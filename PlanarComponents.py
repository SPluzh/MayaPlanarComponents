import maya.cmds as cmds
import numpy as np

# -----------------------------------------------------------------------------------
# linear algebra operations
# -----------------------------------------------------------------------------------

# returns vertex coordinates as numpy array
def Vtx3DtoNpArray(S):
    A = np.empty((0,3), float)
    for Vtx in S:
        VCoor = cmds.xform(Vtx, q = True, ws = True, t = True, absolute = True)
        A = np.append(A, np.array([VCoor]), axis=0)
    return A

# returns normalized vector a
def normalized(a, axis=-1, order=2):
    l2 = np.atleast_1d(np.linalg.norm(a, order, axis))
    l2[l2==0] = 1
    return a / np.expand_dims(l2, axis)

# returns normal of plane fitted to points M
def fitPlaneEigen(M):
    covariant = np.cov(M.T)
    eigenValues,eigenVectors = np.linalg.eig(covariant)
    # sort by smallest eigenvalues
    idx = eigenValues.argsort()
    eigenValues = eigenValues[idx]
    eigenVectors = eigenVectors[:,idx]
    return eigenVectors[:,0]

# returns average point of points M
def average(M):
    return np.mean(M, axis = 0)

# -----------------------------------------------------------------------------------
# Algin vertex to plane function
# -----------------------------------------------------------------------------------

def alignVtxToPlane():
    selCom = cmds.ls(sl = True, fl = True)
    cmds.ConvertSelectionToVertices()
    selVtx = cmds.ls(sl = True, fl = True)

    if len(selVtx) < 3:
        cmds.error('Please select at least 3 Vertices, 2 Edges or 1 Face')

    vtxCoor = Vtx3DtoNpArray(selVtx)
    planeNorm = fitPlaneEigen(vtxCoor)
    avgPoint = average(vtxCoor)
    rows, cols = vtxCoor.shape

    for i in np.arange(rows):
        vtxCoor[i] -= np.inner((vtxCoor[i] - avgPoint), planeNorm) * planeNorm
        cmds.move(vtxCoor[i, 0], vtxCoor[i, 1], vtxCoor[i, 2], selVtx[i],absolute = True)

    # clear selected vertices
    cmds.select(cl = True)

    # select previous components
    for Com in selCom:
        cmds.select(Com, add = True)
alignVtxToPlane()