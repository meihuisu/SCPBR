#!/usr/bin/env python

#
#  create Vp.dat and Vs.dat from
#  from SJFZ_Fangetal2016_VpandVs.csv
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
dimension_z =  16 

def usage():
    print("\n./create_data_inp_file.py\n\n")
    sys.exit(0)

def main():

    total_count=dimension_x * dimension_y * dimension_z

    if not os.path.exists('fang_inp'):
      os.mkdir('fang_inp')

    vptxt=open('fang_inp/Vp.dat','w')
    vstxt=open('fang_inp/Vs.dat','w')

    vp_arr = np.genfromtxt("Fang2016Model/SJFZ_Fangetal2016_VpandVs.csv",
          dtype=np.float32, delimiter=',', skip_header=1,filling_values=9999,usecols=4)
    vs_arr = np.genfromtxt("Fang2016Model/SJFZ_Fangetal2016_VpandVs.csv",
          dtype=np.float32, delimiter=',', skip_header=1,filling_values=9999,usecols=5)

#    print(len(vp_arr))
#    print(len(vs_arr))

## reshape them
    vp_3d=np.reshape(vp_arr,(dimension_z,dimension_y,dimension_x))
    vs_3d=np.reshape(vs_arr,(dimension_z,dimension_y,dimension_x))

#    print(len(vp_3d))
#    print(len(vp_3d[0]))
#    print(len(vp_3d[0][0]))
#    print(vp_3d[0][0])
    
    data=str(vp_3d[0][0])
    for j in np.arange(0,dimension_z, 1):
      for i in np.arange(0,dimension_y, 1):
        vpdatastr=" ".join(str(x) for x in vp_3d[j][i])
        vptxt.write(vpdatastr)
        vptxt.write("\n")
        vsdatastr=" ".join(str(x) for x in vs_3d[j][i])
        vstxt.write(vsdatastr)
        vstxt.write("\n")

    sys.exit(0)


    vptxt.close()
    vstxt.close()

    print("\nDone!")

if __name__ == "__main__":
    main()


