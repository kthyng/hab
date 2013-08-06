'''
Script to run the forward Galveston drifter simulation. Start the 
drifters near Galveston and run them forward.
'''

import numpy as np
import os
import netCDF4 as netCDF
import pdb
import matplotlib.pyplot as plt
import tracpy
import init
from datetime import datetime, timedelta
import glob

def run():
    # Units for time conversion with netCDF.num2date and .date2num
    units = 'seconds since 1970-01-01'

    # Location of TXLA model output
    loc = 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc'

    # Make sure necessary directories exist
    if not os.path.exists('tracks'):
        os.makedirs('tracks')
    if not os.path.exists('figures'):
        os.makedirs('figures')

    # Parameters to be rotated through
    years = np.arange(2004,2012)
    month = 9
    days = np.array([1,8,15,22])
    # Interesting time periods where backward drifters cross the shelf:

    grid = tracpy.inout.readgrid(loc)

    for year in years:
        enddate = datetime(year, 12, 1, 1, 0)
        for day in days:
            date = datetime(year, month, day, 1, 0)

            # number of days to run this simulation
            ndays = timedelta(netCDF.date2num(date,units) 
                            - netCDF.date2num(enddate,units)).days/(24*3600.)

            # Read in simulation initialization
            loc, nstep, ff, date, tseas, ah, av, lon0, lat0, z0, \
                    zpar, do3d, doturb, name, grid = init.params(date, grid=grid)
            pdb.set_trace()
            # If the particle trajectories have not been run, run them
            if not os.path.exists('tracks/' + name + '.nc'):
                lonp, latp, zp, t, grid = tracpy.run.run(loc, nstep, ndays, \
                                                ff, date, tseas, ah, av, \
                                                lon0, lat0, z0, zpar, do3d, \
                                                doturb, name)

            elif not os.path.exists('figures/' + name + 'tracks.png') or \
                 not os.path.exists('figures/' + name + 'histhexbin.png'):
                d = netCDF.Dataset('tracks/' + name + '.nc')
                lonp = d.variables['lonp'][:]
                latp = d.variables['latp'][:]
                tracpy.plotting.tracks(lonp, latp, name, grid=grid)
                tracpy.plotting.hist(lonp, latp, name, grid=grid, which='hexbin')


# This is so the script can be run using reference 
# projects/[projectname].py
if __name__ == "__main__":
    run()    