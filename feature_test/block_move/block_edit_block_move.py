
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


blockEdit[0] = {
    "edit-type" : "move",
    "block-id" : 3,
    "delta" : [0.4, 0.3, 0.2],
    
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
