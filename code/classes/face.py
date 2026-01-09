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
            block: The associated index of the block instance
            name: Name of the face --> front, back, left, right, bottom, top
            vertices: Vertices used to define the face (needs 4 vertices to define each face)
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
        self._block = value
    
    ### Face - name
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        if value not in ["front", "back", "left", "right", "bottom", "top"]:
            raise ValueError("Face name can only be --> front, back, left, right, bottom, top")
        else:
            self._name = value
    
    ### Face - vertices
    @property
    def vertices(self) -> str:
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: str) -> None:
        self._vertices = value