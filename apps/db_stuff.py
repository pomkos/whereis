import pandas as pd
import sqlalchemy as sq
import datetime as dt

class dbInfo():
    def __init__(self):
        engine = sq.create_engine("sqlite:///data/find_me.db")
        cnx = engine.connect()
        meta = sq.MetaData()
        meta.reflect(bind = engine)
        
        self.engine = engine
        self.cnx = cnx
        self.meta = meta
        
    def write_info(self,table_name, data):
        table = self.meta.tables[table_name]
        if table_name == 'location':
            current_loc, future_loc, future_date, confirm_code, message = data
            query = sq.insert(table).values(current_loc = current_loc, 
                                           current_date = dt.datetime.now().date(),
                                           future_loc = future_loc,
                                           future_date = future_date,
                                           confirm_code = confirm_code,
                                           message = message
                                          )
        elif table_name == 'ticket_info':
            query = sq.insert(table).values(
                plane_code = data[0],
                flight_num = data[1],
                year_depart = data[2],
                month_depart = data[3],
                day_depart = data[4],
                confirm_code = data[5],
                date_depart = data[6],
                date_added = dt.datetime.now()
            )
        ResultProxy = self.cnx.execute(query)
        
    
    def read_info(self, table):
        df = pd.read_sql(table,con=self.cnx)
        if table == 'location':
            latest_info = df.loc[len(df)-1,:]
            return latest_info
        elif table == 'ticket_info':
            tickets = pd.read_sql("ticket_info",con=self.cnx)
            return tickets
        elif table == 'airline_info':
            airline = pd.read_sql("airline_info",con=self.cnx)
            return airline