
"""  VERSION """
__version__ = "0.1.0"

import os
import sys
import json
import shutil

from collections import OrderedDict
import classes as mbc
import numpy as np

scriptPath = os.path.abspath(__file__)
scriptDir = os.path.dirname(scriptPath)

sys.path.append(scriptDir)

from lib import (
    wspace,
    indent,
    VSEP,
    hl
)


#---------------------------------------
### Version Notification
print(f"\n\n{VSEP}\nSimply MultiBlockMesh - v{__version__}")


#---------------------------------------
# MAKE MULTI-BLOCK MESH (blockMesh)
#---------------------------------------

def make_multi_block_blockmeshdict(
        boundingBox,
        convertToMeters,
        splitPlanes,
        gridSpacing,
        hex2exclude, 
        caseDir,
    ):
    """
        Calculated the dimensions of the blocks of the final "multi-block".
        Generates the contents of the resultant blockMeshDict file (based 
        on the user's input)
        
        The default settings is --> simpleGrading (1 1 1)
        
        Writes the following files:
            - a text file containing the x/y/z locations outlining the blocks
            - text files containing the face, slice, edge information for the blocks of the "multi-block"
            - the "blockMeshDict" file
                - there is not auto generated boundary information
        
        Remarks:
            - The resultant multi-block is a brick-like object. 
            - The block/hex definitions can be removed/commented out to create complex domain (hex2exclude)
                - The domain is blocky by default, since there is no additional edge attributes are present
                - Adding additional edge attributes/definitions can make the mesh/domain more realistic.

    Args:
        boundingBox (dict): Min/max of the block in x, y, z directions
        splitPlanes (dict): List of locations where the bounding box will be split to create the multi-block
        gridSpacing (dict): Spacing of the grid along x, y, z directions
        hex2exclude (dict): Hex definitions to exclude during in the "blocks" section to create the desired mesh domain.
        caseDir (str): Location/path of the working directory
    """
    
    ### Create a MultiBlockMesh object
    mb = mbc.MultiBlock(
            boundingBox,
            splitPlanes,
            gridSpacing,
            hex2exclude
        )
    ### Calculate/prepare dictionary data
    mb.make()
    
    
    ### Create a Setup object
    setup = mbc.Setup(
            scriptDir,
            caseDir
        )
    setup.run()
    
    
    ### Get split location information
    splitLocationInfo = mb.get_split_info()
    
    ### Write the x/y/z coordinates of the (bounding ox & split/cut locations)
    locationFile = os.path.dirname(caseDir) + os.sep + "xyz_locations.txt"
    
    with open(locationFile, "w") as lf:
        lf.write(splitLocationInfo)
    
    
    ### Create blockMesh dictionary
    setup.blockmeshdict(
            convertToMeters,
            mb,
        )
    
    
    ### Get face information
    faceInfoStr = mb.face_info()
    
    ### Write the face information in a file
    faceInfoFile = os.path.dirname(caseDir) + os.sep + "face_information.txt"
    with open(faceInfoFile, "w") as fif:
        fif.write(faceInfoStr)
    
    
    ### Get slice Information  
    sliceInfoStr = mb.slice_info()
        
    ### Write the slice information in a file
    sliceInfoFile = os.path.dirname(caseDir) + os.sep + "slice_information.txt"
    with open(sliceInfoFile, "w") as sif:
        sif.write(sliceInfoStr)
    
    
    ### Get edge Information
    edgeInfoStr = mb.edge_info()
    
    ### Write the slice information in a file
    edgeInfoFile = os.path.dirname(caseDir) + os.sep + "edge_information.txt"
    with open(edgeInfoFile, "w") as eif:
        eif.write(edgeInfoStr)
    
    
    ### End of process
    hl()
    print("End of process!")
    
    return


if __name__ == "__main__":
    boundingBox = json.loads(os.environ["bounding_box"])
    convertToMeters = os.environ["convert_to_meters"]
    splitPlanes = json.loads(os.environ["split_plane_list"])
    gridSpacing = json.loads(os.environ["gid_spacing"])
    hex2exclude = json.loads(os.environ["hex2exclude"])["exclude-list"]
    caseDir = os.environ["export_directory"] + os.sep + "case"
    
    make_multi_block_blockmeshdict(
            boundingBox,
            convertToMeters,
            splitPlanes,
            gridSpacing,
            hex2exclude,
            caseDir,
        )




