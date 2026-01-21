from collections import OrderedDict
from typing import (
    Dict,
    List, 
    Optional,
    TypeVar,
    Union,
)

from operation.feature import Point
from operation.action.avertex import VertexAction

from utility.udtypes import (
    PointValueType,
    CoordinateValueType,
    DistanceType,
    PointType,
)


VertexT = TypeVar("VertexT", bound = "Vertex")

class Vertex(Point):
    """ Attributes and methods associated with a vertex """
    
    def __init__(
            self,
            id: int,
            x: CoordinateValueType,
            y: CoordinateValueType,
            z: CoordinateValueType,
        ) -> None:
        """
        Initialize boundary instances

        Args:
            id (int): Id of the vertex
            x (float): X-coordinate of the vertex
            y (float): Y-coordinate of the vertex
            z (float): Z-coordinate of the vertex
        """
        
        super().__init__(x, y, z)
        self._id = id
        self._action = VertexAction()
        
        
    def __repr__(self):
        return f"v{self.id} ({self.x} {self.y} {self.z})"
    
    ### Vertex -> id
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: id) -> None:
        """ Check, raise error and assign value of Vertex.id """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Vertex.id' must be an integer.")
        
        self._id = value
    
    ### Vertex -> x
    @property
    def x(self) -> float:
        return self._x
    
    @x.setter
    def x(self, value: CoordinateValueType) -> None:
        """ Check, raise error and assign value of Vertex.x """
        
        if not isinstance(value, CoordinateValueType):
            raise ValueError("Value of 'Vertex.x' must be either an integer or a float.")
        
        self._x = value
    
    ### Vertex -> y
    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value: CoordinateValueType) -> None:
        """ Check, raise error and assign value of Vertex.y """
        
        if not isinstance(value, CoordinateValueType):
            raise ValueError("Value of 'Vertex.y' must be either an integer or a float.")
        
        self._y = value
            
    
    ### Vertex -> z
    @property
    def z(self) -> float:
        return self._z
    
    @z.setter
    def z(self, value: CoordinateValueType) -> None:
        """ Check, raise error and assign value of Vertex.z """
        
        if not isinstance(value, CoordinateValueType):
            raise ValueError("Value of 'Vertex.z' must be either an integer or a float.")
        
        self._z = value
    
    def coordinates(self) -> VertexT:
        """ Returns a tuple of the vertex coordinate as (x, y, z) """
        
        return (self.x, self.y, self.z)
    
    def move(
            self,
            location: Optional[PointType] = None,
            delta: Optional[DistanceType] = None,
        ) -> VertexT:
        """
        Move the vertex to a given location

        Args:
            location (list): Coordinates of the new location.
            delta (list): List of delta values along the x, y, z direction.
        """
                
        self._action.move(
                self,
                location,
                delta,
            )
        
    
    def collapse(
            self,
            collapseTo: VertexT
        ) -> None:
        """
        Collapse the vertex on to another vertex

        Args:
            collapseTo (Vertex): Target vertex to collapse to.
        """
        
        self._action.collapse(
                self,
                collapseTo,
            )
               
    
    def move_collapse(
            self,
            collapseTo: VertexT,
            location: VertexT,
            delta: DistanceType,
        ) -> None:
        """
        Collapse the vertex on to another vertex and then move to a new position

        Args:
            location (List): Coordinates of the new location.
            collapseTo (Vertex): Target vertex to collapse to.
            delta (list): List of delta values along the x, y, z direction.
        
        """
        
        self._action.move_collapse(
                self,
                collapseTo,
                location,
                delta
            )
    
    def scale(
            self,
            ratio: PointValueType,
            reference: PointType,
        ) -> None:
        """
        Scale vertex w.r.t. a reference point.
        There's nothing to scale a vertex, scaling a vertex
        w.r.t. a reference eventually scales the higher level
        entities, such as, edge, face, block.

        Args:
            ratio (PointValueType): Ratio of the scaling operation
            reference (PointType): Coordinate of the reference point w.r.t which the scaling operation will be performed
        """
        
        self._action.scale(
                self,
                ratio,
                reference,
            )
        
        
