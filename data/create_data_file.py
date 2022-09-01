#!/usr/bin/env python

##
#  create scpbr.data.txt from 
#    Vp.dat and Vs.dat
#  
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import pdb

## initial data dimensions
dimension_x = 94
dimension_y = 73 
dimension_z = 16 
step_z =0.5 ## because the first one is -1.5

## output dimension

def usage():
    print("\n./create_data_file.py\n\n")
    sys.exit(0)


def _offset(x_pos, y_pos, z_pos):
   offset=z_pos * (dimension_y * dimension_x) + (y_pos * dimension_x) + x_pos
#   print("x",x_pos,"y",y_pos,"z",z_pos, "offset", offset);
   return offset

def main():

    total_count = dimension_x * dimension_y * dimension_z
    count=0

    ## lons are regular lons
    f_lons = open("./Fang2016Model/lons")
    f_lats = open("./Fang2016Model/lats")
    f_depth = open("./Fang2016Model/depth")
 
    f_vp = open("./fang_inp/Vp.dat")
    f_vs = open("./fang_inp/Vs.dat")

    vp_arr = np.fromfile(f_vp, dtype=np.float32, count=total_count, sep=' ')
    vs_arr = np.fromfile(f_vs, dtype=np.float32, count=total_count, sep=' ')

    f_vp.close()
    f_vs.close()

    count =0

    dep_list=[]
    dep_d_list=[]
    dep=None
    z_last=None
    deps=f_depth.readlines()
    for z in deps:
        dep=float(z.strip())
        dep_list.append(dep)
        if(z_last == None) :
          z_last=dep
        else:
#          print(" >> ",dep," diff(",dep-z_last,")")
          dep_d_list.append(dep-z_last)
          z_last=dep
     
    lat_list=[]
    lat_d_list=[]
    lat=None
    y_last=None
    lats=f_lats.readlines()
    for y in lats:
        lat=round(float(y.strip()),2)
        lat_list.append(lat)
        if(y_last == None) :
          y_last=lat
        else:
#          print(" >> ",lat," diff(",round(lat-y_last,2),")")
          lat_d_list.append(round(lat-y_last,2))
          y_last=lat


    lon_list=[]
    lon_d_list=[]
    lon=None
    x_last=None
    lons=f_lons.readlines()
    for x in lons:
        lon=round(float(x.strip()),2)
        lon_list.append(lon)
        if(x_last == None) :
          x_last=lon
        else:
#          print(" >> ",lon," diff(",round(lon-x_last,2),")")
          lon_d_list.append(round(lon-x_last,2))
          x_last=lon
        
    print("dep_list ",dep_list)
    print("dep_d_list ",dep_d_list)
#    print("lat_d_list ",lat_d_list)
#    print("lon_d_list ",lon_d_list)

    f_depth.close()
    f_lats.close()
    f_lons.close()

    ftxt = open('scpbr.dat.txt','w')

################# need to transform from this depth list 
#[-1.5,0.0,1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0,11.0,13.0,16.0,20.0]
# to this depth list with step of 0.5
# [0.0,0.5,1.0,1.5, ... 21.5]
    offset=0
    z_index=0
    dep_next=0;
    new_zidx_list=[]
    new_z_list=[]
    new_dep_list=[]
    for z in dep_list:
       repeat=1
       if(z_index < dimension_z-1) :
         dep_d=dep_d_list[z_index]
         repeat=dep_d/step_z
         i=0 
         while i<repeat:
           new_zidx_list.append(z_index) 
           new_dep_list.append(dep_list[z_index]);
           i=i+1
#         print("z_index >", z_index,"for z ",z," dep_d repeat .. ",repeat);
         zlist=np.arange(dep_next, dep_next+dep_d, 0.5);
         for k in zlist:
           new_z_list.append(k)
         dep_next=zlist[-1]+step_z
       else:
         print("last one for z ",z, " repeat .. ",repeat);
         new_z_list.append(dep_next);
         new_zidx_list.append(z_index)
         new_dep_list.append(dep_list[z_index]);

#       print(zlist)
       z_index=z_index+1
## repeat the following with different z but same vp_arr, and vs_arr       
    print("new_z_list",new_z_list)
    print("new_zidx_list",new_zidx_list)
    print("new_dep_list",new_dep_list)
    print(len(new_zidx_list))

    idx=0
    for z in new_z_list:
       use_z=new_zidx_list[idx]

       use_y=0
       for y in lat_list:
           use_x=0
           for x in lon_list:
              offset=_offset(use_x, use_y, use_z)
              aline= str(x)+" "+str(y)+" "+str(z)+" "+str(vp_arr[offset])+" "+str(vs_arr[offset])+"\n";
              ftxt.write(aline);
              use_x=use_x+1
           use_y=use_y+1
       idx=idx+1

    ftxt.close()

#    print(dep_list)
#    print(lat_list)
#    print(lon_list)
    print("\nDone!")

if __name__ == "__main__":
    main()


