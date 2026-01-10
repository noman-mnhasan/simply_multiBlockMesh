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
    hl,
    get_block_edge_location
)

from .block import *
from .edge import *
from .face import *
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
        """ Check, raise error and assign value of Edit.filename"""
        
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
        """ Check, raise error and assign value of Edit.task """
                
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
        # print(f"Module Dir  : {self._workingDir}")
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
    
    def execute_edge_operation(
            self,
            blocks
        ) -> None:
        """
        Execute user provided edge edit operations

        Args:
            blocks (Block): Dictionary of the "Blocks" objects defining the multi-block

        Raises:
            ValueError: For improper edge definitions
        """
        
        for taskId, task in self.task.edgeEdit.items():
            
            ### Identify edge
            edgeLocationIndex = get_block_edge_location(task["edge-position"])
            edge = blocks[task["block-id"]].edges[edgeLocationIndex]
            
            if edgeLocationIndex not in range(12):
                raise ValueError("Edge location specification not recognized")
            
            ### Moving edge
            if task["edit-type"].lower() == "move":
                edge.move(task["delta"])
            
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
            vertices: Dict,
            blocks: Dict,
        ) -> None:
        """
        Execute edits defined in task

        Args:
            vertices (Dict): Dictionary of "Vertex" objects defining the multi-block.
            blocks (Dict): Dictionary of "Block" objects defining the multi-block.
        """
        
        taskTypes = [
            self.task.vertexEdit,
            self.task.edgeEdit,
            self.task.boundary
        ]
        
        if not any([bool(x) for x in taskTypes]):
            print("No edit task found!!")
            return
        
        ### Vertex operations
        self.execute_vertex_operation(vertices)
        
        ### Edge operations
        self.execute_edge_operation(blocks)
        
        ## Define boundaries
        self.define_boundaries(blocks)