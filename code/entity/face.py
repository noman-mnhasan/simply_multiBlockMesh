from collections import OrderedDict
from typing import (
    List, 
    Dict,
    Tuple,
    TypeVar
)

from entity.edge import Edge
from entity.vertex import Vertex
from utility.define import blockFaceName
from utility.udtypes import PointValueType
from utility import tool as t
from operation.action.aface import FaceAction

FaceT = TypeVar("FaceT", bound = "Face")

class Face:
    """ Attributes and methods associated with a face """
    
    def __init__(
            self,
            block: int,
            name: str,
            vertices: Tuple[Vertex]
        ) -> None:
        """
        Initialize Face instance
        
        Args:
            block (int): The associated index of the block instance
            name (str): Name of the face --> front, back, left, right, bottom, top
            vertices (tuple): Tuple of vertices used to define the face (needs 4 vertices to define each face)
        """
        
        self._block = block
        self._name = name
        self._vertices = vertices
        self._edges = None
        self._action = FaceAction(self)
    
    def __repr__(self) -> str:
        return f"\nBlock-{self.block}-Face-{self.name}"
    
    ### Face - block
    @property
    def block(self) -> int:
        return self._block
    
    @block.setter
    def block(self, value: int) -> None:
        """ Check, raise error and assign value of Face.block  """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Face.block' must be an integer.")
        
        self._block = value
    
    ### Face - name
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        """ Check, raise error and assign value of Face.name """
        
        if value not in blockFaceName:
            raise ValueError("Value of Face.name can only be --> front, back, left, right, bottom, top")
        
        self._name = value
    
    ### Face - vertices
    @property
    def vertices(self) -> Tuple[Vertex]:
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: Tuple[Vertex]) -> None:
        """ Check, raise error and assign value of Face.vertices """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Face.vertices' must be an tuple.")

            if not all([isinstance(x, Vertex) for x in value]):
                raise ValueError("Elements of 'Face.vertices' must either be an integers or a float.")
        
        self._vertices = value
    
    ### Face - edges
    @property
    def edges(self) -> Tuple[Edge]:
        return self._edges
    
    @edges.setter
    def edges(self, value: Tuple[Edge]) -> None:
        """ Check, raise error and assign value of Face.edges """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Face.edges' must be an tuple.")

            if not all([isinstance(x, Edge) for x in value]):
                raise ValueError("Elements of 'Face.vertices' must be instance of teh class Edge.")
        
        self._edges = value
    
    def move(
            self,
            delta: List
        ) -> None:
        """
        Move a given face

        Args:
            delta (List): List of delta values along x, y, z direction
        """

        
        t.check_coordinate(delta)
        location = None
        
        for ivertex in self.vertices:
            ivertex.move(location,delta)
        
        return self
    
    def scale(
            self,
            ratio: PointValueType
        ) -> None:
        """
        Scale a given face at the plane that contains the face

        Args:
            ratio (PointValueType): Ratio of the scaling operation
        """
        
        self._action.scale(ratio)
        
        return self