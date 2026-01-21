
import math
import numpy as np

from collections import OrderedDict, defaultdict
from typing import List, Dict, TypeVar

from entity.block import Block
from entity.face import Face
from entity.slice import Slice
from entity.vertex import Vertex
from operation.action.amblock import MultiBlockAction
from utility.define import (
    indent,
    VSEP,
    quadrantEdgeRule,
    slicePlaneAxisIndex,
)
from utility.udtypes import PointValueType
from utility import tool as t


class MultiBlock:
    """ Class to contain all attributes and generate the desired blockMeshDict """
    
    def __init__(
            self, 
            boundingBox: Dict,
            splitPlanes: List[float],
            gridSpacing: Dict,
            hex2exclude: List[int],
        ):
        """
        Initialize MultiBlock instance
        
        Args:
            boundingBox (dict): Bounding box of the multi-block mesh region
            splitPlanes (list): Planes at which the bounding box will be split
            gridSpacing (dict): Grid spacing for the blocks
            hex2exclude {list}: Ids of the block/hex to exclude in the dictionary to modify the multi-block mesh region
        """
        self._boundingBox = boundingBox
        self._splitPlanes = splitPlanes
        self._gridSpacing = gridSpacing
        self._hex2exclude = hex2exclude
        self._blockGrid = None
                
        self._dx = self._gridSpacing["x"]
        self._dy = self._gridSpacing["y"]
        self._dz = self._gridSpacing["z"]
        
        self.xVertices = []
        self.yVertices = []
        self.zVertices = []
        
        self.vertices = OrderedDict()
        self.blocks = OrderedDict()
        self.slices = OrderedDict()
        
        self.edges = []
        
        self._action = MultiBlockAction(self)
    
    ### MultiBlock - bounding box
    @property
    def boundingBox(self):
        return self._boundingBox
    
    @boundingBox.setter
    def boundingBox(self, value: Dict):
        """ Check, raise error and assign value of MultiBlock.boundingBox """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'MultiBlock.boundingBox' must be a dictionary.")
        
        self._boundingBox = value
    
    ### MultiBlock - split planes
    @property
    def splitPlanes(self):
        return self._splitPlanes
    
    @splitPlanes.setter
    def splitPlanes(self, value: List[PointValueType]) -> None:
        """ Check, raise error and assign value of MultiBlock.splitPlanes """
        
        if not isinstance(value, list):
            raise ValueError("Value of 'MultiBlock.splitPlanes' must be a tuple.")
            
            if not all([isinstance(x, PointValueType) for x in value]):
                raise ValueError("Elements of 'MultiBlock.splitPlanes' must be floats.")
        
        self._splitPlanes = value
    
    ### MultiBlock - grid spacing
    @property
    def gridSpacing(self):
        return self._gridSpacing
    
    @gridSpacing.setter
    def gridSpacing(self, value: Dict) -> None:
        """ Check, raise error and assign value of MultiBlock.vertices """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'MultiBlock.vertices' must be a tuple.")
            
            if not all([isinstance(x, int) for x in value]):
                raise ValueError("Elements of 'MultiBlock.vertices' must be integers.")
        
        self._gridSpacing = value
                
        self._dx = self._gridSpacing["x"]
        self._dy = self._gridSpacing["y"]
        self._dz = self._gridSpacing["z"]
    
    ### MultiBlock - hex2exclude
    @property
    def hex2exclude(self):
        return self._hex2exclude
    
    @hex2exclude.setter
    def hex2exclude(self, value: List[Block]):
        """ Check, raise error and assign value of MultiBlock.hex2exclude """
        
        if not isinstance(value, list):
            raise ValueError("Value of 'MultiBlock.hex2exclude' must be a list.")
        
        self._hex2exclude = value
    
    ### MultiBlock - blockGrid
    @property
    def blockGrid(self):
        return self._blockGrid
    
    @blockGrid.setter
    def blockGrid(self, value: Dict):
        """ Check, raise error and assign value of MultiBlock.blockGrid """
        
        if not isinstance(value, dict):
            raise ValueError("Value of 'MultiBlock.blockGrid' must be a dictionary.")
        
        self._blockGrid = value
    
    def split_locations(self) -> None:
        """
        Organize and the store the split plane 
        locations along x, y, z directions
        """
        
        xSplitCoordinate = sorted(self.splitPlanes["x"])
        ySplitCoordinate = sorted(self.splitPlanes["y"])
        zSplitCoordinate = sorted(self.splitPlanes["z"])
        
        xMinOutOfBound = any([i < self.boundingBox["x-min"] for i in xSplitCoordinate])
        xMaxOutOfBound = any([i > self.boundingBox["x-max"] for i in xSplitCoordinate])
        
        yMinOutOfBound = any([i < self.boundingBox["y-min"] for i in ySplitCoordinate])
        yMaxOutOfBound = any([i > self.boundingBox["y-max"] for i in ySplitCoordinate])
        
        zMinOutOfBound = any([i < self.boundingBox["z-min"] for i in zSplitCoordinate])
        zMaxOutOfBound = any([i > self.boundingBox["z-max"] for i in zSplitCoordinate])
        
        if True in [
                xMinOutOfBound, xMaxOutOfBound, 
                yMinOutOfBound, yMaxOutOfBound,
                zMinOutOfBound, zMaxOutOfBound
            ]:
            raise ValueError("Split plane location is outside of the user defined bounding box.")
        
        self.xVertices.append(self.boundingBox["x-min"])
        if bool(xSplitCoordinate):
            self.xVertices.extend(xSplitCoordinate)
        self.xVertices.append(self.boundingBox["x-max"])
        
        self.yVertices.append(self.boundingBox["y-min"])
        if bool(ySplitCoordinate):
            self.yVertices.extend(ySplitCoordinate)
        self.yVertices.append(self.boundingBox["y-max"])
        
        self.zVertices.append(self.boundingBox["z-min"])
        if bool(zSplitCoordinate):
            self.zVertices.extend(zSplitCoordinate)
        self.zVertices.append(self.boundingBox["z-max"]) 
        
        
    def block_count(self) -> Dict:
        """ Get the block count in x, y, z directions """
        
        self.nBlock = {
                "x" : len(self.xVertices) - 1,
                "y" : len(self.yVertices) - 1,
                "z" : len(self.zVertices) - 1,
            }
        self.nBlock["total"] = self.nBlock["x"] * self.nBlock["y"] * self.nBlock["z"]
        self.display_block_count()
        
        return self.nBlock
    
    
    def display_block_count(self) -> None:
        """ Display number of blocks """
        
        str2print = VSEP + "\n"
        str2print += f"Blocks along X : {self.nBlock['x']}\n"
        str2print += f"Blocks along Y : {self.nBlock['y']}\n"
        str2print += f"Blocks along Z : {self.nBlock['z']}\n\n"
        str2print += f"Total blocks   : {self.nBlock['total']}"
        print(str2print)
    
    
    def _define_block_point_order(
            self,
            zBack: int, 
            zFront: int,
            yBottom: int,
            yTop: int,
            ix: int
        ) -> tuple:
        """
        Define and arrange vertices needed to define a block.

        Args:
            zBack (int): z-index associated with the back face
            zFront (int): z-index associated with the front face
            yBottom (int): y-index associated with the bottom face
            yTop (int): y-index associated with the yop face
            ix (int): Index /vertex id

        Returns:
            tuple: of 8 instances of the Vertex class defining 
                the block ordered according to blockMesh convention
        """
        
        pointBackBottomLeft = self.vertexGroupDict[zBack][yBottom][ix]
        pointBackBottomRight = self.vertexGroupDict[zBack][yBottom][ix + 1]
        
        pointBackTopRight = self.vertexGroupDict[zBack][yTop][ix + 1]
        pointBackTopLeft = self.vertexGroupDict[zBack][yTop][ix]
        
        pointFrontBottomLeft = self.vertexGroupDict[zFront][yBottom][ix]
        pointFrontBottomRight = self.vertexGroupDict[zFront][yBottom][ix + 1]
        
        pointFrontTopRight = self.vertexGroupDict[zFront][yTop][ix + 1]
        pointFrontTopLeft = self.vertexGroupDict[zFront][yTop][ix]
        
        return (
                pointBackBottomLeft,
                pointBackBottomRight,
                pointBackTopRight,
                pointBackTopLeft,
                pointFrontBottomLeft,
                pointFrontBottomRight,
                pointFrontTopRight,
                pointFrontTopLeft
            )
    
    def _define_face(
            self,
            index: int,
            pointBackBottomLeft: Vertex,
            pointBackBottomRight: Vertex,
            pointBackTopRight: Vertex,
            pointBackTopLeft: Vertex,
            pointFrontBottomLeft: Vertex,
            pointFrontBottomRight: Vertex,
            pointFrontTopRight: Vertex,
            pointFrontTopLeft: Vertex
        ) -> Dict:
        """
        Define block faces for a given block id.

        Args:
            index (int): Id of the block to which these faces belong
            pointBackBottomLeft (Vertex): point position, back-bottom-left
            pointBackBottomRight (Vertex): point position,  back-bottom-right
            pointBackTopRight (Vertex): point position, back-top-right
            pointBackTopLeft (Vertex): point position, back-yop-left
            pointFrontBottomLeft (Vertex): point position, front-bottom-left
            pointFrontBottomRight (Vertex): point position, front-bottom-right
            pointFrontTopRight (Vertex): point position, front-top-right
            pointFrontTopLeft (Vertex): point position, front-top-left

        Returns:
            Dict: of 6 instances of the Face class which defines the 
                given block
        """
        
        faces = {}
        
        faceName =   "front"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointFrontBottomLeft,
                                pointFrontTopLeft,
                                pointFrontTopRight,
                                pointFrontBottomRight,
                            ]
                        )
        
        faceName =   "back"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointBackBottomLeft,
                                pointBackBottomRight,
                                pointBackTopRight,
                                pointBackTopLeft,
                            ]
                        )
        
        faceName =   "left"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointBackBottomLeft,
                                pointBackTopLeft,
                                pointFrontTopLeft,
                                pointFrontBottomLeft,
                            ]
                        )
        
        faceName =   "right"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointFrontBottomRight,
                                pointFrontTopRight,
                                pointBackTopRight,
                                pointBackBottomRight,
                            ]
                        )
        
        faceName =   "bottom"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointBackBottomLeft,
                                pointFrontBottomLeft,
                                pointFrontBottomRight,
                                pointBackBottomRight,
                            ]
                        )
        
        faceName =   "top"          
        faces[faceName] = Face(
                            index,
                            faceName,
                            [
                                pointBackTopLeft,
                                pointBackTopRight,
                                pointFrontTopRight,
                                pointFrontTopLeft,
                            ]
                        )
        return faces
    
    def _define_block(
            self,
            hexCount: int,
            blockIndex: str,
            isActive: bool,
            blockVertices: tuple,
            blockVertexCoordinates: Dict
        ) -> None:
        """
        Define block for a given block id.

        Args:
            hexCount (int): Block/hex id.
            blockIndex (str): A string representing the x, y, z position of the block in the multi-block
            isActive (bool): block status. Included/active is True, excluded/inactive is False
            blockVertices (tuple): Tuple of 8 instances of the Vertex class
            blockVertexCoordinates (Dict): Coordinates of the vertex defining the block
        """
        
        grading = {
            "x" : 1,
            "y" : 1,
            "z" : 1,
        }
        
        faces = self._define_face(
                hexCount,
                *blockVertices
            )
        
        self.blocks[hexCount] = Block(
                                        hexCount,
                                        blockIndex,
                                        isActive,
                                        blockVertices,
                                        blockVertexCoordinates,
                                        faces,
                                        self._gridSpacing,
                                        grading
                                    )
        self.blocks[hexCount].get_edges()
    
    def create_vertex_group(self):
        """ Calculated vertex location, create groups/dicts """
        
        vertexCount = 0
        
        self.zSplitIndex = []
        self.ySplitIndex = []
        self.xSplitIndex = []
        
        self.vertexGroupDict = OrderedDict()
        
        for k in range(self.nBlock["z"] + 1):
            zIndex = "z_" + str(k)
            self.zSplitIndex.append(zIndex)
            self.vertexGroupDict[zIndex] = OrderedDict()
            
            for j in range(self.nBlock["y"] + 1):
                yIndex = "y_" + str(j)
                self.ySplitIndex.append(yIndex)
                self.vertexGroupDict[zIndex][yIndex] = {}
                
                for i in range(self.nBlock["x"] + 1):
                    self.vertices[vertexCount] = Vertex(
                                                        vertexCount,
                                                        self.xVertices[i],
                                                        self.yVertices[j],
                                                        self.zVertices[k]
                                                    )
                    self.xSplitIndex.append(self.xVertices[i])
                    self.vertexGroupDict[zIndex][yIndex][i] = self.vertices[vertexCount]
                    vertexCount += 1
    
    
    def create_blocks(self):
        """ Creates a dictionary to contain all the block/hex definitions """
        
        blockVertexCoordinates = {}
        hexCount = 0
        xCount = 0
        
        for iz in range(self.nBlock["z"]):
            zBack = self.zSplitIndex[iz]
            zFront = self.zSplitIndex[iz + 1]
            
            for iy in range(self.nBlock["y"]):
                yBottom = self.ySplitIndex[iy]
                yTop = self.ySplitIndex[iy + 1]
                
                for ix in range(self.nBlock["x"]):
                    if hexCount in self._hex2exclude:
                        isActive = False
                    else:
                        isActive = True
                    blockVertices = self._define_block_point_order(
                                            zBack, 
                                            zFront,
                                            yBottom,
                                            yTop,
                                            ix
                                        )
                    blockIndex = "x-" + str(ix) + "_y-" + str(iy) + "_z-" + str(iz)
                    
                    for iv, blockVertex in enumerate(blockVertices):
                        blockVertexCoordinates[iv] = blockVertex.coordinates()
                    
                    self._define_block(
                            hexCount,
                            blockIndex,
                            isActive,
                            blockVertices,
                            blockVertexCoordinates
                        )
                    
                    hexCount += 1
                    xCount +=1
        
        
        return self.blocks
    
    def get_edges(self) -> None:
        """  """
        
        for blockId, iblock in self.blocks.items():
            for iedge in iblock.edges:
                if iedge not in self.edges:
                    self.edges.append(iedge)
        
    
    def get_slices(self) -> None:
        """
        Blocks are stacked in the following manner :
            First stack along x, then along y, then along z
        
        In NumPy, the axes typically follow the ZYX convention when
        dealing with spatial data to be consistent with C-style, 
        row-major memory ordering. This means that the X, Y, and Z indices
        correspond to different axes in a NumPy array with shape=(Z, Y, X).
        https://stackoverflow.com/a/46857263
                
        """
        
        blockArray = np.array(list(self.blocks.keys()))
        blockArray = blockArray.reshape(
                self.nBlock["z"] ,
                self.nBlock["y"] , 
                self.nBlock["x"] , 
            )
        
        self.nBlockXyPlane = self.nBlock["x"] * self.nBlock["y"]
        self.nBlockYzPlane = self.nBlock["y"] * self.nBlock["z"]
        self.nBlockZxPlane = self.nBlock["z"] * self.nBlock["x"]
        
        xSortedMbBlocks = blockArray.flatten().tolist()
        ySortedMbBlocks = np.transpose(blockArray, axes = (2, 0, 1)).flatten().tolist()
        zSortedMbBlocks = np.transpose(blockArray, axes = (1, 2, 0)).flatten().tolist()
        
        self.xyStackedBlocks = [xSortedMbBlocks[i : i + self.nBlockXyPlane] for i in range(0, self.nBlock["total"], self.nBlockXyPlane)]
        self.yzStackedBlocks = [ySortedMbBlocks[j : j + self.nBlockYzPlane] for j in range(0, self.nBlock["total"], self.nBlockYzPlane)]
        self.zxStackedBlocks = [zSortedMbBlocks[k : k + self.nBlockZxPlane] for k in range(0, self.nBlock["total"], self.nBlockZxPlane)]
        
        # ### Checking/slicing the ndarray representation of the blocks 
        # print("x-slices")
        # for i in range(self.nBlock["z"]):
        #     print(blockArray[i, :, :])
        
        # print("y-slices")
        # for i in range(self.nBlock["x"]):
        #     print(blockArray[:, :, i])
        
        # print("z-slices")
        # for i in range(self.nBlock["y"]):
        #     print(blockArray[:, i, :].swapaxes(0, 1))
        
        self.slices = {
            "xy" : {},
            "yz" : {},
            "zx" : {},
        }
        
        for i in range(len(self.xyStackedBlocks)):
            self.slices["xy"][i] = Slice(
                                            "xy",
                                            i,
                                            tuple(self.xyStackedBlocks[i])
                                        )
        
        for j in range(len(self.yzStackedBlocks)):
            self.slices["yz"][j] = Slice(
                                            "yz",
                                            j,
                                            tuple(self.yzStackedBlocks[j])
                                        )
        
        for k in range(len(self.zxStackedBlocks)):
            self.slices["zx"][k] = Slice(
                                            "zx",
                                            k,
                                            tuple(self.zxStackedBlocks[k])
                                        )
    
    def assign_multiblock_index_to_block(self) -> None:
        """ Assign (x, y, z) index to blocks in the multi-block grid """
        
        xIndexCount = 0
        yIndexCount = 0
        zIndexCount = 0
        
        for i in range(len(self.blocks)):
            self.blocks[i].multiBlockIndex = (xIndexCount, yIndexCount, zIndexCount)
            xIndexCount += 1
            if (i + 1) % (self.nBlock["x"]) == 0:
                xIndexCount = 0
                yIndexCount += 1
                if (i + 1) % (self.nBlock["x"] * self.nBlock["y"]) == 0:
                    yIndexCount = 0
                    zIndexCount += 1
    
    def create_multiblock_grid(
            self
        ) -> None:
        """ Create block-grid for MultiBlock object """
        
        ### defining a 3-level empty nested dictionary
        ### for initializing empty grid
        blockGrid = defaultdict(lambda: defaultdict(dict))
        
        for blockId, iblock in self.blocks.items():
            ix, iy, iz = iblock.multiBlockIndex
            blockGrid[ix][iy][iz] = iblock
            
        self.blockGrid = blockGrid
    
    def make(self) -> None:
        """ Run the multi-block operations """
        
        self.split_locations()
        self.block_count()
        self.create_vertex_group()
        self.create_blocks()
        self.get_edges()
        self.get_slices()
        self.assign_multiblock_index_to_block()
        self.create_multiblock_grid()
    
    def get_block_with_multiblock_index(
            self,
            multiblockIndex: tuple
        ) -> Block:
        
        x, y, z = multiblockIndex
        
        return self.blockGrid[x][y][z]
    
    def slice_info(self) -> str:
        """ Generate slice information of the multi-block """
        
        t.hl()
        print(f"Number of blocks in each XY plane : {self.nBlockXyPlane}")
        print(f"Number of blocks in each YZ plane : {self.nBlockYzPlane}")
        print(f"Number of blocks in each ZX plane : {self.nBlockZxPlane}")
        
        
        print("\n")
        t.hl()
        sliceInfoStr = "### SLICE INFO ###\n"
        sliceInfoStr += VSEP + "\n"
        
        ### blw -> blockLabelWidth
        blw = len(str(self.nBlock["total"] - 1))
        sliceInfoStr += "SLICE PLANE - XY\n"
        sliceInfoStr += VSEP + "\n"
        
        for i, _slice in self.slices["xy"].items():
            sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
        
        sliceInfoStr += VSEP + "\n"
        sliceInfoStr += "SLICE PLANE - YZ\n"
        sliceInfoStr += VSEP + "\n"
        
        for j, _slice in self.slices["yz"].items():
            sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
        
        sliceInfoStr += VSEP + "\n"
        sliceInfoStr += "SLICE PLANE - ZX\n"
        sliceInfoStr += VSEP + "\n"
        
        for k, _slice in self.slices["zx"].items():
            sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
        
        print(sliceInfoStr)
        
        return sliceInfoStr
    
    
    def scaleSliceBlocks (
            self,
            blocks2scale: List,
            scalingPlane: str,
            ratio: float,
            reference: tuple
        ) -> None:
        
        vertices = []
        
        for iblock in blocks2scale:
            vertices.extend(iblock.vertices)
        
        vertices = list(set(vertices))
        
        xCoordinates = []
        yCoordinates = []
        zCoordinates = []
        
        ### Unique coordinates
        xCoordinates = list(set([i.coordinates()[0] for i in vertices]))
        yCoordinates = list(set([i.coordinates()[1] for i in vertices]))
        zCoordinates = list(set([i.coordinates()[2] for i in vertices]))
        
        meanX = sum(xCoordinates)/len(xCoordinates)
        meanY = sum(yCoordinates)/len(yCoordinates)
        meanZ = sum(zCoordinates)/len(zCoordinates)
        
        if scalingPlane == "xy":
            xScaledValues = {}
            yScaledValues = {}
            for ix in xCoordinates:
                xScaledValues[ix] = meanX + (ix - meanX) * ratio
            for iy in yCoordinates:
                yScaledValues[iy] = meanY + (iy - meanY) * ratio
                
            for ivertex in vertices:
                ix, iy, iz = ivertex.coordinates()
                ivertex.x = xScaledValues[ix]
                ivertex.y = yScaledValues[iy]
        
        elif scalingPlane == "yz":
            yScaledValues = {}
            zScaledValues = {}
            for iy in yCoordinates:
                yScaledValues[iy] = meanY + (iy - meanY) * ratio
            for iz in zCoordinates:
                zScaledValues[iz] = meanZ + (iz - meanZ) * ratio
                
            for ivertex in vertices:
                ix, iy, iz = ivertex.coordinates()
                ivertex.y = yScaledValues[iy]
                ivertex.z = zScaledValues[iz]
        
        elif scalingPlane == "zx":
            zScaledValues = {}
            xScaledValues = {}
            for iz in zCoordinates:
                zScaledValues[iz] = meanZ + (iz - meanZ) * ratio
            for ix in xCoordinates:
                xScaledValues[ix] = meanX + (ix - meanX) * ratio
                
            for ivertex in vertices:
                ix, iy, iz = ivertex.coordinates()
                ivertex.z = xScaledValues[iz]
                ivertex.x = xScaledValues[ix]
    
    #---------------------------------------
    ### Quadrant Section - Start
    #---------------------------------------
    
    def make_quadrant(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
        ) -> list:
        """
        Make quadrant based on the block selection

        Args:
            startblockId (int): Id of selected starting block (diagonally left-bottom) 
            endblockId (int): Id of selected end block (diagonally left-bottom) 
            radius (float): Radius of the quadrant
            slicePlane (str): Name of the slice plane
            blockConditionCheckNeeded (bool, optional): True means block selection validity is needed. Defaults to True.

        Raises:
            ValueError: If the block selections were invalid for making a quadrant
            ValueError: If common edge among the center and side blocks can't be identified

        Returns:
            list: List of edge definitions to implement the quadrant shape
        """
        
        centerBlock = self.blocks[startblockId]
        cornerBlock = self.blocks[endblockId]
        
        self._action.make_four_block_quadrant(
                centerBlock,
                cornerBlock,
                radius,
            )
        
        return
    
    def make_semicircle(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
        ) -> list:
        """
        Make semicircle based on the block selection

        Args:
            startblockId (int): Id of selected starting block (diagonally left-bottom)
            endblockId (int): Id of selected end block (diagonally left-bottom) 
            radius (float): Radius of the quadrant
            slicePlane (str): Name of the slice plane

        Raises:
            ValueError: If the block selections were invalid for making a quadrant

        Returns:
            list: List of edge definitions to implement the quadrant shape
        """
        
        centerBlock = self.blocks[startblockId]
        cornerBlock = self.blocks[endblockId]
        
        self._action.make_eight_block_semicircle(
                centerBlock,
                cornerBlock,
                radius,
            )
    
    def make_circle(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
        ) -> list:
        """
        Make circle based on the block selection

        Args:
            startblockId (int): Id of selected starting block (diagonally left-bottom)
            endblockId (int): Id of selected end block (diagonally left-bottom) 
            radius (float): Radius of the quadrant
            slicePlane (str): Name of the slice plane

        Raises:
            ValueError: If the block selections were invalid for making a quadrant

        Returns:
            list: List of edge definitions to implement the quadrant shape
        """
        
        centerBlock = self.blocks[startblockId]
        cornerBlock = self.blocks[endblockId]
        
        self._action.make_sixteen_block_circle(
                centerBlock,
                cornerBlock,
                radius,
            )
    
    #---------------------------------------
    ### Quadrant Section - Start
    #---------------------------------------
        
            





