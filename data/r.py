#!/usr/bin/env python

#
#  create SJFZ_Fangetal2019_VpandVs_clean.csv
#  from Fang_19_new.csv created by Hao
#  eliminate entry that is NA and also entry that got shifted out 
#  beyond 31.5km
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import os
import pdb
import math

dimension_x =  94
dimension_y =  73
dimension_z =  64

def usage():
    print("\n./rework_fang_data.py\n\n")
    sys.exit(0)

def main():
    total_count=dimension_x * dimension_y * dimension_z
    layer_count=dimension_x * dimension_y

    f_old=open('FangModel/Fang_19_new.csv','r')
    olds=f_old.readlines()
    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')


## get shift index    
## should be 94 x 73
    surf_list=[]

#    f_surf=open('FangModel/surfs','r')
    f_surf=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        dif=0
        sur=float(s.strip())
        surf_list.append(sur)
    f_surf.close()
    print("max surf ",max(surf_list))
    print("min surf ",min(surf_list))

# shift, positive shift/shift down
#        negative z/shift  up
#          current value + (500)* shift

    header=1
    valid_cnt=0

    layer_i=0;
    track_arr = array.array('f', (-9999.0,) * (layer_count))
    for oline in olds:
        ## copy header
        if(header) : ## skip first line 
          nline="longitude,latitude,depth,Vp,Vs\n"
          f_new.write(nline)
          header=0
          continue
#latitude,longitude,depth,Vp,Vs
#32.38,-118.17,-1.5,nan,nan
#to
#longitude,latitude,depth,Vp,Vs
#-118.17,32.38,-1.5,-9.999,-9.999
        l=oline.split(",")
        if(l[3] != "nan" and track_arr[layer_i] == -9999.0) : 
## valid point
          f_new.write(oline)
          oldz=float(l[2])
          track_arr[layer_i]=oldz
        layer_i = layer_i + 1
        if(layer_i >= layer_count):
          layer_i=0

    print("max layer ",max(track_arr))
    print("min layer ",min(track_arr))

    f_new.close()
    f_old.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


