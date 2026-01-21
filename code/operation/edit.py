import os
import importlib.util
import types

from pathlib import Path
from collections import OrderedDict
from typing import (
    List, 
    Dict,
)

from entity.block import *
from entity.edge import *
from entity.face import *
from entity.multiblock import *
from entity.vertex import *


from utility.define import (
    indent,
    taskTypeCheck
)

from utility import tool as t


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
        """ Check, raise error and assign value of Edit.fileExist """
        
        if not isinstance(value, bool):
            raise ValueError("Edit.fileExist must be a bool.")
        
        self._fileExist = value
    
    @property
    def task(self) -> bool:
        return self._task
    
    @task.setter
    def task(self, value: types.ModuleType) -> None:                
        self._task = value
    
    @property
    def edgeDefinition(self) -> str:
        return self._edgeDefinition
    
    @edgeDefinition.setter
    def edgeDefinition(self, value: list) -> None:        
        self._edgeDefinition = value
    
    @property
    def boundaryDefinition(self) -> str:
        return self._boundaryDefinition
    
    @boundaryDefinition.setter
    def boundaryDefinition(self, value: list) -> None:        
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
        t.hl()
        print(f"Module name : {moduleName}")
        
        spec = importlib.util.spec_from_file_location(
                                    moduleName,
                                    modulePath
                                )
        self.task = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.task)
        
    
    def execute_vertex_operation(
            self,
            vertices: Dict
        ) -> None:
        """
        Execute user provided vertex edit operations

        Args:
            vertices (Vertex): Dictionary of the "Vertex" objects defining the multi-block
        """
        
        for taskId, task in self.task.vertexEdit.items():
            
            ### Moving vertex
            if task["edit-type"].lower() == "move":
                
                if "new-location" in task:
                    location = task["new-location"]
                    delta = None
                elif "delta" in task:
                    location = None
                    delta = task["delta"]
                    
                vertices[task["id"]].move(
                        location,
                        delta 
                    )
            
            ### Collapsing vertices
            if task["edit-type"].lower() == "collapse":
                vertices[task["id"]].collapse(
                        vertices[task["target-vertex"]]
                    )
            
            ### Move_Collapse vertices
            if task["edit-type"].lower() == "move-collapse":
                
                if "new-location" in task:
                    location = task["new-location"]
                    delta = None
                elif "delta" in task:
                    location = None
                    delta = task["delta"]
                
                vertices[task["id"]].move_collapse(
                        vertices[task["target-vertex"]],
                        location,
                        delta
                    )
            
            ### Scaling vertex
            if task["edit-type"].lower() == "scale":
                    
                vertices[task["id"]].scale(
                        task["ratio"],
                        task["reference"]
                    )
        
    def process_edge_edit_input(
            self,
            blocks: Dict,
            task: Dict,
        ) -> Dict:
        """
        Identifies required edges and prepares dictionary containing action/operation details.

        Args:
            blocks (Dict): Dictionary of instances of the 'Block' class.
            task (Dict): Dictionary containing edit operation input from user

        Returns:
            Dict: Returns dictionary containing edge action/operation details
        """
        
        editInfo = {}
        
        for key, value in task.items():
            if "edge" in key:
                editInfo[key] = blocks[task[key]["block-id"]].find_edge(task[key]["position"])
            else:
                editInfo[key] = value
        
        return editInfo
    
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
            editInfo = self.process_edge_edit_input(
                    blocks,
                    task
                )
            
            ### Moving edge
            if task["edit-type"].lower() == "move":
                editInfo["edge"].move(task["delta"])
            
            ### Collapsing edge
            if task["edit-type"].lower() == "collapse":
                editInfo["edge"].collapse(editInfo["target-edge"])
            
            ### Moving-collapsing edge
            if task["edit-type"].lower() == "move-collapse":
                editInfo["edge"].move_collapse(
                        task["delta"],
                        editInfo["target-edge"]
                    )
            
            ### Scaling edge
            if task["edit-type"].lower() == "scale":
                editInfo["edge"].scale(task["ratio"])
            
            
            
            ### Create arc definition
            if task["edit-type"].lower() == "make-arc":
                editInfo["edge"].arc(editInfo)
            
            ### Create spline definition
            if task["edit-type"].lower() == "make-spline":
                editInfo["edge"].spline(editInfo)
    
        
    def process_face_edit_input(
            self,
            blocks: Dict,
            task: Dict,
        ) -> Dict:
        """
        Identifies required edges and prepares dictionary containing action/operation details.

        Args:
            blocks (Dict): Dictionary of instances of the 'Block' class.
            task (Dict): Dictionary containing edit operation input from user

        Returns:
            Dict: Returns dictionary containing face action/operation details
        """
        
        editInfo = {}
        
        for key, value in task.items():
            if "face" in key:
                editInfo[key] = blocks[task[key]["block-id"]].faces[task[key]["side"]]
            else:
                editInfo[key] = value
        
        return editInfo
    
    def execute_face_operation(
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
        
        for taskId, task in self.task.faceEdit.items():
            
            ### Identify edge
            editInfo = self.process_face_edit_input(
                    blocks,
                    task
                )
            
            ### Moving face
            if task["edit-type"].lower() == "move":
                editInfo["face"].move(task["delta"])
            
            ### Scaling face
            if task["edit-type"].lower() == "scale":
                editInfo["face"].scale(task["ratio"])
    
    def execute_block_operation(
            self,
            mb: MultiBlock
        ) -> None:
        """
        Execute user provided block edit operations

        Args:
            mb (MultiBlock): Instance of the "Blocks" class defining the multi-block
        """
        for taskId, task in self.task.blockEdit.items():
            
            ### Moving block
            if task["edit-type"].lower() == "move":
                mb.blocks[task["block-id"]].move(
                        delta = task["delta"]
                    )
            
            ### scaling-2d block
            if task["edit-type"].lower() == "scale-2d":
                if isinstance(task["block-id"], list):
                    blocks2scale = [mb.blocks[i] for i in task["block-id"]]
                    mb.scaleSliceBlocks(
                            blocks2scale,
                            task["plane"],
                            task["ratio"],
                        )
                    
                elif isinstance(task["block-id"], int):
                    mb.blocks[task["block-id"]].scale2d(
                            task["plane"],
                            task["ratio"],
                        )
            
            ### scaling-3d block     
            if task["edit-type"].lower() == "scale-3d":
                if isinstance(task["block-id"], list):
                    blocks2scale = [mb.blocks[i] for i in task["block-id"]]
                    mb.scaleSliceBlocks(
                            blocks2scale,
                            task["ratio"],
                        )
                    
                elif isinstance(task["block-id"], int):
                    mb.blocks[task["block-id"]].scale3d(
                            task["ratio"],
                        )
            
            ### Making quadrant
            if task["edit-type"].lower() == "make-quadrant":
                mb.make_quadrant(
                        task["starting-block-id"],
                        task["ending-block-id"],
                        task["radius"],
                    )
            
            ### Making semicircle
            if task["edit-type"].lower() == "make-semicircle":
                mb.make_semicircle(
                        task["starting-block-id"],
                        task["ending-block-id"],
                        task["radius"],
                    )
            
            ### Making circle
            if task["edit-type"].lower() == "make-circle":
                mb.make_circle(
                        task["starting-block-id"],
                        task["ending-block-id"],
                        task["radius"],
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
            mb (MultiBlock): Instance of the MultiBlock class.
        """
        
        taskTypes = {
            "vertexEdit" : [], 
            "edgeEdit" : [],
            "faceEdit" : [],
            "blockEdit" : [],
            "boundary" : []
        }
        
        t.hl()
        for taskType in taskTypeCheck:
            if hasattr(self.task, taskType):
                status = True
                taskEntry = getattr(self.task, taskType)
                if taskEntry != {}:
                    taskTypes[taskType].append(getattr(self.task, taskType))
            else:
                status = False
            print(f"Task type - {taskType:12} exists? - {status}")
        
        if not any([bool(x) for x in taskTypes]):
            print("No edit task found!!")
            return
        
        vertices =  mb.vertices
        blocks = mb.blocks
        
        ### Vertex operations
        if taskTypes["vertexEdit"] != []:
            self.execute_vertex_operation(vertices)
        
        ### Edge operations
        if taskTypes["edgeEdit"] != []:
            self.execute_edge_operation(blocks)
        
        ### Face operations
        if taskTypes["faceEdit"] != []:
            self.execute_face_operation(blocks)
        
        ### Block operations
        if taskTypes["blockEdit"] != []:
            self.execute_block_operation(mb)
        
        ## Define boundaries
        if taskTypes["boundary"] != []:
            self.define_boundaries(blocks)