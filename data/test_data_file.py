#!/usr/bin/env python

##
#  Retrieve the original data with original z (-1.5 to 20) 
#  to test what is in the scpbr binary data files
#  ./create_data_infile.py  and use scpbr_inp_dat.txt
#  ./test_data_file.py 
#

import getopt
import sys
import subprocess
import struct
import numpy as np
import pdb

dimension_x = 32
dimension_y = 32 
dimension_z = 44 

lon_origin = -118.17
lat_origin = 32.38
lon_upper = -115.38
lat_upper = 34.55

delta_lon = (lon_upper - lon_origin )/(dimension_x-1)
delta_lat = (lat_upper - lat_origin)/(dimension_y-1)

def usage():
    print("\n./test_data_files.py\n\n")
    sys.exit(0)

def myrange(start, end, step):
    while start < end+(step/2):
        yield start
        start = start + step

def main():

    f_vp = open("./scpbr/vp.dat")
    vp_arr = np.fromfile(f_vp, dtype=np.float32)
    f_vp.close()

    f_vs = open("./scpbr/vs.dat")
    vs_arr = np.fromfile(f_vs, dtype=np.float32)
    f_vs.close()

    f_inp=open("./scpbr_inp.dat.txt");
    flines=f_inp.readlines()
    fclose(f_inp)

    for line in flines :
       arr = line.split(' ')
       t_lon=float(arr[0])
       t_lat=float(arr[1])
       t_dep=float(arr[2])
       t_vp=float(arr[3])
       t_vs=float(arr[4])
       off_x= int(round((t_lon - lon_origin)/delta_lon))
       off_y= int(round((t_lat - lat_origin)/delta_lat))
       off_z= int(rount((t_z - 1.5) / 0.5))
       offset= off_z * (dimension_y * dimension_x) + (off_y * dimension_x) + off_x
       print("off_x ",off_x, "off_y ",off_y,"off_z ",off_z);
       n_vp=vp_arr[offset]
       n_vs=vs_arr[offset]
       if(t_vp != n_vp) :
          print(" NO match vp ",t_vp, " with ", n_vp)
          exit(1)
       if(t_vs != n_vs) :
          print(" NO match vs ",t_vs, " with ", n_vs)
          exit(1)

    print("Done!")

if __name__ == "__main__":
    main()


