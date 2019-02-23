from RasterHandler import createRanRasterSlope
import matplotlib.pyplot as mp
from Flow import FlowRaster

def createRaster():

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
    
    raster=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)        
    data=raster.getData()

    return raster, data

#mp.matshow(data)
#mp.colorbar()

FLOW, DAT=createRaster()
FLOW = FlowRaster(FLOW)
FLOW.setDownCells()

POINTS = FLOW.getPointList()

DOWNNODE = FLOW.getDownnode()

