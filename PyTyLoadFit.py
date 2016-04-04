'''
Created on 

@author: 


'''
import os
import pyfits
path = 'E:\\as\\AutoFlat'
errorFiles=[]
def renameErrorFits(path):
    for fileName in os.listdir(path):
        filePath=os.path.join(path, fileName)
        if os.path.isfile(filePath):
            if fileName.lower().endswith(".fits"):
                try:
                    fitsData=pyfits.open(filePath)[0].data
                    print filePath, '         ok'
                except:
#                     newname = fileName.replace(".fits", ".fitsError")
#                     os.rename(os.path.join(path, fileName), os.path.join(path, newname))
#                     copyfile(os.path.join(path, fileName), os.path.join(path, newname))
#                     os.remove(os.path.join(path, fileName))
                    errorFiles.append(filePath)
                    print filePath,'        Err'
        elif os.path.isdir(os.path.join(path, fileName)):
            print os.path.join(path, fileName)
            renameErrorFits(os.path.join(path, fileName))
renameErrorFits(path)
print errorFiles
for errFile in errorFiles:
    print errFile
    os.rename(errFile, errFile.replace('.fits','.fitsError'))        
#        print fileName.split('.')[-1] 