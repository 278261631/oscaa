'''
Created on 

@author: 


'''
import os
path = 'E:\\xiaolong'
def renameErrorFits(path):
    for fileName in os.listdir(path):
        if os.path.isfile(os.path.join(path, fileName)):
            if fileName.lower().endswith(".fts"):
                newname = fileName.replace(".fts", ".fits")
                os.rename(os.path.join(path, fileName), os.path.join(path, newname))
                print fileName, 'ok'
            elif fileName.lower().endswith(".fit"):
                newname = fileName.replace(".fit", ".fits")
                os.rename(os.path.join(path, fileName), os.path.join(path, newname))
                print fileName, 'ok'
        elif os.path.isdir(os.path.join(path, fileName)):
            renameErrorFits(os.path.join(path, fileName))
            print 'hehe'
renameErrorFits(path)
        
#        print fileName.split('.')[-1] 