from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from lib import (
    wspace,
    indent,
    VSEP,
    is_vertex_coordinate_valid
)

from .vertex import *


class Edge:
    """ Attributes and methods associated with an edge """
    
    def __init__(
            self,
            id: int,
            direction: str,
            position: Vertex,
            start: Vertex,
            end: int
        ) -> None:
        """
        Initialize edge instance
        
        Args: 
            id: Id of an edge, between 0-11
            direction: Direction at which the edge is aligned.
            position: Position of the edge in a block
            start: Vertex id defining the start of the edge
            end: Vertex id defining the end of the edge
        """
        
        self._id = id
        self._direction = direction
        self._position = position
        self._start = start
        self._end = end
    
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
            raise ValueError("Value of 'Edge.id' must be a string.")
        
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
        
        edgePosition = [
                "back-bottom",
                "back-top",
                "front-bottom",
                "front-top",
                "back-left",
                "back-right",
                "front-left",
                "front-right",
                "left-bottom",
                "left-top",
                "right-bottom",
                "right-top"
            ]
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
            raise ValueError("Value of 'Edge.start' must be an integer.")
        self._start = value
    
    ### Edge -> end
    @property
    def end(self) -> int:
        return self._end
    
    @end.setter
    def end(self, value: int):
        """ Check, raise error and assign value of Edge.end """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Edge.end' must be an integer.")
        self._end = value
    
    def arc(
            self,
            arcPoint: tuple
        ) -> str:
        """
        Creates definition of an arc

        Args:
            arcPoint (tuple): x, y, z coordinates for the point needed to define the arc

        Returns:
            str: Definition of the edge arc for the blockMeshDict
        """
        
        is_vertex_coordinate_valid(arcPoint)
        arcDef = (indent * 1) + f"arc {self.start.id} {self.end.id} ({arcPoint[0]} {arcPoint[1]} {arcPoint[2]})"
        
        return arcDef
    
    def spline(
            self,
            splinePoints: tuple[tuple]
        ) -> str:
        """
        Create definition for a spline through given points

        Args:
            splinePoints (tuple[tuple]): tuple of x, y, z coordinates for the point needed to define the spline

        Returns:
            str: Definition of the edge spline for the blockMeshDict
        """
        
        for _p in splinePoints:
            is_vertex_coordinate_valid(_p)
        
        splineDef = (indent * 1)+ f"spline {self._start.id} {self._end.id} \n"
        splineDef += (indent * 1) + "(\n"
        for _p in splinePoints:
            splineDef += (indent * 2) + f"({_p[0]} {_p[1]} {_p[2]})\n"
        splineDef += (indent * 1) + ")\n"
        
        return splineDef
    
    def polyline(
            self,
            polylinePoints: tuple[tuple]
        ) -> None:
        """
        Create definition of polyline for given points 

        Args:
            polylinePoints (tuple[tuple]): tuple of x, y, z coordinates for the point needed to define the polyline

        Returns:
            _type_: Definition of the edge polyline for the blockMeshDict
        """
        
        for _p in polylinePoints:
            is_vertex_coordinate_valid(_p)
        
        polylineDef = (indent * 1) + f"polyline {self._start.id} {self._end.id} \n"
        polylineDef += (indent * 1) + "(\n"
        for _p in polylinePoints:
            polylineDef += (indent * 2) + f"({_p[0]} {_p[1]} {_p[2]})\n"
        polylineDef += (indent * 1) + ")\n"
        
        return polylineDef
    
    def polySpline(self) -> None:
        """ Create definition of polySpline for given points """
        
        pass
    
    def bSpline(self) -> None:
        """ Create definition of bSpline for given points """
        
        pass
    
    def move(
            self,
            delta: List
        ) -> None:
        """
        Move a given edge 

        Args:
            delta (List): Delta value along x, y, z, coordinate for the edge to move.
        """
        
        is_vertex_coordinate_valid(delta)
        
        ### Edge-start
        startCoordinate = self.start.coordinates()
        newLocationStart = (
                startCoordinate[0] + delta[0],
                startCoordinate[1] + delta[1],
                startCoordinate[2] + delta[2]
            )
        
        ### Edge-end
        endCoordinate = self.end.coordinates()
        newLocationEnd = (
                endCoordinate[0] + delta[0],
                endCoordinate[1] + delta[1],
                endCoordinate[2] + delta[2]
            )
        
        self.start.move(newLocationStart)
        self.end.move(newLocationEnd)
        