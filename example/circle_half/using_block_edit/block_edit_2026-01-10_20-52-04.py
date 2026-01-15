

vertexEdit = {}
edgeEdit = {}
blockEdit = {}
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

### Making semi-circle with block-edit
blockEdit[1] = {
    ### Block ID
    "starting-block-id" : 0,
    "ending-block-id" : 7,
    
    ### Type of edge edit
    "edit-type" : "make-semicircle",
    
    ### Radius of the quadrant
    "radius" : 1.0,
    
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
