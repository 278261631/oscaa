'''
Created on 

@author: 
'''
import numpy as np
import pyfits
fitsData=pyfits.open('E:\\as\\20151022\\20151022-17.0H31.03D\\17.0H31.03D~9P+A1.fits')[0].data
print fitsData
# E:\as\20151022\20151022-17.0H31.03D
# [dim1, dim2] = np.shape(pyfits.open('E:\\as\\AutoFlat\\AutoFlat-20150419-Dusk-Green-Bin1-001.fits')[0].data)