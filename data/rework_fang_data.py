#!/usr/bin/env python

#
#  create SJFZ_Fangetal2019_VpandVs_clean.csv
#  from Fang_19_new.csv
#
## from Hao
##I had a talk with Fang about the first layer. You are right, "special value" means no data. 
##His inversion using a a regular box as grids, so there are grids above the free surface. 
##Data at these grids are artificial (even if they have values differ from "special value"), 
##so I removed them all using the topo data (first figure below). Besides, 
##layers with depth = -1,-0.5 are interpolated from depth=0 and depth=1.5km, so I also remove them
##if the data at depth=-1.5km is artificial.
##ETOPO1 (Bedrock) from NOAA
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import os
import pdb

dimension_x =  94
dimension_y =  73
dimension_z =  64

def usage():
    print("\n./rework_fang_data.py\n\n")
    sys.exit(0)

def main():
    total_count=dimension_x * dimension_y * dimension_z

    f_old=open('FangModel/Fang_19_new.csv','r')
    olds=f_old.readlines()
    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')

    f_old_i=0
    rewrite_cnt=0

    for oline in olds:
        ## copy header
        if(f_old_i == 0) : 
          nline="longitude,latitude,depth,Vp,Vs\n"
          f_new.write(nline)
        else :
#latitude,longitude,depth,Vp,Vs
#32.38,-118.17,-1.5,nan,nan
#to
#longitude,latitude,depth,Vp,Vs
#-118.17,32.38,-1.5,-9.999,-9.999
          l=oline.split(",")
          if(l[3]== "nan") :
            nline=l[1]+","+l[0]+","+l[2]+","+"-9.999,-9.999\n"
            f_new.write(nline)
            rewrite_cnt = rewrite_cnt +1
          else: 
            nline=l[1]+","+l[0]+","+l[2]+","+l[3]+","+l[4]
            f_new.write(nline)
        f_old_i = f_old_i+1 

    f_new.close()
    f_old.close()

    print("total rewrite count :",rewrite_cnt)

    print("\nDone!")

if __name__ == "__main__":
    main()


