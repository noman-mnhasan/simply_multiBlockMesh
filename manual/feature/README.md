# Feature Manual

Feature manual for **Simply multiBLockMesh** (SimBloM).

To Use these feature to create the intended multi-block, the user need to add the feature/edit entries to the <u>feature edit input file</u> - **`block_edit_*.py`**. As the file extension says. The <u>feature edit input file</u> is a Python file. The user must know basic Python syntax and Python data structures (integer, float, string, list, dictionary)

[Back to manual home](../README.md)


## Table of Contents

- [Vertex Feature](#vertex-feature)
    - [Vertex Move](#vertex-move)
    - [Vertex Collapse](#vertex-collapse)
    - [Vertex Move-Collapse](#vertex-move-collapse)
- [Edge Feature](#edge-feature)
    - [Edge Move](#edge-move)
    - [Edge Collapse](#edge-collapse)
    - [Edge Move-Collapse](#edge-move-collapse)
    - [Edge - Make-arc](#edge---make-arc)
    - [Edge - Make-polyline](#edge---make-polyline)
    - [Edge - Make-polySpline](#edge---make-polyspline)
    - [Edge - Make-bSpline](#edge---make-bspline)
- [Block Feature](#block-feature)


<br>

> ### Vertex Feature

Vertex features with example

<br>

#### Vertex Move

To move `vertex 7` to `(0.1, 0.1, 0.1)` use the **vertex move** feature - 

<img src="../illustrations/vertex-move.png" alt="feature-vertex-move" width="100%" style="display : block; margin : auto;">

<br>

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other VERTEX operation


### Sample entry - vertex - move

vertexEdit[operationId] = {
    ### Vertex ID
    "id" : 7, 
    
    ### Type of vertex edit
    "edit-type" : "move",
    
    ### Coordinate for new location
    "new-location" : [0.6, 1.1, 0.0]
}

```

[Back to the top](#table-of-contents)

<br>

#### Vertex Collapse

To collapse `vertex 16` to `vertex 7` use the **vertex collapse** feature - 

<img src="../illustrations/vertex-collapse.png" alt="feature-vertex-collapse" width="100%" style="display : block; margin : auto;">

<br> 

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other VERTEX operation

### Sample entry - vertex - collapse

vertexEdit[operationId] = {
    ### Vertex ID
    "id" : 1, 
    
    ### Type of vertex edit
    "edit-type" : "collapse",
    
    ### Target vertex to collapse to
    "target-vertex" : 1
}

```

<br>

[Back to the top](#table-of-contents)

#### Vertex Move-Collapse

To collapse `vertex 16` to `vertex 7`  and then move the collapsed vertex to `(0.6, 1.1, 0.0)` use **vertex move** feature - 

<img src="../illustrations/vertex-move-collapse.png" alt="feature-vertex-collapse" width="100%" style="display : block; margin : auto;">

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other VERTEX operation

### Sample entry - vertex - move-collapse

vertexEdit[operationId] = {
    ### Vertex ID
    "id" : 16, 
    
    ### Type of vertex edit
    "edit-type" : "move-collapse",
    
    ### Coordinate for new location
    "new-location" : [0.6, 1.1, 0.0],
    
    ### Coordinate for new location
    "target-vertex" : 7
}

```

[Back to the top](#table-of-contents)

<br><br><br>

> ### Edge Feature

Edge features with example

<br>

#### Edge Move

To move `edge - "top-right" (block 0)` to a distance of `(delta-x, delta-y, delta-z) = (0.1, 0.1, 0.0)` use the **edge move** feature - 

<img src="../illustrations/edge-move.png" alt="feature-edge-move" width="100%" style="display : block; margin : auto;">

<br>

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other EDGE operation


### Sample entry - edge - move

edgeEdit[operationId] = {
    ### Block ID
    "block-id" : 0,

    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "right"],
    
    ### Type of edge edit
    "edit-type" : "move",
    
    ### moving distance in x, y, z directions
    "delta" : [0.1, 0.1, 0.0]
}

```

[Back to the top](#table-of-contents)

<br>

#### Edge Collapse

To collapse `edge - "top-right" (block 2)` to `edge - "top-right" (block 1)` use the **edge collapse** feature - 

<img src="../illustrations/edge-collapse.png" alt="feature-edge-collapse" width="100%" style="display : block; margin : auto;">

<br>

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other EDGE operation


### Sample entry - edge - collapse

edgeEdit[operationId] = {
    ### Block ID
    "block-id" : 2,

    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "right"],
    
    ### Type of edge edit
    "edit-type" : "collapse",
    
    ### Target edge to collapse to
    "target-edge" : {
        ### Target edge id
        "block-id" : 1,

        ### Target edge position
        "edge-position" : ["top", "right"],
    }
}

```

[Back to the top](#table-of-contents)

<br>

#### Edge Move-Collapse

To collapse `edge - top-right (block 2)` to `edge - top-right (block 1)` and then to move the **collapsed edge** to a distance of `(delta-x, delta-y, delta-z) = (-0.2929, 0.2929, 0.0)`use the **edge move-collapse** feature - 

<img src="../illustrations/edge-move-collapse.png" alt="feature-edge-move-collapse" width="100%" style="display : block; margin : auto;">

<br>

```Python

### operationId --> represents operation id.
### recommended to use an integer not assigned to any other EDGE operation


### Sample entry - edge - move-collapse

edgeEdit[operationId] = {
    ### Block ID
    "block-id" : 2,

    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["top", "right"],
    
    ### Type of edge edit
    "edit-type" : "move-collapse",
    
    ### moving distance in x, y, z directions
    "delta" : [-0.2929, 0.2929, 0.1],
    
    ### Target edge to collapse to
    "target-edge" : {
        ### Target edge id
        "block-id" : 1,

        ### Target edge position
        "edge-position" : ["top", "right"],
    }
}

```

[Back to the top](#table-of-contents)

<br>

#### Edge - Make Arc

To create arc for the `edge - back-top (block 2)` and `edge - front-top (block 2)` edges,  use the **edge make-arc** feature - 

**NOTE**: <u>To see the effect of acr/spline/polyline/polySpline/bSpline on block edges, there has to be more than one grid (along the axes)</u>. So, updating the grid spacing for the illustration case - 

```bash

### From this
gid_spacing='{
    "x" : 1000,
    "y" : 1000,
    "z" : 1000
}'

### To this
gid_spacing='{
    "x" : 0.05,
    "y" : 0.05,
    "z" : 0.05
}'

```

<img src="../illustrations/edge-make-arc.png" alt="feature-edge-make-arc" width="100%" style="display : block; margin : auto;">

<br>

```Python

### Perform move-collapse as explained above, then ...

edgeEdit[operationId_1] = {
    ### Block ID
    "block-id" : 2,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "top"],
    
    ### Defining points
    "arc-point" : [0.9293, 0.3827, 0.0]
}

edgeEdit[operationId_2] = {
    ### Block ID
    "block-id" : 2,
    
    ### Type of edge edit
    "edit-type" : "make-arc",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "top"],
    
    ### Defining points
    "arc-point" : [0.9293, 0.3827, 0.2]
}

```

[Back to the top](#table-of-contents)

<br>

#### Edge - Make-Spline

To create spline for the `edge - back-right (block 1)` and `edge - front-right (block 1)` edges,  use the **edge make-spline** feature - 

<u>Make sure to use fine grides to see the effect of splined edge.</u>

<img src="../illustrations/edge-make-spline.png" alt="feature-edge-make-arc" width="100%" style="display : block; margin : auto;">

<br>

```Python

### Perform move-collapse as explained above, then ...

edgeEdit[operationId_1] = {
    ### Block ID
    "block-id" : 1,
    
    ### Type of edge edit
    "edit-type" : "make-spline",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["back", "right"],
    
    ### Defining points
    "spline-points" : [
        [1.0, 0.35, 0.0],
        [0.9, 0.45, 0.0]
    ]
}

edgeEdit[operationId_2] = {
    ### Block ID
    "block-id" : 1,
    
    ### Type of edge edit
    "edit-type" : "make-spline",
    
    ### Edge's position in the block (position order insensitive)
    "edge-position" : ["front", "right"],
    
    ### Defining points
    "spline-points" : [
        [1.0, 0.35, 0.2],
        [0.9, 0.45, 0.2]
    ]
}
```

<br>

#### Edge - Make-polyline

This is similar to the **edge make-spline** feature. Need to specify the correct edit type.

```Python
    ### polySpline
    ### Type of edge edit
    "edit-type" : "make-polyline",

```

<br>

#### Edge - Make-polySpline

This is similar to the **edge make-spline** feature. Need to specify the correct edit type.

```Python
    ### polySpline
    ### Type of edge edit
    "edit-type" : "make-polySpline",

```

<br>

#### Edge - Make-bSpline

This is similar to the **edge make-spline** feature. Need to specify the correct edit type.

```Python
    ### polySpline
    ### Type of edge edit
    "edit-type" : "make-bSpline",

```

<br><br><br>

> ### Block Feature

<br>

<u>Feature development in progress</u>






