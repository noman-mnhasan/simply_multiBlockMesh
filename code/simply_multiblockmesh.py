import os
import sys
import json
import shutil

from collections import OrderedDict
from classes import *

scriptPath = os.path.abspath(__file__)
scriptDir = os.path.dirname(scriptPath)

sys.path.append(scriptDir)


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



def make_multi_block_blockmeshdict(
        boundingBox,
        splitPlaneList,
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
        boundingBox (dict): the min/max of the block in x, y, z directions
        splitPlaneList (dict): the list of locations where the bounding box will be split to create the multi-block
        gridSpacing (dict): the spacing of the grid along x, y, z directions
        hex2exclude (dict): the hex definitions to exclude during in the "blocks" section to create the desired mesh domain.
        caseDir (str): location/path of the working directory
    """
    wspace = " "
    indent = wspace * 4
    
    
    ### Create a MultiBlockMesh object
    mbm = MultiBlockMesh(boundingBox, splitPlaneList, gridSpacing, hex2exclude, caseDir)    
    
    
    ### Calculate/prepare dictionary data
    mbm.get_vertex_locations()
    mbm.number_of_blocks()    
    mbm.create_vertex_group()
    mbm.create_block_and_face_dict()
    
    
    ### Display the x/y/z coordinates of the (bounding ox & split/cut locations)
    str2print = "-"*40 + "\n"
    str2print += "x-coordinates:\n"
    str2print += indent + ", ".join([str(i) for i in mbm.xVextices]) + "\n\n"
    str2print += "y-coordinates:\n"
    str2print += indent + ", ".join([str(i) for i in mbm.yVextices]) + "\n\n"
    str2print += "z-coordinates:\n"
    str2print += indent + ", ".join([str(i) for i in mbm.zVextices]) + "\n\n"
    print(str2print)
    
    
    ### Write the x/y/z coordinates of the (bounding ox & split/cut locations)
    locationFile = os.path.dirname(caseDir) + os.sep + "xyz_locations.txt"
    
    with open(locationFile, "w") as lf:
        lf.write(str2print)
    
    
    ### Ge the vertex and block dictionary for creating the blockMeshDict
    vertexDict = mbm.vertexDict    
    blockDict = mbm.blockDict    
    
    
    ### Create/calculate blockMesh dictionary contents
    wspace = " "
    indent = wspace * 4    
    dictContent = blockMeshDictHeader
    
    dictContent += "vertices\n"
    dictContent += "(\n"
    
    count = 0
    yCount = 0
    zCount = 0
    xCountLen = len(mbm.xVextices)
    yCountLen = len(mbm.yVextices)
    
    dictContent += (indent * 1) + "// ==== y-" + str(yCount) + ", z-" + str(zCount) + " ==== //\n\n"
    for k, v in vertexDict.items():        
        if count >= xCountLen and count%xCountLen == 0:
            yCount += 1
            if yCount%yCountLen == 0:
                yCount = 1
                zCount += 1            
            dictContent += "\n" + (indent * 1) + "// ==== y-" + str(yCount) + ", z-" + str(zCount) + " ==== //\n\n"        
        dictContent += (indent * 1) + "(" + " ".join([str(x) for x in v]) + ")    // vertex-" + k + "\n"
        count += 1
    
    dictContent += ");\n"
    dictContent += "\n"
    dictContent += "blocks\n"
    dictContent += "(\n"
    
    for k, v in blockDict.items():
        nx, ny, nz = mbm.block_spacing(v)
        
        nxs = f"{nx}"
        nys = f"{ny}"
        nzs = f"{nz}"
        
        dictContent += (indent * 1) + "// ==== " + str(k) + " ==== //\n"
        dictContent += (indent * 1) + "hex (" + " ".join([f"{x:3}" for x in v]) + ") (" + nxs + " " + nys + " " + nzs + ") simpleGrading (1 1 1)" + "\n\n"
    
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
    
    
    ### Create case directory - To run "blackMesh"
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
    
        print("-"*40)
        print("export directory cleared!")
    
    for item in caseDirList:
        directory = item.split(os.sep)[-1]
        try:
            os.makedirs(item, exist_ok = True)
            
        except OSError as error:
            print("-"*40)
            print(f"Error creating the \"{directory}\" directory.")
            print("Aborting ... ...")
            exit()
    
    
    ### Write blockMeshDict
    exportFile = caseDir + os.sep + "system" + os.sep + "blockMeshDict"
    with open(exportFile, "w") as bmd:
        bmd.write(dictContent)
    
    
    ### Get face information as string
    faceInfoStr = "FACE INFO\n"
    faceInfoStr += "-"*40 + "\n\n"
    
    for k,v in mbm.faceDict.items():
        faceInfoStr += k + ":\n"
        for faceName, faceIds in v.items():
            faceInfoStr += indent + f"{faceName:6} : (" + " ".join(str(x) for x in faceIds) + ")\n"
        faceInfoStr += "\n"
    
    
    ### Write the face information in a file
    faceInfoFile = os.path.dirname(caseDir) + os.sep + "face_information.txt"
    with open(faceInfoFile, "w") as fif:
        fif.write(faceInfoStr)
    
    
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
    
    
    ### End of process
    print("-"*40)
    print("End of process!")
    
    return




if __name__ == "__main__":
    boundingBox = json.loads(os.environ["bounding_box"])
    splitPlaneList = json.loads(os.environ["split_plane_list"])
    gridSpacing = json.loads(os.environ["gid_spacing"])
    hex2exclude = json.loads(os.environ["hex2exclude"])["exclude-list"]
    caseDir = os.environ["export_directory"] + os.sep + "case"
    
    make_multi_block_blockmeshdict(
            boundingBox,
            splitPlaneList,
            gridSpacing,
            hex2exclude,
            caseDir,
        )




