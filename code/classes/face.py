from collections import OrderedDict
from typing import (
    List, 
    Dict,
)


class Face:
    """ Attributes and methods associated with a face """
    
    def __init__(
            self,
            block: int,
            name: str,
            vertices: tuple
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
        
        if value not in ["front", "back", "left", "right", "bottom", "top"]:
            raise ValueError("Value of Face.name can only be --> front, back, left, right, bottom, top")
        
        self._name = value
    
    ### Face - vertices
    @property
    def vertices(self) -> tuple:
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: tuple) -> None:
        """ Check, raise error and assign value of Face.vertices """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Face.vertices' must be an integer.")

            if not all([isinstance(x, int) for x in value]):
                raise ValueError("Elements of 'Face.vertices' must be integers.")
        
        self._vertices = value