
#---------------------------------------
### Parameter Initialization ###
#---------------------------------------
vertexEdit = {}
edgeEdit = {}
faceEdit = {}
blockEdit = {}
multiBLock = {}
boundary = {}


"""
---------------------------------------
Accepted Directions Labels
----------------------------------------
    - front
    - back
    - left
    - right
    - bottom
    - top
---------------------------------------
Available Edit Types
---------------------------------------
VERTEX
    - move
    - collapse

EDGE
    - make edge an arc
    - make edge a spline
---------------------------------------
Define boundary/patch
---------------------------------------
"""

#---------------------------------------
### VERTEX - EDIT ###
#---------------------------------------



#---------------------------------------
### EDGE - EDIT ###
#---------------------------------------


edgeEdit[0] = {
    "edit-type" : "move-collapse",
    
    "edge":{
        "block-id" : 2,
        "position" : ["top", "right"],
        },
    
    "target-edge" : {
        "block-id" : 1,
        "position" : ["top", "right"],
    },
    
    ### Delta for the "target-edge"
    "delta" : [-0.2929, 0.2929, 0.0],
}


edgeEdit[1] = {
    "edit-type" : "make-arc",
    "method" : "arc-point",
    
    "edge":{
        "block-id" : 2,
        "position" : ["back", "top"],
        },
    
    "arc-point" : [1.25, 0.25, 0.0],
}


edgeEdit[2] = {
    "edit-type" : "make-arc",
    "method" : "arc-point",
    
    "edge":{
        "block-id" : 2,
        "position" : ["front", "top"],
        },
    
    "arc-point" : [1.25, 0.25, 0.2],
}

edgeEdit[3] = {
    "edit-type" : "make-arc",
    "method" : "center-radius",
    
    "edge":{
        "block-id" : 1,
        "position" : ["back", "right"],
        },
    
    "center" : [0.0, 0.0, 0.0],
    "angle" : 22.5,
    "radius" : 1.0,
}

edgeEdit[4] = {
    "edit-type" : "make-arc",
    "method" : "center-radius",
    
    "edge":{
        "block-id" : 1,
        "position" : ["front", "right"],
        },
    
    "center" : [0.0, 0.0, 0.2],
    "angle" : 22.5,
    "radius" : 1.0,
}

# # edgeEdit[5] = {
# #     "edit-type" : "make-arc",
# #     "method" : "center-radius",
    
# #     "edge":{
# #         "block-id" : 3,
# #         "position" : ["front", "right"],
# #         },
    
# #     "center" : [0.50, 0.75, 0.2],
# #     "angle" : 45,
# #     "radius" : 0.75,
# # }



#---------------------------------------
### BOUNDARY/PATCH ###
#---------------------------------------





#---------------------------------------

if __name__ == "__main__":
    """
    Raise an error is the script is being executed.
    This file is intended to be a module for import
    """
    
    raise RuntimeError("This file is not intended to run standalone")

#---------------------------------------
