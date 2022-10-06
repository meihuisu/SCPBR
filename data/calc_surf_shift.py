#!/usr/bin/env python

#
# calculate the amount of shift is needed for each column
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
    print("\n./calc_surf_shift.py\n\n")
    sys.exit(0)

def main():
    total_count=dimension_x * dimension_y * dimension_z

## should be 94 x 73
    surf_list=[]
    surf_i=0
    a1500=0
    a1000=0
    a500=0
    a0=0
    below=0 
#    f_surf=open('FangModel/surfs','r')
    f_surf=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        sur=float(s.strip())
        surf_list.append(sur)
        if(sur >= 1500) :
           a1500=a1500+1;
        elif(sur >= 1000) :
           a1000=a1000+1;
        elif(sur >= 500) :
           a500=a500+1;
        elif(sur >= 0) :
           a0=a0+1;
        else:
           below=below+1
           
        surf_i=surf_i+1
            

    f_surf.close()
    print("more than 1500",a1500)
    print("more than 1000",a1000)
    print("more than 500",a500)
    print("more than 0",a0)
    print("less than 0",below)
    print("total",len(surf_list))

    print("\nDone!")

if __name__ == "__main__":
    main()


