import pandas as pd
import sqlalchemy as sq
import datetime as dt

class dbInfo():
    def __init__(self):
        engine = sq.create_engine("sqlite:///data/find_me.db")
        cnx = engine.connect()
        
        self.engine = engine
        self.cnx = cnx
        
    def write_info(self,current_loc, future_loc, future_date):
        meta = sq.MetaData()
        meta.reflect(bind = self.engine)
        table = meta.tables['location']
        query = sq.insert(table).values(current_loc = current_loc, 
                                       current_date = dt.datetime.now().date(),
                                       future_loc = future_loc,
                                       future_date = future_date
                                      )
        ResultProxy = self.cnx.execute(query)
    
    def read_info(self):
        df = pd.read_sql("location",con=self.cnx)
        latest_info = df.loc[len(df)-1,:]
        self.df = df
        return latest_info
