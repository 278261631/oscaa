#-*-<coding=UTF-8>-*-
'''
Created on 2015年12月25日

@author: O_O
'''
import os
from alipy import imgcat
import oscaarGUI
import wx
import PyRenameFit
from oscaar import AlignFitsAlipy
# from oscaar import RunOsccarS

# 需要导出吗？ 导出一个公共的cat？ 目标star列表 ？
#还是根本不需要导出  直接拿公共区域 和 最亮的星星列表 直接位置比对就可以了？
#还是连公共区域都不用去管了？
#直接写下边的执行部分吧

projectRoot="D:\\workspace_py\\"
srcImagePath=os.path.join(projectRoot,"images")
#也许改成*.& 就不用重命名了  不过还是重命名了好 省去不必要的麻烦
srcImageFileFilter=os.path.join(projectRoot,"images/*.fits")
ref_image =os.path.join(projectRoot,"ref", "X1_dupe-1.fits")
alipy_outdir=os.path.join(projectRoot,"alipy_out")
headFitsDir=os.path.join(projectRoot,"alipy_head")



appRoot=os.path.abspath('.')
srcImagePath=headFitsDir
# images_to_align = sorted(glob.glob(os.path.join(srcImagePath,"*.fits")))
#修改fit 和 fts文件后缀为fits 包含所有目录
PyRenameFit.renameErrorFits(srcImagePath);   
#对其到输出目录  一般是alipy_head             
AlignFitsAlipy.AlignFitsFileWithHeadMessage(srcImageFileFilter, ref_image, alipy_outdir, headFitsDir)

# print '----------------------------------'
# fitsToCat = imgcat.ImgCat('D:/workspace_py/images/alipy_head/X1_dupe-1.fits', hdu=0)
# fitsToCat.makecat(rerun=True, keepcat=True, verbose=False)
# fitsToCat.makestarlist(skipsaturated=True, n=5, verbose=True)
# 
# print fitsToCat.starlist
# for starItem in fitsToCat.starlist:
# #     print starItem
#     print str(starItem.x) +"  :  "+ str(starItem.y) +"  :  "+ str(starItem.flux) +"  :  "+ str(starItem.fwhm)
print '----------------------------------'
fitsToCat = imgcat.ImgCat("D:/workspace_py/alipy_head/X1_dupe-5.fits", hdu=0)
fitsToCat.makecat(rerun=True, keepcat=True, verbose=False)
fitsToCat.makestarlist(skipsaturated=True, n=5, verbose=True)
fitsToCat = imgcat.ImgCat(ref_image, hdu=0)
fitsToCat.makecat(rerun=True, keepcat=True, verbose=False)
fitsToCat.makestarlist(skipsaturated=True, n=5, verbose=True)

def WriteDS9RegFile(initRegFilePath,x=0,y=0,r=20,xc=0,yc=0):
    '''
    x y 为星点坐标 
    xc yc 为比较星的坐标
    '''
    fileDirPath=os.path.dirname(initRegFilePath)
    if not os.path.exists(fileDirPath):
        os.mkdir(fileDirPath);
        
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
#     f.write("circle("+str(x)+","+str(y)+","+str(r)+")\n")
    f.write("circle(%d,%d,%d)\n"%(x,y,r))
    f.write("circle(%d,%d,%d)\n"%(xc,yc,r))
    f.close()
    print 'Finished'

def WriteInitParFile(initParFilePath,dataImageRoot,regFilePath,orignFitFilePath):
    dataImageFiles=""
    if os.path.exists(dataImageRoot):
        f = open(initParFilePath, "w")
        for  filePath in os.listdir(dataImageRoot):
            if filePath.lower().endswith(".fits"):
                dataImageFiles+=os.path.join(dataImageRoot,filePath)+","
#                 print filePath, 'ok'

            print ""
        f.write("Path to Dark Frames: D:\\workspace_py\\alignTest\\dark&bias\\20150305=-30c\\-30c--001bias.fits,D:\\workspace_py\\alignTest\\dark&bias\\20150305=-30c\\-30c--001dark_120s.fits,D:\\workspace_py\\alignTest\\dark&bias\\20150305=-30c\\-30c--001dark_60s.fits\n")
#         f.write("Path to Data Images: E:\\xiaolong\\alipy_out\\X1_dupe-1.fits,E:\\xiaolong\\alipy_out\\X1_dupe-2.fits,E:\\xiaolong\\alipy_out\\X1_dupe-3.fits,E:\\xiaolong\\alipy_out\\X1_dupe-4.fits,E:\\xiaolong\\alipy_out\\X1_dupe-5.fits\n")
        #last , 
        f.write("Path to Data Images: "+dataImageFiles+","+orignFitFilePath+"\n") 
        f.write("Path to Master-Flat Frame: D:\\workspace_py\\alignTest\\AutoFlat.fits\n")
#         f.write("Path to Regions File: E:\\xiaolong\\x1.reg,E:\\xiaolong\\alipy_out\\X1_dupe-1.fits;\n")
        f.write("Path to Regions File: "+regFilePath+","+orignFitFilePath+";\n")
        f.write("Output Path: D:\\workspace_py\\alignTest\\result.txt.pkl\n")
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
    else:
        print ""
        return;


print fitsToCat.starlist
###这里需要固定一张图里的比较星，因为必须有至少一颗比较星才可以运行OSCAAR 
####主星可以按照需求找出并生成
starX=fitsToCat.starlist[0].x
starY=fitsToCat.starlist[0].y
starXc=fitsToCat.starlist[1].x
starYc=fitsToCat.starlist[1].y
for starItem in fitsToCat.starlist:
#     
    print str(starItem.x) +"  :  "+ str(starItem.y) +"  :  "+ str(starItem.flux) +"  :  "+ str(starItem.fwhm)
    
# WriteDS9RegFile(os.path.join(appRoot,'hehe.reg'),starItem.x,starItem.y,)
WriteDS9RegFile(os.path.join(appRoot,'hehe.reg'),x=starX,y=starY,xc=starXc,yc=starYc)
WriteInitParFile(os.path.join(appRoot,'init.par'),srcImagePath,os.path.join(appRoot,'hehe.reg'),ref_image)
    
def RunOscaar():
    print '---------RunOscaar-----------'
    app=wx.App()
    mainFrame=oscaarGUI.OscaarFrame(None,-1)
    mainFrame.runButton.LabelText='xx';
    mainFrame.runOscaar(None)
    
    mainFrame.Close()
    app.MainLoop()
    
RunOscaar()
    
##还可以找出无法对其的星点 比较亮的 消失的 和新生的 或者移动的？ 通量大于3000？还是2000
#D:\ds9>ds9.exe D:\workspace_py\alipy_head\X1_dupe-1.fits  D:\workspace_py\alipy_head\X1_dupe-5.fits  -regions load all D:\workspaces\oscc\oscaar\hehe.reg -blink yes 

#可以用机器学习算法中的分类算法 或者判定是哪一类 是不是新星 （分类为 新星 移动 变亮 变暗 消失
#或者判定是否  新图对于标准图来说 新图上的某颗星 是否约等于标准图上的某颗 （还要计算是不是标准图一定通量以上的都找到了匹配星

#####训练数据可以从高那里要来之前被人点过和标记过的数据