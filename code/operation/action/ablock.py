




from typing import (
    TypeVar,
)
from utility.udtypes import (
    PointValueType,
)


BlockT = TypeVar("BlockT", bound = "Block")

class BlockAction:
    """ A class containing the Block operations/actions """
    
    def __init__(
        self,
        block: BlockT
    ):
        
        self._block = block
    
    @property
    def block(self) -> BlockT:
        return self._block
    
    @block.setter
    def block(self, value: BlockT):
        
        if not isinstance(value, BlockT):
            raise TypeError("BlockAction.block must an instance of 'Block' class.")
        
        self._block = value
    
    def scale2d(
            self,
            scalingPlane: str,
            ratio: PointValueType
        ) -> BlockT:
        """
        Scale a given block long a plane

        Args:
            scalingPlane (str): The plane along which the given block to be scaled
            ratio (PointValueType): Ratio of the scaling operation

        Returns:
            BlockT: Returns the Block which has been scaled
        """
        
        vertices = self.block.vertices
        
        xCoordinates = []
        yCoordinates = []
        zCoordinates = []
        
        xCoordinates = [i.coordinates()[0] for i in vertices]
        yCoordinates = [i.coordinates()[1] for i in vertices]
        zCoordinates = [i.coordinates()[2] for i in vertices]
        
        meanX = sum(xCoordinates)/len(xCoordinates)
        meanY = sum(yCoordinates)/len(yCoordinates)
        meanZ = sum(zCoordinates)/len(zCoordinates)
        
        if scalingPlane == "xy":
            for ivertex in vertices:
                coordinates = ivertex.coordinates()
                
                vx = coordinates[0]
                vy = coordinates[1]
                vz = coordinates[2]
                
                newVx = meanX + (vx - meanX) * ratio
                newVy = meanY + (vy - meanY) * ratio
                newVz = vz
                
                ivertex.x = float(newVx)
                ivertex.y = float(newVy)
                ivertex.z = float(newVz)
        
        elif scalingPlane == "yz":
            for ivertex in vertices:
                coordinates = ivertex.coordinates()
                
                vx = coordinates[0]
                vy = coordinates[1]
                vz = coordinates[2]
                
                newVx = vx
                newVy = meanY + (vy - meanY) * ratio
                newVz = meanZ + (vz - meanZ) * ratio
                
                ivertex.x = float(newVx)
                ivertex.y = float(newVy)
                ivertex.z = float(newVz)
        
        elif scalingPlane == "zx":
            for ivertex in vertices:
                coordinates = ivertex.coordinates()
                
                vx = coordinates[0]
                vy = coordinates[1]
                vz = coordinates[2]
                
                newVx = meanX + (vx - meanX) * ratio
                newVy = vy
                newVz = meanZ + (vz - meanZ) * ratio
                
                ivertex.x = float(newVx)
                ivertex.y = float(newVy)
                ivertex.z = float(newVz)
        
        return self.block
    
    def scale3d(
            self,
            ratio: PointValueType
        ) -> BlockT:
        """
        Scale a given block

        Args:
            ratio (PointValueType): Ratio of the scaling operation

        Returns:
            BlockT: Returns the Block which has been scaled
        """
        
        vertices = self.block.vertices
        
        xCoordinates = []
        yCoordinates = []
        zCoordinates = []
        
        xCoordinates = [i.coordinates()[0] for i in vertices]
        yCoordinates = [i.coordinates()[1] for i in vertices]
        zCoordinates = [i.coordinates()[2] for i in vertices]
        
        meanX = sum(xCoordinates)/len(xCoordinates)
        meanY = sum(yCoordinates)/len(yCoordinates)
        meanZ = sum(zCoordinates)/len(zCoordinates)
        
        for ivertex in vertices:
            coordinates = ivertex.coordinates()
            
            vx = coordinates[0]
            vy = coordinates[1]
            vz = coordinates[2]
            
            newVx = meanX + (vx - meanX) * ratio
            newVy = meanY + (vy - meanY) * ratio
            newVz = meanZ + (vz - meanZ) * ratio
            
            ivertex.x = float(newVx)
            ivertex.y = float(newVy)
            ivertex.z = float(newVz)
        
        return self.block









