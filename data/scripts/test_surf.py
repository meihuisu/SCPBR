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
    diff_list=[]
    surf_list=[]
    surf_i=0
    a1500=0
    a1000=0
    a500=0
    a0=0
    b2000=0 
    b1500=0 
    b1000=0 
    b500=0 
    nochange=0
#    f_surf=open('FangModel/surfs','r')
    f_surf=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        sur=float(s.strip())
        surf_list.append(sur)
        if(sur >= 1500) :
           diff_list.append(sur-1500)
           if(sur-1500 >= 500) :
             print(surf_i,":  high high",sur);
             print("     diff",sur-1500);
           a1500=a1500+1;
        elif(sur >= 1000) :
           diff_list.append(sur-1000)
           a1000=a1000+1;
        elif(sur >= 500) :
           diff_list.append(sur-500)
           a500=a500+1;
        elif(sur >= 0) :
           diff_list.append(sur-0)
           a0=a0+1;
        elif(sur <= -2000) :
           diff_list.append(sur+2000)
           b2000 = b2000+1
        elif(sur <= -1500) :
           diff_list.append(sur+1500)
           b1500 = b1500+1
        elif(sur <= -1000) :
           diff_list.append(sur+1000)
           b1000 = b1000+1
        elif(sur <= -500) :
           diff_list.append(sur+500)
           b500 = b500+1
        else :
           nochange=nochange+1
           diff_list.append(0)
           
        surf_i=surf_i+1
            

    f_surf.close()
    print("more than 1500>",a1500)
    print("more than 1000>",a1000)
    print("more than 500 >",a500)
    print("more than 0   >",a0)
    print("less than -2000 >",b2000)
    print("less than -1500 >",b1500)
    print("less than -1000 >",b1000)
    print("less than -500 >",b500)
    print("no change >",nochange)
    print("total >",len(surf_list))

    print("max surf>", max(surf_list))
    print("min surf>", min(surf_list))
    print("max surf diff>", max(diff_list))
    print("min surf diff>", min(diff_list))

    print("\nDone!")

if __name__ == "__main__":
    main()


