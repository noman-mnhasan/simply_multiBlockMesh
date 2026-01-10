

from typing import (
    List, 
    Dict,
)


#---------------------------------------
### Variables
#---------------------------------------

templateDirName = "input_template"
templateFilenameBlockEdit = "block_edit.py"

ofCaseTemplateDirname = "case_system_template"




#---------------------------------------
### Functions
#---------------------------------------

def is_vertex_coordinate_valid(coordinates) -> bool:
    """ Check if a given coordinate input is valid """
    
    if not isinstance(coordinates, (list, tuple)):
        print(f"(x, y, x) = {tuple(coordinates)}")
        raise ValueError("Coordinate must be a list or tuple type")
    else:
        if len(coordinates) != 3:
            print(f"(x, y, x) = {tuple(coordinates)}")
            raise ValueError("Coordinate must have three elements for x, y, z values.")
        else:
            if not all([isinstance(i, (int, float))] for i in coordinates):
                print(f"(x, y, x) = {tuple(coordinates)}")
                raise ValueError("Coordinate values for x, y, z must be an integer or a float.")


def get_block_edge_location(
        locationStringList: List[str]
    ) -> int:
    """  """
    
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
        
    # print(f"Edge location index : {edgeLocationIndex}")
    
    return edgeLocationIndex
    
    



