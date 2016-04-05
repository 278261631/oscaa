#-*-<coding=UTF-8>-*-
'''
Created on 2015年12月25日

@author: O_O
'''
import alipy
import glob
import pyfits
import os

# images_to_align = sorted(glob.glob("E:/xiaolong/xximages/*.fits"))
imagePathRoot="D:\\workspace_py\\alignTest\\images\\"
images_to_align = sorted(glob.glob(os.path.join(imagePathRoot,"*.fits")))
ref_image = "D:\\workspace_py\\alignTest\\images\\X1_dupe-1.fits"
imgOutPath=os.path.join(imagePathRoot,'alipy_out')

identifications = alipy.ident.run(ref_image, images_to_align,hdu=0, visu=False,sexkeepcat=True)
# That's it !
# Put visu=True to get visualizations in form of png files (nice but much slower)
# On multi-extension data, you will want to specify the hdu (see API doc).

# The output is a list of Identification objects, which contain the transforms :
for id in identifications: # list of the same length as images_to_align.
        if id.ok == True: # i.e., if it worked

                print "%20s : %20s, flux ratio %.2f" % (id.ukn.name, id.trans, id.medfluxratio)
                # id.trans is a alipy.star.SimpleTransform object. Instead of printing it out as a string,
                # you can directly access its parameters :
                #print id.trans.v # the raw data, [r*cos(theta)  r*sin(theta)  r*shift_x  r*shift_y]
                #print id.trans.matrixform()
                #print id.trans.inverse() # this returns a new SimpleTransform object

        else:
                print "%20s : no transformation found !" % (id.ukn.name)

# Minimal example of how to align images :

outputshape = alipy.align.shape(ref_image)
# This is simply a tuple (width, height)... you could specify any other shape.

for id in identifications:
        if id.ok == True:

                # Variant 1, using only scipy and the simple affine transorm :
                alipy.align.affineremap(id.ukn.filepath, id.trans, shape=outputshape, makepng=True ,outdir=imgOutPath)

                # Variant 2, using geomap/gregister, correcting also for distortions :
                alipy.align.irafalign(id.ukn.filepath, id.uknmatchstars, id.refmatchstars, shape=outputshape, makepng=False,outdir=imgOutPath)
                print '--------'+ imgOutPath
                # id.uknmatchstars and id.refmatchstars are simply lists of corresponding Star objects.

                # By default, the aligned images are written into a directory "alipy_out".

                #read and rewrite the Head
appPath=os.path.abspath('.')
print os.path.join(appPath,'images','f.fits')
for id in identifications:
        if id.ok == True:
                #read and rewrite the Head
                srcFitsFileName=os.path.basename(id.ukn.filepath)
#                 imageHeader=pyfits.getheader("images/"+srcFitsFileName)
                imageHeader=pyfits.getheader(os.path.join(imagePathRoot,srcFitsFileName))
                #write JD into head 
                imageDataSrcDir=imgOutPath
                imageDataFileName=os.path.join(imageDataSrcDir,os.path.splitext(srcFitsFileName)[0]+"_affineremap.fits")
                imageData= pyfits.getdata(imageDataFileName)
#                 imageHeader=pyfits.getheader("images/X1_dupe-2.fits")
                
                outdir=os.path.join(imagePathRoot, "head_")
                if not os.path.isdir(outdir):
                    os.makedirs(outdir)         
                outfilename = os.path.join(outdir, srcFitsFileName)
                if os.path.isfile(outfilename):
                    os.remove(outfilename)
                pyfits.writeto(outfilename, imageData, imageHeader)
                
# To be continued ...