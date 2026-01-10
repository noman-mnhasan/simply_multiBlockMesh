from collections import OrderedDict
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
            blockVertices: tuple,
            blockVertexCoordinates: Dict
        ) -> None:
        """
        Define block for a given block id.

        Args:
            hexCount (int): Block/hex id.
            blockIndex (str): A string representing the x, y, z position of the block in the multi-block
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
                        pass
                    else:
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
    
    def make(self) -> None:
        """ Run the multi-block operations """
        
        self.split_locations()
        self.block_count()
        self.create_vertex_group()
        self.create_blocks()
        self.get_slices()
    
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
        
            





