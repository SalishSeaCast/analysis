from sqlalchemy import create_engine, Column, String, Integer, Numeric, MetaData, Table, type_coerce, ForeignKey
from sqlalchemy.orm import mapper, create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.types as types
import re
import os
import glob

def main():

    basepath='/ocean/eolson/MEOPAR/obs/'
    basedir=basepath + 'DFOOPDB/'
    dbname='DFO_OcProfDB'

    fout=open(basedir+'createDBfromDFO_OPDB_log.txt','w')
    ferr=open(basedir+'createDBfromDFO_OPDB_errors.txt','w')
    fout.write('Files processed:\n')

    dirs=[x for x in os.listdir(basedir) if (os.path.isdir(basedir+x) and not re.match('^\.', x))]
    dirs.sort()

    # create set of variable names for Obs table: see develope_createDBfromDFO_OPDB.ipynb
    choosevars={'Ammonia', 'Ammonium', 'Flag_Ammonium', 'Carbon_Dissolved_Organic',
        'Flag_Carbon_Dissolved_Organic', 'Carbon_Particulate_Organic', 'Carbon_Particulate_Total',
        'Flag_Carbon_Particulate_Total','Flag_Chlorophyll', 'Chlorophyll_Extracted',
        'Flag_Chlorophyll_Extracted', 'Chlorophyll_Extracted_gt0point7um',
        'Chlorophyll_Extracted_gt5point0um', 'Chlorophyll_plus_PhaeoPigment_Extracted', 'Date',
        'Depth', 'Depth_Nominal', 'Flag_Salinity', 'Flag_Salinity_Bottle', 'Flag_Silicate',
        'Flag_pH', 'Fluorescence_URU', 'Fluorescence_URU_Seapoint', 'Fluorescence_URU_Seatech',
        'Fluorescence_URU_Wetlabs', 'Latitude', 'Longitude', 'Nitrate', 'Flag_Nitrate',
        'Nitrate_plus_Nitrite', 'Flag_Nitrate_plus_Nitrite', 'Nitrate_plus_nitrite_ISUS',
        'Nitrate_plus_nitrite_ISUS_Voltage', 'Nitrite', 'Flag_Nitrite','Nitrogen_Dissolved_Organic',
        'Flag_Nitrogen_Dissolved_Organic', 'Nitrogen_Particulate_Organic','Nitrogen_Particulate_Total',
        'Flag_Nitrogen_Particulate_Total', 'Oxygen', 'Quality_Flag_Oxyg','Oxygen_Dissolved',
        'Flag_Oxygen_Dissolved', 'Oxygen_Dissolved_SBE', 'PAR', 'PAR_Reference',
        'PhaeoPigment_Extracted', 'Flag_PhaeoPigment_Extracted', 'Flag_Phaeophytin',  'Phosphate',
        'Flag_Phosphate','Quality_Flag_Phos', 'Phosphate(inorg)', 'Phytoplankton_Volume', 'Pressure',
        'Pressure_Reversing', 'Production_Primary', 'Quality_Flag_Nitr', 'Quality_Flag_Time',
        'Quality_Flag_Tota', 'Salinity', 'Salinity_Bottle', 'Salinity_T0_C0', 'Salinity_T1_C1',
        'Salinity__Pre1978','Quality_Flag_Sali','Salinity__Unknown', 'Sample_Method', 'Silicate',
        'Quality_Flag_Sili', 'Station', 'Temperature', 'Quality_Flag_Temp','Temperature_Draw',
        'Temperature_Primary','Temperature_Reversing', 'Temperature_Secondary', 'Time', 'Time_of_Obs',
        'Total_Phosphorus', 'Transmissivity', 'Turbidity_Seapoint'}
    varlistu=choosevars | {x+'_units' for x in choosevars if not re.search('Flag', x)}

    # create database and prepare tables
    engine = create_engine('sqlite:///' + basedir + dbname + '.sqlite')
    Base=declarative_base()

    # create classes for custom data types
    class forceNumeric(types.TypeDecorator):

        impl = types.Numeric
        def process_bind_param(self, value, dialect):
            try:
                int(float(value))
                if int(float(value))==-99:
                    value=None
            except:
                value = None
            if (str(value).startswith('-99') or str(value).startswith('9999')):
                value = None
            return value

    class forceInt(types.TypeDecorator):

        impl = types.Integer
        def process_bind_param(self, value, dialect):
            try:
                int(value)
                if int(value)==-99:
                    value=None
            except:
                value = None
            if (str(value).startswith('-99') or str(value).startswith('9999')):
                value = None
            return value

    # create function that returns datatype for a given field name
    def coltype(ikey):
        typedict = {
            'Date': String(),
            'Sample_Method': String(),
            'Station': String(),
            'Time': String(),
            'Time_of_Obs.': String(),
        }
        for varn in varlistu:
            if (re.search('Flag', varn) or varn in varlistu-choosevars):
                typedict[varn]=String()
        return typedict.get(ikey, forceNumeric())

    # define Table Classes:
    class StationTBL(Base):
        __table__=Table('StationTBL', Base.metadata,
                    Column('ID', Integer, primary_key=True),
                    Column('STATION', String),
                    Column('EVENT NUMBER', String),
                    Column('LATITUDE', String),
                    Column('Lat', forceNumeric),
                    Column('LONGITUDE', String),
                    Column('Lon', forceNumeric),
                    Column('WATER DEPTH', forceNumeric),
                    Column('WDIR', forceNumeric),
                    Column('WSPD', forceNumeric),
                    Column('START TIME', String),
                    Column('StartDay',forceNumeric),
                    Column('StartMonth',forceNumeric),
                    Column('StartYear',forceNumeric),
                    Column('StartHour',forceNumeric),
                    Column('StartTimeZone',String),
                    Column('DATA DESCRIPTION', String),
                    Column('MISSION', String),
                    Column('AGENCY', String),
                    Column('COUNTRY', String),
                    Column('PROJECT', String),
                    Column('SCIENTIST', String),
                    Column('PLATFORM', String),
                    Column('sourceFile', String))

    class ObsTBL(Base):
        __table__=Table('ObsTBL', Base.metadata,
                        Column('ID', Integer, primary_key=True),
                        Column('sourceFile', String),
                        Column('StationTBLID', forceInt, ForeignKey('StationTBL.ID')),
                        *(Column(cname, coltype(cname)) for cname in varlistu))
        station=relationship(StationTBL, primaryjoin=__table__.c.StationTBLID == StationTBL.ID)

    Base.metadata.create_all(engine)
    session = create_session(bind = engine, autocommit = False, autoflush = True)

    stationNo=0
    for cdir in dirs:
        print(cdir)
        cdirpath=os.path.join(basedir, cdir)
        filenames = [f for f in os.listdir(cdirpath) ] #if ( f.endswith('.cnv') or f.endswith('.ctd'))
        filenames.sort()
        for file in filenames:
            stationNo+=1
            sourceFile=os.path.join(cdir,file)
            fout.write(sourceFile+'\n')
            varNames={}
            varLens={}
            varUnits={}
            stationData={}
            stationData['ID']=stationNo
            stationData['sourceFile']=sourceFile
            with open(os.path.join(cdirpath, file), 'rt', encoding = "ISO-8859-1") as f:
                infile=False
                invars=False
                indetail=False
                inadmin=False
                inloc=False
                indata=False
                detformat=False
                for line in f:
                    if infile:
                        if re.match('\s*\$', line) or len(line)==0:
                            infile=False
                        else:
                            splitline=re.split('\s*\:\s*',line.strip(), maxsplit=1)
                            if re.match('START TIME',splitline[0]):
                                stationData['START TIME']=splitline[1]
                                splits=re.split('\s* \s*',splitline[1])
                                stationData['StartTimeZone']=splits[0]
                                date=splits[1]
                                time=splits[2]
                                stationData['StartYear']=date[0:4]
                                stationData['StartMonth']=date[5:7]
                                stationData['StartDay']=date[8:]
                                splitTime=re.split('\:',time)
                                stationData['StartHour']=float(splitTime[0])+float(splitTime[1])/60.0+float(splitTime[2])/3600.0
                            elif re.match('DATA DESCRIPTION',splitline[0]):
                                stationData['DATA DESCRIPTION']=splitline[1]
                    if invars:
                        if re.search('\$END', line):
                            invars=False
                        else:
                            test=re.findall("'.*?'",line) # (.*? matches anything but chooses min len match - not greedy)
                            for expr in test:
                                line=re.sub(re.escape(expr),re.sub(' ','_',expr),line) # remove spaces from items in quotes
                            splitline=re.split('\s* \s*',line.strip())
                            if re.match('[0-9]', splitline[0]):
                                varnum=int(splitline[0])
                                cvar=splitline[1]
                                cvar = re.sub('(?<=[0-9])*\.(?=[0-9])','point',cvar) # decimal points -> point
                                cvar = re.sub('\-','',cvar) # remove - from column names
                                cvar = re.sub('\:','_',cvar) # replace : with _
                                cvar = re.sub('\>','gt',cvar) # replace > with gt
                                cvar = re.sub('\<','lt',cvar) # replace < with lt
                                cvar = re.sub('(\'|\.)','',cvar) # remove special characters (' and .)
                                cunits = splitline[2].strip()
                                varNames[varnum]=cvar
                                varUnits[varnum]=cunits
                    elif indetail:
                        detcount+=1
                        if re.search('\$END', line):
                            indetail=False
                        elif (detcount==1 and re.match('\s*\!\s*No\s*Pad\s*Start\s*Width', line)):
                            detformat=True
                        else:
                            if (detformat and not re.match('\s*\!',line)):
                                test=re.findall("'.*?'",line) # (.*? matches anything but chooses min len match - not greedy)
                                for expr in test:
                                    line=re.sub(re.escape(expr),re.sub(' ','_',expr),line) # remove spaces from items in quotes
                                splitline=re.split('\s* \s*',line.strip())
                                varnum=int(splitline[0])
                                try:
                                    varwid=int(splitline[3])
                                except:
                                    detformat=False
                                varLens[varnum]=varwid
                    elif inadmin:
                        if len(line)==0:
                            inadmin=False
                        else:
                            splitline=re.split('\s*\:\s*',line.strip(), maxsplit=1)
                            if re.match('MISSION',splitline[0]):
                                stationData['MISSION']=splitline[1]
                            elif re.match('AGENCY',splitline[0]):
                                stationData['AGENCY']=splitline[1]
                            elif re.match('COUNTRY',splitline[0]):
                                stationData['COUNTRY']=splitline[1]
                            elif re.match('PROJECT',splitline[0]):
                                stationData['PROJECT']=splitline[1]
                            elif re.match('SCIENTIST',splitline[0]):
                                stationData['SCIENTIST']=splitline[1]
                            elif re.match('PLATFORM',splitline[0]):
                                stationData['PLATFORM']=splitline[1]
                    elif inloc:
                        if len(line)==0:
                            inloc=False
                        else:
                            splitline=re.split('\s*\:\s*',line.strip(), maxsplit=1)
                            if re.match('STATION',splitline[0]):
                                try:
                                    stationData['STATION']=splitline[1]
                                except:
                                    print(line)
                                    return()
                            elif re.match('EVENT NUMBER',splitline[0]):
                                stationData['EVENT NUMBER']=splitline[1]
                            elif re.match('LATITUDE',splitline[0]):
                                stationData['LATITUDE']=splitline[1]
                                latparts=re.split('\s* \s*', splitline[1])
                                signdict={'N':1,'E':1,'S':-1,'W':-1}
                                staLat=signdict[latparts[2]]*(float(latparts[0])+float(latparts[1])/60.0)
                                stationData['Lat']=staLat
                            elif re.match('LONGITUDE',splitline[0]):
                                stationData['LONGITUDE']=splitline[1]
                                lonparts=re.split('\s* \s*', splitline[1])
                                signdict={'N':1,'E':1,'S':-1,'W':-1}
                                staLon=signdict[lonparts[2]]*(float(lonparts[0])+float(lonparts[1])/60.0)
                                stationData['Lon']=staLon
                            elif re.match('WATER DEPTH',splitline[0]):
                                stationData['WATER DEPTH']=splitline[1]
                            elif re.match('WDIR',splitline[0]):
                                stationData['WDIR']=re.split('\s* \s*',splitline[1])[0]
                            elif re.match('WSPD',splitline[0]):
                                stationData['WSPD']=re.split('\s* \s*',splitline[1])[0]
                    elif (indata and len(line)!=0 and not re.match('\s*\!',line)):
                        if detformat:
                            varVals={}
                            istart=0
                            for ii in range(1,1+max(varNames.keys())):
                                varVal=line[istart:(istart+varLens[ii])]
                                istart+=varLens[ii]
                                if varNames[ii] in varlistu:
                                    varVals[varNames[ii]]=varVal.strip()
                                if varNames[ii]+'_units' in varlistu:
                                    varVals[varNames[ii]+'_units']=varUnits[ii]
                            varVals['StationTBLID']=stationNo
                            varVals['sourceFile']=sourceFile
                            #SEND TO DATABASE
                            session.execute(ObsTBL.__table__.insert().values(**varVals))
                        else:
                            splitline=re.split('\s*\:\s*',line.strip())
                            if len(splitline)==max(varNames.keys()):
                                for ii in range(1,1+max(varNames.keys())):
                                    if varNames[ii] in varlistu:
                                        varVals[varNames[ii]]=splitline[ii].strip()
                                    if varNames[ii]+'_units' in varlistu:
                                        varVals[varNames[ii]+'_units']=varUnits[ii]
                                varVals['StationTBLID']=stationNo
                                varVals['sourceFile']=sourceFile
                                #SEND TO DATABASE
                                session.execute(ObsTBL.__table__.insert().values(**varVals))
                            else:
                                ferr.write('ERROR: filename:'+sourceFile+' line:'+line+'\n')
                    if re.match('![- ]*$',line):
                        tem=re.search('(?<=\!)[- ]*$',line)
                        splitline=re.split(r'\s',tem.group(0))
                        for ii in range(1, 1+len(splitline)):
                            varLens[ii]=len(splitline[ii-1])+1
                            detformat=True
                    if re.search('\*FILE', line):
                        infile=True
                    if re.search('\$TABLE\: CHANNELS', line):
                        invars=True
                    if re.search('\$TABLE\: CHANNEL DETAIL', line):
                        indetail=True
                        detcount=0
                    if re.search('\*ADMINISTRATION', line):
                        inadmin=True
                    if re.search('\*LOCATION', line):
                        inloc=True
                        inadmin=False
                    if re.search('\*END OF HEADER', line):
                        indata=True
                        inloc=False
                    if re.search('\$END',line):
                        inloc=False
                # SEND TO DATABASE (at file level)
                session.execute(StationTBL.__table__.insert().values(**stationData))
    session.commit()
    engine.dispose()
    fout.close()
    ferr.close()

if __name__== "__main__":
    main()
