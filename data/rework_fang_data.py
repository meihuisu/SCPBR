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
    f_old.close()

    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')
    f_bad=open('FangModel/SJFZ_Fangetal2019_VpandVs_bad.csv','w')
 
## get shift index    
## should be 94 x 73

    shift_arr = array.array('f', (-9999.0,) * (layer_count))
    shift_i = 0
    header = 1
    valid_cnt = 0
    bad_cnt = 0
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
        if(l[3] != "nan") :
## valid point
          oldz=float(l[2])
          if(shift_arr[shift_i] == -9999.0) : 
## first occur
             shift_arr[shift_i] = oldz
             newz = 0.0
          else:
             newz = oldz - shift_arr[shift_i]
          if(newz >= 0 and newz <= 31.5):
             nline=l[1]+","+l[0]+","+str(newz)+","+l[3]+","+l[4]
             f_new.write(nline)
             valid_cnt=valid_cnt +1
           else:
             f_bad.write(oline)
             bad_cnt=bad_cnt+1
        shift_i = shift_i + 1
        if(shift_i >= layer_count):
           shift_i=0

    print("max shift ",max(shift_arr))
    print("min shift ",min(shift_arr))
    print("valid cnt ",valid_cnt);
    print("bad cnt ",bad_cnt);

    f_new.close()
    f_bad.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


