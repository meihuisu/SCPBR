#!/usr/bin/env python

##
#  Builds the data files in the expected format from scpbr.dat.txt
#
# to >>  /** P-wave velocity in km/s per second */
#        double vp;
# to >>  /** S-wave velocity in km/s per second */
#        double vs;
# depth is in increment of 500m,
#
#The columns of the file are: lon lat z(km) vp(km/s) vs(km/s)

import getopt
import sys
import subprocess
import struct
import array

if sys.version_info.major >= (3) :
  from urllib.request import urlopen
else:
  from urllib2 import urlopen

model = "SCPBR"

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

def download_urlfile(url,fname):
  try:
    response = urlopen(url)
    CHUNK = 16 * 1024
    with open(fname, 'wb') as f:
      while True:
        chunk = response.read(CHUNK)
        if not chunk:
          break
        f.write(chunk)
  except:
    e = sys.exc_info()[0]
    print("Exception retrieving and saving model datafiles:",e)
    raise
  return True

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

    delta_lon = (lon_upper - lon_origin )/(dimension_x-1)
    delta_lat = (lat_upper - lat_origin)/(dimension_y-1)

    print("\nDownloading model file\n")

#    fname="./"+"scpbr.dat.txt"
#    url = path + "/" + fname
#    download_urlfile(url,fname)

    subprocess.check_call(["mkdir", "-p", mdir])

    # Now we need to go through the data files and put them in the correct
    # format for SCPBR. More specifically, we need a binary Vp.dat, and Vs.dat

    f = open("./scpbr.dat.txt")

    f_vp = open("./scpbr/vp.dat", "wb")
    f_vs = open("./scpbr/vs.dat", "wb")

    vp_arr = array.array('f', (-1.0,) * (dimension_x * dimension_y * dimension_z))
    vs_arr = array.array('f', (-1.0,) * (dimension_x * dimension_y * dimension_z))

    print ("dimension is", (dimension_x * dimension_y * dimension_z))

    x_pos=0;
    y_pos=0;
    z_pos=0;
    count=0;
    for line in f:
        count=count+1
        arr = line.split()

        vp = -1.0
        vs = -1.0
        depth_v = float(arr[2])
        tmp_vp = arr[3]
        tmp_vs = arr[4]

        vp = float(tmp_vp)
        vp = vp * 1000.0;

        vs = float(tmp_vs)
        vs = vs * 1000.0;

        loc =z_pos * (dimension_y * dimension_x) + (y_pos * dimension_x) + x_pos
        vp_arr[loc] = vp
        vs_arr[loc] = vs

      
        x_pos = x_pos + 1
        if(x_pos == dimension_x) :
          x_pos = 0;
          y_pos = y_pos+1
          if(y_pos == dimension_y) :
            y_pos=0;
            z_pos = z_pos+1
            if(z_pos == dimension_z) :
              print ("All DONE")

    vp_arr.tofile(f_vp)
    vs_arr.tofile(f_vs)

    f.close()
    f_vp.close()
    f_vs.close()

    print ("number of lines..",count)
    print("Done!")

if __name__ == "__main__":
    main()

