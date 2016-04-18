#-*-<coding=UTF-8>-*-
'''
Created on 2015年12月25日

@author: O_O
'''
import alipy
import glob
import pyfits
import os

projectRoot="D:\\workspace_py\\"
srcImagePath=os.path.join(projectRoot,"images")
#也许改成*.& 就不用重命名了  不过还是重命名了好 省去不必要的麻烦
srcImageFileFilter=os.path.join(projectRoot,"images/*.fits")
ref_image =os.path.join(projectRoot,"ref", "X1_dupe-1.fits")
alipy_outdir=os.path.join(projectRoot,"alipy_out")
headFitsDir=os.path.join(projectRoot,"alipy_head")

def AlignFitsFileWithHeadMessage(srcImageFileFilter,ref_image,alipy_outdir,headFitsDir):
    #参数分别是 文件过滤 对齐用的基础文件 alipy的最终输出文件（不带head信息）  带有head信息的最终输出文件
    images_to_align = sorted(glob.glob(srcImageFileFilter))
    identifications = alipy.ident.run(ref_image, images_to_align,hdu=0, visu=True,sexkeepcat=False)
    # That's it !
    # Put visu=True to get visualizations in form of png files (nice but much slower)
    # On multi-extension data, you will want to specify the hdu (see API doc).
    
    # The output is a list of Identification objects, which contain the transforms :
    # for id in identifications: # list of the same length as images_to_align.
    #         if id.ok == True: # i.e., if it worked
    # 
    #                 print "%20s : %20s, flux ratio %.2f" % (id.ukn.name, id.trans, id.medfluxratio)
    #                 # id.trans is a alipy.star.SimpleTransform object. Instead of printing it out as a string,
    #                 # you can directly access its parameters :
    #                 #print id.trans.v # the raw data, [r*cos(theta)  r*sin(theta)  r*shift_x  r*shift_y]
    #                 #print id.trans.matrixform()
    #                 #print id.trans.inverse() # this returns a new SimpleTransform object
    # 
    #         else:
    #                 print "%20s : no transformation found !" % (id.ukn.name)
    
    # Minimal example of how to align images :
    
    outputshape = alipy.align.shape(ref_image)
    # This is simply a tuple (width, height)... you could specify any other shape.
    
    for id in identifications:
            if id.ok == True:
    
                    # Variant 1, using only scipy and the simple affine transorm :
                    alipy.align.affineremap(id.ukn.filepath, id.trans, shape=outputshape, makepng=True,outdir=alipy_outdir)
    
                    # Variant 2, using geomap/gregister, correcting also for distortions :
                    alipy.align.irafalign(id.ukn.filepath, id.uknmatchstars, id.refmatchstars, shape=outputshape, makepng=False,outdir=alipy_outdir)
                    # id.uknmatchstars and id.refmatchstars are simply lists of corresponding Star objects.
    
                    # By default, the aligned images are written into a directory "alipy_out".
    
                    #read and rewrite the Head
    for id in identifications:
            if id.ok == True:
                    #read and rewrite the Head
                    srcFitsFileName=os.path.basename(id.ukn.filepath)
                    imageHeader=pyfits.getheader(os.path.join(srcImagePath,srcFitsFileName))
                    #write JD into head 
                    imageDataFileName=os.path.join(alipy_outdir,os.path.splitext(srcFitsFileName)[0]+"_affineremap.fits")
                    imageData= pyfits.getdata(imageDataFileName)
    #                 imageHeader=pyfits.getheader("images/X1_dupe-2.fits")
                    
    #                 outdir=os.path.join(projectRoot,"alipy_head")
                    if not os.path.isdir(headFitsDir):
                        os.makedirs(headFitsDir)         
                    outfilename = os.path.join(headFitsDir, srcFitsFileName)
                    if os.path.isfile(outfilename):
                        os.remove(outfilename)
                    pyfits.writeto(outfilename, imageData, imageHeader)
                    
    # To be continued ...