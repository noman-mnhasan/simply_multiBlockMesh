

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



#---------------------------------------
### EDGE - EDIT ###
#---------------------------------------

## Moving-collapsing edge
edgeEdit[1] = {
    ### Block ID
    "block-id" : 5,
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "left"],
    
    ### Type of edge edit
    "edit-type" : "move-collapse",
    
    ### Defining distance
    "delta" : [0.2929, 0.2071, 0.0],
    
    ### Target edge to collapse to
    "target-edge" : {
        ### Target edge id
        "block-id" : 0,
        
        ### Target edge position
        "edge-position" : ["top", "left"],
    }
}


### Moving-collapsing edge
edgeEdit[2] = {
    ### Block ID
    "block-id" : 6,
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "right"],
    
    ### Type of edge edit
    "edit-type" : "move-collapse",
    
    ### Defining distance
    "delta" : [-0.2929, 0.2071, 0.0],
    
    ### Target edge to collapse to
    "target-edge" : {
        ### Target edge id
        "block-id" : 3,
        
        ### Target edge position
        "edge-position" : ["top", "right"],
    }
}


### Making quarter arc
edgeEdit[3] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "left"],
    
    ### Defining points
    "arc-point" : [-0.9293, 0.3827, 0.0]
}


### Making quarter arc
edgeEdit[4] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "left"],
    
    ### Defining points
    "arc-point" : [-0.9293, 0.3827, 0.4]
}


### Making quarter arc
edgeEdit[5] = {
    ### Block ID
    "block-id" : 5,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "top"],
    
    ### Defining points
    "arc-point" : [-0.3827, 0.9293, 0.0]
}


### Making quarter arc
edgeEdit[6] = {
    ### Block ID
    "block-id" : 5,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "top"],
    
    ### Defining points
    "arc-point" : [-0.3827, 0.9293, 0.4]
}


### Making quarter arc
edgeEdit[7] = {
    ### Block ID
    "block-id" : 6,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "top"],
    
    ### Defining points
    "arc-point" : [0.3872, 0.9239, 0.0]
}


### Making quarter arc
edgeEdit[8] = {
    ### Block ID
    "block-id" : 6,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "top"],
    
    ### Defining points
    "arc-point" : [0.3872, 0.9239, 0.4]
}



### Making quarter arc
edgeEdit[9] = {
    ### Block ID
    "block-id" : 3,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "right"],
    
    ### Defining points
    "arc-point" : [0.9239, 0.3827, 0.0]
}


### Making quarter arc
edgeEdit[10] = {
    ### Block ID
    "block-id" : 3,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "right"],
    
    ### Defining points
    "arc-point" : [0.9239, 0.3827, 0.4]
}


### Moving top-right edge inward for smoothing
edgeEdit[11] = {
    ### Block ID
    "block-id" : 1,
    
    ### Type of edge edit
    "edit-type" : "move",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["left", "top"],
    
    ### Defining points
    "delta" : [0.1, -0.1, 0.0]
}


### Moving top-right edge inward for smoothing
edgeEdit[12] = {
    ### Block ID
    "block-id" : 2,
    
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
