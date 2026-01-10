

vertexEdit = {}
edgeEdit = {}
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


### Collapsing face 
###     Block - 1, Face - Top 
###     Block - 2, Face - right 
### Moving outer edge of the collapsed face 

vertexEdit[1] = {
    ### Vertex ID
    "id" : 5, 
    
    ### Type of vertex edit
    "edit-type" : "move-collapse",  
      
    ### Coordinate for new location
    "new-location" : [0.7071, 0.7071, 0.0],
    
    ### Target vertex to collapse to
    "target-vertex" : 7
}


vertexEdit[2] = {
    ### Vertex ID
    "id" : 14, 
    
    ### Type of vertex edit
    "edit-type" : "move-collapse",  
      
    ### Coordinate for new location
    "new-location" : [0.7071, 0.7071, 0.4],
    
    ### Target vertex to collapse to
    "target-vertex" : 16
}

### Moving-collapsing face - Complete


#---------------------------------------
### EDGE - EDIT ###
#---------------------------------------

### Making quarter arc
edgeEdit[1] = {
    ### Block ID
    "block-id" : 1,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "right"],
    
    ### Defining points
    "arc-point" : [0.9293, 0.3827, 0.0]
}


### Making quarter arc
edgeEdit[2] = {
    ### Block ID
    "block-id" : 1,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "right"],
    
    ### Defining points
    "arc-point" : [0.9293, 0.3827, 0.4]
}


### Making quarter arc
edgeEdit[3] = {
    ### Block ID
    "block-id" : 2,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "top"],
    
    ### Defining points
    "arc-point" : [0.2146, 0.9738, 0.0]
}


### Making quarter arc
edgeEdit[4] = {
    ### Block ID
    "block-id" : 2,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "top"],
    
    ### Defining points
    "arc-point" : [0.2146, 0.9738, 0.4]
}


### Moving top-right edge inward for smoothing
edgeEdit[5] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "move",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["right", "top"],
    
    ### Defining points
    "delta" : [-0.1, -0.1, 0.0]
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

