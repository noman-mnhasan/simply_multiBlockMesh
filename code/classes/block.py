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

from .edge import *


class Block:
    """ Attributes and methods associated with a block """
    
    def __init__(
            self,
            id: int,
            index: str,
            vertices: tuple,
            vertexCoordinates: Dict,
            faces: Dict,
            spacing: Dict,
            grading: Dict
        ) -> None:
        """
        Initialize block instance
        
        Args:
            index: The associated index of the block instance
            vertices: Vertices used to define the block (needs 8 vertices to define each block)
            spacing: Grid spacing along x, y, z directions
            grading: Cell expansion ratio
        """
        
        self._id = id
        self._index = index
        self._vertices = vertices
        self._vertexCoordinates = vertexCoordinates
        self._faces = faces
        self._edges = None
        self._spacing = spacing
        self._grading = grading
        self._dx = self._spacing["x"]
        self._dy = self._spacing["y"]
        self._dz = self._spacing["z"]
    
    def __repr__(self):
        return f"\nBlock : {self.id}\nIndex : {self.index}\n"
    
    ### Block -> id
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        self._id = value
    
    ### Block -> index
    @property
    def index(self) -> str:
        return self._index
    
    @index.setter
    def index(self, value: str):
        self._index = value
    
    ### Block -> vertices
    @property
    def vertices(self) -> tuple:
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: tuple):
        self._vertices = value
    
    ### Block -> vertex coordinates
    @property
    def vertexCoordinates(self) -> Dict:
        return self._vertexCoordinates
    
    @vertexCoordinates.setter
    def vertexCoordinates(self, value: Dict):
        self._vertexCoordinates = value
    
    ### Block -> faces
    @property
    def faces(self) -> Dict:
        return self._faces
    
    @faces.setter
    def faces(self, value: Dict):
        self._faces = value
    
    ### Block -> edges
    @property
    def edges(self) -> Dict:
        return self._edges
    
    @edges.setter
    def edges(self, value: Dict):
        self._edges = value
    
    ### Block -> spacing
    @property
    def spacing(self) -> Dict:
        return self._spacing
    
    @spacing.setter
    def spacing(self, value: Dict):
        self._spacing = value
                
        self._dx = self._spacing["x"]
        self._dy = self._spacing["y"]
        self._dz = self._spacing["z"]
    
    ### Block -> grading
    @property
    def grading(self) -> Dict:
        return self._grading
    
    @grading.setter
    def grading(self, value: Dict):
        self._grading = value
    
    def get_edges(self) -> None:
        """
        Define edges from the block definition.
        The vertices are ordered from a lower coordinate
        value to a higher coordinate value. 
        
        Example: On the back face, along x, 
        edges are --> v-0 v-1 and v-3 v-2 (not v-2 v-3)
        
        Convention:
            0  --> back  - bottom - x
            1  --> back  - top    - x
            2  --> front - bottom - x
            3  --> front - top    - x
            4  --> back  - left   - y
            5  --> back  - right  - y
            6  --> front - left   - y
            7  --> front - right  - y
            8  --> left  - bottom - z
            9  --> left  - top    - z
            10 --> right - bottom - z
            11 --> right - top    - z
        """
        
        self._edges = (
                Edge(0, "x", "back-bottom", self.vertices[0], self.vertices[1]),
                Edge(1, "x", "back-top", self.vertices[3], self.vertices[2]),
                Edge(2, "x", "front-bottom", self.vertices[4], self.vertices[5]),
                Edge(3, "x", "front-top", self.vertices[7], self.vertices[6]),
                Edge(4, "y", "back-left", self.vertices[0], self.vertices[3]),
                Edge(5, "y", "back-right", self.vertices[1], self.vertices[2]),
                Edge(6, "y", "front-left", self.vertices[4], self.vertices[7]),
                Edge(7, "y", "front-right", self.vertices[5], self.vertices[6]),
                Edge(8, "z", "left-bottom", self.vertices[0], self.vertices[4]),
                Edge(9, "z", "left-top", self.vertices[3], self.vertices[7]),
                Edge(10, "z", "right-bottom", self.vertices[1], self.vertices[5]),
                Edge(11, "z", "right-top", self.vertices[2], self.vertices[6]),
            )
    
    def _get_hex(self) -> str:
        """ Define the block hex. """
        
        hexDef = "hex ("
        
        hexDef += f"{self.vertices['back']['bottom']['left']}" + wspace
        hexDef += f"{self.vertices['back']['bottom']['right']}" + wspace
        hexDef += f"{self.vertices['back']['top']['right']}" + wspace
        hexDef += f"{self.vertices['back']['top']['left']}" + wspace
        
        hexDef += f"{self.vertices['front']['bottom']['left']}" + wspace
        hexDef += f"{self.vertices['front']['bottom']['right']}" + wspace
        hexDef += f"{self.vertices['front']['top']['right']}" + wspace
        hexDef += f"{self.vertices['front']['top']['left']}"
        hexDef += ")"
        
        return hexDef
    
    
    def _get_spacing(self) -> str:
        """ Define the block grid spacing """
        
        spacingDef = "("
        spacingDef += f"{self.spacing['x']}" + wspace
        spacingDef += f"{self.spacing['y']}" + wspace
        spacingDef += f"{self.spacing['xz']}"
        
        return spacingDef
    
    
    def _get_grading(self):
        """ Define the block edge grading. """
        
        gradingDef = "("
        gradingDef += f"{self.grading['x']}" + wspace
        gradingDef += f"{self.grading['y']}" + wspace
        gradingDef += f"{self.grading['z']}"
        gradingDef += ")"
        
        return gradingDef
    
    
    def definition(self):
        """ Get block definition to write in the dictionary """
        
        blockDef = self._get_hex() + " " + self._get_spacing() + " " + self._get_grading()
        
        return blockDef
    
    
    def get_minmax(self) -> Dict:
        """  
            Calculates min/max along x, y, z direction for a given block
            Returns a dictionary containing the min/max data
        """
        
        xCoord = []
        yCoord = []
        zCoord = []
        
        for loc, coord in self._vertexCoordinates.items():
            xCoord.append(coord[0])
            yCoord.append(coord[1])
            zCoord.append(coord[2])
        
        xMin = min(xCoord)
        xMax = max(xCoord)
        yMin = min(yCoord)
        yMax = max(yCoord)
        zMin = min(zCoord)
        zMax = max(zCoord)
        
        return {
                "x-min" : xMin,
                "x-max" : xMax,
                "y-min" : yMin,
                "y-max" : yMax,
                "z-min" : zMin,
                "z-max" : zMax,
            }
    
    
    def get_spacing(self) -> tuple:
        """
            Calculates the gid spacing along x, y, z direction for a given block.
            Returns a tuple of the spacing along the x, y, z direction
        """
        
        blockMinMax = self.get_minmax()
        
        nx = int((blockMinMax["x-max"] - blockMinMax["x-min"])/float(self._dx))
        ny = int((blockMinMax["y-max"] - blockMinMax["y-min"])/float(self._dy))
        nz = int((blockMinMax["z-max"] - blockMinMax["z-min"])/float(self._dz))
        
        if nx == 0:
            nx = 1
        if ny == 0:
            ny = 1
        if nz == 0:
            nz = 1
        
        return nx, ny, nz
