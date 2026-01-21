from collections import OrderedDict
from typing import (
    List, 
    Dict,
    TypeVar
)

from operation.action.aedge import EdgeFeature
from utility.define import indent, edgePosition
from utility.udtypes import (
    PointValueType,
    PointType,
    PointListType,
    EdgeType, 
    CoordinateValueType
)
from utility import tool as t

from entity.vertex import Vertex

EdgeT = TypeVar("EdgeT", bound = "Edge")

class Edge:
    """ Attributes and methods associated with an edge """
    
    def __init__(
            self,
            id: int,
            direction: str,
            position: str,
            start: Vertex,
            end: Vertex
            
        ) -> None:
        """
        Initialize edge instance
        
        Args: 
            id (int): Id of an edge, between 0-11
            direction (str): Direction at which the edge is aligned.
            position (str): Position of the edge in a block
            start (Vertex): Vertex id defining the start of the edge
            end (Vertex): Vertex id defining the end of the edge
        """
        
        self._id = id
        self._direction = direction
        self._position = position
        self._start = start
        self._end = end
        self._center: PointType = t.center([start, end])
        self._type: EdgeType = ""
        self._feature: EdgeFeature
        self._editPoints: PointListType
        self._definition: str = ""
        
    
    def __repr__(self):
        return f"{self.direction:3} - {self.position:12} - ({self.start}, {self.end})"
    
    def __eq__(self, value):
        if not isinstance(value, Edge):
            return False
        return self.start == value.start and self.end == value.end
    
    ### Edge -> id
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        """ Check, raise error and assign value of Edge.id """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Edge.id' must be an integer.")
        
        self._id = value
    
    ### Edge -> direction
    @property
    def direction(self) -> str:
        return self._direction
    
    @direction.setter
    def direction(self, value: str):
        """ Check, raise error and assign value of Edge.direction """
        
        if value.lower() not in ["x", "y", "z"]:
            raise ValueError("Value of 'Edge.direction' must be 'x' or 'y' or 'z'")
        
        self._direction = value.lower()
    
    ### Edge -> position
    @property
    def position(self) -> str:
        return self._position
    
    @position.setter
    def position(self, value: str):
        """ Check, raise error and assign value of Edge.position """
        
        print("Edge Position : " + value)
        if value not in edgePosition:
            raise ValueError("Value of Edge.direction must be any of the following:\n    " + "\n    ".join(edgePosition))
        
        self._position = value
    
    ### Edge -> start
    @property
    def start(self) -> Vertex:
        return self._start
    
    @start.setter
    def start(self, value: Vertex):
        """ Check, raise error and assign value of Edge.start """
        
        if not isinstance(value, Vertex):
            raise TypeError("Value of 'Edge.start' must be an instance of 'Vertex' class.")
        self._start = value
    
    ### Edge -> end
    @property
    def end(self) -> int:
        return self._end
    
    @end.setter
    def end(self, value: int):
        """ Check, raise error and assign value of Edge.end """
        
        if not isinstance(value, int):
            raise TypeError("Value of 'Edge.end' must be an instance of 'Vertex' class.")
        self._end = value
    
    ### Edge -> center
    @property
    def center(self) -> Vertex:
        return self._center
    
    @center.setter
    def center(self, value: PointType):
        """ Check, raise error and assign value of Edge.center """
        
        if not isinstance(value, PointType):
            raise TypeError("Value of 'Edge.center' must be a PointType.")
        self._center = value
    
    ### Edge -> type
    @property
    def type(self) -> EdgeType:
        return self._type
    
    @type.setter
    def type(self, value: str):
        """ Check, raise error and assign value of Edge.type """
        
        if not isinstance(value, str):
            raise TypeError("Value of 'Edge.type' must be a string.")
        self._type = value
    
    ### Edge -> editPoints
    @property
    def editPoints(self) -> PointListType:
        return self._editPoints
    
    @editPoints.setter
    def editPoints(self, value: PointListType):
        """ Check, raise error and assign value of Edge.editPoints"""
        
        if not isinstance(value, tuple):
            raise TypeError("Value of 'Edge.editPoints' must be an tuple of PointType.")
        self._editPoints = value
    
    ### Edge -> definition
    @property
    def definition(self) -> str:
        return self._definition
    
    @definition.setter
    def definition(self, value: str):
        """ Check, raise error and assign value of Edge.definition """
        
        self._definition = value
    
    
    def move(
            self,
            delta: List
        ) -> None:
        """
        Move a given edge 

        Args:
            delta (List): Delta value along x, y, z, coordinate for the edge to move.
        """
        
        t.check_coordinate(delta)
        location = None
        
        self.start.move(location,delta)
        self.end.move(location,delta)
        
        return self
    
    def collapse(
            self,
            collapseTo: "Edge"
        ) -> None:
        """
        Collapse the edge on to another edge

        Args:
            collapseTo (edge): Target edge to collapse to.
        """
        
        self.start.collapse(collapseTo.start)
        self.end.collapse(collapseTo.end)
        
        return self
    
    def move_collapse(
            self,
            delta: List,
            collapseTo: "Edge"
        ) -> None:
        """
        Collapse the edge on to another edge and then move to a new position

        Args:
            delta (List): Coordinates of the new location
            collapseTo (Edge): Target edge to collapse to.
        
        """
        
        t.check_coordinate(delta)
        location = None
        
        ### Edge-start
        self.start.move_collapse(
                collapseTo.start,
                location,
                delta
            )
        
        ### Edge-end
        self.end.move_collapse(
                collapseTo.end,
                location,
                delta
            )
        
        return self
    
    def scale(
            self,
            ratio: PointValueType
        ) -> None:
        """
        Scale edge respect to it's center

        Args:
            ratio (PointValueType): Ratio of the scaling operation
        """
        
        ### Edge start
        self.start.scale(
                ratio,
                self.center
            )
        
        ### Edge end
        self.end.scale(
                ratio,
                self.center
            )
        
        return self
    
    def arc(
            self,
            editInfo: Dict
        ) -> None:
        """
        Define an arch for the edge

        Args:
            editInfo (Dict): Dictionary containing the task (making arc) details.
        """
        
        self.type = "arc"
        self._feature = EdgeFeature(self.type, self)
        self._feature.make_arc(editInfo)
        
        return
    
    def spline(
            self,
            editInfo: Dict
        ) -> None:
        """
        Create definition for a spline through given points

        Args:
            editInfo (Dict): Dictionary containing the task (making arc) details.
        """
        
        self.type = "spline"
        self._feature = EdgeFeature(self.type, self)
        self._feature.make_spline(editInfo)
        
        return
    
    # def polyline(
    #         self,
    #         polylinePoints: tuple[tuple]
    #     ) -> None:
    #     """
    #     Create definition of polyline for given points 

    #     Args:
    #         polylinePoints (tuple[tuple]): tuple of x, y, z coordinates for the point needed to define the polyline

    #     Returns:
    #         _type_: Definition of the edge polyline for the blockMeshDict
    #     """
        
    #     for _p in polylinePoints:
    #         t.check_coordinate(_p)
        
    #     polylineDef = (indent * 1) + f"polyline {self._start.id} {self._end.id} \n"
    #     polylineDef += (indent * 1) + "(\n"
    #     for _p in polylinePoints:
    #         polylineDef += (indent * 2) + f"({_p[0]} {_p[1]} {_p[2]})\n"
    #     polylineDef += (indent * 1) + ")\n"
        
    #     return polylineDef
    
    # def polySpline(self) -> None:
    #     """ Create definition of polySpline for given points """
        
    #     pass
    
    # def bSpline(self) -> None:
    #     """ Create definition of bSpline for given points """
        
    #     pass
        