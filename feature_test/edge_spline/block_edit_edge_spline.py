
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
    - move-collapse

EDGE
    - move
    - collapse
    - move-collapse
    - scale
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

edgeEdit[1] = {
    "edit-type" : "make-spline",
    "method" : "spline-point",
    
    "edge":{
        "block-id" : 3,
        "position" : ["back", "top"],
        },
    
    "spline-point" : [
            [0.6, 1.2, 0.0],
            [0.7, 1.5, 0.0],
            [0.8, 1.2, 0.0],
        ],
}

edgeEdit[2] = {
    "edit-type" : "make-spline",
    "method" : "spline-point",
    
    "edge":{
        "block-id" : 3,
        "position" : ["front", "top"],
        },
    
    "spline-point" : [
            [0.6, 1.2, 0.1],
            [0.7, 1.5, 0.1],
            [0.8, 1.2, 0.1],
        ],
}



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
