'''
Aggregated CTD reader for NOAA/IOS CTD data.

Rob Irwin, June 2015
v0.1

Reads the various formats of the IOS CTD data
'''
import csv
import numpy as np

IOS_QUANTITIES = ['Pressure','Temperature:Primary','Temperature:Secondary','Temperature','Salinity:T0:C0']
IOS_READ_STATE = 'N/A'
IOS_SKIP_LINES = 0
IOS_FI = None

def ios_read(fnm):
    '''
    ios_read
    Reads files from the IOS ocean database.
    
    Arguments
    ---------
    fnm - string - the path and filename of the file.
    
    The format is divided into separate sections per file.
    '''
    # define the globals, otherwise the code redefines these variables within new scope
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI

    # open the global file handle    
    IOS_FI = open(fnm,'rb')
    
    # set the default read state and skip lines variables
    IOS_READ_STATE = 'N/A'
    IOS_SKIP_LINES = 0
    
    # instantiate the dat structure
    dat = {'Variables' : [], 'DATA' : []}

    # loop through the IOS_FI handle
    for line in IOS_FI:
        # if we have lines to skip, then skip
        if IOS_SKIP_LINES > 0:
            IOS_SKIP_LINES = IOS_SKIP_LINES-1
            continue
            
        # otherwise, begin looking at the line
        # - first check to see if we are at a change of state line
        if line.startswith('*FILE'):
            IOS_READ_STATE = 'FILE'
        elif line.startswith('*ADMINISTRATION'):
            IOS_READ_STATE = 'ADMINISTRATION'
        elif line.startswith('*LOCATION'):
            IOS_READ_STATE = 'LOCATION'
        elif line.startswith('*INSTRUMENT'):
            IOS_READ_STATE = 'INSTRUMENT'
        elif line.startswith('*HISTORY'):
            IOS_READ_STATE = 'HISTORY'
        elif line.startswith('*COMMENTS'):
            IOS_READ_STATE = 'COMMENTS'
        elif line.startswith('*CALIBRATION'):
            IOS_READ_STATE = 'CALIBRATION'
        elif line.startswith('*END OF HEADER'):
            IOS_READ_STATE = 'DATA'
        else:
            # otherwise, handle the current line depending on file state
            if IOS_READ_STATE is 'FILE':
                dat = ios_read_state_file(dat,line)
            elif IOS_READ_STATE is 'FILE_TABLE_CHANNELS':
                dat = ios_read_state_file_table_channels(dat,line)
            elif IOS_READ_STATE is 'ADMINISTRATION':
                dat = ios_read_state_admin(dat,line)
            elif IOS_READ_STATE is 'LOCATION':
                dat = ios_read_state_location(dat,line)
            elif IOS_READ_STATE is 'DATA':
                dat = ios_read_state_data(dat,line)
    
    # make sure to close the file
    IOS_FI.close()
    
    # return the modified data structure
    return dat

def ios_read_state_data(dat,line):
    # define the globals, otherwise the code redefines these variables within new scope
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI
    
    # split each row into separate entries
    raw_dat = line.split()
    
    # loop through the variables and match up
    # - the variables in $TABLE - CHANNELS are in the same order
    #   as they appear in the data section of the CTD file
    for count,var in enumerate(dat['Variables']):
        if count < len(raw_dat):
            try:
                dat['DATA'][count].append(float(raw_dat[count]))
            except:
                print '> ERR: ', raw_dat[count]
                dat['DATA'][count].append(np.nan)
    
    # return the modified data structure
    return dat

def ios_read_state_admin(dat,line):
    # define the globals, otherwise the code redefines these variables within new scope
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI
    
    if ':' in line:
        # store the admin data, but don't necessarily do anything with it
        dat[line.split(':')[0].strip()] = ' '.join(line.split(':')[1:]).strip()
    # return the modified data structure
    return dat
        
def ios_read_state_location(dat,line):
    # define the globals, otherwise the code redefines these variables within new scope
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI
    
    # check if the lines are lat/lon
    # - if they are, then modify them from degree minute.decimal string to floating point
    # RLI: need to check N/S/E/W modifiers on each to determine signage
    if 'LATITUDE' in line:
        dat['Latitude'] = float(line.split(':')[1].split()[0])+float(line.split(':')[1].split()[1])/60.0
    elif 'LONGITUDE' in line:
        dat['Longitude'] = -(float(line.split(':')[1].split()[0])+float(line.split(':')[1].split()[1])/60.0)
    elif ':' in line:
        # otherwise, just store the data as it appears
        dat[line.split(':')[0].strip()] = ' '.join(line.split(':')[1:]).strip()
    return dat

def ios_read_state_file_table_channels(dat,line):
    # define the globals, otherwise the code redefines these variables within new scope
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI

    # if we've reached the end of the TABLE, then swap back to N/A state as the
    # rest of the *FILE section is not useful info
    if '$END' in line:
        IOS_READ_STATE = 'N/A'
    else:
        # otherwise, we have a variable defined (note that we've skipped the two header
        # rows of the table by this point)
        tmpstr = line.split()
        
        # create the variable dictionary, and instantiate an empty list at the end of the 
        # dat['DATA'] list
        dat['Variables'].append({'Name' : tmpstr[1], 'Units' : tmpstr[2]})
        dat['DATA'].append([])
    return dat
        
def ios_read_state_file(dat,line):
    global IOS_READ_STATE, IOS_SKIP_LINES, IOS_FI
    if 'START TIME' in line:
        # this complicated statement parses the time to something digestible
        # by the dateutil class
        tmp_str = ' '.join(':'.join(line.split(':')[1:]).split()[1:])
        # date is saved by a string right now -- will have to 
        # save year/month/day format
        dat['Date'] = tmp_str
    elif '$TABLE:' in line:
        # check if we're looking at the CHANNELS table
        if 'CHANNELS' in line:
            IOS_READ_STATE = 'FILE_TABLE_CHANNELS'
            IOS_SKIP_LINES = 2
    elif ':' in line:
        # otherwise just save whatever is defined in the line
        dat[line.split(':')[0].strip()] = ' '.join(line.split(':')[1:]).strip()
        
    # return the modified data structure
    return dat
