

from typing import (
    Dict,
    Optional,
    Sequence,
    Union,
    TypeVar,
)

from utility.udtypes import (
    AngleType,
    DistanceType,
    EdgeType,
    PointType,
    PointListType,
    PointValueType,
)

from operation.feature import Point
from utility.exception import MoveDefinitionError
from utility import tool as t


VertexActionT = TypeVar("VertexActionT", bound = "VertexAction")
VertexT = TypeVar("VertexT", bound = "Vertex")
EdgeT = TypeVar("EdgeT", bound = "Edge")
FaceT = TypeVar("FaceT", bound = "Face")
BlockT = TypeVar("BlockT", bound = "Block")
 
 
                
            
 

