from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from .block import *
from .face import *
from .slice import *

import numpy as np


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
            boundingBox: Bounding box of the multi-block mesh region
            splitPlanes: Planes at which the bounding box will be split
            gridSpacing: Grid spacing for the blocks
            hex2exclude: Ids of the block/hex to exclude in the dictionary to modify the multi-block mesh region
        """
        self._boundingBox = boundingBox
        self._splitPlanes = splitPlanes
        self._gridSpacing = gridSpacing
        self._hex2exclude = hex2exclude
                
        self._dx = self._gridSpacing["x"]
        self._dy = self._gridSpacing["y"]
        self._dz = self._gridSpacing["z"]
        
        self.xVertices = []
        self.yVertices = []
        self.zVertices = []
        
        self.vertices = OrderedDict()
        self.blocks = OrderedDict()
        self.slices = OrderedDict()
        # self.edges = []
    
    ### MultiBlock - bounding box
    @property
    def boundingBox(self):
        return self._boundingBox
    
    @boundingBox.setter
    def boundingBox(self, value: Dict):
        self._boundingBox = value
    
    ### MultiBlock - split planes
    @property
    def splitPlanes(self):
        return self._splitPlanes
    
    @splitPlanes.setter
    def splitPlanes(self, value: List[float]):
        self._splitPlanes = value
    
    ### MultiBlock - grid spacing
    @property
    def gridSpacing(self):
        return self._gridSpacing
    
    @gridSpacing.setter
    def gridSpacing(self, value: Dict):
        self._gridSpacing = value
                
        self._dx = self._gridSpacing["x"]
        self._dy = self._gridSpacing["y"]
        self._dz = self._gridSpacing["z"]
    
    def split_locations(self) -> None:
        """
        Organize and the store the split plane 
        locations along x, y, z directions
        """
        
        xSplitCoordinate = sorted(self.splitPlanes["x"])
        ySplitCoordinate = sorted(self.splitPlanes["y"])
        zSplitCoordinate = sorted(self.splitPlanes["z"])
        
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
        return self.nBlock
    
    def _define_block_point_order(
            self,
            zBack: int, 
            zFront: int,
            yBottom: int,
            yTop: int,
            ix: int
        ) -> tuple:
        """ Define and arrange vertices needed to define a block. """
        
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
            pointBackBottomLeft: int,
            pointBackBottomRight: int,
            pointBackTopRight: int,
            pointBackTopLeft: int,
            pointFrontBottomLeft: int,
            pointFrontBottomRight: int,
            pointFrontTopRight: int,
            pointFrontTopLeft: int
        ) -> Dict:
        """ Define block faces for a given block id. """
        
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
            blockVertexIds: tuple,
            blockVertexCoordinates: Dict
        ) -> None:
        """ Define block for a given block id. """
        
        grading = {
            "x" : 1,
            "y" : 1,
            "z" : 1,
        }
        
        faces = self._define_face(
                hexCount,
                *blockVertexIds
            )
        
        self.blocks[hexCount] = Block(
                                        hexCount,
                                        blockIndex,
                                        blockVertexIds,
                                        blockVertexCoordinates,
                                        faces,
                                        self._gridSpacing,
                                        grading
                                    )
        self.blocks[hexCount].get_edges()
    
    def create_vertex_group(self):
        """ Calculated vertex location, create groups/dicts """
        
        vertexCount = 0
        
        # self.vertexCount = 0
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
                self.vertexGroupDict[zIndex][yIndex] = []
                
                for i in range(self.nBlock["x"] + 1):
                    self.vertices[vertexCount] = (self.xVertices[i], self.yVertices[j], self.zVertices[k])
                    self.xSplitIndex.append(self.xVertices[i])
                    self.vertexGroupDict[zIndex][yIndex].append(vertexCount)
                    vertexCount += 1
    
    
    def create_blocks(self):
        """ Creates a dictionary to contain all the block/hex definitions """
        
        blockVertexCoordinates = {}
        hexCount = 0
        
        for iz in range(self.nBlock["z"]):
            zBack = self.zSplitIndex[iz]
            zFront = self.zSplitIndex[iz + 1]
            
            for iy in range(self.nBlock["y"]):
                yBottom = self.ySplitIndex[iy]
                yTop = self.ySplitIndex[iy + 1]
                
                for ix in range(self.nBlock["x"]):
                    if hexCount in self._hex2exclude:
                        pass
                    else:
                        blockVertexIds = self._define_block_point_order(
                                                zBack, 
                                                zFront,
                                                yBottom,
                                                yTop,
                                                ix
                                            )
                        blockIndex = "x-" + str(ix) + "_y-" + str(iy) + "_z-" + str(iz)
                        
                        for iv in blockVertexIds:
                            blockVertexCoordinates[iv] = self.vertices[iv]
                        
                        self._define_block(
                                hexCount,
                                blockIndex,
                                blockVertexIds,
                                blockVertexCoordinates
                            )
                        
                        hexCount += 1
        
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
        # for i in range(mb.nBlock["z"]):
        #     print(blockArray[i, :, :])
        
        # print("y-slices")
        # for i in range(mb.nBlock["x"]):
        #     print(blockArray[:, :, i])
        
        # print("z-slices")
        # for i in range(mb.nBlock["y"]):
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
        
        





