'''
Script to run the backward Galveston drifter simulation. Start the 
drifters near Galveston and run them backward.
'''

import matplotlib as mpl
mpl.use("Agg") # set matplotlib to use the backend that does not require a windowing system
import numpy as np
import os
import netCDF4 as netCDF
import pdb
import matplotlib.pyplot as plt
import tracpy
import init
from datetime import datetime, timedelta
import glob

# files = list(('roms_his_20130826_a_n0.nc','roms_his_20130827_a_n0.nc','roms_his_20130828_a_n0.nc','roms_his_20130829_a_n0.nc','roms_his_20130830_a_n0.nc','roms_his_20130831_a_n0.nc','roms_his_20130901_a_n0.nc','roms_his_20130902_a_n0.nc','roms_his_20130903_a_n0.nc','roms_his_20130904_a_n0.nc','roms_his_20130905_f_n0.nc'))

def run():

    # Location of TXLA model output
    loc = 'OUT/'
    # loc = 'GROM-hind-crv-13-08-26-00-thru-13-09-03-06.nc'#,
            # 'http://barataria.tamu.edu:8080/thredds/dodsC/NcML/txla_nesting6.nc']

    # These seem like pretty random units I have to use to get the first date correct
    units = 'seconds since 1970-01-01'

    # Make sure necessary directories exist
    if not os.path.exists('tracks'):
        os.makedirs('tracks')
    if not os.path.exists('tracks/forecast'):
        os.makedirs('tracks/forecast')
    if not os.path.exists('figures'):
        os.makedirs('figures')
    if not os.path.exists('figures/forecast'):
        os.makedirs('figures/forecast')

    # Parameters to be rotated through
    years = np.array([2013])
    # oil spill from April 20 - July 15, 2010
    # startdate = datetime(years[0], 4, 20, 0, 1)
    # Interesting time periods where backward drifters cross the shelf:
    # 5-23-10 to 5-28-10 and 6-21-10 to 6-26-10
    # Need 1 min to get correct model output out
    startdate = datetime(years[0], 8, 26, 0, 1)#,
                            # datetime(years[0], 6, 21, 0, 1)])
    date = startdate

    # how many days to start drifters from, starting from startdate
    # rundays = 3

    hgrid = tracpy.inout.readgrid(loc)

    # initialize counter for number of hours to increment through simulation by
    nh = 0

    # keep starting simulations until we hit August 29th
    while date.day < 29:

        name = 'forecast/' + date.isoformat()[0:13] 

        # If the particle trajectories have not been run, run them
        if not os.path.exists('tracks/' + name + '.nc'):

            # Read in simulation initialization
            nstep, ndays, ff, tseas, ah, av, lon0, lat0, z0, zpar, do3d, doturb, \
                    dostream, N = init.forecast(date, loc, hgrid)
            # pdb.set_trace()

            # Run tracpy
            lonp, latp, zp, t, grid \
                = tracpy.run.run(loc, nstep, ndays, ff, date, tseas, ah, av, \
                                    lon0, lat0, z0, zpar, do3d, doturb, name, \
                                    dostream=dostream)

        # # If basic figures don't exist, make them
        # if not os.path.exists('figures/' + name + '*.png'):

            # Read in and plot tracks
            d = netCDF.Dataset('tracks/' + name + '.nc')
            lonp = d.variables['lonp'][:]
            latp = d.variables['latp'][:]
            tracpy.plotting.tracks(lonp, latp, name, grid=grid)
            tracpy.plotting.hist(lonp, latp, name, grid=grid, which='hexbin')
            d.close()

        # Increment by 4 hours for next loop, to move through more quickly
        nh = nh + 4
        date = startdate + timedelta(hours=nh)
        # pdb.set_trace()
    # # Do transport plot
    # tracpy.plotting.transport(name='galv_b', Title='Transport to Galveston', dmax=1.5)

    # Overall plot
    hgrid = tracpy.inout.readgrid(loc, llcrnrlat=27, urcrnrlat=30, llcrnrlon=-98, urcrnrlon=-94.5)
    # fig = figure(figsize=(11,10))
    Files = glob.glob('tracks/forecast/*.nc')
    Files.sort()
    lonp = np.ones((238*18,451))*np.nan
    latp = np.ones((238*18,451))*np.nan
    for i,File in enumerate(Files):
        d = netCDF.Dataset(File)
        # lonp and latp are different sizes each simulation
        lonp[i*238:i*238+238,0:d.variables['tp'][:].size-31] = d.variables['lonp'][:,:-31]
        latp[i*238:i*238+238,0:d.variables['tp'][:].size-31] = d.variables['latp'][:,:-31]
        d.close()
    tracpy.plotting.tracks(lonp, latp, 'forecast/overall_2013-09-09-00', grid=hgrid)

if __name__ == "__main__":
    run()    