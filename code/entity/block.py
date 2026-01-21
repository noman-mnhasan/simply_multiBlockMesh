
import math
from collections import OrderedDict
from typing import (
    List, 
    Dict,
    Tuple,
)

from utility.define import wspace
from utility import tool as t
from utility.udtypes import (
    PointValueType
)
from operation.action.ablock import BlockAction

from entity.face import Face
from entity.edge import Edge
from entity.vertex import Vertex


class Block:
    """ Attributes and methods associated with a block """
    
    def __init__(
            self,
            id: int,
            index: str,
            isActive: bool,
            vertices: tuple,
            vertexCoordinates: Dict,
            faces: Dict,
            spacing: Dict,
            grading: Dict
        ) -> None:
        """
        Initialize block instance
        
        Args:
            id (int): ID of the block
            index (str): The associated index of the block instance
            isActive (bool): block status. Included/active is True, excluded/inactive is False
            vertices (tuple): Vertices (Type: Vertex class) used to define the block (needs 8 vertices to define each block)
            vertexCoordinates: Coordinates of the vertex defining the block
            faces (dict): Faces (Type: Face class) used to define the block (needs 6 faces to define each block)
            spacing (dict): Grid spacing along x, y, z directions
            grading (dict): Cell expansion ratio
        """
        
        self._id = id
        self._index = index
        self._isActive = isActive
        self._vertices = vertices
        self._vertexCoordinates = vertexCoordinates
        self._faces = faces
        self._edges = None
        self._multiBlockIndex = None
        self._spacing = spacing
        self._grading = grading
        self._dx = self._spacing["x"]
        self._dy = self._spacing["y"]
        self._dz = self._spacing["z"]
        self._action = BlockAction(self)
    
    def __repr__(self):
        return f"\nBlock : {self.id}\nIndex : {self.index}\n"
    
    ### Block -> id
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, value: int):
        """ Check, raise error and assign value of Block.id  """
        
        if not isinstance(value, int):
            raise ValueError("Value of 'Block.id' must be an integer.")
        
        self._id = value
    
    ### Block -> index
    @property
    def index(self) -> str:
        return self._index
    
    @index.setter
    def index(self, value: str):
        """ Check, raise error and assign value of Block.index """
        
        if not isinstance(value, str):
            raise ValueError("Value of 'Block.index' must be a string.")
        
        self._index = value
    
    ### Block -> isActive
    @property
    def isActive(self) -> bool:
        return self._isActive
    
    @isActive.setter
    def isActive(self, value: bool):
        """ Check, raise error and assign value of Block.isActive """
        
        if not isinstance(value, bool):
            raise ValueError("Value of 'Block.isActive' must be a bool.")
        
        self._isActive = value
    
    ### Block -> vertices
    @property
    def vertices(self) -> tuple:
        return self._vertices
    
    @vertices.setter
    def vertices(self, value: Tuple[Vertex]):
        """ Check, raise error and assign value of Block.vertices """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Block.vertices' must be a tuple.")
            
            if not all([isinstance(x, Vertex) for x in value]):
                raise ValueError("Elements of 'Block.vertices' must be instances of 'Vertex' class.")
        
        self._vertices = value
    
    ### Block -> vertex coordinates
    @property
    def vertexCoordinates(self) -> Dict:
        return self._vertexCoordinates
    
    @vertexCoordinates.setter
    def vertexCoordinates(self, value: dict):
        """ Check, raise error and assign value of Block.vertexCoordinates """
        
        if not isinstance(value, Dict):
            raise ValueError("Value of 'Block.vertexCoordinates' must be a dictionary.")
            if not all([isinstance(x, tuple) for x in value.values()]):
                raise ValueError("Elements of 'Block.vertexCoordinates' must be floats.")
        
        self._vertexCoordinates = value
    
    ### Block -> faces
    @property
    def faces(self) -> Dict:
        return self._faces
    
    @faces.setter
    def faces(self, value: Dict):
        """ Check, raise error and assign value of Block.faces """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'Block.faces' must be a dictionary.")
            if not all([isinstance(x, Face) for x in value]):
                raise ValueError("Elements of 'Block.faces' must be instances of 'face' class.")
        
        self._faces = value
    
    ### Block -> edges
    @property
    def edges(self) -> tuple:
        return self._edges
    
    @edges.setter
    def edges(self, value: Tuple[Edge]):
        """ Check, raise error and assign value of Block.edges """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Block.edges' must be a tuple.")
            if not all([isinstance(x, Edge) for x in value]):
                raise ValueError("Elements of 'Block.edges' must be instances of 'edge' class.")
        
        self._edges = value
    
    ### Block -> multiBlockIndex
    @property
    def multiBlockIndex(self):
        return self._multiBlockIndex
    
    @multiBlockIndex.setter
    def multiBlockIndex(self, value: tuple) -> None:
        """ Check, raise error and assign value of Block.multiBlockIndex """
        
        if not isinstance(value, tuple):
            raise ValueError("Value of 'Block.multiBlockIndex' must be a tuple.")
            if not all([isinstance(x, int) for x in value]):
                raise ValueError("Elements of of 'Block.multiBlockIndex' must be integers.")
        
        self._multiBlockIndex = value
    
    ### Block -> spacing
    @property
    def spacing(self) -> Dict:
        return self._spacing
    
    @spacing.setter
    def spacing(self, value: Dict):
        """ Check, raise error and assign value of block spacing """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'Block.spacing' must be a dictionary.")
            if not all([isinstance(x, int) for x in value]):
                raise ValueError("Elements of 'Block.spacing' must be integers")
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
        """ Check, raise error and assign value of block edge grading """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'Block.grading' must be a dictionary.")
            if not all([isinstance(x, PointValueType) for x in value]):
                raise ValueError("Elements of 'Block.grading' must be integers or floats")
        
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
        
        self.edges = (
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
    

    def get_block_edge_location(
            self,
            locationStringList: List[str]
        ) -> int:
        """
        Get location/index of the edge from the edge description

        Args:
            locationStringList (List[str]): 
                List of two of the following strings - 
                front, back, left, right, top, bottom

        Raises:
            ValueError: if a valid edge position index is not found

        Returns:
            int: position index of an edge in a block
        """
        
        if len(locationStringList) != 2:
            raise ValueError("Edge location specification list must have 2 elements (string)")
        
        locationString1 = f"{locationStringList[0]}-{locationStringList[1]}"
        locationString2 = f"{locationStringList[1]}-{locationStringList[0]}"
        
        edgePosition = [
                    "back-bottom",
                    "back-top",
                    "front-bottom",
                    "front-top",
                    "back-left",
                    "back-right",
                    "front-left",
                    "front-right",
                    "left-bottom",
                    "left-top",
                    "right-bottom",
                    "right-top"
                ]
        
        edgeLocationIndex = None
        
        for locationString in [locationString1, locationString2]:
            if locationString in edgePosition:
                edgeLocationIndex = edgePosition.index(locationString)
            
        return edgeLocationIndex


    def find_edge(
            self,
            edgePosition: List
        ) -> Edge:
        """
        Get the Edge object for a given Block and edge location

        Args:
            blocks (Block): The Block object where the edge is location
            edgePosition (List): List of strings defining the edge location

        Returns:
            Edge: The identified edge object
        """
        
        edgeLocationIndex = self.get_block_edge_location(edgePosition)
            
        if edgeLocationIndex not in range(12):
            raise ValueError("Edge location specification not recognized")
        
        edge = self.edges[edgeLocationIndex]
        
        return edge
    
    def get_hex(self) -> str:
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
    
    
    def get_spacing(self) -> str:
        """ Define the block grid spacing """
        
        spacingDef = "("
        spacingDef += f"{self.spacing['x']}" + wspace
        spacingDef += f"{self.spacing['y']}" + wspace
        spacingDef += f"{self.spacing['z']}"
        
        return spacingDef
    
    
    def get_grading(self):
        """ Define the block edge grading. """
        
        gradingDef = "("
        gradingDef += f"{self.grading['x']}" + wspace
        gradingDef += f"{self.grading['y']}" + wspace
        gradingDef += f"{self.grading['z']}"
        gradingDef += ")"
        
        return gradingDef
    
    
    def definition(self):
        """ Get block definition to write in the dictionary """
        
        blockDef = self.get_hex() + " " + self.get_spacing() + " " + self.get_grading()
        
        return blockDef
    
    
    def minmax(self) -> Dict:
        """  
            Calculates min/max along x, y, z direction for a given block
            Returns a dictionary containing the min/max data
        """
        
        xCoord = []
        yCoord = []
        zCoord = []
        
        for loc, blockVertex in self._vertexCoordinates.items():
            coord = blockVertex
            
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
        
        blockMinMax = self.minmax()
        nx, ny, nz = t.grid_spacing(
                blockMinMax,
                self._dx,
                self._dy,
                self._dz
            )
        
        return nx, ny, nz
    
    def move(
            self,
            delta : tuple[float]
        ) -> None:
        """
        Move selected block

        Args:
            delta (tuple): a tuple of delta values along x, y, z direction
        """
        
        for ivertex in self.vertices:
            ivertex.move(delta = delta)
    
    def scale2d (
            self,
            scalingPlane: str,
            ratio: PointValueType,
        ) -> None:
        """
        Scale block along a specified plane

        Args:
            scalingPlane (str): Name of the plane along which the block will be scaled
            ratio (PointValueType): Ratio of the scaling operation
        """
        
        self._action.scale2d(scalingPlane, ratio)
    
    def scale3d (
            self,
            ratio: PointValueType,
        ) -> None:
        """
        Scale block

        Args:
            ratio (PointValueType): Ratio of the scaling operation
        """
        
        self._action.scale3d(ratio)
        
        
