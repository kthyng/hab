import numpy as np
import os
import netCDF4 as netCDF
import pdb
import glob
from datetime import datetime, timedelta
from matplotlib.mlab import *
import tracpy

def params(date=None, grid=None, ndays=None):
    '''
    Initialization for seeding drifters near Galveston Bay to be run
    forward.

    Optional inputs for making tests easy to run:
        date    Input date for name in datetime format
                e.g., datetime(2009, 11, 20, 0). If date not input,
                name will be 'temp' 
        grid    If input, will not redo this step. 
                Default is to load in grid.
    '''

    # Location of TXLA model output
    loc = 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc'

    # Initialize parameters
    nsteps = 5 # 5 time interpolation steps
    ff = 1 # This is a backward-moving simulation

    # Time between outputs
    tseas = 4*3600 # 4 hours between outputs, in seconds, time between model outputs 
    ah = 0.
    av = 0. # m^2/s

    if grid is None:
        # if loc is the aggregated thredds server, the grid info is
        # included in the same file
        grid = tracpy.inout.readgrid(loc)
    else:
        grid = grid

    # Initial lon/lat locations for drifters
    d = np.load('/pong/raid/kthyng/hab/data/exp2/starting_locations.npz')
    lon0 = d['lon0']
    lat0 = d['lat0']

    # Eliminate points that are outside domain or in masked areas
    lon0,lat0 = tracpy.tools.check_points(lon0,lat0,grid)

    # surface drifters
    z0 = 's'  
    zpar = 29 

    # for 3d flag, do3d=0 makes the run 2d and do3d=1 makes the run 3d
    do3d = 0
    doturb = 0

    # simulation name, used for saving results into netcdf file
    if date is None:
        name = 'temp' #'5_5_D5_F'
    else:
        name = 'exp2_f/' + date.isoformat()[0:13] 

    return loc, nsteps, ff, date, tseas, ah, av, lon0, lat0, \
            z0, zpar, do3d, doturb, name, grid
