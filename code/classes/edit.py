import os
import importlib.util
import types

from pathlib import Path
from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from lib import (
    wspace,
    indent,
    VSEP,
    hl
)

from .block import *
from .edge import *
from .face import *
from .multiblock import *
from .vertex import *


class Edit:
    """ Attributes and methods associated with the multi-block edit operations """
    
    def __init__(
            self,
            workingDir: str
        ) -> None:
        """
        Initialize edit instance

        Args:
            workingDir (str): Path string of the working directory
        """
        
        self._workingDir = workingDir
        self._filename = None
        self._fileExist = False
        self._task = None
        self._taskExist = False
        
        self._filePrefix = "block_edit_"
        
        self._edgeDefinition = []
        
        self._boundaryDefinition = []
    
    def __repr__(self):
        return "Class for the edit operation"
    
    @property
    def filename(self) -> str:
        return self._filename
    
    @filename.setter
    def filename(self, value: str) -> None:
        """ Check, raise error and assign value of Edit.filename """
        
        if not isinstance(value, str):
            raise ValueError("Edit input filename must be a string.")
        self._filename = value
    
    @property
    def fileExist(self) -> bool:
        return self._fileExist
    
    @fileExist.setter
    def fileExist(self, value: bool) -> None:
        """  """
        
        self._fileExist = value
    
    @property
    def task(self) -> bool:
        return self._task
    
    @task.setter
    def task(self, value: types.ModuleType) -> None:
        """  """
                
        self._task = value
    
    @property
    def edgeDefinition(self) -> str:
        return self._edgeDefinition
    
    @edgeDefinition.setter
    def edgeDefinition(self, value: list) -> None:
        """  """
        
        self._edgeDefinition = value
    
    @property
    def boundaryDefinition(self) -> str:
        return self._boundaryDefinition
    
    @boundaryDefinition.setter
    def boundaryDefinition(self, value: list) -> None:
        """  """
        
        self._boundaryDefinition = value
    
    
    def does_file_exists(self) -> None:
        """ Check if edit file exists """
               
        p = Path(self._workingDir)
        result = tuple(p.glob(f"{self._filePrefix}*.py"))
        if len(result)> 1:
            raise RuntimeError("\n\nMore than one 'block_edit' file exists!")
        
        for item in result:
            if item.is_file():
                self.fileExist = True
                self._filename = os.path.basename(item)
            
        if self.fileExist == False:
            print("Edit file does not exist!")
        
    
    def read(self) -> None:
        """ Read edit definition file """
        
        moduleName = self.filename.split(".")[0]
        modulePath = self._workingDir + os.sep + self.filename
        hl()
        print(f"Module name : {moduleName}")
        
        spec = importlib.util.spec_from_file_location(
                                    moduleName,
                                    modulePath
                                )
        self.task = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.task)
    
    def execute_vertex_operation(
            self,
            vertices: Vertex
        ) -> None:
        """
        Execute user provided vertex edit operations

        Args:
            vertices (Vertex): Dictionary of the "Vertex" objects defining the multi-block
        """
        
        for taskId, task in self.task.vertexEdit.items():
            
            ### Moving vertex
            if task["edit-type"].lower() == "move":
                vertices[task["id"]].move(
                        task["new-location"]
                    )
            
            ### Collapsing vertices
            if task["edit-type"].lower() == "collapse":
                vertices[task["id"]].collapse(
                        vertices[task["target-vertex"]]
                    )
            
            ### Move_Collapse vertices
            if task["edit-type"].lower() == "move-collapse":
                vertices[task["id"]].move_collapse(
                        task["new-location"],
                        vertices[task["target-vertex"]]
                    )
        
    
    
    def execute_edge_operation(
            self,
            blocks: Dict
        ) -> None:
        """
        Execute user provided edge edit operations

        Args:
            blocks (dict): Dictionary of the "Blocks" objects defining the multi-block

        Raises:
            ValueError: For improper edge definitions
        """
        
        for taskId, task in self.task.edgeEdit.items():
            
            ### Identify edge
            edge = task["block-id"].find_edge(
                    task["edge-position"]
                )
            if "target-edge" in task.keys():
                targetEdge = task["block-id"].find_edge(
                        task["target-edge"]["edge-position"]
                    )
            
            ### Moving edge
            if task["edit-type"].lower() == "move":
                edge.move(task["delta"])
            
            ### Collapsing edge
            if task["edit-type"].lower() == "collapse":
                edge.collapse(targetEdge)
            
            ### Moving-collapsing edge
            if task["edit-type"].lower() == "move-collapse":
                edge.move_collapse(
                        task["delta"],
                        targetEdge
                    )
            
            ### Create arc definition
            if task["edit-type"].lower() == "make-arc":
                self.edgeDefinition.append(
                        edge.arc(task["arc-point"])
                    )
            
            ### Create spline definition
            if task["edit-type"].lower() == "make-spline":
                self.edgeDefinition.append(
                        edge.spline(task["spline-points"])
                    )
            
            ### Create polyline definition
            if task["edit-type"].lower() == "make-polyline":
                self.edgeDefinition.append(
                        edge.spline(task["polyline-points"])
                    )
        
    
    
    def execute_block_operation(
            self,
            mb: MultiBlock
        ) -> None:
        
        for taskId, task in self.task.blockEdit.items():
            
            ### Making quadrant
            if task["edit-type"].lower() == "make-quadrant":
                slicePlane, sliceIndex = self.get_slice_info_from_block_pair(
                        mb.blocks[task["starting-block-id"]],
                        mb.blocks[task["ending-block-id"]]
                    )
                self.edgeDefinition.extend(
                    mb.make_quadrant(
                            task["block-face"],
                            task["starting-block-id"],
                            task["ending-block-id"],
                            task["radius"],
                            slicePlane,
                            sliceIndex
                        )
                    )
    
        
    def get_slice_info_from_block_pair(
            self,
            block1: Block,
            block2: Block
        ) -> tuple:
        """
        Compares multi-block index between two blocks.
        Get matching "slice plane" and matching "slice index"

        Args:
            blockPair (Block): One of the two blocks to be compared
            blockPair (Block): The other block to be compared

        Returns:
            tuple: (matching slice plane, index of the matching slice plane)
        """
        
        planeMatchIndexMap = {
            0 : "yz",
            1 : "zx",
            2 : "xy"
        }
        
        gridIndexBlock1 = block1.multiBlockIndex
        gridIndexBlock2 = block2.multiBlockIndex
        
        gridIndexCompare = [
            gridIndexBlock1[0] == gridIndexBlock2[0],
            gridIndexBlock1[1] == gridIndexBlock2[1],
            gridIndexBlock1[2] == gridIndexBlock2[2],
        ]
        
        matchedIndex = gridIndexCompare.index(True)
        slicePlane = planeMatchIndexMap[matchedIndex]
        sliceIndex = gridIndexBlock1[matchedIndex]
        
        return (
            slicePlane,
            sliceIndex
        )
    
    def define_boundaries(
            self,
            blocks
        ) -> None:
        """
        Define boundary entry for blockMeshDict

        Args:
            blocks (Block): Dictionary of the "Vertex" objects defining the multi-block
        """
        
        for taskId, task in self.task.boundary.items():
            
            boundaryDef = (indent * 1) + task["name"] + "\n"
            boundaryDef += (indent * 1) + "{\n"
            boundaryDef += (indent *2) + f"type    {task['type']};\n"
            boundaryDef += (indent *2) + f"faces\n"
            boundaryDef += (indent *2) + f"(\n"
            
            for iface in task['faces']:
                faceVertices = blocks[iface[0]].faces[iface[1]].vertices
                orderedVerticesString = "(" + " ".join([str(x.id) for x in faceVertices]) + ")"
                
                boundaryDef += (indent *3) + orderedVerticesString + "\n"
            
            boundaryDef += (indent *2) + f");\n"
            boundaryDef += (indent * 1) + "}\n"
            
            self.boundaryDefinition.append(boundaryDef)
    
    def execute(
            self,
            mb: MultiBlock,
        ) -> None:
        """
        Execute edits defined in task

        Args:
            vertices (Dict): Dictionary of "Vertex" objects defining the multi-block.
            blocks (Dict): Dictionary of "Block" objects defining the multi-block.
        """
        
        taskTypeCheck = [
            "vertexEdit", 
            "edgeEdit",
            "blockEdit",
            "boundary",
        ]
        
        taskTypes = []
        
        hl()
        for taskType in taskTypeCheck:
            if hasattr(self.task, taskType):
                status = True
                taskTypes.append(getattr(self.task, taskType))
            else:
                status = False
            print(f"Task type - {taskType:12} exists? - {status}")
        
        if not any([bool(x) for x in taskTypes]):
            print("No edit task found!!")
            return
        
        vertices =  mb.vertices,
        blocks = mb.blocks,
        slices = mb.slices
            
        
        ### Vertex operations
        self.execute_vertex_operation(vertices)
        
        ### Edge operations
        self.execute_edge_operation(blocks)
        
        ### Block operations
        self.execute_block_operation(mb)
        
        ## Define boundaries
        self.define_boundaries(blocks)