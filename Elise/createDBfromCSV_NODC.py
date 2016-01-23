# inputs: csvfile, sqlitefile: filenames and paths for input and output
# reads csvfile and creates database in sqlitefile with 2 tables
#         table and profile
#
# THE PLAN:
# 0) identify all variable types in file?? (need them to create the table structure)
# 1) locate first section
# -> locate cast variable and store
# 2) enter location data in station table with cast number as primary key
# -> locate each important data type and verify units (enter as text just in case?)
# 3) enter profile data in profile table with cast number key to station table
# 4) repeat for each cast

from sys import argv
from sqlalchemy import create_engine, Column, String, Integer, Numeric, MetaData, Table, type_coerce
from sqlalchemy.orm import mapper, create_session
import sqlalchemy.types as types
import numbers
import re

def main(csvfile, sqlitefile):

    # open csvfile for reading
    f=open(csvfile,'r')

    # create empty set to hold all profile variables in the file
    varlist=set()
    # scan all sections labeled 'VARIABLES' and assemble variable names; remove 'F' and 'O'
    for line in f:
        # if start of line matches 'VARIABLES', list all variables and add unique to group
        if re.search('^VARIABLES', line):
            # split line at commas
            varlist0=re.split('\s*,\s*',line)
            varlist = varlist | {x for x in varlist0 if x not in {'F','O','','VARIABLES'}}

    # add additional variable names to store flag and unit info
    varlistFOu=varlist
    varlistFOu=varlistFOu | {x+'_units' for x in varlist}
    varlistFOu=varlistFOu | {x+'_F' for x in varlist}
    varlistFOu=varlistFOu | {x+'_O' for x in varlist}
    varlistFOu=varlistFOu | {x+'_profFlagF' for x in varlist}

    # create database file
    engine = create_engine('sqlite:///' + sqlitefile + '.sqlite')
    metadata = MetaData(bind=engine)

    # define custom types:
    class forceNumeric(types.TypeDecorator):
        impl = types.Numeric
        def process_bind_param(self, value, dialect):
            try:
                int(float(value))
            except:
                value = None
            return value

    class forceInt(types.TypeDecorator):
        impl = types.Integer
        def process_bind_param(self, value, dialect):
            try:
                int(value)
            except:
                value = None
            return value

    # create station table with basic variable names
    # primary key is CAST #
    tableStation = Table('stationTBL', metadata, Column('CastID', Integer, primary_key=True),
                         Column('NODC_Cruise_ID', String), Column('Originators_Station_ID', String),
                         Column('Originators_Cruise_ID', String), Column('Latitude',forceNumeric), 
                         Column('Longitude',forceNumeric), Column('Year',forceInt), 
                         Column('Month',forceInt), Column('Day',forceInt), 
                         Column('Time_hr',forceNumeric), Column('Country', String), 
                         Column('Accession_Number',forceInt), Column('Platform', String), 
                         Column('Institute', String), Column('Bottom_depth_m',forceNumeric), Column('Secchi_disk_depth_m',forceNumeric))
    tableStation.create()
    class Station(object): pass
    mapper(Station, tableStation)

    # create profile table with variable, variable_F, variable_O, variable_units with CAST as key to station table
    tableProfile = Table('profileTBL', metadata, Column('ProfileID', Integer, primary_key=True),
                          Column('CastID', Integer),
                         *(Column(colname, forceNumeric) for colname in varlistFOu))
    tableProfile.create()
    class Prof(object): pass
    mapper(Prof, tableProfile)

    # read lines in CSV file and parse them into sqlite tables
    f.seek(0) # return to beginning of file
    inheader=False
    inprof=False
    for line in f:
        # if line matches 'CAST', start header
        if re.search('^CAST', line):
            inheader=True
            headerdict={}
        # if line matches 'VARIABLES', end header
        elif re.search('^VARIABLES', line):
            #print(headerdict)
            tableStation.insert().values(**headerdict).execute()
            inheader = False
            # add header entry here
            inprof = True
        elif re.search('^END\sOF\sVARIABLES',line):
            inprof = False
            # add profile entry here
        if inheader:
            splitline=re.split('\s*,\s*',line)
            if re.match('CAST', splitline[0]):
                castID=splitline[2]
                headerdict['CastID']=castID
            elif re.match('NODC Cruise ID', splitline[0]):
                headerdict['NODC_Cruise_ID']=splitline[2]
            elif re.match('Originators Station ID', splitline[0]):
                headerdict['Originators_Station_ID']=splitline[2]
            elif re.match('Originators Cruise ID', splitline[0]):
                headerdict['Originators_Cruise_ID']=splitline[2]
            elif re.match('Latitude', splitline[0]):
                headerdict['Latitude']=splitline[2]
                if not re.match('decimal degrees', splitline[3]):
                    print('ERROR: Latitude units: ', splitline[3], ', CAST=', headerdict['CastID'])
            elif re.match('Longitude', splitline[0]):
                headerdict['Longitude']=splitline[2]
            elif re.match('Year', splitline[0]):
                headerdict['Year']=splitline[2]
            elif re.match('Month', splitline[0]):
                headerdict['Month']=splitline[2]
            elif re.match('Day', splitline[0]):
                headerdict['Day']=splitline[2]
            elif re.match('Time', splitline[0]):
                headerdict['Time_hr']=splitline[2]
                if not re.match('decimal hours', splitline[3]):
                    print('ERROR: Hour units: ', splitline[3], ', CAST=', headerdict['CastID'])
            elif re.match('Country', splitline[0]):
                headerdict['Country']=splitline[2]
            elif re.match('Accession Number', splitline[0]):
                headerdict['Accession_Number']=splitline[2]
            elif re.match('Platform', splitline[0]):
                headerdict['Platform']=splitline[2]
            elif re.match('Institute', splitline[0]):
                headerdict['Institute']=splitline[2]
            elif re.match('Bottom depth', splitline[0]):
                headerdict['Bottom_depth_m']=splitline[2]
            elif re.match('Secchi disk depth', splitline[0]):
                headerdict['Secchi_disk_depth_m']=splitline[2]
        elif inprof:
            splitline=re.split('\s*,\s*',line)
            if re.match('VARIABLES', splitline[0]):
                # remove any empty variable name entries and save vars in varline:
                sear=re.compile('^.+$').search
                varline=[m.group(0) for m in map(sear, splitline) if m]
                # n = number of variables in prof
                n=int((len(varline)-1)/3)
            elif re.match('UNITS', splitline[0]):
                runits=splitline
            elif re.match('Prof-Flag', splitline[0]):
                rflags=splitline
            else:
                profdict={}
                for i in range(0,n):
                    profdict[varline[i*3+1]]=splitline[i*3+1]
                    profdict[varline[i*3+1]+'_F']=splitline[i*3+2]
                    profdict[varline[i*3+1]+'_O']=splitline[i*3+3]
                    profdict[varline[i*3+1]+'_units']=runits[i*3+1]
                    profdict[varline[i*3+1]+'_profFlagF']=rflags[i*3+2]
                    profdict['CastID']=castID
                #print(profdict)
                tableProfile.insert().values(**profdict).execute()

if __name__ == "__main__":
    main(arvg)
