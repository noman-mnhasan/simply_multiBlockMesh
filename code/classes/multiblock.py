
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
        """ """
        
        # hl()
        # print(f"self.slices['xy'] : {self.slices['xy']}")
        # print(f"self.slices['yz'] : {self.slices['yz']}")
        # print(f"self.slices['zx'] : {self.slices['zx']}")
        # exit(-1)
        
        xIndexCount = 0
        yIndexCount = 0
        zIndexCount = 0
        
        hl()
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
        
        ### Converting the nested defaultdict to standard dictionary
        for k,v in blockGrid.items():
            blockGrid[k] = dict(v)
            
        self.blockGrid = dict(blockGrid)
    
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
        """_summary_

        Args:
            multiblockIndex1Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Center (int): Axis index for center block. 0 for x, 1 for y, 2 for z
            multiblockIndex1Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z
            multiblockIndex2Corner (int): Axis index for corner block. 0 for x, 1 for y, 2 for z

        Returns:
            int: _description_
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
    
    def get_quadrant_block_details(
            self,
            centerBlock,
            slicePlane,
            quadrantNumber,
        ) -> dict:
        
        quadrantInfo = {}
        
        ix, iy, iz = centerBlock.multiBlockIndex
        
        # hl()
        # print(f"Quadrant number : {quadrantNumber}")
        # exit(-1)
        
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
        
        if slicePlane == "xy":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + topShift,
                        iz
                    )
                )
            
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix + sideShift,
                        iy,
                        iz
                    )
                )
            
            if quadrantNumber == 1:
                collapseEdgeDirection = ["top", "right"]
                axisEdgeDirection = ["bottom", "left"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["top", "front"],
                                ["top", "back"]
                            ],
                        "side-block" : [
                                ["right", "front"],
                                ["right", "back"]
                            ],
                    }
            if quadrantNumber == 2:
                collapseEdgeDirection = ["top", "left"]
                axisEdgeDirection = ["bottom", "right"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["top", "front"],
                                ["top", "back"]
                            ],
                        "side-block" : [
                                ["left", "front"],
                                ["left", "back"]
                            ],
                    }
            if quadrantNumber == 3:
                collapseEdgeDirection = ["bottom", "left"]
                axisEdgeDirection = ["top", "right"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["bottom", "front"],
                                ["bottom", "back"]
                            ],
                        "side-block" : [
                                ["left", "front"],
                                ["left", "back"]
                            ],
                    }
            if quadrantNumber == 4:
                collapseEdgeDirection = ["bottom", "right"]
                axisEdgeDirection = ["top", "left"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["bottom", "front"],
                                ["bottom", "back"]
                            ],
                        "side-block" : [
                                ["right", "front"],
                                ["right", "back"]
                            ],
                    }
        
        elif slicePlane == "yz":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy,
                        iz + topShift
                    )
                )
            
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + sideShift,
                        iz
                    )
                )
            
            if quadrantNumber == 1:
                collapseEdgeDirection = ["top", "front"]
                axisEdgeDirection = ["bottom", "back"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["front", "right"],
                                ["front", "left"]
                            ],
                        "side-block" : [
                                ["top", "right"],
                                ["top", "left"]
                            ],
                    }
            if quadrantNumber == 2:
                collapseEdgeDirection = ["bottom", "front"]
                axisEdgeDirection = ["top", "back"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["front", "right"],
                                ["front", "left"]
                            ],
                        "side-block" : [
                                ["bottom", "right"],
                                ["bottom", "left"]
                            ],
                    }
            if quadrantNumber == 3:
                collapseEdgeDirection = ["bottom", "back"]
                axisEdgeDirection = ["top", "front"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["back", "right"],
                                ["back", "left"]
                            ],
                        "side-block" : [
                                ["bottom", "right"],
                                ["bottom", "left"]
                            ],
                    }
            if quadrantNumber == 4:
                collapseEdgeDirection = ["top", "back"]
                axisEdgeDirection = ["bottom", "front"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["back", "right"],
                                ["back", "left"]
                            ],
                        "side-block" : [
                                ["top", "right"],
                                ["top", "left"]
                            ],
                    }
        
        elif slicePlane == "zx":
            topBlock = self.get_block_with_multiblock_index(
                    (
                        ix + topShift,
                        iy,
                        iz
                    )
                )
            sideBlock = self.get_block_with_multiblock_index(
                    (
                        ix,
                        iy,
                        iz + sideShift
                    )
                )
            
            if quadrantNumber == 1:
                collapseEdgeDirection = ["front", "right"]
                axisEdgeDirection = ["back", "left"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["right", "top"],
                                ["right", "bottom"]
                            ],
                        "side-block" : [
                                ["front", "top"],
                                ["front", "bottom"]
                            ],
                    }
            if quadrantNumber == 2:
                collapseEdgeDirection = ["back", "right"]
                axisEdgeDirection = ["front", "left"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["right", "top"],
                                ["right", "bottom"]
                            ],
                        "side-block" : [
                                ["back", "top"],
                                ["back", "bottom"]
                            ],
                    }
            if quadrantNumber == 3:
                collapseEdgeDirection = ["back", "left"]
                axisEdgeDirection = ["front", "right"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["left", "top"],
                                ["left", "bottom"]
                            ],
                        "side-block" : [
                                ["back", "top"],
                                ["back", "bottom"]
                            ],
                    }
            if quadrantNumber == 4:
                collapseEdgeDirection = ["front", "left"]
                axisEdgeDirection = ["back", "right"]
                arcEdgeDirection = {
                        "top-block" : [
                                ["left", "top"],
                                ["left", "bottom"]
                            ],
                        "side-block" : [
                                ["front", "top"],
                                ["front", "bottom"]
                            ],
                    }
        # hl()
        # print(f"Center block : {centerBlock.multiblock_index()}")
        # print(f"Top block    : {topBlock.multiblock_index()}")
        # print(f"Side block   : {sideBlock.multiblock_index()}")
        # exit(-1)
                
        quadrantInfo["top-block"] = topBlock
        quadrantInfo["side-block"] = sideBlock
        quadrantInfo["collapse-edge-direction"] = collapseEdgeDirection
        quadrantInfo["axis-edge-direction"] = axisEdgeDirection
        quadrantInfo["arc-edge-direction"] = arcEdgeDirection
        
        return quadrantInfo
    
    
    ### TOO LONG - NEED TO SIMPLIFY ###
    
    def make_quadrant(
            self,
            viewFace: str,
            startblockId: int,
            endblockId: int,
            radius: float,
            slicePlane: str,
            sliceIndex : int
        ) -> list:
        """  """
        
        edgeDefinitionToSend = []
        
        centerBlock = self.blocks[startblockId]
        cornerBlock = self.blocks[endblockId]
        
        if slicePlane == "xy":
            axisIndex1 = 0    ### x-axis
            axisIndex2 = 1    ### y-axis
        elif slicePlane == "yz":
            axisIndex1 = 1    ### y-axis
            axisIndex2 = 2    ### z-axis
        elif slicePlane == "zx":
            axisIndex1 = 2    ### z-axis
            axisIndex2 = 0    ### x-axis
            
        # axisIndex1 = self.get_axis_index(slicePlane[0])
        # axisIndex2 = self.get_axis_index(slicePlane[1])
        
        quadrantNumber = self.get_quadrant_number(
                centerBlock.multiBlockIndex[axisIndex1],
                centerBlock.multiBlockIndex[axisIndex2],
                cornerBlock.multiBlockIndex[axisIndex1],
                cornerBlock.multiBlockIndex[axisIndex2],
            )
        
        # hl()
        # print(f"Center block - ID  : {startblockId}")
        # print(f"Corner block - ID  : {endblockId}")
        # print(f"Center block       : {centerBlock}")
        # print(f"Corner block       : {cornerBlock}")
        # print(f"Axis index 1       : {axisIndex1}")
        # print(f"Axis index 2       : {axisIndex2}")
        # print(f"Slice plane        : {slicePlane}")
        # hl()
        # print(f"Center block index : {centerBlock.multiblock_index()}")
        # print(f"Corner block index : {cornerBlock.multiblock_index()}")
        # hl()
        # print(f"Center block - index 1 : {centerBlock.multiblock_index()[axisIndex1]}")
        # print(f"Center block - index 2 : {centerBlock.multiblock_index()[axisIndex2]}")
        # print(f"Corner block - index 1 : {cornerBlock.multiblock_index()[axisIndex1]}")
        # print(f"Corner block - index 2 : {cornerBlock.multiblock_index()[axisIndex2]}")
        # hl()
        # print(f"Quadrant number    : {quadrantNumber}")
        # exit(-1)
        
        # quadrantInfo = self.get_quadrant_block_details(
        #         centerBlock,
        #         # cornerBlock,
        #         slicePlane,
        #         # sliceIndex,
        #         quadrantNumber,
        #     )
        
        # topBlock = quadrantInfo["top-block"]
        # sideBlock = quadrantInfo["side-block"]
        # collapseEdge = quadrantInfo["collapse-edge"]
        # axisEdge = quadrantInfo["axis-edge"]
        # arcEdge = quadrantInfo["arc-edge"]
        
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
        
        sinThetaCorner = math.sin(math.radians(thetaCorner))
        cosThetaCorner = math.cos(math.radians(thetaCorner))
        
        sinThetaSideArc = math.sin(math.radians(thetaSideArc))
        cosThetaSideArc = math.cos(math.radians(thetaSideArc))
        
        sinThetaTopArc = math.sin(math.radians(thetaTopArc))
        cosThetaTopArc = math.cos(math.radians(thetaTopArc))
        
        quadrantCenter = centerBlockAxisEdge.start.coordinates()
        
        if slicePlane == "xy":
            radialCornerX = (radius * cosThetaCorner) + quadrantCenter[0]
            radialCornerY = (radius * sinThetaCorner) + quadrantCenter[1]
            
            deltaX = radialCornerX - sideBlockCollapseEdge.start.coordinates()[0]
            deltaY = radialCornerY - sideBlockCollapseEdge.start.coordinates()[1]
            deltaZ = 0
            
            radialTopArcX = (radius * cosThetaTopArc) + quadrantCenter[0]
            radialTopArcY = (radius * sinThetaTopArc) + quadrantCenter[1]
            
            radialSideArcX = (radius * cosThetaSideArc) + quadrantCenter[0]
            radialSideArcY = (radius * sinThetaSideArc) + quadrantCenter[1]
        
        elif slicePlane == "yz":
            radialCornerY = (radius * cosThetaCorner) + quadrantCenter[1]
            radialCornerZ = (radius * sinThetaCorner) + quadrantCenter[2]
            
            deltaX = 0
            deltaY = radialCornerY - sideBlockCollapseEdge.start.coordinates()[1]
            deltaZ = radialCornerZ - sideBlockCollapseEdge.start.coordinates()[2]
            
            radialTopArcY = (radius * cosThetaTopArc) + quadrantCenter[1]
            radialTopArcZ = (radius * sinThetaTopArc) + quadrantCenter[2]
            
            radialSideArcY = (radius * cosThetaSideArc) + quadrantCenter[1]
            radialSideArcZ = (radius * sinThetaSideArc) + quadrantCenter[2]
        
        elif slicePlane == "zx":
            radialCornerZ = (radius * cosThetaCorner) + quadrantCenter[2]
            radialCornerX = (radius * sinThetaCorner)+ quadrantCenter[0]
            
            deltaZ = radialCornerZ - sideBlockCollapseEdge.start.coordinates()[2]
            deltaY = 0
            deltaX = radialCornerX - sideBlockCollapseEdge.start.coordinates()[0]
            
            radialTopArcZ = (radius * cosThetaTopArc) + quadrantCenter[2]
            radialTopArcX = (radius * sinThetaTopArc) + quadrantCenter[0]
            
            radialSideArcZ = (radius * cosThetaSideArc) + quadrantCenter[2]
            radialSideArcX = (radius * sinThetaSideArc) + quadrantCenter[0]
        
        
        # hl()
        # print(f"Quadrant center  : {quadrantCenter}")
        # print(f"Corner angle     : {thetaCorner}")
        # print(f"Delta X, Delta Y : {deltaX}, {deltaY}")
        # print(f"Radian corner, X : {radialCornerX}")
        # print(f"Radian corner, Y : {radialCornerY}")
        # print(f"cos theta : {cosThetaCorner}")
        # exit(-1)
        
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
        
        # # hl()
        # # print(f"Common edge : {commonEdge}")
        # # exit(-1)
        
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
        
        compressionFactor = 0.20
        
        if slicePlane == "xy":
            deltaX = shiftFactor1stAxis * radius/2.0 * compressionFactor
            deltaY = shiftFactor2ndAxis * radius/2.0 * compressionFactor
            deltaZ = 0
        elif slicePlane == "yz":
            deltaY = shiftFactor1stAxis * radius * compressionFactor
            deltaZ = shiftFactor2ndAxis * radius * compressionFactor
            deltaX = 0
        elif slicePlane == "zx":
            deltaZ = shiftFactor1stAxis * radius * compressionFactor
            deltaX = shiftFactor2ndAxis * radius * compressionFactor
            deltaY = 0
        
        centerBlockInnerCorner.move([deltaX, deltaY, deltaZ])
        
        
        
        ### Adding arc to the edges
        
        ### Top Block
        arcEdgeTopBlock1 = topBlock.find_edge(
                arcEdgeDirection["top-block"][0]
            )
        arcEdgeTopBlock2 = topBlock.find_edge(
                arcEdgeDirection["top-block"][1]
            )
        
        if slicePlane == "xy":
            radialTopArcZ1 = arcEdgeTopBlock1.start.coordinates()[2]
            radialTopArcZ2 = arcEdgeTopBlock2.start.coordinates()[2]
        
            edgeDefinitionToSend.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX,
                            radialTopArcY,
                            radialTopArcZ1
                        )
                    )
                )
            edgeDefinitionToSend.append(
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
        
            edgeDefinitionToSend.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX1,
                            radialTopArcY,
                            radialTopArcZ
                        )
                    )
                )
            edgeDefinitionToSend.append(
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
        
            edgeDefinitionToSend.append(
                arcEdgeTopBlock1.arc(
                        (
                            radialTopArcX,
                            radialTopArcY1,
                            radialTopArcZ
                        )
                    )
                )
            edgeDefinitionToSend.append(
                arcEdgeTopBlock2.arc(
                        (
                            radialTopArcX,
                            radialTopArcY2,
                            radialTopArcZ
                        )
                    )
                )
        
        ### Side Block
        arcEdgeSideBlock1 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][0]
            )
        arcEdgeSideBlock2 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][1]
            )
        
        if slicePlane == "xy":
            radialSideArcZ1 = arcEdgeSideBlock1.start.coordinates()[2]
            radialSideArcZ2 = arcEdgeSideBlock2.start.coordinates()[2]
            
            edgeDefinitionToSend.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX,
                            radialSideArcY,
                            radialSideArcZ1
                        )
                    )
                )
            edgeDefinitionToSend.append(
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
            
            edgeDefinitionToSend.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX1,
                            radialSideArcY,
                            radialSideArcZ
                        )
                    )
                )
            edgeDefinitionToSend.append(
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
            
            edgeDefinitionToSend.append(
                    arcEdgeSideBlock1.arc(
                        (
                            radialSideArcX,
                            radialSideArcY1,
                            radialSideArcZ
                        )
                    )
                )
            edgeDefinitionToSend.append(
                    arcEdgeSideBlock2.arc(
                        (
                            radialSideArcX,
                            radialSideArcY2,
                            radialSideArcZ
                        )
                    )
                )
        
        return edgeDefinitionToSend
    
    def make_semicircle(self) -> None:
        """  """
        
        pass
    
    def make_circle(self) -> None:
        """  """
        
        pass
        
            





