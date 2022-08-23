#!/usr/bin/env python

##
#  Retrieve the latlons form the original data txt file and
#  and retrieve the material properties from binary vp.dat file 
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import array
import pdb

if sys.version_info.major >= (3) :
  from urllib.request import urlopen
else:
  from urllib2 import urlopen

model = "FANG"

dimension_x = 0 
dimension_y = 0 
dimension_z = 0 

lon_origin = 0
lat_origin = 0

lon_upper = 0
lat_upper = 0

def usage():
    print("\n./make_data_files.py\n\n")
    sys.exit(0)


def main():

    # Set our variable defaults.
    path = ""
    mdir = ""

    try:
        fp = open('./config','r')
    except:
        print("ERROR: failed to open config file")
        sys.exit(1)

    ## look for model_data_path and other varaibles
    lines = fp.readlines()
    for line in lines :
        if line[0] == '#' :
          continue
        parts = line.split('=')
        if len(parts) < 2 :
          continue;
        variable=parts[0].strip()
        val=parts[1].strip()

        if (variable == 'model_data_path') :
            path = val + '/' + model
            continue
        if (variable == 'model_dir') :
            mdir = "./"+val
            continue
        if (variable == 'nx') :
            dimension_x = int(val)
            continue
        if (variable == 'ny') :
            dimension_y = int(val)
            continue
        if (variable == 'nz') :
            dimension_z = int(val)
            continue
        if (variable == 'bottom_left_corner_lon') :
            lon_origin = float(val)
            continue
        if (variable == 'bottom_left_corner_lat') :
            lat_origin = float(val)
            continue
        if (variable == 'top_right_corner_lon') :
            lon_upper = float(val)
            continue
        if (variable == 'top_right_corner_lat') :
            lat_upper = float(val)
            continue

        continue
    if path == "" :
        print("ERROR: failed to find variables from config file")
        sys.exit(1)

    fp.close()

    total_count = dimension_x * dimension_y * dimension_z
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

    ftxt = open('scpbr.dat.txt','w')
    offset=0
    for z in dep_list:
       for y in lat_list:
           for x in lon_list:
              aline= str(x)+" "+str(y)+" "+str(z)+" "+str(vp_arr[offset])+" "+str(vs_arr[offset])+"\n";
              ftxt.write(aline);
              offset=offset+1
    ftxt.close()

#    fvp = open('vp.dat')
#    fvs = open('vs.dat)

#    print("retrieve..", dimension_x * dimension_y * dimension_z)
#    print("vp size >> ",np.shape(vp_arr))
#    print("vs size >> ",np.shape(vs_arr))
#    print(dep_list)
#    print(lat_list)
#    print(lon_list)
    print("\nDone!")

if __name__ == "__main__":
    main()


