#/* -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
#
# File Name : plotFangModel.py
#
# Purpose :
#
# Creation Date : 08-06-2020
#
# Last Modified : Mon 08 Jun 2020 12:16:15 PM EDT
#
# Created By : Hongjian Fang: hfang@mit.edu
#
#_._._._._._._._._._._._._._._._._._._._._.*/

import pandas as pd
from matplotlib import pyplot as plt

velsjfz = pd.read_csv('SJFZ_VpandVs_Fangetal.csv')
plotdepth = 2
vel2km = velsjfz[velsjfz['depth']==plotdepth]
fig,ax = plt.subplots(1,2,figsize=(10,6))
plt.subplot(121)
plt.scatter(vel2km['longitude'],vel2km['latitude'],c=vel2km['Vp'],cmap='seismic_r')
plt.colorbar(orientation='horizontal')
plt.title('Vp at '+str(plotdepth)+'km')
plt.subplot(122)
plt.scatter(vel2km['longitude'],vel2km['latitude'],c=vel2km['Vs'],cmap='seismic_r')
plt.colorbar(orientation='horizontal')
plt.title('Vs at '+str(plotdepth)+'km')
plt.show()
