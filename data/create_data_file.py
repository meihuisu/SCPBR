#!/usr/bin/env python

#
#  create scpbr/vp.dat and scpbr/vs.dat from
#  from SJFZ_Fangetal2019_VpandVs_clean.csv
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

lon_origin = -118.17
lat_origin = 32.38

lon_upper = -115.38
lat_upper = 34.54

delta_lon = (lon_upper - lon_origin )/(dimension_x-1)
delta_lat = (lat_upper - lat_origin)/(dimension_y-1)

def usage():
    print("\n./create_data_file.py\n\n")
    sys.exit(0)

def main():

    total_count=dimension_x * dimension_y * dimension_z

    if not os.path.exists('scpbr'):
      os.mkdir('scpbr')

    f_old=open('FangModel/SJFZ_Fangetal2019_VpandVs_clean.csv','r')
    olds=f_old.readlines()
    f_old.close()

    vp_arr = array.array('f', (-9999.0,) * (dimension_x * dimension_y * dimension_z))
    vs_arr = array.array('f', (-9999.0,) * (dimension_x * dimension_y * dimension_z))

    f_vp = open("./scpbr/vp.dat", "wb")
    f_vs = open("./scpbr/vs.dat", "wb")

    o_idx=0
    header=1;
    for oline in olds:
       if(header) :
          header=0
          continue
       arr = oline.split(',')
       t_lon=float(arr[0])
       t_lat=float(arr[1])
       t_depth=float(arr[2])
       t_vp=float(arr[3])
       t_vs=float(arr[4])

       y_pos = int(round((t_lat - lat_origin) / delta_lat))
       x_pos = int(round((t_lon - lon_origin) / delta_lon))
       z_pos = int(t_depth/0.5)

       offset= z_pos * (dimension_y * dimension_x) + (y_pos * dimension_x) + x_pos
       print( "X",x_pos,"Y",y_pos,"Z",z_pos)

       n_vp=t_vp * 1000
       n_vs=t_vs * 1000

       vp_arr[offset]=n_vp
       vs_arr[offset]=n_vs
       o_idx=o_idx+1

    vp_arr.tofile(f_vp)
    vs_arr.tofile(f_vs)

    minvs=min(vs_arr)
    print("vs min...",minvs)
    maxvs=max(vs_arr)
    print("vs max...",maxvs)

    minvp=min(vp_arr)
    print("vp min...",minvp)
    maxvp=max(vp_arr)
    print("vp max...",maxvp)

    print("TOTAL valid data points >> ",o_idx)
    print("\nDone!")

if __name__ == "__main__":
    main()


