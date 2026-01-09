from collections import OrderedDict
from typing import (
    List, 
    Dict,
)


class Edge:
    """ Attributes and methods associated with an edge """
    
    def __init__(
            self,
            id: int,
            direction: str,
            position: str,
            start: int,
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
        self._id = value
    
    ### Edge -> direction
    @property
    def direction(self) -> str:
        return self._direction
    
    @direction.setter
    def direction(self, value: str):
        if value.lower() not in ["x", "y", "z"]:
            raise ValueError("Edge direction must be 'x' or 'y' or 'z'")
        else:
            self._direction = value
    
    ### Edge -> position
    @property
    def position(self) -> str:
        return self._position
    
    @position.setter
    def position(self, value: str):
        if value.lower() not in ["x", "y", "z"]:
            raise ValueError("Edge direction must be 'x' or 'y' or 'z'")
        else:
            self._position = value
    
    ### Edge -> start
    @property
    def start(self) -> int:
        return self._start
    
    @start.setter
    def start(self, value: int):
        self._start = value
    
    ### Edge -> end
    @property
    def end(self) -> int:
        return self._end
    
    @end.setter
    def end(self, value: int):
        self._end = value
    
    def arc(
            self,
            midPoint: tuple
        ) -> str:
        """ Creates definition of an arc """
        
        arcDef = f"arc {self._start} {self._end} ({midPoint[0]} {midPoint[1]} {midPoint[2]})"
        
        return arcDef
    
    def spline(
            self,
            points: tuple[tuple]
        ) -> str:
        """ Create definition for a spline through given points """
        
        wspace = " "
        indent = 4 * wspace
        
        splineDef = indent*1 + f"({self._start} {self._end} spline\n"
        splineDef += indent*1 + "(\n"
        for _p in points:
            splineDef += indent*2 + f"({_p[0]} {_p[1]} {_p[2]})\n"
        splineDef += indent*1 + ")\n"
        
        return splineDef