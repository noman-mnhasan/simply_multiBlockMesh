


from typing import (
    TypeVar,
)
from utility.udtypes import (
    PointValueType
)
from utility import tool as t

FaceT = TypeVar("FaceT", bound = "Face")

class FaceAction:
    """ A class containing the Face operations/actions """
    
    def __init__(self, face: FaceT):
        
        self._face = face
        
    @property
    def face(self) -> FaceT:
        return self._face
    
    @face.setter
    def face(self, value: FaceT):
        
        if not isinstance(value, FaceT):
            raise TypeError("FaceAction.face must an instance of 'Face' class.")
        
        self._face = value
    
    def scale(
            self,
            ratio: PointValueType
        ) -> FaceT:
        """
        Scale a given face

        Args:
            ratio (PointValueType): Ratio of the scaling operation.

        Returns:
            FaceT: Returns the face which has been scaled.
        """
        
        center = t.center(self.face.vertices)
        
        for ivertex in self.face.vertices:
            coordinates = ivertex.coordinates()
            
            vx = coordinates[0]
            vy = coordinates[1]
            vz = coordinates[2]
            
            newVx = center[0] + (vx - center[0]) * ratio
            newVy = center[1] + (vy - center[1]) * ratio
            newVz = center[2] + (vz - center[2]) * ratio
            
            ivertex.x = float(newVx)
            ivertex.y = float(newVy)
            ivertex.z = float(newVz)
            
        return self.face