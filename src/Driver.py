from RasterHandler import createRanRasterSlope
from RasterHandler import readRaster
import matplotlib.pyplot as mp
from Flow import FlowRaster
from Flow import FlowNode

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
    
    resampleFactorA = 1
    
    raster=createRanRasterSlope(rows,cols,cellsize,xorg,yorg,nodata,levels,datahi,datalow,xp,yp,randpercent)        
    data=raster.getData()
    rainraster=createRanRasterSlope(rows//resampleFactorA,cols//resampleFactorA,cellsize*resampleFactorA,xorg,yorg,nodata,levels,4000,1,36,4,.1)   


    return raster, data, rainraster


FLOW, DAT, RAIN=createRaster()
FLOW = FlowRaster(FLOW)
FLOW.setDownCells()

FLOW.addRainfall(RAIN.getData())
FLOW._data

mp.matshow(DAT)
mp.colorbar()


POINTS = FLOW.getPointList()

#################################################################
#################################################################

#Somehow this function enables to use get_x()
#and get_y() as well as getDownnode()
for p in POINTS:
    mp.scatter(p.get_x(),p.get_y(), color='yellow')
    
    if (p.getDownnode()!=None):
        x1=p.get_x()
        y1=p.get_y()
        x2=p.getDownnode().get_x()
        y2=p.getDownnode().get_y()
        mp.plot([x1,x2],[y1,y2],color="black")

mp.show()

###################################################################
###################################################################

upList = []
for p in POINTS:
    upList.append(p.numUpnodes())

print(POINTS[0]._data)
