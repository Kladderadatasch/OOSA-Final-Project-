import numpy as np

from Points import Point2D
from Raster import Raster

class FlowNode(Point2D):
    
    def __init__(self,x,y, value):
        Point2D.__init__(self,x,y)
        self._downnode=None
        self._upnodes=[]
        self._pitflag=True
        self._value=value
        self._rain = 0
        
    def setDownnode(self, newDownNode):
        self._pitflag=(newDownNode==None)
        
        if (self._downnode!=None): # change previous
            self._downnode._removedUpnode(self)
            
        if (newDownNode!=None):
            newDownNode._addUpnode(self)
            
        self._downnode=newDownNode 
        
    def getDownnode(self):
        return self._downnode 
        
    def getUpnodes(self):
        return self._upnodes
    
    def _removedUpnode(self, nodeToRemove):
        self._upnodes.remove(nodeToRemove)
    
    def _addUpnode(self, nodeToAdd):
        self._upnodes.append(nodeToAdd)

    def numUpnodes(self):
        return len(self._upnodes)
        
    def getPitFlag(self):
        return self._pitflag 
    
    def getElevation(self):
        return self._value
    
    def getFlow(self, israin = False):
    
        if israin == True:
            
            sumRain = 0
            
            for i in self.getUpnodes():
                
                sumRain = sumRain + i._rain
                
            return sumRain
        
        if israin == False:
            return self.numUpnodes()
                
      
    def __str__(self):
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())
    
class FlowRaster(Raster):

    def __init__(self,araster):
        super().__init__(None, araster.getOrgs()[0],araster.getOrgs()[1],araster.getCellsize())
        data = araster.getData()
        nodes=[]
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y=(i)*self.getCellsize()+self.getOrgs()[0]
                x=(j)*self.getCellsize()+self.getOrgs()[1]
                nodes.append(FlowNode(x,y, data[i,j]))
            
        nodearray=np.array(nodes)
        nodearray.shape=data.shape
        
        self._data = nodearray
        
        
        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
        self.setDownCells()
              
    def getNeighbours(self, r, c):
        neighbours=[]
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])
                
        return neighbours
    
    def lowestNeighbour(self,r,c):
        lownode=None
        
        for neighbour in self.getNeighbours(r,c):
            if lownode==None or neighbour.getElevation() < lownode.getElevation():
                lownode=neighbour
        
        return lownode

    def setDownCells(self):
       for r in range(self.getRows()):
           for c in range(self.getCols()):
               lowestN = self.lowestNeighbour(r,c)
               if (lowestN.getElevation() < self._data[r,c].getElevation()):
                   self._data[r,c].setDownnode(lowestN)
               else:
                   self._data[r,c].setDownnode(None)
    
    def addRainfall(self, rainObject):
        
        for i in range(rainObject.shape[0]):
            for j in range(rainObject.shape[1]):
                self._data[i,j]._rain = rainObject[i,j]
                

            
    def calculateLakes(self):
        return self
            
    def getPointList(self):
        return np.reshape(self._data, -1)
    
    def extractValues(self, extractor, isR):
        values=[]
        maxRain = 0
        for i in range(self._data.shape[0]):
            for j in range(self._data.shape[1]):
                values.append(extractor.getValue(self._data[i,j], isRainfall = isR))
                
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        for i in range(valuesarray.shape[0]):
            for j in range(valuesarray.shape[1]):
                if valuesarray[i,j] > maxRain:
                    maxRain = valuesarray[i,j]
                    k = i
                    l = j
        print('''The maximum flow rate is :'''+str(round(maxRain))+''' mm''')
        print('''Location of the maximum '''+self._data[k,l].__str__())
        return valuesarray

    
class FlowExtractor():
            
    def getValue(self, node, isRainfall):
       
            return node.getFlow(israin = isRainfall)
        
    