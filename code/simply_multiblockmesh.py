
"""  VERSION """
__version__ = "0.1.1"

import os
import sys
import json
import shutil

from datetime import datetime
from collections import OrderedDict

scriptPath = os.path.abspath(__file__)
scriptDir = os.path.dirname(scriptPath)

import operation as op

from entity.multiblock import MultiBlock
from operation.edit import Edit
from operation.setup import Setup

from utility.define import (
    VSEP,
    indent,
    templateDirName,
    templateFilenameBlockEdit,
)

from utility import tool as t


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
        workingDir,
        caseDir,
        need2modify
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
        workingDir (str): Location/path of the working directory
        caseDir (str): Location/path of the Openfoam case directory
        need2modify (bool): True, it edits needs to be applied in the multi-block
    """
    
    t.hl()
    print("Working Directory : " + workingDir)
    
    ### Create a MultiBlockMesh object
    mb = MultiBlock(
            boundingBox,
            splitPlanes,
            gridSpacing,
            hex2exclude
        )
    
    ### Create an Edit object
    edit = Edit(workingDir)
    
    ### Create a Setup object
    setup = Setup(
            scriptDir,
            caseDir
        )
    
    ### Calculate/prepare dictionary data
    mb.make()
    
    print("\n\n")
    t.hl()
    print("Multi-block indices for blocks:")
    t.hl()
    for blockName, iblock in mb.blocks.items():
        print(f"Block-{iblock.id} | Indices - {iblock.multiBlockIndex}")
        
    
    
    ### Run blockMesh setup
    setup.run()
    
    
    ### Get split location information
    splitLocationInfo = VSEP + "\n"
    splitLocationInfo += "Split location information\n"
    
    splitLocationInfo = VSEP + "\n"
    splitLocationInfo += "[*] Split plane(s) along X:"
    splitLocationInfo += indent + ", ".join([str(i) for i in mb.xVertices]) + "\n"
    splitLocationInfo += "[*] Split plane(s) along Y:"
    splitLocationInfo += indent + ", ".join([str(i) for i in mb.yVertices]) + "\n"
    splitLocationInfo += "[*] Split plane(s) along Z:"
    splitLocationInfo += indent + ", ".join([str(i) for i in mb.zVertices]) + "\n"
    
    print(splitLocationInfo)
    
    ### Write the x/y/z coordinates of the (bounding ox & split/cut locations)
    locationFile = os.path.dirname(caseDir) + os.sep + "xyz_locations.txt"
    
    with open(locationFile, "w") as lf:
        lf.write(splitLocationInfo)
    
    
    ### Update multi-block based on "edit task(s)"
    ### Read edit entries
    edit.does_file_exists()
    if not edit.fileExist:
        t.hl()
        print("File 'block_edit_*.py' doesn't exist")
    
    if edit.fileExist:
        if need2modify:
            edit.read()
            ### Performing edits
            edit.execute(mb)
        else:
            t.hl()
            print(f"Execute multi-block edit? - {need2modify}")
            print("No multi-block edits will be applied.")
    
    
    ### Create blockMesh dictionary
    setup.blockmeshdict(
            convertToMeters,
            mb,
            edit.boundaryDefinition
        )
    
    
    ### Get face information
    faceInfoStr = "FACE INFO\n" 
    faceInfoStr += VSEP + "\n\n"
    
    for k,v in mb.blocks.items():
        faceInfoStr += "Block-" + str(k) + " : " + str(v.index) + "\n\n"
        for faceName, faces in v.faces.items():
            faceInfoStr += indent + f"{faceName:6} : (" + " ".join(str(x) for x in faces.vertices) + ")\n"
        faceInfoStr += "\n\n"
    
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
    edgeInfoStr = "### EDGE INFO ###\n"
    edgeInfoStr += VSEP + "\n"
    
    for blockId, iblock in mb.blocks.items():
        edgeInfoStr += f"\n\n{VSEP}\nBlock ID - {blockId}\n"
        edgeInfoStr += VSEP + "\n"
        edgeInfoStr += "Index | ->  - Position     - Definition\n"
        edgeInfoStr += VSEP + "\n"
        
        for iedge in iblock.edges:
            edgeInfoStr += f"{iedge.id:5} | {iedge}\n"
    
    
    ### Write the slice information in a file
    edgeInfoFile = os.path.dirname(caseDir) + os.sep + "edge_information.txt"
    with open(edgeInfoFile, "w") as eif:
        eif.write(edgeInfoStr)
    
    ### Create edit-input file if doesn't exist
    if not edit.fileExist:
        currentTime = datetime.now()
        currentTimeStr = currentTime.strftime("%Y-%m-%d_%H-%M-%S")
        
        sourcefile = os.path.dirname(scriptDir) + os.sep + templateDirName + os.sep + templateFilenameBlockEdit
        
        targetFilename = templateFilenameBlockEdit[:-3] + "_" + currentTimeStr + ".py"
        targetFile = workingDir + os.sep + targetFilename
        
        shutil.copy2(
                sourcefile,
                workingDir
            )
        
        shutil.move(
                workingDir + os.sep + templateFilenameBlockEdit,
                targetFile
            )
        t.hl()
        print("File created for defining edit and boundary/patch.")
        print(f"File : {targetFilename}")
    
    if edit.fileExist:
        t.hl()
        print(f"Input file for block edit exists.\nFile: {edit.filename}")
    
    
    ### End of process
    t.hl()
    print("End of process!")
    
    return


if __name__ == "__main__":
    boundingBox = json.loads(os.environ["bounding_box"])
    convertToMeters = os.environ["convert_to_meters"]
    splitPlanes = json.loads(os.environ["split_plane_list"])
    gridSpacing = json.loads(os.environ["gid_spacing"])
    hex2exclude = json.loads(os.environ["hex2exclude"])["exclude-list"]
    workingDir = os.environ["export_directory"]
    caseDir = workingDir + os.sep + "case"
    if "read_edit_file" in os.environ:
        if os.environ["read_edit_file"].lower() =="yes":
            need2modify = True
        else:
            need2modify = False
    else:
        raise ValueError("Missing user input - 'read_edit_file?'")
    
    make_multi_block_blockmeshdict(
            boundingBox,
            convertToMeters,
            splitPlanes,
            gridSpacing,
            hex2exclude,
            workingDir,
            caseDir,
            need2modify
        )




