
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


#---------------------------------------

VSEP = "-"*40

def hl() -> None:
    """ Prints a horizontal line on screen based on VSEP definition """
    
    print(VSEP)

#---------------------------------------

### Version Notification
print(f"\n\n{VSEP}\nSimply MultiBlockMesh - v{__version__}")


blockMeshDictHeader = """/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2412                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
\\*---------------------------------------------------------------------------*/

FoamFile
{
    version     2.0;
    format      ascii;
    class       dictionary;
    location    "system";
    object      blockMeshDict;
}

// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //
\n"""




def make_multiblock(mb: mbc.MultiBlock) -> None:
    """ Run the multi-block operations """
    
    mb.split_locations()
    mb.block_count()
    mb.create_vertex_group()
    mb.create_blocks()
    mb.get_slices()


def create_case_directory(caseDir: str) -> None:
    """ Clear and create a case directory to run blockMesh """
    
    caseDirList = [
            caseDir + os.sep + "constant",
            caseDir + os.sep + "system",
        ]
    
    if os.path.exists(caseDir):
        for item in os.listdir(caseDir):
            itemPath = caseDir + os.sep + item
            if os.path.isfile(itemPath) or os.path.islink(itemPath):
                os.remove(itemPath)
            
            elif os.path.isdir(itemPath):
                shutil.rmtree(itemPath)
    
        hl()
        print("export directory cleared!")
    
    for item in caseDirList:
        directory = item.split(os.sep)[-1]
        try:
            os.makedirs(item, exist_ok = True)
            
        except OSError as error:
            hl()
            print(f"Error creating the \"{directory}\" directory.")
            print("Aborting ... ...")
            exit()
    
    ### Creating a *.foam file for ease of use with ParaView
    os.system("touch " + caseDir + os.sep + "case.foam")
    
    ### Copying template case files - to run "blockMesh" 
    copyFileList = [
            scriptDir + os.sep + "case_system_template" + os.sep + "controlDict",
            scriptDir + os.sep + "case_system_template" + os.sep + "fvSchemes",
            scriptDir + os.sep + "case_system_template" + os.sep + "fvSolution",
        ]
    
    for sourceFile in copyFileList:
        targetFile = caseDir + os.sep + "system"
        shutil.copy(sourceFile, targetFile)


def make_blockmeshdict(
        convertToMeters: float,
        mb: mbc.MultiBlock
    ) -> None:
    """ Generate the content of blockMeshDict and write in file """
    
    wspace = " "
    indent = wspace * 4    
    dictContent = blockMeshDictHeader
    
    dictContent +="\nconvertToMeters=" + str(convertToMeters) + ";\n"
    
    dictContent += "vertices\n"
    dictContent += "(\n"
    
    count = 0
    yCount = 0
    zCount = 0
    xCountLen = len(mb.xVertices)
    yCountLen = len(mb.yVertices)
    
    dictContent += (indent * 1) + "// ==== y-" + str(yCount) + ", z-" + str(zCount) + " ==== //\n\n"
    for k, v in mb.vertices.items():        
        if count >= xCountLen and count%xCountLen == 0:
            yCount += 1
            if yCount%yCountLen == 0:
                yCount = 1
                zCount += 1            
            dictContent += "\n" + (indent * 1) + "// ==== y-" + str(yCount) + ", z-" + str(zCount) + " ==== //\n\n"        
        dictContent += (indent * 1) + "(" + " ".join([str(x) for x in v]) + ")    // vertex-" + str(k) + "\n"
        count += 1
    
    dictContent += ");\n"
    dictContent += "\n"
    dictContent += "blocks\n"
    dictContent += "(\n"
    
    for k, v in mb.blocks.items():
        nx, ny, nz = mb.blocks[k].get_spacing()
        
        nxs = f"{nx}"
        nys = f"{ny}"
        nzs = f"{nz}"
        
        dictContent += (indent * 1) + "// ==== Block-" + str(k) + ", Index : "  +  str(v.index) + " ==== //\n"
        dictContent += (indent * 1) + "hex (" + " ".join([f"{x:3}" for x in mb.blocks[k].vertices]) + ") (" + nxs + " " + nys + " " + nzs + ") simpleGrading (1 1 1)" + "\n\n"
    
    dictContent += ");\n"
    dictContent += "\n"
    dictContent += "edges\n"
    dictContent += "(\n"
    dictContent += ");\n"
    dictContent += "\n"
    dictContent += "boundary\n"
    dictContent += "(\n"
    dictContent += ");\n"
    dictContent += "\n"
    dictContent += "mergePatchPair\n"
    dictContent += "(\n"
    dictContent += ");\n"
    dictContent += "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    dictContent += "// Comments/Notes\n"
    dictContent += "//\n"
    dictContent += "//\n"
    dictContent += "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    dictContent += "\n"    
    
    
    ### Write blockMeshDict
    exportFile = caseDir + os.sep + "system" + os.sep + "blockMeshDict"
    with open(exportFile, "w") as bmd:
        bmd.write(dictContent)


def write_face_info(
        mb: mbc.MultiBlock,
        caseDir: str
    ) -> None:
    """ Generate face information of the multi-block and write in file """
    
    wspace = " "
    indent = wspace * 4
    
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



def write_slice_info(
        mb: mbc.MultiBlock
    ) -> None:
    """ Generate slice information of the multi-block and write in file """
    
    hl()
    print(f"Number of blocks in each XY plane : {mb.nBlockXyPlane}")
    print(f"Number of blocks in each YZ plane : {mb.nBlockYzPlane}")
    print(f"Number of blocks in each ZX plane : {mb.nBlockZxPlane}")
    
    
    print("\n")
    hl()
    sliceInfoStr = "### SLICE INFO ###\n"
    sliceInfoStr += VSEP + "\n"
    
    ### blw -> blockLabelWidth
    blw = len(str(mb.nBlock["total"] - 1))
    sliceInfoStr += "SLICE PLANE - XY\n"
    sliceInfoStr += VSEP + "\n"
    
    for i, _slice in mb.slices["xy"].items():
        sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
    
    sliceInfoStr += VSEP + "\n"
    sliceInfoStr += "SLICE PLANE - YZ\n"
    sliceInfoStr += VSEP + "\n"
    
    for j, _slice in mb.slices["yz"].items():
        sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
    
    sliceInfoStr += VSEP + "\n"
    sliceInfoStr += "SLICE PLANE - ZX\n"
    sliceInfoStr += VSEP + "\n"
    
    for k, _slice in mb.slices["zx"].items():
        sliceInfoStr += f"Slice Index - {_slice.index:4} | Blocks : {", ".join(f'{x:{blw}}' for x in _slice.blocks)}\n"
    
    print(sliceInfoStr)
    
    ### Write the slice information in a file
    sliceInfoFile = os.path.dirname(caseDir) + os.sep + "slice_information.txt"
    with open(sliceInfoFile, "w") as sif:
        sif.write(sliceInfoStr)


def write_edge_information(
        mb: mbc.MultiBlock
    ) -> None:
    """ Generate edge information of the multi-block and write in file """
    
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
            - a text file containing the face information for each of the blocks of the "multi-block"
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
    wspace = " "
    indent = wspace * 4
    
    ### Create a MultiBlockMesh object
    mb = mbc.MultiBlock(
                boundingBox,
                splitPlanes,
                gridSpacing,
                hex2exclude
            )
    
    ### Calculate/prepare dictionary data
    make_multiblock(mb)
    
    totalBlocks = mb.nBlock["total"]
    
    ### Display the x/y/z coordinates of the (bounding ox & split/cut locations)
    str2print = VSEP + "\n"
    str2print += "[*] Split plane(s) along X:"
    str2print += indent + ", ".join([str(i) for i in mb.xVertices]) + "\n"
    str2print += "[*] Split plane(s) along Y:"
    str2print += indent + ", ".join([str(i) for i in mb.yVertices]) + "\n"
    str2print += "[*] Split plane(s) along Z:"
    str2print += indent + ", ".join([str(i) for i in mb.zVertices]) + "\n"
    print(str2print)   
    
    ### Display number of blocks
    str2print = VSEP + "\n"
    str2print += f"Blocks along X : {mb.nBlock['x']}\n"
    str2print += f"Blocks along Y : {mb.nBlock['y']}\n"
    str2print += f"Blocks along Z : {mb.nBlock['z']}\n\n"
    str2print += f"Total blocks   : {totalBlocks}"
    print(str2print) 
    
    ### Write the x/y/z coordinates of the (bounding ox & split/cut locations)
    locationFile = os.path.dirname(caseDir) + os.sep + "xyz_locations.txt"
    
    with open(locationFile, "w") as lf:
        lf.write(str2print)
    
    ### Create case directory - To run "blackMesh"
    create_case_directory(caseDir)
    
    ### Create blockMesh dictionary
    make_blockmeshdict(
            convertToMeters,
            mb,
        )
    
    
    ### Get face information
    write_face_info(
            mb,
            caseDir
        )
    
    
    ### Get slice Information  
    write_slice_info(
            mb
        )
    
    
    ### Get edge Information
    write_edge_information(
            mb
        )
    
    
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




