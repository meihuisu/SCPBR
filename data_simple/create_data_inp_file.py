#!/usr/bin/env python

##
#  create scpbr_inp.data.txt from
#    fang_inp/Vp.dat and fang_inp/Vs.dat
#  no filling in of gap rows
#  This is just a testing program, not being used
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import pdb

model = "SCPBR"

dimension_x =  32
dimension_y =  32 
dimension_z =  16 

def usage():
    print("\n./create_data_inp_file.py\n\n")
    sys.exit(0)


def main():

    total_count=dimension_x * dimension_y * dimension_z
    count=0

    f_lons = open("./fang_inp/lons")
    f_lats = open("./fang_inp/lats")
    f_depth = open("./fang_inp/depth")
 
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
        lon=round((float(x.strip())-360.0),2)
        lon_list.append(lon)
        if(x_last == None) :
          x_last=lon
        else:
#          print(" >> ",lon," diff(",round(lon-x_last,2),")")
          lon_d_list.append(round(lon-x_last,2))
          x_last=lon
        
    print(dep_d_list)
    print(lat_d_list)
    print(lon_d_list)

    f_depth.close()
    f_lats.close()
    f_lons.close()

    ftxt = open('scpbr_inp.dat.txt','w')
    offset=0
    for z in dep_list:
       for y in lat_list:
           for x in lon_list:
              aline= str(x)+" "+str(y)+" "+str(z)+" "+str(vp_arr[offset])+" "+str(vs_arr[offset])+"\n";
              ftxt.write(aline);
              offset=offset+1
    ftxt.close()

#    print(dep_list)
#    print(lat_list)
#    print(lon_list)
    print("\nDone!")

if __name__ == "__main__":
    main()


