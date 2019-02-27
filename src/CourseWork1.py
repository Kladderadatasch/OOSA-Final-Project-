from RasterHandler import createRanRasterSlope
from RasterHandler import readRaster
import matplotlib.pyplot as mp
import Flow as flow

def plotstreams(flownode,colour):
    for node in flownode.getUpnodes():
        x1=flownode.get_x()
        y1=flownode.get_y()
        x2=node.get_x()
        y2=node.get_y()
        mp.plot([x1,x2],[y1,y2],color=colour)
        if (node.numUpnodes()>0):
            plotstreams(node,colour)

def plotFlowNetwork(originalRaster, flowRaster, title="", plotLakes=True):
    print ("\n\n{}".format(title))
    mp.imshow(originalRaster._data)
    mp.colorbar()
    colouri=-1
    colours=["black","red","magenta","yellow","green","cyan","white","orange","grey","brown"]

    for i in range(flowRaster.getRows()):
        for j in range(flowRaster.getCols()):
            node = flowRaster._data[i,j]
            
            if (node.getPitFlag()): # dealing with a pit
                mp.scatter(node.get_x(),node.get_y(), color="red")
                colouri+=1
                plotstreams(node, colours[colouri%len(colours)])
                
            if (plotLakes and node.getLakeDepth() > 0):
                mp.scatter(node.get_x(),node.get_y(), color="blue")

    mp.show()

def plotExtractedData(flowRaster, extractor, title="", isRainFall = False):
    print ("\n\n{}".format(title))
    mp.imshow(flowRaster.extractValues(extractor, isR = isRainFall))
    mp.colorbar()
    mp.show()

def plotRaster(araster, title=""):
    print ("\n\n{}, shape is  {}".format(title, araster.shape))
    mp.imshow(araster)
    mp.colorbar()
    mp.show()


def calculateFlowsAndPlot(elevation, rain, resampleF):
    # plot input rasters
    plotRaster(elevation.getData(), "Original elevation (m)")
    plotRaster(rain.getData(), "Rainfall")
    resampledElevations = elevation.createWithIncreasedCellsize(resampleF)
    
    ################# step 1 find and plot the intial network #######
    '''
    1. From Raster import Raster
    2. Execute full code 
    '''
    
    fr=flow.FlowRaster(resampledElevations)
#    plotFlowNetwork(elevation, fr, "Network structure - before lakes", plotLakes=False)
    
    ################Step 2 ######################################
    '''
    Calculate flow volume
    Resursively call each up-node and add one each time
    Solution:  
        def getValue(self, node):
            return node.numUpnodes()
    '''
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - constant rain")
    
    ################# step 3 #######################################
    #handle variable rainfall
    ''' addRainfall function 
            not written in FlowRaster - need to add
        Either replace the numUpNodes()
            or implement 
                if(addRainfall == True): return x
                else(): return numUpNodes()
            in getValues() 
    '''
    fr.addRainfall(rain.getData())
    plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall", isRainFall = True)
    
    ############# step 4 and step 5 #######################################
    # handle lakes
	#fr.defineLakes()
    #fr.calculateLakes()
    #plotFlowNetwork(elevation, fr, "Network structure (i.e. watersheds) - with lakes")
    #plotExtractedData(fr, flow.LakeDepthExtractor(), "Lake depth")
    #plotExtractedData(fr, flow.FlowExtractor(), "River flow rates - variable rainfall")


############# step 1 to 4 #######################################
# Create Random Raster
rows=40
cols=60
xorg=0.
yorg=0.
xp=5
yp=5
nodata=-999.999
cellsize=1.
levels=4
datahi=100.
datalow=0
randpercent=0.2
    
resampleFactorA = 1
elevationRasterA=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)   
rainrasterA=createRanRasterSlope(rows//resampleFactorA,cols//resampleFactorA,cellsize*resampleFactorA,xorg,yorg,nodata,levels,4000,1,36,4,.1)   

calculateFlowsAndPlot(elevationRasterA, rainrasterA, resampleFactorA)

############# step 5 #######################################
#calculateFlowsAndPlot(readRaster('../data/dem_hack.txt'), readRaster('../data/rain_small_hack.txt'), 10)



