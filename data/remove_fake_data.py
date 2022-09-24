#!/usr/bin/env python

#
#  create SJFZ_Fangetal2019_VpandVs_clean.csv
#  from SJFZ_Fangetal2019_VpVsratio.csv
#
#
## For both models I sent a couple of weeks ago, we were using the sea 
## level as 0 km with positive depth downwards (e.g. -1.5 km would be 1.5 km
## above sea level).
## 
## (1) Are values above the free surface artificial, and should  be ignored?
## Yes. The program using a regular box that contains all events and stations,
## thus regions above the free surface are artificial.
## (2) How do you suggest separating the actual volume of the crust from 
## "artificial material" above it?
## I would use the real topography as a layer to mask those values; everything 
## above the topography should be removed. There will be some interpolation 
## problem, but with the resolution we have, it won't matter.
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
    print("\n./remove_fake_data.py\n\n")
    sys.exit(0)

def no_need_val(d_val,s_val) :
    if(d_val < s_val) :
      return 0
    else:
      return 1

def no_need(oline,dep_i) :
    global tmp
    l=oline.split(",")
    vs=float(l[3].strip())
    vp=float(l[4].strip())
    if (dep_i == 0) :
        if ((vs == 5.5) & (vp == 3.14) ):
          return 0
    elif (dep_i == 1) :
        if ((vs == 5.52)  & (vp == 3.16) ):
          return 0
    elif ( dep_i == 2 ): 
        if ((vs == 5.55)  & (vp == 3.17) ):
          return 0
    elif ( dep_i == 3 ): 
        if ((vs == 5.57)  & (vp == 3.18) ):
          return 0
    elif ( dep_i == 4 ): 
        if ((vs == 5.6)  & (vp == 3.2) ):
          return 0
    elif ( dep_i == 5 ): 
        if ((vs == 5.63)  & (vp == 3.22) ):
          return 0
    elif ( dep_i == 6 ): 
        if ((vs == 5.67)  & (vp == 3.24) ):
          return 0
    elif ( dep_i == 7 ): 
        if ((vs == 5.7)  & (vp == 3.26) ):
          return 0
    elif ( dep_i == 8 ): 
        if ((vs == 5.73)  & (vp == 3.28) ):
          return 0
    elif ( dep_i == 9 ): 
        if ((vs == 5.76)  & (vp == 3.29) ):
          return 0
    elif ( dep_i == 10 ): 
        if ((vs == 5.8)  & (vp == 3.31) ):
          return 0
    else:
      return 1

    return 1

#-118.17,32.38,-1.50,5.50,3.14
# to
#-118.17,32.38,-1.50,-9.999,-9.999
def rewrite_fake(oline):
    l=oline.split(",")
    nline=l[0]+","+l[1]+","+l[2]+","+"-9.999,-9.999\n"
    return nline

def main():
    total_count=dimension_x * dimension_y * dimension_z

## should be 94 x 73
    surf_list=[]
    f_surf=open('FangModel/surfs','r')
    surfs=f_surf.readlines()
    for s in surfs:
        sur=float(s.strip())
        surf_list.append(sur)
    f_surf.close()

    dep_list=[]
    f_depth=open('FangModel/depth','r')
    deps=f_depth.readlines()
    for z in deps:
        dep=float(z.strip())
        dep_list.append(dep)
    f_depth.close()

    f_old=open('FangModel/SJFZ_Fangetal2019_VpVsratio.csv','r')
    olds=f_old.readlines()
    f_new=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','w')

    dep_i=0
    surf_i=0
    f_old_i=0;

    rewrite_cnt=0
    no_rewrite_cnt = 0

    d_val= -1.0 * (dep_list[dep_i]*1000) 
    for oline in olds:
        ## copy header
        if(f_old_i == 0) : 
          f_new.write(oline)
        else :
          s_val = surf_list[surf_i]
          if(surf_i == 0) : 
             print(dep_list[dep_i])
             print("  first one :",oline.strip())
#         if no_need_val(d_val,s_val) :
          if no_need(oline,dep_i) :
            ## no change
            f_new.write(oline)
            no_rewrite_cnt=no_rewrite_cnt+1
          else:
            ## rewrite vp/vs to -9999.000
            nline=rewrite_fake(oline)
            f_new.write(nline)
            rewrite_cnt=rewrite_cnt+1
          surf_i=surf_i+1
          if(surf_i >= dimension_x * dimension_y) :
            print("  last one :",oline.strip())
            print("  no_rewrite_cnt :",no_rewrite_cnt," at ", d_val)
            no_rewrite_cnt=0
            surf_i=0;
            dep_i=dep_i+1
            if(dep_i < dimension_z) :
              d_val= -1.0 * (dep_list[dep_i]*1000) 
        f_old_i = f_old_i+1 

    print("total rewrite count :",rewrite_cnt)

    f_new.close()
    f_old.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


