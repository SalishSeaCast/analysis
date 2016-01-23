
# loops through directory structure and creates tables based on csv files; adds data
# produces sqlite database
#

from sqlalchemy import create_engine, Column, String, Integer, Numeric, MetaData, Table, type_coerce, ForeignKey
from sqlalchemy.orm import mapper, create_session, relationship
from sqlalchemy.ext.declarative import declarative_base
import csv
from sqlalchemy import case
import numpy as np
from sqlalchemy.ext.automap import automap_base
import sqlalchemy.types as types
import numbers
from sqlalchemy.sql import and_, or_, not_
import os
import glob
import re

def main():

    basepath='/ocean/eolson/MEOPAR/obs/'
    basedir=basepath + 'NANOOS_PRISMCRUISES/'
    dbname='PRISM'
    
    fout=open(basedir+'createDB_log.txt','w')
    
    engine = create_engine('sqlite:///' + basedir + dbname + '.sqlite')
    Base=declarative_base()

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

    def coltype(ikey):
        typedict = {
            'cast_lat': forceNumeric(),
            'cast_lon': forceNumeric(),
            'cast_dbid': forceInt(),
            'depth': forceNumeric(),
            'value': forceNumeric(),
            'station_lat': forceNumeric(),
            'station_lon': forceNumeric(),
        }
        return typedict.get(ikey, String())
    
    dirs=[x for x in os.listdir(basedir) if os.path.isdir(basedir+x)]
    fout.write('directories to be processed:\n' + repr(dirs) + '\n\n')
    
    f0Obs=glob.glob(basedir+dirs[0]+'/*_ObservationsData_*.csv')[0]
    fout.write('f0Obs='+f0Obs+'\n')
    f0Info=glob.glob(basedir+dirs[0]+'/*_Information_*.csv')[0]
    fout.write('f0Info='+f0Info+'\n')
    f0Cast=glob.glob(basedir+dirs[0]+'/*_CastInformation_*.csv')[0]
    fout.write('f0Cast='+f0Cast+'\n\n')

    f=open(f0Info,'r')
    headerInfo=re.split('\s*,\s*',f.readline().rstrip())
    #print (headerInfo)
    headerInfo = [x for x in headerInfo if x not in {'cruise_code'}]
    #print(headerInfo)
    f.close()
    f=open(f0Cast,'r')
    headerCast=re.split('\s*,\s*',f.readline().rstrip())
    #print (headerCast)
    headerCast = [x for x in headerCast if x not in {'cast_dbid'}]
    #print(headerCast)
    f.close()
    f=open(f0Obs,'r')
    headerObs=re.split('\s*,\s*',f.readline().rstrip())
    #print (headerObs)
    headerObs = [x for x in headerObs if x not in {'cast_dbid'}]
    #print(headerObs)
    f.close()

    class InfoTBL(Base):
        __table__ = Table('InfoTBL', Base.metadata, 
                    Column('cruise_code', String, primary_key=True),
                    *(Column(cname, coltype(cname)) for cname in headerInfo))


    class CastTBL(Base):
        __table__=Table('CastTBL', Base.metadata,
                    Column('cast_dbid', forceInt, primary_key=True),
                    Column('cruise_code',String, ForeignKey('InfoTBL.cruise_code')),
                    *(Column(cname, coltype(cname)) for cname in headerCast))
        
        info=relationship(InfoTBL, primaryjoin=__table__.c.cruise_code == InfoTBL.cruise_code)
        

    class ObsTBL(Base):
        __table__=Table('ObsTBL', Base.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('cast_dbid', forceInt, ForeignKey('CastTBL.cast_dbid')),
                        *(Column(cname, coltype(cname)) for cname in headerObs))
               
        cast=relationship(CastTBL, primaryjoin=__table__.c.cast_dbid == CastTBL.cast_dbid)
    
    Base.metadata.create_all(engine)
    session = create_session(bind = engine, autocommit = False, autoflush = True)
    
    fout.write('Files processed:\n')
    for idir in dirs:
        fObs=glob.glob(basedir+idir+'/*_ObservationsData_*.csv')[0]
        fInfo=glob.glob(basedir+idir+'/*_Information_*.csv')[0]
        fCast=glob.glob(basedir+idir+'/*_CastInformation_*.csv')[0]
        
        f=open(fInfo,'r')
        cf = csv.DictReader(f, delimiter=',')
        ri=0
        for row in cf:
            ri+=1
            session.execute(InfoTBL.__table__.insert().values(**row))
            if ri>1: 
                print('WARNING: Multiple rows in Info csv')
        cc=row['cruise_code']
        f.close()
        fout.write(fInfo+'\n')
        
        f=open(fCast,'r')
        cf = csv.DictReader(f, delimiter=',')
        for row in cf:
            session.execute(CastTBL.__table__.insert().values(cruise_code=cc,**row))
        f.close()
        fout.write(fCast+'\n')

        f=open(fObs,'r')
        cf = csv.DictReader(f, delimiter=',')
        for row in cf:
            session.execute(ObsTBL.__table__.insert().values(**row))
        f.close()
        fout.write(fObs+'\n')
    
    session.commit()
    
    # identified several rows containing zero salinity values in oceanic locations; set those values to None;
    # create record in log file
    fout.write('\nThe following rows were changed so that salinity values were None rather than zero:\n')
    qry=session.query(ObsTBL).filter_by(variable = 'water_salinity', value=0).all()
    for row in qry:
        fout.write('\n')
        fout.writelines("%s" % column.name + ':' + str(getattr(row, column.name)) +'\t ' for column in row.__table__.columns)
    session.query(ObsTBL).filter_by(variable = 'water_salinity', value=0).update({ 'value': None })

    session.commit()
    
    fout.close()
    session.close()
    engine.dispose()



if __name__ == "__main__":
    main()
