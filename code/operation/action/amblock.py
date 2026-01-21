


import math

from typing import (
    TypeVar
)
from utility.udtypes import (
    PointValueType
)
from utility.define import (
    slicePlaneAxisIndex,
    quadrantEdgeRule,
    blockShiftCoefficient,
    angleForQuadrant,
    quadrantCompressionFactor,
)
from utility import tool as t

BlockT = TypeVar("BlockT", bound = "Block")
MultiblockT = TypeVar("MultiblockT", bound = "MultiBlock")

class MultiBlockAction:
    
    def __init__(self, multiblock: MultiblockT):
        
        self._multiblock = multiblock
        
    
    @property
    def multiblock(self) -> MultiblockT:
        return self._multiblock
    
    @multiblock.setter
    def multiblock(self, value: MultiblockT) -> None:
        
        self._multiblock = value
        
    
    def get_top_block_for_quadrant(
            self,
            slicePlane,
            centerBlockGridPosition,
            topShift
        ) -> BlockT:
        """
        Get the top-block in reference to the center-block (the block 
        that contains the axis of the quadrant) of the quadrant
        """
        
        ix, iy, iz = centerBlockGridPosition
        
        if slicePlane == "xy":
            topBlock = self.multiblock.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + topShift,
                        iz
                    )
                )
        
        elif slicePlane == "yz":
            topBlock = self.multiblock.get_block_with_multiblock_index(
                    (
                        ix,
                        iy,
                        iz + topShift
                    )
                )
        
        elif slicePlane == "zx":
            topBlock = self.multiblock.get_block_with_multiblock_index(
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
        ) -> BlockT:
        """
        Get the side-block in reference to the center-block (the block 
        that contains the axis of the quadrant) of the quadrant
        """
        
        ix, iy, iz = centerBlockGridPosition
        
        if slicePlane == "xy":
            sideBlock = self.multiblock.get_block_with_multiblock_index(
                    (
                        ix + sideShift,
                        iy,
                        iz
                    )
                )
        
        elif slicePlane == "yz":
            sideBlock = self.multiblock.get_block_with_multiblock_index(
                    (
                        ix,
                        iy + sideShift,
                        iz
                    )
                )
        
        elif slicePlane == "zx":
            sideBlock = self.multiblock.get_block_with_multiblock_index(
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
        
        topShift, sideShift = blockShiftCoefficient[quadrantNumber].values()
        
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
        radialEdgeDirection = quadrantEdgeRule[slicePlane][quadrantNumber]["radial-edge-location"]
                
        quadrantInfo["top-block"] = topBlock
        quadrantInfo["side-block"] = sideBlock
        quadrantInfo["collapse-edge-direction"] = collapseEdgeDirection
        quadrantInfo["axis-edge-direction"] = axisEdgeDirection
        quadrantInfo["arc-edge-direction"] = arcEdgeDirection
        quadrantInfo["radial-edge-location"] = radialEdgeDirection
        
        return quadrantInfo
    
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
            quadrantCompressionFactor,
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
            centerBlockInnerEdgeDeltaX = shiftFactor1stAxis * radius/2.0 * quadrantCompressionFactor
            centerBlockInnerEdgeDeltaY = shiftFactor2ndAxis * radius/2.0 * quadrantCompressionFactor
            centerBlockInnerEdgeDeltaZ = 0
        elif slicePlane == "yz":
            centerBlockInnerEdgeDeltaY = shiftFactor1stAxis * radius/2.0 * quadrantCompressionFactor
            centerBlockInnerEdgeDeltaZ = shiftFactor2ndAxis * radius/2.0 * quadrantCompressionFactor
            centerBlockInnerEdgeDeltaX = 0
        elif slicePlane == "zx":
            centerBlockInnerEdgeDeltaZ = shiftFactor1stAxis * radius/2.0 * quadrantCompressionFactor
            centerBlockInnerEdgeDeltaX = shiftFactor2ndAxis * radius/2.0 * quadrantCompressionFactor
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
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX, radialTopArcY, radialTopArcZ1],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX, radialTopArcY, radialTopArcZ2],
            }
            
            arcEdgeTopBlock1.arc(editInfoS1)
            arcEdgeTopBlock2.arc(editInfoS2)
            
        elif slicePlane == "yz":
            radialTopArcX1 = arcEdgeTopBlock1.start.coordinates()[0]
            radialTopArcX2 = arcEdgeTopBlock2.start.coordinates()[0]
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX1, radialTopArcY, radialTopArcZ],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX2, radialTopArcY, radialTopArcZ],
            }
            
            arcEdgeTopBlock1.arc(editInfoS1)
            arcEdgeTopBlock2.arc(editInfoS2)
            
        elif slicePlane == "zx":
            radialTopArcY1 = arcEdgeTopBlock1.start.coordinates()[1]
            radialTopArcY2 = arcEdgeTopBlock2.start.coordinates()[1]
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX, radialTopArcY1, radialTopArcZ],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialTopArcX, radialTopArcY2, radialTopArcZ],
            }
            
            arcEdgeTopBlock1.arc(editInfoS1)
            arcEdgeTopBlock2.arc(editInfoS2)
        
        return 
            
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
        
        arcEdgeSideBlock1 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][0]
            )
        arcEdgeSideBlock2 = sideBlock.find_edge(
                arcEdgeDirection["side-block"][1]
            )
        
        if slicePlane == "xy":
            radialSideArcZ1 = arcEdgeSideBlock1.start.coordinates()[2]
            radialSideArcZ2 = arcEdgeSideBlock2.start.coordinates()[2]
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX, radialSideArcY, radialSideArcZ1],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX, radialSideArcY, radialSideArcZ2],
            }
            
            arcEdgeSideBlock1.arc(editInfoS1)
            arcEdgeSideBlock2.arc(editInfoS2)
            
        elif slicePlane == "yz":
            radialSideArcX1 = arcEdgeSideBlock1.start.coordinates()[0]
            radialSideArcX2 = arcEdgeSideBlock2.start.coordinates()[0]
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX1, radialSideArcY, radialSideArcZ],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX2, radialSideArcY, radialSideArcZ],
            }
            
            arcEdgeSideBlock1.arc(editInfoS1)
            arcEdgeSideBlock2.arc(editInfoS2)
            
        elif slicePlane == "zx":
            radialSideArcY1 = arcEdgeSideBlock1.start.coordinates()[1]
            radialSideArcY2 = arcEdgeSideBlock2.start.coordinates()[1]
            
            editInfoS1 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX, radialSideArcY1, radialSideArcZ],
            }
            editInfoS2 = {
                "method" : "arc-point",
                "arc-point" : [radialSideArcX, radialSideArcY2, radialSideArcZ],
            }
            
            arcEdgeSideBlock1.arc(editInfoS1)
            arcEdgeSideBlock2.arc(editInfoS2)
        
        return 
        
    
    def check_quadrant_block_selection(
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
        
    def make_four_block_quadrant(
            self,
            centerBlock: BlockT,
            cornerBlock: BlockT,
            radius: PointValueType,
            blockConditionCheckNeeded: bool = True
        ) -> MultiblockT:
        
        slicePlane = t.slice_plane_from_block_pair(
                centerBlock,
                cornerBlock
            )
        axisIndex1 = slicePlaneAxisIndex[slicePlane]["index1"]
        axisIndex2 = slicePlaneAxisIndex[slicePlane]["index2"]
        
        if blockConditionCheckNeeded:
            isBlockConditionValid = self.check_quadrant_block_selection(
                    slicePlane,
                    centerBlock,
                    cornerBlock,
                )
        else:
            isBlockConditionValid = True
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        
        quadrantNumber = t.get_quadrant_number(
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
            arcEdgeDirection,
            radialEdgeDirection
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
        
        ### Move edges to the distance of the given radius
        topBlockRadialEdgeIndex = topBlock.get_block_edge_location(
                                radialEdgeDirection["top-block"]
                            )
        sideBlockRadialEdgeIndex = sideBlock.get_block_edge_location(
                                radialEdgeDirection["side-block"]
                            )
        topBlockRadialEdge = topBlock.edges[topBlockRadialEdgeIndex]
        sideBlockRadialEdge = sideBlock.edges[sideBlockRadialEdgeIndex]
        
        vertexPairForSettingRadius = [
                [centerBlockAxisEdge.start, topBlockRadialEdge.start],
                [centerBlockAxisEdge.end, topBlockRadialEdge.end],
                [centerBlockAxisEdge.start, sideBlockRadialEdge.start],
                [centerBlockAxisEdge.end, sideBlockRadialEdge.end],
            ]
        
        for [reference, ivertex] in vertexPairForSettingRadius:
            distance = t.points2distance(
                    reference.coordinates(),
                    ivertex.coordinates()
                )
            ratio = radius/float(distance)
            ivertex.scale(
                    ratio,
                    reference.coordinates()
                )
        
        
        ### Calculating "Delta" for the collapsed edges
        (
            thetaCorner,
            thetaSideArc,
            thetaTopArc
        ) = angleForQuadrant[quadrantNumber].values()
        
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
        
        self.reshape_quadrant_center_block(
                slicePlane,
                radius,
                quadrantNumber,
                quadrantCompressionFactor,
                centerBlockInnerCorner
            )
        
        ### Adding arc to the edges
        ### Top Block
        self.add_quadrant_arc_top_block(
            slicePlane,
            topBlock,
            arcEdgeDirection,
            radialTopArcX,
            radialTopArcY,
            radialTopArcZ
        )
        ### Side Block
        self.add_quadrant_arc_side_block(
            slicePlane,
            sideBlock,
            arcEdgeDirection,
            radialSideArcX,
            radialSideArcY,
            radialSideArcZ
        )
        
    def make_eight_block_semicircle(
            self,
            centerBlock: BlockT,
            cornerBlock: BlockT,
            radius: PointValueType,
            blockConditionCheckNeeded: bool = True
        ) -> MultiblockT:
        
        nQuadrant = 2
        
        slicePlane = t.slice_plane_from_block_pair(
                centerBlock,
                cornerBlock
            )
        
        startingBlockIndex = centerBlock.multiBlockIndex
        
        isBlockConditionValid = self.check_quadrant_block_selection(
                slicePlane,
                centerBlock,
                cornerBlock,
            )
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        else:
            blockConditionCheckNeeded = False
        
        centerBlocks = []
        cornerBlocks = []
        
        
        ### Quadrant - 1
        #---------------------------------------
        cornerBlocks.append(cornerBlock)
        
        if slicePlane == "xy":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
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
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        for i in range(nQuadrant):
            self.make_four_block_quadrant(
                centerBlocks[i],
                cornerBlocks[i],
                radius,
                blockConditionCheckNeeded
            )
        return
    
    def make_sixteen_block_circle(
            self,
            centerBlock: BlockT,
            cornerBlock: BlockT,
            radius: PointValueType,
            blockConditionCheckNeeded: bool = True
        ) -> MultiblockT:
        
        nQuadrant = 4
        
        slicePlane = t.slice_plane_from_block_pair(
                centerBlock,
                cornerBlock
            )
        
        startingBlockIndex = centerBlock.multiBlockIndex
        
        isBlockConditionValid = self.check_quadrant_block_selection(
                slicePlane,
                centerBlock,
                cornerBlock,
            )
        
        if not isBlockConditionValid:
            raise ValueError("Invalid block selection.\nCheck block selection for making circular section.")
        else:
            blockConditionCheckNeeded = False
        
        centerBlocks = []
        cornerBlocks = []
        
        
        ### Quadrant - 1
        #---------------------------------------
        cornerBlocks.append(cornerBlock)
        
        if slicePlane == "xy":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2] + 2
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
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
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 3,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2] + 2
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 3
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 3,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        
        
        ### Quadrant - 3
        #---------------------------------------
        cornerBlocks.append(centerBlock)
        
        if slicePlane == "xy":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2] + 1
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
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
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 2,
                                startingBlockIndex[1] + 1,
                                startingBlockIndex[2]
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 3,
                                startingBlockIndex[1],
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "yz":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 2,
                                startingBlockIndex[2] + 1
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1] + 3,
                                startingBlockIndex[2]
                            )
                        )
                )
        elif slicePlane == "zx":
            centerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0] + 1,
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 2
                            )
                        )
                )
            cornerBlocks.append(
                    self.multiblock.get_block_with_multiblock_index(
                            (
                                startingBlockIndex[0],
                                startingBlockIndex[1],
                                startingBlockIndex[2] + 3
                            )
                        )
                )
        
        for i in range(nQuadrant):
            self.make_four_block_quadrant(
                centerBlocks[i],
                cornerBlocks[i],
                radius,
                blockConditionCheckNeeded
            )
        
        return










