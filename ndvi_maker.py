#!/usr/bin/env python
"""
author: Trokhymenko Viktor
e-mail: trokhymenkoviktor@gmail.com
program: ndvi_maker
version: 1.0
data: 05/2017
"""

#to excec
#scenario/ndvi_maker.py pwd

import sys
import os #https://pythonworld.ru/moduli/modul-os.html http://pythoner.name/file-system  
import glob #list all files of a directory
from osgeo import gdal
import json
from pprint import pprint
import numpy as np

import other_moduls as om
#https://wombat.org.ua/AByteOfPython/first_steps.html

def cut(satellite,ll1,ll2,ur1,ur2):
    if satellite=='S2A':

        os.chdir('{}'.format(glob.glob('L1C*')[0]))
        os.chdir('IMG_DATA');   

        b02_jp2=glob.glob('*_B02.jp2')[0]
        b03_jp2=glob.glob('*_B03.jp2')[0]
        b04_jp2=glob.glob('*_B04.jp2')[0]
        b08_jp2=glob.glob('*_B08.jp2')[0]
        
        cmd_b02_cuted='gdalwarp -te {} {} {} {} {} {}cuted.jp2'.format(ll1,ll2,ur1,ur2, b02_jp2, b02_jp2[:len(b02_jp2)-3])
        os.system(cmd_b02_cuted)
        cmd_b03_cuted='gdalwarp -te {} {} {} {} {} {}cuted.jp2'.format(ll1,ll2,ur1,ur2, b03_jp2, b03_jp2[:len(b03_jp2)-3])
        os.system(cmd_b03_cuted)
        cmd_b04_cuted='gdalwarp -te {} {} {} {} {} {}cuted.jp2'.format(ll1,ll2,ur1,ur2, b04_jp2, b04_jp2[:len(b04_jp2)-3])
        os.system(cmd_b04_cuted)
        cmd_b08_cuted='gdalwarp -te {} {} {} {} {} {}cuted.jp2'.format(ll1,ll2,ur1,ur2, b08_jp2, b08_jp2[:len(b08_jp2)-3])
        os.system(cmd_b08_cuted)

        b02_cuted_jp2=glob.glob('*_B02.cuted.jp2')[0]
        b03_cuted_jp2=glob.glob('*_B03.cuted.jp2')[0]
        b04_cuted_jp2=glob.glob('*_B04.cuted.jp2')[0]
        b08_cuted_jp2=glob.glob('*_B08.cuted.jp2')[0]
        
        cmd_b02_tif='gdal_translate -of GTiff {} {}tif'.format(b02_cuted_jp2, b02_cuted_jp2[:len(b02_cuted_jp2)-9])
        os.system(cmd_b02_tif)
        cmd_b03_tif='gdal_translate -of GTiff {} {}tif'.format(b03_cuted_jp2, b03_cuted_jp2[:len(b03_cuted_jp2)-9])
        os.system(cmd_b03_tif)
        cmd_b04_tif='gdal_translate -of GTiff {} {}tif'.format(b04_cuted_jp2, b04_cuted_jp2[:len(b04_cuted_jp2)-9])
        os.system(cmd_b04_tif)
        cmd_b08_tif='gdal_translate -of GTiff {} {}tif'.format(b08_cuted_jp2, b08_cuted_jp2[:len(b08_cuted_jp2)-9])
        os.system(cmd_b08_tif)
        
        cmd_5='rm {} {} {} {}'.format(b02_cuted_jp2,b03_cuted_jp2,b04_cuted_jp2,b08_cuted_jp2)
        os.system(cmd_5)
        
        #os.chdir('..')
    elif satellite=='LC08':
        os.chdir('{}'.format(glob.glob('LC08*')[0]))

        b2=glob.glob('*_B2.TIF')[0]
        b3=glob.glob('*_B3.TIF')[0]
        b4=glob.glob('*_B4.TIF')[0]
        b5=glob.glob('*_B5.TIF')[0]
        b8=glob.glob('*_B8.TIF')[0]
        
        cmd_b2='gdalwarp -te {} {} {} {} {} {}cut.tif'.format(ll1,ll2,ur1,ur2, b2, b2[:len(b2)-3])
        os.system(cmd_b2)
        cmd_b3='gdalwarp -te {} {} {} {} {} {}cut.tif'.format(ll1,ll2,ur1,ur2, b3, b3[:len(b3)-3])
        os.system(cmd_b3)
        cmd_b4='gdalwarp -te {} {} {} {} {} {}cut.tif'.format(ll1,ll2,ur1,ur2, b4, b4[:len(b4)-3])
        os.system(cmd_b4)
        cmd_b5='gdalwarp -te {} {} {} {} {} {}cut.tif'.format(ll1,ll2,ur1,ur2, b5, b5[:len(b5)-3])
        os.system(cmd_b5)
        cmd_b8='gdalwarp -te {} {} {} {} {} {}cut.tif'.format(ll1,ll2,ur1,ur2, b8, b8[:len(b8)-3])
        os.system(cmd_b8)

        #os.chdir('..')          
    else:
        print 'Errordone cute'    
    print 'cut done!'

def create_ndvi(satellite):
    if satellite=='S2A':
        #os.chdir('{}'.format(glob.glob('L1C*')[0]))
        #os.chdir('IMG_DATA');   
        
        b04_ndvi=glob.glob('*_B04.tif')[0]
        b08_ndvi=glob.glob('*_B08.tif')[0]
        
        cmd_ndvi='gdal_calc.py -A {}tif -B {}tif --outfile={}NDVI.TIF --calc="((((A.astype(float)-B.astype(float))/(A.astype(float)+B.astype(float))))*255)" --type=Byte'.format(b08_ndvi[:len(b08_ndvi)-3], b04_ndvi[:len(b04_ndvi)-3], b08_ndvi[:len(b08_ndvi)-7])
        os.system(cmd_ndvi)
        
        #bs2a_ndvi=glob.glob('*_NDVI.TIF')[0]
        cdm_add_lut='python {}add_lut.py {}cm2.lut {}NDVI.TIF'.format(system_dir, system_dir, b08_ndvi[:len(b08_ndvi)-7])
        os.system(cdm_add_lut)
        
        #os.chdir('..')
    elif satellite=='LC08':
        #os.chdir('{}'.format(glob.glob('LC8*')[0]))
        
        #Warping to 15 meters
        b2_cut_warp=glob.glob('*_B2.cut.tif')[0]
        b3_cut_warp=glob.glob('*_B3.cut.tif')[0]
        b4_cut_warp=glob.glob('*_B4.cut.tif')[0]
        b5_cut_warp=glob.glob('*_B5.cut.tif')[0]
        b8_cut_warp=glob.glob('*_B8.cut.tif')[0]
        
        cmd_b2_warp='gdalwarp -tr 15 15 {} {}15.tif'.format(b2_cut_warp,b2_cut_warp[:len(b2_cut_warp)-3])
        os.system(cmd_b2_warp)
        cmd_b3_warp='gdalwarp -tr 15 15 {} {}15.tif'.format(b3_cut_warp,b3_cut_warp[:len(b3_cut_warp)-3])
        os.system(cmd_b3_warp)
        cmd_b4_warp='gdalwarp -tr 15 15 {} {}15.tif'.format(b4_cut_warp,b4_cut_warp[:len(b4_cut_warp)-3])
        os.system(cmd_b4_warp)
        cmd_b5_warp='gdalwarp -tr 15 15 {} {}15.tif'.format(b5_cut_warp,b5_cut_warp[:len(b5_cut_warp)-3])
        os.system(cmd_b5_warp)
        cmd_b8_warp='gdalwarp -tr 15 15 {} {}15.tif'.format(b8_cut_warp,b8_cut_warp[:len(b8_cut_warp)-3])
        os.system(cmd_b8_warp)
        
        #PanSharpening R+G+B+NIR, for making LC8 30to15 meters
        b2_cut_warp_15=glob.glob('*_B2.cut.15.tif')[0]
        b3_cut_warp_15=glob.glob('*_B3.cut.15.tif')[0]
        b4_cut_warp_15=glob.glob('*_B4.cut.15.tif')[0]
        b5_cut_warp_15=glob.glob('*_B5.cut.15.tif')[0]
        b8_cut_warp_15=glob.glob('*_B8.cut.15.tif')[0]
                                                            
        #cmd_redPan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=RedPan.TIF --calc="(D.astype(float)*A.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b4_cut_warp_15, b3_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15)
        cmd_redPan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=RedPan.TIF --calc="(D.astype(float)*A.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b4_cut_warp_15, b3_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15)
        os.system(cmd_redPan)
        
        #cmd_greenPlan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=GreenPan.TIF --calc="(D.astype(float)*A.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b3_cut_warp_15, b4_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15)
        #os.system(cmd_greenPlan)
        #cmd_bluePlan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=BluePan.TIF --calc="(D.astype(float)*A.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b2_cut_warp_15, b3_cut_warp_15, b4_cut_warp_15, b8_cut_warp_15)
        #os.system(cmd_bluePlan)
        
        #cmd_nirPan='gdal_calc.py -A {} -B {} -C {} -D {} -E {} --outfile=NIRPan.TIF --calc="(D.astype(float)*E.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b2_cut_warp_15, b3_cut_warp_15, b4_cut_warp_15, b8_cut_warp_15, b5_cut_warp_15)
        cmd_nirPan='gdal_calc.py -A {} -B {} -C {} -D {} -E {} --outfile=NIRPan.TIF --calc="(D.astype(float)*E.astype(float))/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b4_cut_warp_15, b3_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15, b5_cut_warp_15)
        os.system(cmd_nirPan)
        
        #cmd_toaPlan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=TOAPan.TIF --calc="(D.astype(float)*10000)/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b4_cut_warp_15, b3_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15)
        cmd_toaPlan='gdal_calc.py -A {} -B {} -C {} -D {} --outfile=TOAPan.TIF --calc="(D.astype(float)*10000)/(A.astype(float)+B.astype(float)+C.astype(float))" --type=Int16'.format(b4_cut_warp_15, b3_cut_warp_15, b2_cut_warp_15, b8_cut_warp_15)
        os.system(cmd_toaPlan)                                                    
        
        cmd_ndvi='gdal_calc.py -A NIRPan.TIF -B RedPan.TIF -C TOAPan.TIF --outfile={}NDVI.TIF --calc="((((A.astype(float)-B.astype(float))/(A.astype(float)+B.astype(float)-C.astype(float))))*255)" --type=Byte'.format(b8_cut_warp_15[:len(b8_cut_warp_15)-13])
        os.system(cmd_ndvi) 
        
        cdm_add_lut='python {}add_lut.py {}cm2.lut {}NDVI.TIF'.format(system_dir, system_dir, b8_cut_warp_15[:len(b8_cut_warp_15)-13])
        os.system(cdm_add_lut)
        
        #delete
        cmd_6='rm {} {} {} {} {} RedPan.TIF NIRPan.TIF TOAPan.TIF'.format(b2_cut_warp,b3_cut_warp,b4_cut_warp,b5_cut_warp,b8_cut_warp)
        os.system(cmd_6)
                
        #os.chdir('..')          
    else:
        print 'Error done ndvi'    
    print 'ndvi done!'


def create_rgb(satellite):
    if satellite=='S2A':
        #os.chdir('{}'.format(glob.glob('L1C*')[0]))
        #os.chdir('IMG_DATA');   
        
        b02_rgb=glob.glob('*_B02.tif')[0]
        b03_rgb=glob.glob('*_B03.tif')[0]
        b04_rgb=glob.glob('*_B04.tif')[0]
        
        cmd_b02_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b02_rgb[:len(b02_rgb)-3],b02_rgb[:len(b02_rgb)-3])
        os.system(cmd_b02_rgb)
        cmd_b03_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b03_rgb[:len(b03_rgb)-3],b03_rgb[:len(b03_rgb)-3])
        os.system(cmd_b03_rgb)
        cmd_b04_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b04_rgb[:len(b04_rgb)-3],b04_rgb[:len(b04_rgb)-3])
        os.system(cmd_b04_rgb)
        
        b02_02_rgb=glob.glob('*_B02.02.tif')[0]
        b03_02_rgb=glob.glob('*_B03.02.tif')[0]
        b04_02_rgb=glob.glob('*_B04.02.tif')[0]
        
        cmd_rgb_k='gdal_merge.py -of GTiff -o {}RGB_k.tif -separate {} {} {}'.format(b02_rgb[:len(b02_rgb)-7], b04_02_rgb,b03_02_rgb,b02_02_rgb)
        os.system(cmd_rgb_k)        
        
        #gdal_translate for bands
        rgb=glob.glob('*_RGB_k.tif')[0]
        ds=gdal.Open(rgb)          
        el1=ds.GetRasterBand(1).ReadAsArray()
        el2=ds.GetRasterBand(2).ReadAsArray()
        el3=ds.GetRasterBand(3).ReadAsArray()
        cmd_rgb='gdal_translate -of GTiff -ot Byte -b 1 -scale {} {} -b 2 -scale {} {} -b 3 -scale {} {} {}RGB_k.tif {}RGB.TIF'.format(el1.min()+5,el1.max()-5, el2.min()+5,el2.max()-5, el3.min()+5,el3.max()-5, b02_rgb[:len(b02_rgb)-7],b02_rgb[:len(b02_rgb)-7])
        os.system(cmd_rgb) 
        
        #delete
        cmd_6='rm {} {} {} {}RGB_k.tif *.xml'.format(b02_02_rgb,b03_02_rgb,b04_02_rgb,b02_rgb[:len(b02_rgb)-7])
        os.system(cmd_6)
        
        #os.chdir('..')
    elif satellite=='LC08': 
        #os.chdir('{}'.format(glob.glob('LC8*')[0]))
            
        b2_cut_warp_15=glob.glob('*_B2.cut.15.tif')[0]
        b3_cut_warp_15=glob.glob('*_B3.cut.15.tif')[0]
        b4_cut_warp_15=glob.glob('*_B4.cut.15.tif')[0]
        b5_cut_warp_15=glob.glob('*_B5.cut.15.tif')[0]
        b8_cut_warp_15=glob.glob('*_B8.cut.15.tif')[0]
        
        
        cmd_b2_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b2_cut_warp_15[:len(b2_cut_warp_15)-3],b2_cut_warp_15[:len(b2_cut_warp_15)-3])
        os.system(cmd_b2_rgb)
        cmd_b3_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b3_cut_warp_15[:len(b3_cut_warp_15)-3],b3_cut_warp_15[:len(b3_cut_warp_15)-3])
        os.system(cmd_b3_rgb)
        cmd_b4_rgb='gdal_translate -scale {} {} {}tif {}02.tif'.format(MinScale1,MaxScale1, b4_cut_warp_15[:len(b4_cut_warp_15)-3],b4_cut_warp_15[:len(b4_cut_warp_15)-3])
        os.system(cmd_b4_rgb)
        
        b2_02_rgb=glob.glob('*_B2.cut.15.02.tif')[0]
        b3_02_rgb=glob.glob('*_B3.cut.15.02.tif')[0]
        b4_02_rgb=glob.glob('*_B4.cut.15.02.tif')[0]
        
        cmd_rgb_k='gdal_merge.py -of GTiff -o {}RGB_k.tif -separate {} {} {}'.format(b2_02_rgb[:len(b2_02_rgb)-16], b4_02_rgb,b3_02_rgb,b2_02_rgb)
        os.system(cmd_rgb_k)        
        
        #gdal_translate for bands
        rgb=glob.glob('*_RGB_k.tif')[0]
        ds=gdal.Open(rgb)          
        el1=ds.GetRasterBand(1).ReadAsArray()
        el2=ds.GetRasterBand(2).ReadAsArray()
        el3=ds.GetRasterBand(3).ReadAsArray()
        cmd_rgb='gdal_translate -of GTiff -ot Byte -b 1 -scale {} {} -b 2 -scale {} {} -b 3 -scale {} {} {}RGB_k.tif {}RGB.TIF'.format(el1.min()+5,el1.max()-5, el2.min()+5,el2.max()-5, el3.min()+5,el3.max()-5, b2_02_rgb[:len(b2_02_rgb)-16],b2_02_rgb[:len(b2_02_rgb)-16])
        os.system(cmd_rgb)  
        
        #delete
        cmd_7='rm {} {} {} {} {}'.format(b2_cut_warp_15,b3_cut_warp_15,b4_cut_warp_15,b5_cut_warp_15,b8_cut_warp_15)
        os.system(cmd_7)        
        cmd_8='rm {} {} {} {}RGB_k.tif *.xml'.format(b2_02_rgb,b3_02_rgb,b4_02_rgb,b2_02_rgb[:len(b2_02_rgb)-16])
        os.system(cmd_8)
        
        #os.chdir('..')          
    else:
        print 'Error done rgb'    
    print 'rgb done!'

#------------------------------------------------------------
if __name__ == '__main__':
	#chmod a+x ndvi_maker.py 

	pwd=sys.argv[1]
	os.chdir(sys.argv[1])
	system_dir = '/home/admin-pc/scenario/'
	MinScale1 = 0;  #RGB min for 1-lvl scaling S2A
	MaxScale1 = 2550; #RGB max for 1-lvl scaling S2A

	#-------------------------------
	#farm identification & satellite 
	farm=glob.glob('*.json')[0]
	farm=farm[:2]

	if glob.glob('LC08*'):
	    satellite='LC08'
	    #folder_satellite=glob.glob('LC8*')[0]
	elif glob.glob('L1C*'):
	    satellite='S2A'
	    #folder_satellite=glob.glob('L1C*')[0]
	else:
	    print 'No satellite data directory'
	#-------------------------------	
	
	#-------------------------------
	#find utmZone reading mtl
	if satellite=='S2A':
	    os.chdir('{}'.format(glob.glob('L1C*')[0]))
	    
	    with open('{}'.format(glob.glob('*.xml')[0])) as file_mtd:
	        for i,line in enumerate(file_mtd):
	            if i==16:
	                utmZone=line   
	    utm=utmZone[43:45]
	    print 'utm='+utm  
	    
	    os.chdir('..')
	elif satellite=='LC08':	    
	    os.chdir('{}'.format(glob.glob('LC08*')[0]))
	    
	    utmZone=''
	    with open('{}'.format(glob.glob('*MTL.txt')[0])) as file_mtd:
	        for i,line in enumerate(file_mtd):
	            if i==216:
	                utmZone=line

	    utm=utmZone[15:17]  
	    print 'utm='+utm  
	    
	    os.chdir('..')    
	else:
	    print 'Error'	
	#-------------------------------

	#-------------------------------
	#conversion & searchCoordinates 
	#ll1,ll2,ur1,ur2=om.Conversion_searchCoordinates(farm,utm,pwd)
	ll1,ll2,ur1,ur2=om.Conversion_searchCoordinates_new(farm,utm,pwd)
	#-------------------------------

	#-------------------------------
	#cutting tiles & create rgb & create rgb
	cut(satellite,ll1,ll2,ur1,ur2)
	create_ndvi(satellite)
	create_rgb(satellite)
	#-------------------------------

	print '='*20
	print 'maker done!'
	print '='*20