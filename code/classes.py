
from collections import OrderedDict

class MultiBlockMesh:
    """ Class to contain all attributes and generate the desired blockMeshDict """
    
    def __init__(self, boundingBox, splitPlaneList, gridSpacing, hex2exclude, caseDir):
        self.boundingBox = boundingBox
        self.splitPlaneList = splitPlaneList
        self.gidSpacing = gridSpacing
        self.hex2exclude = hex2exclude
        self.caseDir = caseDir
        
        self.xVextices = []
        self.yVextices = []
        self.zVextices = []
        
        self.nBlock = {}
        
        self.vertexDict = {}
        self.vertexGroupDict = OrderedDict()
        self.blockDict = {}
        
        self.faceDict = {}
        
        self.vertexCount = 0
        self.zPlaneList = []
        self.yLineList = []
        self.xCoordList = []
        
        self.dx = gridSpacing["x"]
        self.dy = gridSpacing["y"]
        self.dz = gridSpacing["z"]
    
    
    def get_vertex_locations(self):
        """ Organizes all the coordinates """
        
        xSplitCoordinate = sorted(self.splitPlaneList["x"])
        ySplitCoordinate = sorted(self.splitPlaneList["y"])
        zSplitCoordinate = sorted(self.splitPlaneList["z"])
        
        self.xVextices.append(self.boundingBox["x-min"])
        if bool(xSplitCoordinate):
            self.xVextices.extend(xSplitCoordinate)
        self.xVextices.append(self.boundingBox["x-max"])
        
        self.yVextices.append(self.boundingBox["y-min"])
        if bool(ySplitCoordinate):
            self.yVextices.extend(ySplitCoordinate)
        self.yVextices.append(self.boundingBox["y-max"])
        
        self.zVextices.append(self.boundingBox["z-min"])
        if bool(zSplitCoordinate):
            self.zVextices.extend(zSplitCoordinate)
        self.zVextices.append(self.boundingBox["z-max"])
    
    
    def number_of_blocks(self):
        """ Calculates the number of blocks on each direction """
        
        self.nBlock = {
                "x" : len(self.xVextices) - 1,
                "y" : len(self.yVextices) - 1,
                "z" : len(self.zVextices) - 1,
            }
    
    
    def create_vertex_group(self):
        """ Calculated vertex location, create groups/dicts """
        
        vertexCount = 0
        for k in range(self.nBlock["z"] + 1):
            zPlaneName = "z_" + str(k)
            self.zPlaneList.append(zPlaneName)
            self.vertexGroupDict[zPlaneName] = OrderedDict()
            
            for j in range(self.nBlock["y"] + 1):
                yLineName = "y_" + str(j)
                self.yLineList.append(yLineName)
                self.vertexGroupDict[zPlaneName][yLineName] = []
                
                for i in range(self.nBlock["x"] + 1):
                    self.vertexDict[str(vertexCount)] = (self.xVextices[i], self.yVextices[j], self.zVextices[k])
                    self.xCoordList.append(self.xVextices[i])
                    self.vertexGroupDict[zPlaneName][yLineName].append(vertexCount)
                    vertexCount += 1
    
    
    def create_block_and_face_dict(self):
        """ Creates a dictionary to contain all the block/hex definitions """
        
        hexCount = 0        
        for iz in range(self.nBlock["z"]):
            zPlane_1 = self.zPlaneList[iz]
            zPlane_2 = self.zPlaneList[iz + 1]
            
            for iy in range(self.nBlock["y"]):
                yLine_1 = self.yLineList[iy]
                yLine_2 = self.yLineList[iy + 1]
                
                for ix in range(self.nBlock["x"]):
                    if hexCount in self.hex2exclude:
                        pass
                    else:
                        pointFrontBottom_1 = self.vertexGroupDict[zPlane_1][yLine_1][ix]
                        pointFrontBottom_2 = self.vertexGroupDict[zPlane_1][yLine_1][ix + 1]
                        
                        pointBackBottom_2 = self.vertexGroupDict[zPlane_2][yLine_1][ix + 1]
                        pointBackBottom_1 = self.vertexGroupDict[zPlane_2][yLine_1][ix]
                        
                        pointFrontTop_1 = self.vertexGroupDict[zPlane_1][yLine_2][ix]
                        pointFrontTop_2 = self.vertexGroupDict[zPlane_1][yLine_2][ix + 1]
                        
                        pointBackTop_2 = self.vertexGroupDict[zPlane_2][yLine_2][ix + 1]
                        pointBackTop_1 = self.vertexGroupDict[zPlane_2][yLine_2][ix]
                        
                        blockId = "block-" + str(hexCount) + "__x-" + str(ix) + "_y-" + str(iy) + "_z-" + str(iz)
                        self.blockDict[blockId] = (pointFrontBottom_1, pointFrontBottom_2,                                            
                                                    pointFrontTop_2, pointFrontTop_1,
                                                    pointBackBottom_1, pointBackBottom_2,
                                                    pointBackTop_2, pointBackTop_1)
                        
                        self.faceDict[blockId] = {
                                "front" : [
                                            pointFrontBottom_1,
                                            pointFrontBottom_2,
                                            pointFrontTop_2,
                                            pointFrontTop_1,
                                        ],
                                "back" : [
                                            pointBackBottom_1,
                                            pointBackTop_1,
                                            pointBackTop_2,
                                            pointBackBottom_2,
                                        ],
                                "left" : [
                                            pointFrontBottom_1,
                                            pointFrontTop_1,
                                            pointBackTop_1,
                                            pointBackBottom_1,
                                        ],
                                "right" : [
                                            pointBackBottom_2,
                                            pointBackTop_2,
                                            pointFrontTop_2,
                                            pointFrontBottom_2,
                                        ],
                                "bottom" : [
                                            pointFrontBottom_1,
                                            pointBackBottom_1,
                                            pointBackBottom_2,
                                            pointFrontBottom_2,
                                        ],
                                "top" : [
                                            pointFrontTop_1,
                                            pointFrontTop_2,
                                            pointBackTop_2,
                                            pointBackTop_1,
                                        ],
                            }
                    hexCount += 1
        return self.blockDict
    
    
    def block_minmax(self, block):
        """  
            Calculates min/max along x, y, z direction for a given block
            Returns a dictionary containing the min/max data
        """
        
        xCoord = []
        yCoord = []
        zCoord = []
        
        for loc in block:
            xCoord.append(self.vertexDict[str(loc)][0])
            yCoord.append(self.vertexDict[str(loc)][1])
            zCoord.append(self.vertexDict[str(loc)][2])
        
        xMin = min(xCoord)
        xMax = max(xCoord)
        yMin = min(yCoord)
        yMax = max(yCoord)
        zMin = min(zCoord)
        zMax = max(zCoord)
        
        return {
                "x-min" : xMin,
                "x-max" : xMax,
                "y-min" : yMin,
                "y-max" : yMax,
                "z-min" : zMin,
                "z-max" : zMax,
            }
    
    
    def block_spacing(self, block):
        """
            Calculates the gid spacing along x, y, z direction for a given block.
            Returns a tuple of the spacing along the x, y, z direction
        """
        
        blockMinMax = self.block_minmax(block)
        
        nx = int((blockMinMax["x-max"] - blockMinMax["x-min"])/float(self.dx))
        ny = int((blockMinMax["y-max"] - blockMinMax["y-min"])/float(self.dy))
        nz = int((blockMinMax["z-max"] - blockMinMax["z-min"])/float(self.dz))
        
        if nx == 0:
            nx = 1
        if ny == 0:
            ny = 1
        if nz == 0:
            nz = 1
        
        return nx, ny, nz
        




