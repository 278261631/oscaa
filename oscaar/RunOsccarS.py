import os
import wx
# import oscaar.oscaarGUI
from win32file import CreateFile
import oscaarGUI
from numpy.distutils.fcompiler import none

path = 'E:\\xiaolong'
appRoot=os.path.abspath('.')
print appRoot
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
# renameErrorFits(path)

        
        

def WriteInitParFile(initParFilePath):
    if os.path.isfile(initParFilePath):
        f = open(initParFilePath, "r")
        print f.read()
        f.close()
        print initParFilePath
    else:
        print ''
    f = open(initParFilePath, "w")
    f.write("Path to Dark Frames: E:\\as\\dark&bias\\20150305=-30c\\-30c--001bias.fits,E:\\as\\dark&bias\\20150305=-30c\\-30c--001dark_120s.fits,E:\\as\\dark&bias\\20150305=-30c\\-30c--001dark_60s.fits\n")
    f.write("Path to Data Images: E:\\xiaolong\\alipy_out\\X1_dupe-1.fits,E:\\xiaolong\\alipy_out\\X1_dupe-2.fits,E:\\xiaolong\\alipy_out\\X1_dupe-3.fits,E:\\xiaolong\\alipy_out\\X1_dupe-4.fits,E:\\xiaolong\\alipy_out\\X1_dupe-5.fits\n")
    f.write("Path to Master-Flat Frame: E:\\as\\AutoFlat.fits\n")
    f.write("Path to Regions File: E:\\xiaolong\\x1.reg,E:\\xiaolong\\alipy_out\\X1_dupe-1.fits;\n")
    f.write("Output Path: E:\\xiaolong\\result.txt.pkl\n")
    f.write("Ingress: 2013-05-15 ; 10:06:30\n")
    f.write("Egress: 2013-05-15 ; 11:02:35\n")
    f.write("Plot Tracking: on\n")
    f.write("Plot Photometry: on\n")
    f.write("Smoothing Constant: 3\n")
    f.write("Radius: 4.5\n")
    f.write("Tracking Zoom: 15\n")
    f.write("CCD Gain: 1.0\n")
    f.write("Exposure Time Keyword: DATE-OBS\n")
    f.close()
    print 'Finished'
# print '---------' 
#write init.par
initParFilePath=os.path.join(appRoot,'initTest.par')
print initParFilePath
# initParFilePath='D:\\workspace_py\\oscc\\oscaar\\init.par'
WriteInitParFile(initParFilePath)
#write region file
initRegFilePath=os.path.join(appRoot,'ds9.reg')
def WriteDS9RegFile(initRegFilePath):
    if os.path.isfile(initRegFilePath):
        f = open(initRegFilePath, "r")
        print f.read()
        f.close()
        print initRegFilePath
    else:
        print ''
    f = open(initRegFilePath, "w")
    f.write("# Region file format: DS9 version 4.1\n")
    f.write("global color=green dashlist=8 3 width=1 font=\"helvetica 10 normal roman\" select=1 highlite=1 dash=0 fixed=0 edit=1 move=1 delete=1 include=1 source=1\n")
    f.write("physical\n")
    f.write("circle(136,136,20)\n")
    f.close()
    print 'Finished'
print initRegFilePath
WriteDS9RegFile(initRegFilePath)


##align 


def ExportStartList():
    print ''
    
ExportStartList()
#start oscaar

def RunOscaar():
    print '---------RunOscaar-----------'
    app=wx.App()
    mainFrame=oscaarGUI.OscaarFrame(None,-1)
#     mainFrame.runButton.LabelText='xx';
#     mainFrame.runOscaar(None)
    
#     mainFrame.Close()
    app.MainLoop()
    
RunOscaar()
