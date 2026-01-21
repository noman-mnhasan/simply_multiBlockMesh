"""
udTypes --> User Defined Types
"""

from typing import (
    Any,
    List,
    Literal,
    Sequence,
    Tuple,
    Union,
)


PointValueType = Union[int, float]
CoordinateValueType = PointValueType
AngleType = PointValueType
AxisType = Literal["x", "y", "z"]

PointType = Tuple[PointValueType, 3]
PointListType = Tuple[PointType]

DistanceType = Union[PointType, None]

EdgeType = Literal["arc", "spline", "polyline"]

FaceType = Literal["right", "left", "front", "back", "top", "bottom"]

SliceType = Literal["xy", "yz", "zx"]

VectorType = PointType



