#!/usr/bin/env python3

import argparse
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.colors as colors
import cmocean.cm as cmo
import numpy as np
from pylab import cm

from netCDF4 import Dataset

parser = argparse.ArgumentParser()
parser.add_argument('modelfile', type=str)
args = parser.parse_args()

secInMonth = 60*60*24*30

# the one used in the model
crs = ccrs.NorthPolarStereo(-44, 71)
extent = (-6240000, 6240000, -6240000, 6240000)

vminTemp = -10
vmaxTemp = 10

vminPrec = 0
vmaxPrec = 2000


fig, axes = plt.subplots(1,
                         3,
                         subplot_kw={'projection': crs},
                         figsize=(12, 4))

print(axes)

data = Dataset(args.modelfile, mode='r')
x = data.variables['x'][:]
y = data.variables['y'][:]
thk = data.variables['thk'][:]
# model_timebnds = data.variables['time_bounds'][:]

# # print(data.variables['air_temp'].units)
# if data.variables['air_temp_snapshot'].units == 'Kelvin':
#     modeltemp = modeltemp - 273
# data.close()


cmap = cm.get_cmap('GnBu', 21)    # 11 discrete colors
cmap_diff = cm.get_cmap('RdBu', 21)    # 11 discrete colors

title = args.modelfile.split('/')[-1]

axThk = axes[0]
axDiff1 = axes[1]
axDiffPerc = axes[2]
thk_last= thk[-1,:,:]
thk_first= thk[0,:,:]



thk_diff = thk_last - thk_first
thk_diffperc = thk_diff / thk_first

axThk.coastlines(resolution='110m')
axThk.set_extent(extent, crs=crs)
imgThk = axThk.imshow(thk_last,
                        transform=crs,
                        extent=[-6240000, 6240000, -6240000, 6240000],
                        cmap=cmap,
                        origin='lower',
                        vmin=0,
                        vmax=5000)
cbThk = plt.colorbar(imgThk, ax=axThk, shrink=0.8)
cbThk.set_label('Ice Thickness (m)')

axDiff1.coastlines(resolution='110m')
axDiff1.set_extent(extent, crs=crs)
imgDiff = axDiff1.imshow(thk_diff,
                        transform=crs,
                        extent=[-6240000, 6240000, -6240000, 6240000],
                        cmap=cmap_diff,
                        origin='lower',
                        vmin=-2000,
                        vmax=2000)
cbDiff = plt.colorbar(imgDiff, ax=axDiff1, shrink=0.8)
cbDiff.set_label('Thickness difference (m)')

axDiffPerc.coastlines(resolution='110m')
axDiffPerc.set_extent(extent, crs=crs)
imgDiffPerc= axDiffPerc.imshow(thk_diffperc,
                        transform=crs,
                        extent=[-6240000, 6240000, -6240000, 6240000],
                        cmap=cmap_diff,
                        origin='lower',
                        vmin=-1,
                        vmax=1)
cbDiffPerc = plt.colorbar(imgDiffPerc, ax=axDiffPerc, shrink=0.8)
cbDiffPerc.set_label('Thickness difference (normalized)')

axThk.set_title(title)

# ax.gridlines()
plt.savefig(args.modelfile + "result" + ".png", dpi=300)
