
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
