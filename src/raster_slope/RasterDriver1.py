from RasterHandler import readRaster
from Raster import Raster
import matplotlib.pyplot as mp

raster=readRaster("M:\\Teaching\\OOSA\\2018\\week_4_Raster_Flow_NN\\code for teachers\\raster_test2.txt")

data=raster.getData()

print (data)
        
mp.imshow(data)
mp.colorbar()
mp.matshow(data)
mp.colorbar()

mp.show()