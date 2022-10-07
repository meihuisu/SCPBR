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
import math

dimension_x =  94
dimension_y =  73
dimension_z =  64

def usage():
    print("\n./calc_surf_shift.py\n\n")
    sys.exit(0)

def main():
    total_count=dimension_x * dimension_y * dimension_z

## should be 94 x 73
    shift_list=[]
    surf_list=[]
    surf_i=0
    nochange=0

#    f_surf=open('FangModel/surfs','r')
    f_surf=open('FangModel/ETOPO1.surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        sur=float(s.strip())
        surf_list.append(sur)
        dif=math.floor((sur-1500)/500);
        shift_list.append(dif)
        if(dif == 0) :
          nochange=nochange+1
        surf_i=surf_i+1
            

    f_surf.close()
    print("total >",len(surf_list))

    print("max surf>", max(surf_list))
    print("min surf>", min(surf_list))
# shift, positive shift/shift down
#        negative z/shift  up
#          current value + (500)* shift
    print("max surf shift>", max(shift_list))
    print("min surf shift>", min(shift_list))
    print("no surf shift>", nochange)

    print(surf_list[0]); 
    print(shift_list[0]); 
   

    print("\nDone!")

if __name__ == "__main__":
    main()


