from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from .block import *

class Slice:
    """ Attributes and methods associated with a slice """
    
    def __init__(
            self,
            plane: str,
            index: int,
            blocks: tuple
        ) -> None:
        """
        Initialize slice instance
        
        Args: 
            plane: The plane along which the slice is made -> XY, YZ, ZX
            index: Index of the slice 
            blocks: A tuple containing the block which are contained in the slice 
        """
        
        self._plane = plane
        self._index = index
        self._blocks = blocks
    
    def __repr__(self):
        return f"\nPlane-{self.plane}-Slice-{self.index}"
    
    ### Slice -> plane
    @property
    def plane(self) -> str:
        return self._plane
    
    @plane.setter
    def plane(self, value: str) -> None:
        self._plane = value
    
    ### Slice -> index
    @property
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, value: int) -> None:
        self._index = value
    
    ### Slice -> blocks
    @property
    def blocks(self) -> tuple:
        return self._blocks
    
    @blocks.setter
    def blocks(self, value: tuple) -> None:
        self._blocks = value
        