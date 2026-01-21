




from typing import (
    Dict,
    TypeVar,
)
from utility.udtypes import (
    AngleType,
    EdgeType,
    PointType,
)
from utility.define import indent
from utility import tool as t


EdgeT = TypeVar("EdgeT", bound = "Edge")

class EdgeFeature:
    """ A class containing the Edge operations/actions """
    
    def __init__(
        self,
        type: EdgeType,
        edge: EdgeT
    ):
        
        self._type = type
        self._edge = edge
    
    @property
    def edge(self) -> None:
        return self._edge
    
    def arc_from_center_and_radius(
            self,
            arcOrigin: PointType,
            angle: AngleType
        ) -> PointType:
        """
        Get arch point from a given point/coordinate and a distance/radius

        Args:
            arcOrigin (PointType): Location/coordinate of the arc center
            angle (AngleType): Value of the angle form the start of the edge

        Returns:
            PointType: Returns coordinates of the arc point
        """
        
        ### Set the surface normal for the plane containing these three points
        normalVector = t.surface_normal_from_tree_points(
                self.edge.start.coordinates(),
                self.edge.end.coordinates(),
                arcOrigin,
                normalize = False
            )
        
        arcPoint = t.point_rotation_coordinates(
                self.edge.start.coordinates(),
                arcOrigin,
                normalVector,
                angle
            )
        
        return arcPoint
    
    def make_arc(
            self,
            editInfo: Dict
        ) -> EdgeT:
        """
        make arc with a given edge

        Args:
            editInfo (Dict): Dictionary containing the arch formation details

        Returns:
            EdgeT: Returns the Edge for which the arc has been defined
        """
        
        t.check_coordinate(editInfo["arc-point"])
        
        if editInfo["method"] == "arc-point":
            arcPoint = editInfo["arc-point"]
            self.edge.definition = f"arc {self.edge.start.id} {self.edge.end.id} ({arcPoint[0]} {arcPoint[1]} {arcPoint[2]})"
        
        elif editInfo["method"] == "center-radius":
            arcPoint = self.arc_from_center_and_radius(
                    editInfo["center"],
                    editInfo["angle"]
                )
            self.edge.definition = f"arc {self.edge.start.id} {self.edge.end.id} ({arcPoint[0]} {arcPoint[1]} {arcPoint[2]})"
            
        self.edge.editPoints = tuple(arcPoint)
        
        return self.edge
    
    def make_spline(
            self,
            editInfo: Dict
        ) -> EdgeT:
        """
        make spline with a given edge

        Args:
            editInfo (Dict): Dictionary containing the arch formation details

        Returns:
            EdgeT: Returns the Edge for which the spline has been defined
        """
        
        splinePoints = editInfo["spline-point"]
        
        for ipoint in splinePoints:
            t.check_coordinate(ipoint)
        
        self.edge.definition = f"spline {self.edge.start.id} {self.edge.end.id}\n{indent}(\n"
        if editInfo["method"] == "spline-point":
            for ipoint in splinePoints:
                self.edge.definition += f"{indent*2}({ipoint[0]} {ipoint[1]} {ipoint[2]})\n"
            self.edge.definition += f"{indent})"
            
        self.edge._editPoints = tuple([tuple(j) for j in splinePoints])
        
        return self.edge









