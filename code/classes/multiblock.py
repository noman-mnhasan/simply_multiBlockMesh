
import math

from collections import (
    OrderedDict,
    defaultdict
)
from typing import (
    List, 
    Dict,
)

from .block import *
from .face import *
from .slice import *
from .vertex import *

import numpy as np

from lib import (
    wspace,
    indent,
    VSEP,
    quadrantEdgeRule,
    slicePlaneAxisIndex,
    hl
)


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
    def splitPlanes(self, value: List[float]):
        """ Check, raise error and assign value of MultiBlock.splitPlanes """
        
        if not isinstance(value, list):
            raise ValueError("Value of 'MultiBlock.splitPlanes' must be a tuple.")
            
            if not all([isinstance(x, (float)) for x in value]):
                raise ValueError("Elements of 'MultiBlock.splitPlanes' must be floats.")
        
        self._splitPlanes = value
    
    ### MultiBlock - grid spacing
    @property
    def gridSpacing(self):
        return self._gridSpacing
    
    @gridSpacing.setter
    def gridSpacing(self, value: Dict):
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
    def hex2exclude(self, value: list):
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
    
    
    def get_split_info(self) -> str:
        """ Display the x/y/z coordinates of the (bounding ox & split/cut locations) """
        
        splitLocationInfo = VSEP + "\n"
        splitLocationInfo += "[*] Split plane(s) along X:"
        splitLocationInfo += indent + ", ".join([str(i) for i in self.xVertices]) + "\n"
        splitLocationInfo += "[*] Split plane(s) along Y:"
        splitLocationInfo += indent + ", ".join([str(i) for i in self.yVertices]) + "\n"
        splitLocationInfo += "[*] Split plane(s) along Z:"
        splitLocationInfo += indent + ", ".join([str(i) for i in self.zVertices]) + "\n"
                
        return splitLocationInfo
        
        
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
        
        for blockId, iBlock in self.blocks.items():
            ix, iy, iz = iBlock.multiBlockIndex
            blockGrid[ix][iy][iz] = iBlock
            
        self.blockGrid = blockGrid
    
    def make(self) -> None:
        """ Run the multi-block operations """
        
        self.split_locations()
        self.block_count()
        self.create_vertex_group()
        self.create_blocks()
        self.get_slices()
        self.assign_multiblock_index_to_block()
        self.create_multiblock_grid()
    
    def get_block_with_multiblock_index(
            self,
            multiblockIndex: tuple
        ) -> Block:
        
        x, y, z = multiblockIndex
        
        return self.blockGrid[x][y][z]
    
    def face_info(self) -> str:
        """ Generate face information of the multi-block """
        
        faceInfoStr = "FACE INFO\n" 
        faceInfoStr += VSEP + "\n\n"
        
        for k,v in self.blocks.items():
            faceInfoStr += "Block-" + str(k) + " : " + str(v.index) + "\n\n"
            for faceName, faces in v.faces.items():
                faceInfoStr += indent + f"{faceName:6} : (" + " ".join(str(x) for x in faces.vertices) + ")\n"
            faceInfoStr += "\n\n"
        
        return faceInfoStr
    
    def slice_info(self) -> str:
        """ Generate slice information of the multi-block """
        
        hl()
        print(f"Number of blocks in each XY plane : {self.nBlockXyPlane}")
        print(f"Number of blocks in each YZ plane : {self.nBlockYzPlane}")
        print(f"Number of blocks in each ZX plane : {self.nBlockZxPlane}")
        
        
        print("\n")
        hl()
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
    
    def edge_info(self) -> str:
        """ Generate edge information of the multi-block """
        
        edgeInfoStr = "### EDGE INFO ###\n"
        edgeInfoStr += VSEP + "\n"
        
        for blockId, iblock in self.blocks.items():
            edgeInfoStr += f"\n\n{VSEP}\nBlock ID - {blockId}\n"
            edgeInfoStr += VSEP + "\n"
            edgeInfoStr += "Index | ->  - Position     - Definition\n"
            edgeInfoStr += VSEP + "\n"
            
            for iedge in iblock.edges:
                edgeInfoStr += f"{iedge.id:5} | {iedge}\n"
        
        return edgeInfoStr
    
    def get_axis_index(
            self,
            axisName: str
        ) -> int:
        """
        Get multi-block indices axis index

        Args:
            axisName (str): Name of an axis (x, y, z)

        Returns:
            int: 0 for x, 1 for y, and 2 for z
        """
        
        if axisName == "x":
            index = 0
        elif axisName == "y":
            index = 1
        elif axisName == "z":
            index = 2
        return index
    
    def get_quadrant_number(
            self,
            multiblockIndex1Center,
            multiblockIndex2Center,
            multiblockIndex1Corner,
            multiblockIndex2Corner,
        ) -> int:
        """
        Get the quadrant number (1, 2, 3, 4) based on the definition of the staring and end block selection

        Args:
            multiblockIndex1Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex1Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z

        Returns:
            int: The quadrant number based on the block selection
        """
        
        ### 1 --> 1st quadrant
        ### 2 --> 2nd quadrant
        ### 3 --> 3rd quadrant
        ### 4 --> 4th quadrant
        quadrantNumber = None
        
        if (multiblockIndex1Center < multiblockIndex1Corner and
            multiblockIndex2Center < multiblockIndex2Corner):
            quadrantNumber = 1
        
        elif (multiblockIndex1Center > multiblockIndex1Corner and
            multiblockIndex2Center < multiblockIndex2Corner):
            quadrantNumber = 2
        
        elif (multiblockIndex1Center > multiblockIndex1Corner and
            multiblockIndex2Center > multiblockIndex2Corner):
            quadrantNumber = 3
        
        elif (multiblockIndex1Center < multiblockIndex1Corner and
            multiblockIndex2Center > multiblockIndex2Corner):
            quadrantNumber = 4
        
        return quadrantNumber
    
    
    ### TOO LONG - NEED TO SIMPLIFY ###
    
    def get_block_shift_coefficient_for_quadrant(
            self,
            quadrantNumber
        ) -> int:
        """ Set the multi-block index offset to select the top and side bloc, relative to the center block. """
        
        if quadrantNumber == 1:
            topShift = 1
            sideShift = 1
        elif quadrantNumber == 2:
            topShift = 1
            sideShift = -1
        elif quadrantNumber == 3:
            topShift = -1
            sideShift = -1
        elif quadrantNumber == 4:
            topShift = -1
            sideShift = 1
        return (
                topShift,
                sideShift
            )
    
    def get_top_block_for_quadrant(
            self,
            slicePlane,
            centerBlockGridPosition,
            topShift
        ) -> Block:
        """
        Get the top-block in reference to the center-block (the block 
        that contains the axis of the quadrant) of the quadrant
        """
        
        ix, iy, iz = centerBlockGridPosition
        
        if slicePlane == "xy":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + topShift,
                        iz
                    )
                )
        
        elif slicePlane == "yz":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy,
                        iz + topShift
                    )
                )
        
        elif slicePlane == "zx":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix + topShift,
                        iy,
                        iz
                    )
                )
        return topBlock
    
    def get_side_block_for_quadrant(
            self,
            slicePlane,
            centerBlockGridPosition,
            sideShift
        ) -> Block:
        """
        Get the side-block in reference to the center-block (the block 
        that contains the axis of the quadrant) of the quadrant
        """
        
        ix, iy, iz = centerBlockGridPosition
        
        if slicePlane == "xy":
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix + sideShift,
                        iy,
                        iz
                    )
                )
        
        elif slicePlane == "yz":
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + sideShift,
                        iz
                    )
                )
        
        elif slicePlane == "zx":
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy,
                        iz + sideShift
                    )
                )
        
        return sideBlock
    
    def get_quadrant_block_details(
            self,
            centerBlock,
            slicePlane,
            quadrantNumber,
        ) -> dict:
        
        quadrantInfo = {}
        
        ix, iy, iz = centerBlock.multiBlockIndex
        
        topShift, sideShift = self.get_block_shift_coefficient_for_quadrant(quadrantNumber)
        
        topBlock = self.get_top_block_for_quadrant(
                slicePlane,
                centerBlock.multiBlockIndex,
                topShift
            )
        
        sideBlock = self.get_side_block_for_quadrant(
                slicePlane,
                centerBlock.multiBlockIndex,
                sideShift
            )
        
        collapseEdgeDirection = quadrantEdgeRule[slicePlane][quadrantNumber]["collapse-edge-location"]
        axisEdgeDirection = quadrantEdgeRule[slicePlane][quadrantNumber]["axis-edge-location"]
        arcEdgeDirection = quadrantEdgeRule[slicePlane][quadrantNumber]["arc-edge-location"]
                
        quadrantInfo["top-block"] = topBlock
        quadrantInfo["side-block"] = sideBlock
        quadrantInfo["collapse-edge-direction"] = collapseEdgeDirection
        quadrantInfo["axis-edge-direction"] = axisEdgeDirection
        quadrantInfo["arc-edge-direction"] = arcEdgeDirection
        
        return quadrantInfo
    
    def get_angles_for_quadrant(
            self,
            quadrantNumber
        ) -> tuple:
        """
        Get the angles to define the arc points to apply curvature 
        on the block edges of teh quadrant 
        """
        
        if quadrantNumber == 1:
            thetaCorner = 45
            thetaSideArc = 45/2.0
            thetaTopArc = 3*45/2.0
            
        elif quadrantNumber == 2:
            thetaCorner = (1*90) + 45
            thetaSideArc = (1*90) + (3*45/2.0)
            thetaTopArc = (1*90) + (45/2.0)
        
        elif quadrantNumber == 3:
            thetaCorner = (2*90) + 45
            thetaSideArc = (2*90) + (45/2.0)
            thetaTopArc = (2*90) + (3*45/2.0)
        
        elif quadrantNumber == 4:
            thetaCorner = (3*90) + 45
            thetaSideArc = (3*90) + (3*45/2.0)
            thetaTopArc = (3*90) + (45/2.0)
        
        return (
                thetaCorner,
                thetaSideArc,
                thetaTopArc
            )
    
    def get_quadrant_arc_coordinates(
            self,
            slicePlane,
            radius,
            quadrantCenter,
            thetaCorner,
            thetaSideArc,
            thetaTopArc,
        ) -> tuple:
        
        sinThetaCorner = math.sin(math.radians(thetaCorner))
        cosThetaCorner = math.cos(math.radians(thetaCorner))
        
        sinThetaSideArc = math.sin(math.radians(thetaSideArc))
        cosThetaSideArc = math.cos(math.radians(thetaSideArc))
        
        sinThetaTopArc = math.sin(math.radians(thetaTopArc))
        cosThetaTopArc = math.cos(math.radians(thetaTopArc))
        
        if slicePlane == "xy":
            radialCornerX = (radius * cosThetaCorner) + quadrantCenter[0]
            radialCornerY = (radius * sinThetaCorner) + quadrantCenter[1]
            radialCornerZ = None
            
            radialTopArcX = (radius * cosThetaTopArc) + quadrantCenter[0]
            radialTopArcY = (radius * sinThetaTopArc) + quadrantCenter[1]
            radialTopArcZ = None
            
            radialSideArcX = (radius * cosThetaSideArc) + quadrantCenter[0]
            radialSideArcY = (radius * sinThetaSideArc) + quadrantCenter[1]
            radialSideArcZ = None
        
        elif slicePlane == "yz":
            radialCornerX = None
            radialCornerY = (radius * cosThetaCorner) + quadrantCenter[1]
            radialCornerZ = (radius * sinThetaCorner) + quadrantCenter[2]
            
            radialTopArcX = None
            radialTopArcY = (radius * cosThetaTopArc) + quadrantCenter[1]
            radialTopArcZ = (radius * sinThetaTopArc) + quadrantCenter[2]
            
            radialSideArcX = None
            radialSideArcY = (radius * cosThetaSideArc) + quadrantCenter[1]
            radialSideArcZ = (radius * sinThetaSideArc) + quadrantCenter[2]
        
        elif slicePlane == "zx":
            radialCornerX = (radius * sinThetaCorner)+ quadrantCenter[0]
            radialCornerY = None
            radialCornerZ = (radius * cosThetaCorner) + quadrantCenter[2]
            
            radialTopArcX = (radius * sinThetaTopArc) + quadrantCenter[0]
            radialTopArcY = None
            radialTopArcZ = (radius * cosThetaTopArc) + quadrantCenter[2]
            
            radialSideArcX = (radius * sinThetaSideArc) + quadrantCenter[0]
            radialSideArcY = None
            radialSideArcZ = (radius * cosThetaSideArc) + quadrantCenter[2]
        
        return(
                radialCornerX,
                radialCornerY,
                radialCornerZ,
                radialTopArcX,
                radialTopArcY,
                radialTopArcZ,
                radialSideArcX,
                radialSideArcY,
                radialSideArcZ
            )
    
    def get_quadrant_collapsed_edge_delta (
            self,
            slicePlane,
            sideBlockCollapseEdge,
            radialCornerX,
            radialCornerY,
            radialCornerZ,
        ) -> tuple:
        """
        Get the move distance of the collapsed edge after edges have been
        been collapsed.
        """
        
        if slicePlane == "xy":
            deltaX = radialCornerX - sideBlockCollapseEdge.start.coordinates()[0]
            deltaY = radialCornerY - sideBlockCollapseEdge.start.coordinates()[1]
            deltaZ = 0
            
        elif slicePlane == "yz":
            deltaX = 0
            deltaY = radialCornerY - sideBlockCollapseEdge.start.coordinates()[1]
            deltaZ = radialCornerZ - sideBlockCollapseEdge.start.coordinates()[2]
            
        elif slicePlane == "zx":
            deltaZ = radialCornerZ - sideBlockCollapseEdge.start.coordinates()[2]
            deltaY = 0
            deltaX = radialCornerX - sideBlockCollapseEdge.start.coordinates()[0]
        
        return (
                deltaX,
                deltaY,
                deltaZ
            )
    
    def reshape_quadrant_center_block(
            self,
            slicePlane,
            radius,
            quadrantNumber,
            compressionFactor,
            centerBlockInnerCorner
        ) -> None:
        """
        Reshape the center block (block containing the axis of the quadrant)
        to smooth out the quadrant mesh
        """
        
        if quadrantNumber == 1:
            shiftFactor1stAxis = -1
            shiftFactor2ndAxis = -1
        elif quadrantNumber == 2:
            shiftFactor1stAxis = 1
            shiftFactor2ndAxis = -1
        elif quadrantNumber == 3:
            shiftFactor1stAxis = 1
            shiftFactor2ndAxis = 1
        elif quadrantNumber == 4:
            shiftFactor1stAxis = -1
            shiftFactor2ndAxis = 1
            
        if slicePlane == "xy":
            centerBlockInnerEdgeDeltaX = shiftFactor1stAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaY = shiftFactor2ndAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaZ = 0
        elif slicePlane == "yz":
            centerBlockInnerEdgeDeltaY = shiftFactor1stAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaZ = shiftFactor2ndAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaX = 0
        elif slicePlane == "zx":
            centerBlockInnerEdgeDeltaZ = shiftFactor1stAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaX = shiftFactor2ndAxis * radius/2.0 * compressionFactor
            centerBlockInnerEdgeDeltaY = 0
        
        centerBlockInnerCorner.move([
                centerBlockInnerEdgeDeltaX,
                centerBlockInnerEdgeDeltaY,
                centerBlockInnerEdgeDeltaZ
            ])
            
    def add_quadrant_arc_top_block(
            self,
            slicePlane,
            topBlock,
            arcEdgeDirection,
            radialTopArcX,
            radialTopArcY,
            radialTopArcZ
        ) -> list:
        """
        Implement the arc on the edges of a top block of the quadrant

        Args:
            slicePlane (str): Name of the slice plane
            topBlock (Block): A Block object which lies on top of the center block
            arcEdgeDirection (list): A list describing the position of an edge in a block
            radialTopArcX (float): X coordinate of the arch at the edges of the top block
            radialTopArcY (float): Y coordinate of the arch at the edges of the top block
            radialTopArcZ (float): Z coordinate of the arch at the edges of the top block

        Returns:
            list: List of strings containing the blockMeshDict entry
        """
        
        edgeDefinitionTopBlock = []
        
        arcEdgeTopBlock1 = topBlock.find_edge(
                arcEdgeDirection["top-block"][0]
            )
        arcEdgeTopBlock2 = topBlock.find_edge(
                arcEdgeDirection["top-block"][1]
            )
        
        if slicePlane == "xy":
            radialTopArcZ1 = arcEdgeTopBlock1.start.coordinates()[2]
            radialTopArcZ2 = arcEdgeTopBlock2.start.coordinates()[2]
        
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX,
                            radialTopArcY,
                            radialTopArcZ1
                        )
                    )
                )
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock2.arc(
                        (
                            radialTopArcX,
                            radialTopArcY,
                            radialTopArcZ2
                        )
                    )
                )
            
        elif slicePlane == "yz":
            radialTopArcX1 = arcEdgeTopBlock1.start.coordinates()[0]
            radialTopArcX2 = arcEdgeTopBlock2.start.coordinates()[0]
        
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX1,
                            radialTopArcY,
                            radialTopArcZ
                        )
                    )
                )
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock2.arc(
                        (
                            radialTopArcX2,
                            radialTopArcY,
                            radialTopArcZ
                        )
                    )
                )
        elif slicePlane == "zx":
            radialTopArcY1 = arcEdgeTopBlock1.start.coordinates()[1]
            radialTopArcY2 = arcEdgeTopBlock2.start.coordinates()[1]
        
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX,
                            radialTopArcY1,
                            radialTopArcZ
                        )
                    )
                )
            edgeDefinitionTopBlock.append(
                arcEdgeTopBlock2.arc(
                        (
                            radialTopArcX,
                            radialTopArcY2,
                            radialTopArcZ
                        )
                    )
                )
        
        return edgeDefinitionTopBlock
            
    def add_quadrant_arc_side_block(
            self,
            slicePlane,
            sideBlock,
            arcEdgeDirection,
            radialSideArcX,
            radialSideArcY,
            radialSideArcZ
        ) -> list:
        """
        Implement the arc on the edges of a side block of the quadrant

        Args:
            slicePlane (str): Name of the slice plane
            sideBlock (Block): A Block object which lies on side of the center block
            arcEdgeDirection (list): A list describing the position of an edge in a block
            radialSideArcX (float): X coordinate of the arch at the edges of the side block
            radialSideArcY (float): Y coordinate of the arch at the edges of the side block
            radialSideArcZ (float): Z coordinate of the arch at the edges of the side block

        Returns:
            list: List of strings containing the blockMeshDict entry
        """
        
        edgeDefinitionSideBlock = []
        
        arcEdgeSideBlock1 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][0]
            )
        arcEdgeSideBlock2 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][1]
            )
        
        if slicePlane == "xy":
            radialSideArcZ1 = arcEdgeSideBlock1.start.coordinates()[2]
            radialSideArcZ2 = arcEdgeSideBlock2.start.coordinates()[2]
            
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX,
                            radialSideArcY,
                            radialSideArcZ1
                        )
                    )
                )
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock2.arc(
                        (
                            radialSideArcX,
                            radialSideArcY,
                            radialSideArcZ2
                        )
                    )
                )
            
        elif slicePlane == "yz":
            radialSideArcX1 = arcEdgeSideBlock1.start.coordinates()[0]
            radialSideArcX2 = arcEdgeSideBlock2.start.coordinates()[0]
            
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX1,
                            radialSideArcY,
                            radialSideArcZ
                        )
                    )
                )
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock2.arc(
                        (
                            radialSideArcX2,
                            radialSideArcY,
                            radialSideArcZ
                        )
                    )
                )
            
        elif slicePlane == "zx":
            radialSideArcY1 = arcEdgeSideBlock1.start.coordinates()[1]
            radialSideArcY2 = arcEdgeSideBlock2.start.coordinates()[1]
            
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX,
                            radialSideArcY1,
                            radialSideArcZ
                        )
                    )
                )
            edgeDefinitionSideBlock.append(
                    arcEdgeSideBlock2.arc(
                        (
                            radialSideArcX,
                            radialSideArcY2,
                            radialSideArcZ
                        )
                    )
                )
        
        return edgeDefinitionSideBlock
        
    
    def check_block_condition_for_making_disc(
            self,
            slicePlane,
            startingBlock,
            endBlock,
        ) -> bool:
        """
        Check the block selections if a disc can be created

        Args:
            slicePlane (str): Name of the slice plane
            startingBlock (Block): Selected starting block (diagonally left-bottom) 
            endBlock (Block): Selected end block (diagonally top-right) 

        Returns:
            bool: True/false if the black selections were valid
        """
        
        axisIndex1 = slicePlaneAxisIndex[slicePlane]["index1"]
        axisIndex2 = slicePlaneAxisIndex[slicePlane]["index2"]
        
        blockCheckCondition1 = (startingBlock.multiBlockIndex[axisIndex1]
                                < endBlock.multiBlockIndex[axisIndex1])
        
        blockCheckCondition2 = (startingBlock.multiBlockIndex[axisIndex2]
                                < endBlock.multiBlockIndex[axisIndex2])
        
        if blockCheckCondition1 and blockCheckCondition2:
            return True
        else:
            return False
    
    def make_quadrant(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
            slicePlane: str,
            blockConditionCheckNeeded: bool = True
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
        
        edgeDefinitionToSend = []
        
        centerBlock = self.blocks[startblockId]
        cornerBlock = self.blocks[endblockId]
        
        axisIndex1 = slicePlaneAxisIndex[slicePlane]["index1"]
        axisIndex2 = slicePlaneAxisIndex[slicePlane]["index2"]
        
        if blockConditionCheckNeeded:
            isBlockConditionValid = self.check_block_condition_for_making_disc(
                    slicePlane,
                    centerBlock,
                    cornerBlock,
                )
        else:
            isBlockConditionValid = True
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        
        quadrantNumber = self.get_quadrant_number(
                centerBlock.multiBlockIndex[axisIndex1],
                centerBlock.multiBlockIndex[axisIndex2],
                cornerBlock.multiBlockIndex[axisIndex1],
                cornerBlock.multiBlockIndex[axisIndex2],
            )
        
        ### Get necessary information to create the quadrant
        (
            topBlock,
            sideBlock,
            collapseEdgeDirection,
            axisEdgeDirection,
            arcEdgeDirection
        ) = self.get_quadrant_block_details(
                centerBlock,
                slicePlane,
                quadrantNumber,
            ).values()
        
        cornerBlock.isActive = False
        
        topBlockCollapseEdge = topBlock.find_edge(
                collapseEdgeDirection
            )
        sideBlockCollapseEdge = sideBlock.find_edge(
                collapseEdgeDirection
            )
        centerBlockAxisEdge = centerBlock.find_edge(
                axisEdgeDirection
            )
        
        ### Calculating "Delta" for the collapsed edges
        (
            thetaCorner,
            thetaSideArc,
            thetaTopArc
        ) = self.get_angles_for_quadrant(quadrantNumber)
        
        quadrantCenter = centerBlockAxisEdge.start.coordinates()
        
        (
            radialCornerX,
            radialCornerY,
            radialCornerZ,
            radialTopArcX,
            radialTopArcY,
            radialTopArcZ,
            radialSideArcX,
            radialSideArcY,
            radialSideArcZ
        ) = self.get_quadrant_arc_coordinates(
                slicePlane,
                radius,
                quadrantCenter,
                thetaCorner,
                thetaSideArc,
                thetaTopArc,
            )
        
        (
            deltaX,
            deltaY,
            deltaZ
        ) = self.get_quadrant_collapsed_edge_delta(
                slicePlane,
                sideBlockCollapseEdge,
                radialCornerX,
                radialCornerY,
                radialCornerZ,
            )
        
        ### Move-Collapse for Quadrant
        topBlockCollapseEdge.move_collapse(
                [deltaX, deltaY, deltaZ],
                sideBlockCollapseEdge
            )
        
        ## moving the Top-Right edge of the center bloc
        commonEdge = [
                x for x in centerBlock.edges if (x in topBlock.edges and
                                                    x in sideBlock.edges)
            ]
        
        if not bool(commonEdge):
            raise ValueError("Common edge can not be found among the blocks of the quadrant")
        else:
            centerBlockInnerCorner = commonEdge[0]
        
        compressionFactor = 0.20
        
        self.reshape_quadrant_center_block(
                slicePlane,
                radius,
                quadrantNumber,
                compressionFactor,
                centerBlockInnerCorner
            )
        
        ### Adding arc to the edges
        
        ### Top Block
        edgeDefinitionToSend.extend(
                self.add_quadrant_arc_top_block(
                    slicePlane,
                    topBlock,
                    arcEdgeDirection,
                    radialTopArcX,
                    radialTopArcY,
                    radialTopArcZ
                )
            )
        
        ### Side Block
        edgeDefinitionToSend.extend(
                self.add_quadrant_arc_side_block(
                    slicePlane,
                    sideBlock,
                    arcEdgeDirection,
                    radialSideArcX,
                    radialSideArcY,
                    radialSideArcZ
                )
            )
        
        return edgeDefinitionToSend
    
    def make_semicircle(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
            slicePlane: str,
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
        
        nQuadrant = 2
        
        edgeDefinitionToSend = []
        
        startingBlock = self.blocks[startblockId]
        endBlock = self.blocks[endblockId]
        
        startingBlockIndex = startingBlock.multiBlockIndex
        
        isBlockConditionValid = self.check_block_condition_for_making_disc(
                slicePlane,
                startingBlock,
                endBlock,
            )
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        else:
            blockConditionCheckNeeded = False
        
        centerBlock = []
        cornerBlock = []
        
        
        ### Quadrant - 1
        #---------------------------------------
        cornerBlock.append(endBlock)
        
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 2
                            )
                        )
                )
        
        
        ### Quadrant - 2
        #---------------------------------------
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        for i in range(nQuadrant):
            edgeDefinitionToSend.extend(
                self.make_quadrant(
                    centerBlock[i].id,
                    cornerBlock[i].id,
                    radius,
                    slicePlane,
                    blockConditionCheckNeeded
                )
            )
        return edgeDefinitionToSend
    
    def make_circle(
            self,
            startblockId: int,
            endblockId: int,
            radius: float,
            slicePlane: str,
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
        
        nQuadrant = 4
        
        edgeDefinitionToSend = []
        
        startingBlock = self.blocks[startblockId]
        endBlock = self.blocks[endblockId]
        
        startingBlockIndex = startingBlock.multiBlockIndex
        
        isBlockConditionValid = self.check_block_condition_for_making_disc(
                slicePlane,
                startingBlock,
                endBlock,
            )
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        else:
            blockConditionCheckNeeded = False
        
        centerBlock = []
        cornerBlock = []
        
        
        ### Quadrant - 1
        #---------------------------------------
        cornerBlock.append(endBlock)
        
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2] + 2
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 2
                            )
                        )
                )
        
        
        ### Quadrant - 2
        #---------------------------------------
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 3,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2] + 2
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 3
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 3,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        
        
        ### Quadrant - 3
        #---------------------------------------
        cornerBlock.append(startingBlock)
        
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2] + 1
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
        
        
        ### Quadrant - 4
        #---------------------------------------
        if slicePlane == "xy":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 3,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 3,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 2
                            )
                        )
                )
            cornerBlock.append(
                    self.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 3
                            )
                        )
                )
        
        for i in range(nQuadrant):
            edgeDefinitionToSend.extend(
                self.make_quadrant(
                    centerBlock[i].id,
                    cornerBlock[i].id,
                    radius,
                    slicePlane,
                    blockConditionCheckNeeded
                )
            )
        
        return edgeDefinitionToSend
        
            





