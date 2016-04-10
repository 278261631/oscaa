#-*-<coding=UTF-8>-*-
'''
Created on 2015年12月25日

@author: O_O
'''
import alipy
import glob
import pyfits
import os
from alipy import imgcat

# 需要导出吗？ 导出一个公共的cat？ 目标star列表 ？
#还是根本不需要导出  直接拿公共区域 和 最亮的星星列表 直接位置比对就可以了？
#还是连公共区域都不用去管了？
#直接写下边的执行部分吧
                
print '----------------------------------'
fitsToCat = imgcat.ImgCat('D:/workspace_py/alignTest/images/head_/X1_dupe-1.fits', hdu=0)
fitsToCat.makecat(rerun=True, keepcat=True, verbose=False)
fitsToCat.makestarlist(skipsaturated=True, n=5, verbose=True)

print fitsToCat.starlist
for starItem in fitsToCat.starlist:
#     print starItem
    print str(starItem.x) +"  :  "+ str(starItem.y) +"  :  "+ str(starItem.flux) +"  :  "+ str(starItem.fwhm)
print '----------------------------------'
fitsToCat = imgcat.ImgCat('D:/workspace_py/alignTest/images/head_/X1_dupe-5.fits', hdu=0)
fitsToCat.makecat(rerun=True, keepcat=True, verbose=False)
fitsToCat.makestarlist(skipsaturated=True, n=5, verbose=True)

print fitsToCat.starlist
for starItem in fitsToCat.starlist:
    print str(starItem.x) +"  :  "+ str(starItem.y) +"  :  "+ str(starItem.flux) +"  :  "+ str(starItem.fwhm)