

from utility.exception import MoveDefinitionError
from typing import (
    Dict,
    Optional,
    Sequence,
    Union,
    TypeVar,
)
from utility.udtypes import (
    PointType,
    PointValueType,
    VectorType,
)

VertexT = TypeVar("VertexT", bound = "Vertex")

class VertexAction:
    """ A class containing the Vertex operations/actions """
    
    def move (
            self,
            vertex: VertexT,
            location: Optional[PointType] = None,
            delta: Optional[VectorType] = None,
    ) -> VertexT:
        """
        Move a given point to new coordinate or to a given distance

        Args:
            vertex (VertexT): Instance of the 'Vertex' class which needs to be moved
            location (Optional[PointType], optional): Location to which the given Vertex to be moved. Defaults to None.
            delta (Optional[VectorType], optional): Distance to which the given Vertex to be moved. Defaults to None.

        Raises:
            MoveDefinitionError: Raises error if either a new location nor a move distance is defined
            MoveDefinitionError: Raises error if both a new location and a move distance is defined

        Returns:
            VertexT: Returns the Vertex which has been moved
        """
        
        if location == None and delta == None:    
            raise MoveDefinitionError("No location or distance is provided for move operation.")
        else:
            if location != None and delta != None:
                raise MoveDefinitionError("Only define a new location or a distance for a vertex move, not both.")
            else:
                if delta == None:
                    vertex.x = location[0]
                    vertex.y = location[1]
                    vertex.z = location[2]
                elif location == None:
                    vertex.x += delta[0]
                    vertex.y += delta[1]
                    vertex.z += delta[2]
        return vertex
    
    def collapse (
            self,
            selection: VertexT,
            target : VertexT
        ) -> VertexT:
        """
        Collapse a given vertex on to another vertex

        Args:
            selection (VertexT): Instance of the 'Vertex' class which needs to be collapsed
            target (VertexT): Instance of the 'Vertex' class at which another vertex will collapse

        Returns:
            VertexT: Returns the Vertex which has been collapsed/collapsed to
        """
        
        selection.x = target.x
        selection.y = target.y
        selection.z = target.z
    
        return selection
    
    def move_collapse(
            self,
            selection: VertexT,
            target : VertexT,
            location: Optional[PointType] = None,
            delta: Optional[VectorType] = None,
        ) -> VertexT:
        """
        Collapse and move a given point

        Args:
            selection (VertexT): Instance of the 'Vertex' class which needs to be collapsed
            target (VertexT): Instance of the 'Vertex' class at which another vertex will collapse and moved
            location (Optional[PointType], optional): Location to which the given Vertex to be moved. Defaults to None.
            delta (Optional[VectorType], optional): Distance to which the given Vertex to be moved. Defaults to None.

        Returns:
            VertexT: Returns the Vertex which has been moved and collapsed/collapsed to
        """
        
        self.move(
                target,
                location,
                delta
            )
        
        self.collapse(
                selection,
                target
            )
        
        return selection
    
    def scale(
            self,
            selection: VertexT,
            ratio: PointValueType,
            reference: PointType
        ) -> VertexT:
        """
        Scale a given Vertex i.e. move thw given point to a new location w.r.t a reference point

        Args:
            selection (VertexT): Instance of the 'Vertex' class which needs to be scaled
            ratio (PointValueType): Ratio of the scaling operation
            reference (PointType): A point/coordinate w.r.t which the given Vertex to be scaled

        Returns:
            VertexT: Returns the Vertex which has been scaled
        """
        
        delta = None
        
        location = (
            reference[0] + ratio * (selection.x - reference[0]),
            reference[1] + ratio * (selection.y - reference[1]),
            reference[2] + ratio * (selection.z - reference[2])
        )
        self.move(
                selection,
                location,
                delta
            )