
import math
import numpy as np
from scipy.spatial.transform import Rotation as R

from typing import (
    Dict,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)

from utility.define import VSEP
from utility.udtypes import (
    AngleType,
    AxisType,
    PointType,
    PointListType,
    PointValueType,
    VectorType,
)

VertexT = TypeVar("VertexT", bound = "Vertex")
BlockT = TypeVar("BlockT", bound = "Block")

def hl() -> None:
    """ Prints a horizontal line on screen based on VSEP definition """
    print(VSEP)



def check_coordinate(coordinates) -> None:
    """ Check if a given coordinate input is valid """
    
    if not isinstance(coordinates, Sequence):
        raise TypeError("Incorrect input for a point.")



def center(points: Sequence[VertexT]) -> PointType:
    """
    Calculate the center/midpoint for a given point list

    Args:
        points (Sequence[VertexT]): List/tuple of a PointType

    Returns:
        PointType: Returns the location/coordinates of the center of the given points
    """
    
    xCenter = sum([i.coordinates()[0] for i in points])/len(points)
    yCenter = sum([i.coordinates()[1] for i in points])/len(points)
    zCenter = sum([i.coordinates()[2] for i in points])/len(points)
    
    return (xCenter, yCenter, zCenter)



def deg2rad(angle: AngleType) -> AngleType:
    return (angle * math.pi /180.0)



def rad2deg(angle: AngleType) -> AngleType:
    return (180 *angle / math.pi)



def unit_vector(vector: VectorType) -> VectorType:
    """
    Convert a vector in a unit vector

    Args:
        vector (VectorType): Tuple of PointTypes describing direction

    Returns:
        VectorType: Returns the calculated vector
    """
    
    norm = np.linalg.norm(vector)
    
    if norm == 0:
        return (0.0, 0.0, 0.0)
    
    return vector/norm
    


def points2distance(
        point1: PointType,
        point2: PointType,
    ) -> VectorType:
    """_summary_

    Args:
        point1 (PointType): First of the two given points
        point2 (PointType): The other point

    Returns:
        VectorType: Distance between the two given points
    """
    
    dx = point1[0] - point2[0]
    dy = point1[1] - point2[1]
    dz = point1[2] - point2[2]
    
    return math.sqrt(dx**2 + dy**2 + dz**2)
    


def surface_normal_from_tree_points(
        point1: PointType,
        point2: PointType,
        point3: PointType,
        normalize: Optional[bool] = True
    ) -> VectorType:
    """
    Calculate surface normal from given three points

    Args:
        point1 (PointType): First of the three given points
        point2 (PointType): Second of the given three points
        point3 (PointType): Third of the given three points
        normalize (Optional[bool], optional): To normalize the calculated vector or not. Defaults to True.

    Returns:
        VectorType: Calculated vector of the plane contained the given three points.
    """
    
    ### Convert points to numpy arrays for vector operations
    ### pa --> point array
    pa1 = np.array(point1)
    pa2 = np.array(point2)
    pa3 = np.array(point3)
    
    ### Calculate two vectors that lie in the plane
    ### e.g., vector from p1 to p2 (v1) and vector from p1 to p3 (v2)
    vec1 = pa2 - pa1
    vec2 = pa3 - pa1
    
    ### The cross product of these two vectors gives the normal vector
    normalVector = np.cross(vec1, vec2)
    
    ### Normalize the vector to get a unit normal vector
    if normalize:
        unitNormalVector = unit_vector(normalVector)
        return unitNormalVector
    
    return normalVector
        


def point_rotation_coordinates(
        point: PointType,
        axisPoint: PointType,
        normalVector: VectorType,
        rotationAngle: AngleType
    ) -> PointType:
    """
    Get point coordinate after rotation in 3D space

    Args:
        point (PointType): Point to be rotated
        axisPoint (PointType): Point on the rotation axis
        normalVector (VectorType): Unit vector along the rotation axis
        rotationAngle (AngleType): Angle of rotation

    Returns:
        PointType: Return the point coordinates after rotation.
    """
    
    point = np.array(point)
    axisPoint = np.array(axisPoint)
    normalVector = np.array(normalVector)
    
    ### Translate the axis point to the origin
    pointRelativeToOrigin = point - axisPoint
    
    ### Define the rotation using the normal vector as the axis
    ### The normal vector should be normalized for correct rotation application
    normalVector = normalVector / np.linalg.norm(normalVector)
    
    ### SciPy's Rotation.from_rotvec takes a vector 
    ### where direction is axis and norm is angle in radians
    angleRadian = np.deg2rad(rotationAngle)
    rotationVector = normalVector * angleRadian
    
    rotation = R.from_rotvec(rotationVector)
    
    ### Apply the rotation
    relativeRotatedPoint = rotation.apply(pointRelativeToOrigin)
    
    ### Translate the point back to its original position
    rotatedPoint = relativeRotatedPoint + axisPoint
    
    return tuple(rotatedPoint)



def get_axis_index(axisName: AxisType) -> int:
    """
    Get multi-block indices axis index

    Args:
        axisName (AxisType): Name of an axis (x, y, z)

    Returns:
        int: 0 for x, 1 for y, and 2 for z
    """
    
    if axisName == "x":
        index = 0
    elif axisName == "y":
        index = 1
    elif axisName == "z":
        index = 2
    return index



def grid_spacing(
        minmax: Dict,
        dx: PointValueType,
        dy: PointValueType,
        dz: PointValueType,
    ) -> Tuple[int]:
    """
    Get block grid spacing from 

    Args:
        minmax (Dict): Min/max of the block along x, y, z direction.
        dx (PointValueType): Delta along x-axis
        dy (PointValueType): Delta along y-axis
        dz (PointValueType): Delta along z-axis

    Returns:
        Tuple[int]: Returns a tuple of grid spacing along x, y, z direction
    """
        
    nx = int((minmax["x-max"] - minmax["x-min"])/float(dx))
    ny = int((minmax["y-max"] - minmax["y-min"])/float(dy))
    nz = int((minmax["z-max"] - minmax["z-min"])/float(dz))
    
    if nx == 0:
        nx = 1
    if ny == 0:
        ny = 1
    if nz == 0:
        nz = 1
    
    return nx, ny, nz



def slice_plane_from_block_pair(
        block1: BlockT,
        block2: BlockT
    ) -> str:
    """
    Compares multi-block index between two blocks.
    Get matching "slice plane" and matching "slice index"

    Args:
        block1 (Block): One of the two blocks to be compared
        block2 (Block): The other block to be compared

    Returns:
        str: slice plane
    """
    
    mbi1 = block1.multiBlockIndex
    mbi2 = block2.multiBlockIndex
    
    comparison = [
        mbi1[0] == mbi2[0],
        mbi1[1] == mbi2[1],
        mbi1[2] == mbi2[2],
    ]
    
    if comparison.index(True) == 0:
        return "yz"
    elif comparison.index(True) == 1:
        return "zx"
    elif comparison.index(True) == 2:
        return "xy"




def get_quadrant_number(
            multiblockIndex1Center,
            multiblockIndex2Center,
            multiblockIndex1Corner,
            multiblockIndex2Corner,
        ) -> int:
        """
        Get the quadrant number (1, 2, 3, 4) based on the definition of the staring and end block selection

        Args:
            multiblockIndex1Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex1Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z

        Returns:
            int: The quadrant number based on the block selection
        """
        
        ### 1 --> 1st quadrant
        ### 2 --> 2nd quadrant
        ### 3 --> 3rd quadrant
        ### 4 --> 4th quadrant
        quadrantNumber = None
        
        if (multiblockIndex1Center < multiblockIndex1Corner and
            multiblockIndex2Center < multiblockIndex2Corner):
            quadrantNumber = 1
        
        elif (multiblockIndex1Center > multiblockIndex1Corner and
            multiblockIndex2Center < multiblockIndex2Corner):
            quadrantNumber = 2
        
        elif (multiblockIndex1Center > multiblockIndex1Corner and
            multiblockIndex2Center > multiblockIndex2Corner):
            quadrantNumber = 3
        
        elif (multiblockIndex1Center < multiblockIndex1Corner and
            multiblockIndex2Center > multiblockIndex2Corner):
            quadrantNumber = 4
        
        return quadrantNumber

