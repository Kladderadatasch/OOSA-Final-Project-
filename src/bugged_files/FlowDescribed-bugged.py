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
  
    def __str__(self):
        return "Flownode x={}, y={}".format(self.get_x(), self.get_y())

class FlowRaster(Raster):
    ''' This Class creates a Raster grid of 
    flow nodes which is related to the topography

    The class inherits functions from 
    the Raster method'''

    def __init__(self,araster):
        super().__init__(None,araster.getOrgs()[0],araster.getOrgs()[1],araster.getCellsize())
        data = araster.getData()
        nodes=[]
		
		
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                y=(i)*self.getCellsize()+self.getOrgs()[0]
                x=(j)*self.getCellsize()+self.getOrgs()[1]
                nodes.append(FlowNode(x,y, data[i,j]))
				
        #According to notes on slides(AtNoS) this adds a flow node to a list for each cell 
				#nodes[] is this list, and getOrgs()[0] is the x orientation
				#getOrgs()[1] is the y orientation 
				#how is data.shape[1] included - what does it do ?
				#does node mean point ?
				#FlowNode is called here
		
		
        nodearray=np.array(nodes)
        nodearray.shape=data.shape
        self._data = nodearray
		#AtNoS this converts the nodes to an array of nodes and reshape it 
		
		
        self.__neighbourIterator=np.array([1,-1,1,0,1,1,0,-1,0,1,-1,-1,-1,0,-1,1] )
        self.__neighbourIterator.shape=(8,2)
		#Neighbour Iterator
				#AtNoS Iterating to locate the nearest points
				#Hardcoded to define the flow of the lookup
				#From topright neighbour downwards
				#8 Cases of neighbours around the center 
                
				#Why shape = (8,2)
		
        self.setDownCells()

        
    	
    def getNeighbours(self, r, c):
		#Returns a list containing the values of the neighbours
				#r - rows, c - columns
				#range hardcoded - because just 8 neighbours are possible
				#rr row + neighbour, beginning from top right 
                
				#if rr >-1 / cc>-1 ? 
                
				#Somehow as long as the iteration is within the borders, 
				#append the value of the neighbours to the list of neighbours 
        neighbours=[]
        for i in range(8):
            rr=r+self.__neighbourIterator[i,0]
            cc=c+self.__neighbourIterator[i,1]
            if (rr>-1 and rr<self.getRows() and cc>-1 and cc<self.getCols()):
                neighbours.append(self._data[rr,cc])
		
                
        return neighbours
    
	
    def lowestNeighbour(self,r,c):
	#Retrieves the lowest neighbour by comparing elevations of the neighbours
				#r - rows, c - columns
				#calling getNeighbours() for each row and column / for each cell 
				#calling getElevation() in the iteration 
				#sets the index of neighbour [from getNeighbours()] to lownode, if
				#there is no lownode [to start the process] or
				#if the elevation of the current index is smaller then
				#the elevation of the index stored in lownode 
        lownode=None
        
        for neighbour in self.getNeighbours(r,c):
            if lownode==None or neighbour.getElevation() < lownode.getElevation():
                lownode=neighbour
        
        return lownode

	
    def setDownCells(self):
	#calculates the lowest cells in the whole dataset
				#calling lowestNeighbour()
				#iterates through all rows and columns 
				#set the lowest neighbour of all columns covered by the current iteration
				#if the elevation of neighbour is smaller then the elevation of the data at the same node, then
				#call setDownnode() and set this node as a downnode (lowest point)
       for r in range(self.getRows()):
           for c in range(self.getCols()):
               lowestN = self.lowestNeighbour(r,c)
               if (lowestN.getElevation() < self._data[r,c].getElevation()):
                   self._data[r,c].setDownnode(lowestN)
               else:
                   self._data[r,c].setDownnode(None)
    
    def extractValues(self, extractor):
	#Retrieves an array containing the values of 
	#the flow raster 
        values=[]
        for i in range(self._data.shape[0]):
            for j in range(self._data.shape[1]):
                values.append(extractor.getValue(self._data[i,j]))
        valuesarray=np.array(values)
        valuesarray.shape=self._data.shape
        return valuesarray

    
class FlowExtractor(FlowRaster):
    '''For Task2: A method which caluclates and plots the flow volume'''

    def __init__(self, givenRaster):
        super().__init__(givenRaster)
        self.nNodes = self.numUpnodes()

    def getValue(self):
	#Recursively summarize the values of all upnodes flowing down to the downnode 
				#For Task2, the rainfall is constant and every cell has value 1
				#Therefore, it's enough to summarize the amount of upnodes 
        
        for i in range(self.nNodes):
            print(i)
        fr = FlowRaster.extractValues(self)
        
        return self.nNodes
