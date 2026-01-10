

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

### Sample entry - vertex - move
vertexEdit[1] = {
    ### Vertex ID
    "id" : 0, 
    
    ### Type of vertex edit
    "edit-type" : "move",
    
    ### Coordinate for new location
    "new-location" : [0.0, 0.0, 0.0]
}


### Sample entry - vertex - collapse
vertexEdit[2] = {
    ### Vertex ID
    "id" : 0, 
    
    ### Type of vertex edit
    "edit-type" : "collapse",
    
    ### Target vertex to collapse to
    "target-vertex" : 8
}


#---------------------------------------
### EDGE - EDIT ###
#---------------------------------------

### Sample entry - edge - make arc
edgeEdit[1] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "left"],
    
    ### Defining points
    "arc-point" : [0.0, 0.0, 0.0]
}


### Sample entry - edge - make spline
edgeEdit[2] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "make-spline",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "right"],
    
    ### Defining points
    "spline-points" : [
    		[0.0, 0.0, 0.0],
    		[0.0, 0.0, 0.0]
    	]
}


### Sample entry - edge - make polyline
edgeEdit[2] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "make-polyline",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "right"],
    
    ### Defining points
    "polyline-points" : [
    		[0.0, 0.0, 0.0],
    		[0.0, 0.0, 0.0]
    	]
}


### Sample entry - edge - move
edgeEdit[3] = {
    ### Block ID
    "block-id" : 0,
    
    ### Type of edge edit
    "edit-type" : "move",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "front"],
    
    ### Moving distance
    "delta" : [0.0 , 0.0, 0.0]
}



#---------------------------------------
### BOUNDARY/PATCH ###
#---------------------------------------

boundary[1] = {
    ### Boundary Name
    "name" : "dummy_inlet",
    
    ### Boundary type
    "type" : "inlet",
    
    ### Block faces to define boundary Condition
    "faces" : [
            [0, "left"],    ### [block-id, face-name]
            [1, "back"],    ### [block-id, face-name]
        ]
    
}

boundary[2] = {
    ### Boundary Name
    "name" : "dummy_outlet",
    
    ### Boundary type
    "type" : "outlet",
    
    ### Block faces to define boundary Condition
    "faces" : [
            [2, "right"],    ### [block-id, face-name]
        ]
}



#---------------------------------------

if __name__ == "__main__":
    """
    Raise an error is the script is being executed.
    This file is intended to be a module for import
    """
    
    raise RuntimeError("This file is not intended to run standalone")

#---------------------------------------
