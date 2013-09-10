'''
Functions to initialize various numerical experiments.

Make a new init_* for your application.

loc     Path to directory of grid and output files
nsteps  Number of steps to do between model outputs (iter in tracmass)
ndays   number of days to track the particles from start date
ff      ff=1 to go forward in time and ff=-1 for backward in time
date    Start date in datetime object
tseas   Time between outputs in seconds
ah      Horizontal diffusion in m^2/s. 
        See project values of 350, 100, 0, 2000. For -turb,-diffusion
av      Vertical diffusion in m^2/s.
do3d    for 3d flag, do3d=0 makes the run 2d and do3d=1 makes the run 3d
doturb  turbulence/diffusion flag. 
        doturb=0 means no turb/diffusion,
        doturb=1 means adding parameterized turbulence
        doturb=2 means adding diffusion on a circle
        doturb=3 means adding diffusion on an ellipse (anisodiffusion)
lon0    Drifter starting locations in x/zonal direction.
lat0    Drifter starting locations in y/meridional direction.
z0/zpar Then z0 should be an array of initial drifter depths. 
        The array should be the same size as lon0 and be negative
        for under water. Currently drifter depths need to be above 
        the seabed for every x,y particle location for the script to run.
        To do 3D but start at surface, use z0=zeros(ia.shape) and have
         either zpar='fromMSL'
        choose fromMSL to have z0 starting depths be for that depth below the base 
        time-independent sea level (or mean sea level).
        choose 'fromZeta' to have z0 starting depths be for that depth below the
        time-dependent sea surface. Haven't quite finished the 'fromZeta' case.
        Then: 
        set z0 to 's' for 2D along a terrain-following slice
         and zpar to be the index of s level you want to use (0 to km-1)
        set z0 to 'rho' for 2D along a density surface
         and zpar to be the density value you want to use
         Can do the same thing with salinity ('salt') or temperature ('temp')
         The model output doesn't currently have density though.
        set z0 to 'z' for 2D along a depth slice
         and zpar to be the constant (negative) depth value you want to use
        To simulate drifters at the surface, set z0 to 's' 
         and zpar = grid['km']-1 to put them in the upper s level
         z0='s' is currently not working correctly!!!
         In the meantime, do surface using the 3d set up option but with 2d flag set
xp      x-locations in x,y coordinates for drifters
yp      y-locations in x,y coordinates for drifters
zp      z-locations (depths from mean sea level) for drifters
t       time for drifter tracks
name    Name of simulation to be used for netcdf file containing final tracks

'''

import numpy as np
import os
import netCDF4 as netCDF
import pdb
import glob
from datetime import datetime, timedelta
from matplotlib.mlab import *
import tracpy


def forecast(date, loc, hgrid):
    '''
    Initialization for seeding drifters near Port Aransas and Surfside to be run
    forward to forecast where K brevis cells may be located.

    Optional inputs for making tests easy to run:
        grid    If input, will not redo this step. 
                Default is to load in grid.
    '''

    units = 'seconds since 1970-01-01'

    # Initialize parameters
    nsteps = 5 # 5 time interpolation steps
    # d = netCDF.MFDataset(loc + 'ocean_his*.nc')
    # pdb.set_trace()
    # Want to track from start day through the day Darren will be sampling
    ndays = (datetime(2013, 9, 10, 0, 1) - date).days
    # pdb.set_trace()
    # d.close()
    ff = 1 # This is a forward-moving simulation

    # Time between outputs
    tseas = 4*3600 # 4 hours between outputs, in seconds, time between model outputs 
    ah = 20.
    av = 0. # m^2/s

    # Can use a subset of the drifters in order to test sensitivity to N
    N = 100

    # Initial lon/lat locations for drifters
    # Port Aransas
    dx = .3; dy = .3
    lon0a,lat0a = np.meshgrid(np.linspace(-97.07-dx,-97.07+dx,15), 
                            np.linspace(27.83-dy,27.83+dy,15))
    # surfside
    dx = .3; dy = .3
    lon0b,lat0b = np.meshgrid(np.linspace(-95.28-dx,-95.28+dx,15), 
                            np.linspace(28.95-dy,28.95+dy,15))

    lon0 = np.concatenate((lon0a.flatten(),lon0b.flatten()))
    lat0 = np.concatenate((lat0a.flatten(),lat0b.flatten()))

    # Eliminate points that are outside domain or in masked areas
    lon0,lat0 = tracpy.tools.check_points(lon0,lat0,hgrid)

    # surface drifters
    z0 = 's'  
    zpar = 29 

    # for 3d flag, do3d=0 makes the run 2d and do3d=1 makes the run 3d
    do3d = 0
    doturb = 1

    # Flag for streamlines. All the extra steps right after this are for streamlines.
    dostream = 0

    return nsteps, ndays, ff, tseas, ah, av, lon0, lat0, \
            z0, zpar, do3d, doturb, dostream, N
