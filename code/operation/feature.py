

from typing import (
    Union
)

from utility.exception import *




### Point is equivalent ot coordinates
class Point:
    """ A class to represent coordinate """
    
    __slots__ = ["x", "y", "z"]
    
    def __init__(self, *args: Union[int, float]):
        
        if len(args) != 3:
            raise PointTypeError("PointYpe must have a dimension of 3.")
        else:
            if not all([isinstance(i, (int, float)) for i in args]):
                raise ValueError("Point much contain a sequence of either integer or float values.")
        
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
        
    def __repr__(self):
        return f"({self.x} {self.y} {self.z})"



