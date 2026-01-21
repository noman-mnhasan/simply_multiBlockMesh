
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


vertexEdit[0] = {
    "edit-type" : "scale",
    "id":8,
    "ratio" : 2.0,
    "reference" : [1.0, 1.0, 0.05]
}

vertexEdit[1] = {
    "edit-type" : "scale",
    "id":17,
    "ratio" : 2.0,
    "reference" : [1.0, 1.0, 0.05]
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
