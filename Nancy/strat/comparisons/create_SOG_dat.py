# Create the Salish.dat file from Rob's IOS data
# Looks for data points close to the mouth of JdF.

import ACTDR
import netCDF4 as nc

# Load IOS data
ACTDR.load_ios('/ocean/rich/home/SoG/ios/che/')
ACTDR.load_ios('/ocean/rich/home/SoG/ios/che2/')
ACTDR.load_ios('/ocean/nsoontie/MEOPAR/IOS/2011/',ignore_che=False)
ACTDR.load_ios('/ocean/nsoontie/MEOPAR/IOS/2013/',ignore_che=False)


## Remove duplicates
ACTDR.remove_duplicates()

# Filter year
ACTDR.filter_year(2000)

# Filter data without Temperature and Salinity keys
ACTDR.filter_keys()

#Filter anomalies
ACTDR.filter_anom()

# Filter lon/lats.
#define a max and min lon
#min_lon = -123
#max_lon = -122
#min_lat = 49
#max_lat = 50
# remove indices outside of range
#rm_ind = []
# rm_ind contains the indices to remove
# loop through all casts
#for ii, cast in enumerate(ACTDR.CTD_DAT):
    # see if cast is outside of my region region
#    if (cast['Latitude'] > max_lat or cast['Latitude'] < min_lat or
#       cast['Longitude'] > max_lon or cast['Longitude'] < min_lon):
#        rm_ind.append(ii)  # append to the remove list if outside

# loop through the removed indices list
#for ii in rm_ind[::-1]:
#    del ACTDR.CTD_DAT[ii]  # delete said index

# let the user know the new number of available casts

print '> ', len(ACTDR.CTD_DAT), ' casts'

# save new database
ACTDR.save_dat('SOG_2000.dat')
