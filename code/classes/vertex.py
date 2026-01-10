from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from lib import (
    wspace,
    indent,
    VSEP,
    hl
)


class Vertex:
    """ Attributes and methods associated with a vertex """
    
    def __init__(
            self,
            id: int,
            x: float,
            y: float,
            z: float
        ) -> None:
        """
        Initialize boundary instances

        Args:
            id (int): Id of the vertex
            x (float): X-coordinate of the vertex
            y (float): Y-coordinate of the vertex
            z (float): Z-coordinate of the vertex
        """
        
        self._id = id
        self._x = x
        self._y = y
        self._z = z
        
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
    def x(self, value: float) -> None:
        """ Check, raise error and assign value of Vertex.x """
        
        if not isinstance(value, float):
            raise ValueError("Value of 'Vertex.x' must be a float.")
        
        self._x = value
    
    ### Vertex -> y
    @property
    def y(self) -> float:
        return self._y
    
    @y.setter
    def y(self, value: float) -> None:
        """ Check, raise error and assign value of Vertex.y """
        
        if not isinstance(value, float):
            raise ValueError("Value of 'Vertex.y' must be a float.")
        
        self._y = value
            
    
    ### Vertex -> z
    @property
    def z(self) -> float:
        return self._z
    
    @z.setter
    def z(self, value: float) -> None:
        """ Check, raise error and assign value of Vertex.z """
        
        if not isinstance(value, float):
            raise ValueError("Value of 'Vertex.z' must be a float.")
        
        self._z = value
    
    def coordinates(self) -> tuple:
        """ Returns a tuple of the vertex coordinate as (x, y, z) """
        
        return (self.x, self.y, self.z)
    
    def move(
            self,
            newLocation: List
        ) -> None:
        """
        Move the vertex to a given location

        Args:
            newLocation (List): Coordinates of the new location
        """
        
        if not all([isinstance(i, (int, float)) for i in newLocation]):
            raise ValueError ("Coordinates of the new location must be either an integer of a float.")
        
        self.x = newLocation[0]
        self.y = newLocation[1]
        self.z = newLocation[2]
    
    def collapse(
            self,
            collapseTo: "Vertex"
        ) -> None:
        """
        Collapse the vertex on to another vertex

        Args:
            collapseTo (Vertex): Target vertex to collapse to.
        """
        
        self.x = collapseTo.x
        self.y = collapseTo.y
        self.z = collapseTo.z