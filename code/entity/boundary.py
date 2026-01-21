from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from entity.face import Face
from utility.define import indent

class Boundary:
    """  Attributes and methods associated with a boundary/patch """
    
    def __init__(
            self,
            name: str,
            bcType: str,
            faces: tuple[Face]
        ):
        """
        Initialize boundary instance
        
        Args:
            name: Name of the boundary
            bcType: Type of the boundary condition
            faces: Face(s) where the patch/boundary condition will be applied
        """
        
        self._name = name,
        self._bcType = bcType,
        self._faces = faces
        
    ### Boundary - name
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str):
        """ Check, raise error and assign value of Boundary.name """
        
        if not isinstance(value, str):
            raise ValueError("Value of 'Boundary.name' must be an string.")
        
        self._name = value
        
    ### Boundary - bcType
    @property
    def bcType(self) -> str:
        return self._bcType
    
    @bcType.setter
    def bcType(self, value: str):
        """ Check, raise error and assign value of Boundary.bcType """
        
        if not isinstance(value, str):
            raise ValueError("Value of 'Boundary.bcType' must be an string.")
        
        self._nbcType = value
        
    ### Boundary - faces
    @property
    def faces(self) -> tuple[Face]:
        return self._faces
    
    @faces.setter
    def faces(self, value: tuple[Face]):
        """ Check, raise error and assign value of Boundary.faces """
        
        if not isinstance(value, tuple) and not all([isinstance(x, tuple) for x in values]):
            raise ValueError("Value of 'boundary.faces' must be a tuple of tuples.")
        
            if not all([[isinstance(f, Face) for f in x] for x in value]):
                raise ValueError("Elements of 'Boundary.faces' must be instances of 'Face' class.")
        
        self._faces = value
    
    def definition(self) -> str:
        """ Get definition of a boundary """
        
        boundaryDef = indent *1 + f"{self._name}\n"
        boundaryDef += indent *1 + "{\n"
        boundaryDef += indent *2 + f"type    {self._bcType};\n"
        boundaryDef += indent *2 + "faces;\n"
        boundaryDef += indent *2 + "(\n"
        for f in self._faces:
            boundaryDef += indent *3 + f"({f[0]} {f[1]} {f[2]} {f[3]})"
        boundaryDef += indent *2 + ");\n"
        boundaryDef += indent *1 + "}\n"
        
        return boundaryDef