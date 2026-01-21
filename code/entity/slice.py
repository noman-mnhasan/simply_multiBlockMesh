from collections import OrderedDict
from typing import (
    List, 
    Dict,
    Tuple,
)

from entity.block import Block

class Slice:
    """ Attributes and methods associated with a slice """
    
    def __init__(
            self,
            plane: str,
            index: int,
            blocks: Tuple[Block]
        ) -> None:
        """
        Initialize slice instance
        
        Args: 
            plane (str): The plane along which the slice is made -> XY, YZ, ZX
            index (int): Index of the slice 
            blocks (tuple): A tuple containing the blocks (class: Block) which are contained in the slice 
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
        """ Check, raise error and assign value of Slice.plane """
        
        if not isinstance(value, str):
            raise ValueError("Value of 'Slice.plane' must be a string.")
        
        self._plane = value
    
    ### Slice -> index
    @property
    def index(self) -> int:
        return self._index
    
    @index.setter
    def index(self, value: int) -> None:
        """ Check, raise error and assign value of Slice.index """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Slice.index' must be an integer.")
        
        self._index = value
    
    ### Slice -> blocks
    @property
    def blocks(self) -> Tuple[Block]:
        return self._blocks
    
    @blocks.setter
    def blocks(self, value: Tuple[Block]) -> None:
        """ Check, raise error and assign value of Slice.blocks """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Slice.blocks' must be a tuple.")
            
            if not all([isinstance(x, Block) for x in value]):
                raise ValueError("Elements of 'Slice.blocks' must be integers.")
        
        self._blocks = value