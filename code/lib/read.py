

from typing import (
    List, 
    Dict,
)
import classes


#---------------------------------------
### Variables
#---------------------------------------

templateDirName = "input_template"
templateFilenameBlockEdit = "block_edit.py"

ofCaseTemplateDirname = "case_system_template"

quadrantEdgeRule = {
    "xy": {
            1 : {
                "collapse-edge-location" : ["top", "right"],
                "axis-edge-location" : ["bottom", "left"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["top", "front"],
                            ["top", "back"]
                        ],
                    "side-block" : [
                            ["right", "front"],
                            ["right", "back"]
                        ],
                }
            },
            2 : {
                "collapse-edge-location" : ["top", "left"],
                "axis-edge-location" : ["bottom", "right"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["top", "front"],
                            ["top", "back"]
                        ],
                    "side-block" : [
                            ["left", "front"],
                            ["left", "back"]
                        ],
                }
            },
            3 : {
                "collapse-edge-location" : ["bottom", "left"],
                "axis-edge-location" : ["top", "right"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["bottom", "front"],
                            ["bottom", "back"]
                        ],
                    "side-block" : [
                            ["left", "front"],
                            ["left", "back"]
                        ],
                }
            },
            4 : {
                "collapse-edge-location" : ["bottom", "right"],
                "axis-edge-location" : ["top", "left"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["bottom", "front"],
                            ["bottom", "back"]
                        ],
                    "side-block" : [
                            ["right", "front"],
                            ["right", "back"]
                        ],
                }
            },
        },
    "yz": {
            1 : {
                "collapse-edge-location" : ["top", "front"],
                "axis-edge-location" : ["bottom", "back"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["front", "right"],
                            ["front", "left"]
                        ],
                    "side-block" : [
                            ["top", "right"],
                            ["top", "left"]
                        ],
                }
            },
            2 : {
                "collapse-edge-location" : ["bottom", "front"],
                "axis-edge-location" : ["top", "back"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["front", "right"],
                            ["front", "left"]
                        ],
                    "side-block" : [
                            ["bottom", "right"],
                            ["bottom", "left"]
                        ],
                }
            },
            3 : {
                "collapse-edge-location" : ["bottom", "back"],
                "axis-edge-location" : ["top", "front"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["back", "right"],
                            ["back", "left"]
                        ],
                    "side-block" : [
                            ["bottom", "right"],
                            ["bottom", "left"]
                        ],
                }
            },
            4 : {
                "collapse-edge-location" : ["top", "back"],
                "axis-edge-location" : ["bottom", "front"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["back", "right"],
                            ["back", "left"]
                        ],
                    "side-block" : [
                            ["top", "right"],
                            ["top", "left"]
                        ],
                }
            },
        },
    "zx": {
            1 : {
                "collapse-edge-location" : ["front", "right"],
                "axis-edge-location" : ["back", "left"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["right", "top"],
                            ["right", "bottom"]
                        ],
                    "side-block" : [
                            ["front", "top"],
                            ["front", "bottom"]
                        ],
                }
            },
            2 : {
                "collapse-edge-location" : ["back", "right"],
                "axis-edge-location" : ["front", "left"],
                "arc-edge-location" : {
                        "top-block" : [
                                ["right", "top"],
                                ["right", "bottom"]
                            ],
                        "side-block" : [
                                ["back", "top"],
                                ["back", "bottom"]
                            ],
                }
            },
            3 : {
                "collapse-edge-location" : ["back", "left"],
                "axis-edge-location" : ["front", "right"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["left", "top"],
                            ["left", "bottom"]
                        ],
                    "side-block" : [
                            ["back", "top"],
                            ["back", "bottom"]
                        ],
                }
            },
            4 : {
                "collapse-edge-location" : ["front", "left"],
                "axis-edge-location" : ["back", "right"],
                "arc-edge-location" : {
                    "top-block" : [
                            ["left", "top"],
                            ["left", "bottom"]
                        ],
                    "side-block" : [
                            ["front", "top"],
                            ["front", "bottom"]
                        ],
                }
            },
        },
}

slicePlaneAxisIndex = {
    "xy" : {
        "index1" : 0,
        "index2" : 1
    },
    "yz" : {
        "index1" : 1,
        "index2" : 2
    },
    "zx" : {
        "index1" : 2,
        "index2" : 0
    }
}


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


