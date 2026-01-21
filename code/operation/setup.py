
import os
import shutil

from typing import (
    List
)


from entity.multiblock import MultiBlock

from utility.define import (
    indent,
    ofCaseTemplateDirname,
)

from utility import tool as t




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


class Setup:
    """ Setup case directory to run blockMesh """
    
    def __init__(
            self,
            scriptDir: str,
            caseDir: str,
            
        ) -> None:
        """
        Initialize Setup instance

        Args:
            templateDir (str): Directory where the template case files are stored
            caseDir (str): OpenFoam case directory
        """
        
        self._scriptDir = scriptDir
        self._caseDir = caseDir
        
        self._caseSubDirs = [
                self._caseDir + os.sep + "constant",
                self._caseDir + os.sep + "system",
            ]
        
        self._templateDirname = ofCaseTemplateDirname
        self._templateDir = self._scriptDir + os.sep + self._templateDirname
    
    @property
    def scriptDir(self) -> None:
        return self._scriptDir
    
    @scriptDir.setter
    def scriptDir(self, value: str) -> None:
        """ Check, raise error and assign value of Setup.scriptDir """
        
        if not isinstance(value, str):
            raise ValueError("Value of Setup.scriptDir must be a string")
        
        self._scriptDir = value
    
    @property
    def caseDir(self) -> None:
        return self._caseDir
    
    @caseDir.setter
    def caseDir(self, value: str) -> None:
        """ Check, raise error and assign value of Setup.caseDir """
        
        if not isinstance(value, str):
            raise ValueError("Value of Setup.caseDir must be a string")
        
        self._caseDir = value
    
    def remove_case_dir(self) -> bool:
        """ Check path if the path exists  """
        
        casePath = self._caseDir + os.sep + "case"
        if os.path.exists(casePath):
            for item in os.listdir(casePath):
                itemPath = casePath + os.sep + item
                if os.path.isfile(itemPath) or os.path.islink(itemPath):
                    os.remove(itemPath)
                
                elif os.path.isdir(itemPath):
                    shutil.rmtree(itemPath)
        
        t.hl()
        print("OpenFoam case directory for blockMesh cleared!")
    
    def make_case_dir(self) -> None:
        """ Setup openfoam case directory to run blockMesh """
        
        for item in self._caseSubDirs:
            directory = item.split(os.sep)[-1]
            try:
                os.makedirs(item, exist_ok = True)
                
            except OSError as error:
                t.hl()
                print(f"Error creating the \"{directory}\" directory.")
                print("Aborting ... ...")
                exit(-2)
        
    def create_foam_file(self) -> None:
        """ Creating a *.foam file for ease of use with ParaView """
        
        os.system("touch " + self._caseDir + os.sep + "case.foam")
        
    def copy_template_files(self) -> None:
        """ Copying template case files - to run "blockMesh"  """
        
        copyFileList = [
                self._templateDir + os.sep + "controlDict",
                self._templateDir + os.sep + "fvSchemes",
                self._templateDir + os.sep + "fvSolution",
            ]
        
        for sourceFile in copyFileList:
            targetFile = self._caseDir + os.sep + "system"
            shutil.copy(sourceFile, targetFile)
    
    def run(self) -> None:
        """ Run the case setup sequence """
        
        self.remove_case_dir()
        self.make_case_dir()
        self.create_foam_file()
        self.copy_template_files()
    
    def blockmeshdict(
            self,
            convertToMeters: float,
            mb: MultiBlock,
            boundaryDefinition: List
        ) -> None:
        """
        Generate the content of blockMeshDict and write in file

        Args:
            convertToMeters (float): "convertToMeter" value for blockMeshDict
            mb (mbc.MultiBlock): MultiBlock object
            edgeDefinition (List): Definition of edge modifications to add to blockMeshDict
            boundaryDefinition (List): Definition of boundary to add to blockMeshDict
        """
        
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
            dictContent += (indent * 1) + "(" + " ".join([str(i) for i in [v.x, v.y, v.z]]) + ")    // vertex-" + str(k) + "\n"
            count += 1
        
        dictContent += ");\n"
        dictContent += "\n"
        dictContent += "blocks\n"
        dictContent += "(\n"
        
        for k, iblock in mb.blocks.items():
            
            if iblock.isActive == False:
                continue
            
            nx, ny, nz = mb.blocks[k].get_spacing()
            
            nxs = f"{nx}"
            nys = f"{ny}"
            nzs = f"{nz}"
            
            dictContent += (indent * 1) + "// ==== Block-" + str(k) + ", Index : "  +  str(iblock.index) + " ==== //\n"
            dictContent += (indent * 1) + "hex (" + " ".join([f"{x:3}" for x in [v.id for v in iblock.vertices]]) + ") (" + nxs + " " + nys + " " + nzs + ") simpleGrading (1 1 1)" + "\n\n"
        
        dictContent += ");\n"
        dictContent += "\n"
        dictContent += "edges\n"
        dictContent += "(\n"
        
        for iedge in mb.edges:
            if iedge.type in ["arc", "spline", "polyline"]:
                dictContent += indent + iedge.definition + "\n\n"
        
        dictContent += ");\n"
        dictContent += "\n"
        dictContent += "boundary\n"
        dictContent += "(\n"
        
        for entry in boundaryDefinition:
            dictContent += entry + "\n\n"
        
        dictContent += ");\n"
        dictContent += "\n"
        dictContent += "mergePatchPair\n"
        dictContent += "(\n"
        dictContent += ");\n"
        dictContent += "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
        dictContent += "// Comments/Notes\n"
        dictContent += "// Prepared by \"Simply multiBlockMesh\" (SimBloM)\n"
        dictContent += "// - https://github.com/noman-mnhasan/simply_multiBlockMesh\n"
        dictContent += "//\n"
        dictContent += "//\n"
        dictContent += "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
        dictContent += "\n"    
        
        ### Write blockMeshDict
        exportFile = self._caseDir + os.sep + "system" + os.sep + "blockMeshDict"
        with open(exportFile, "w") as bmd:
            bmd.write(dictContent)
        