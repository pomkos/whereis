import pandas as pd # type: ignore
import sqlalchemy as sq # type: ignore
import datetime as dt
from typing import List, Any, Literal, Tuple

class dbInfo():
    def __init__(self):
        '''
        Series of functions to manipulate an SQLite database
        '''
        engine = sq.create_engine("sqlite:///data/find_me.db")
        cnx = engine.connect()
        meta = sq.MetaData()
        meta.reflect(bind = engine)
        
        self.engine = engine
        self.cnx = cnx
        self.meta = meta
        
    def write_info(self, table_name: Literal['location', 'ticket_info', 'airline_info'], data: Any) -> None:
        '''
        Writes everything in the {data} list to {table_name} in db

        input
        ------
        table_name
            Must be one of location or ticket_info
        data
            The data to be saved to the table. Must be a list of one of below, with variables in that order:
                - current_loc, future_loc, future_date, confirm_code, message
                - plane_code, flight_num, year_depart, month_depart, day_depart, confirm_code, date_depart
                - airline, country, iata, icao
        '''
        table = self.meta.tables[table_name]
        if table_name == 'location':
            current_loc, future_loc, future_date, confirm_code, message = data
            query = sq.insert(table).values(
                current_loc = current_loc, 
                current_date = dt.datetime.now().date(),
                future_loc = future_loc,
                future_date = future_date,
                confirm_code = confirm_code,
                message = message
                                          )
        elif table_name == 'ticket_info':
            plane_code, flight_num, year_depart, month_depart, day_depart, confirm_code, date_depart = data
            query = sq.insert(table).values(
                plane_code = plane_code,
                flight_num = flight_num,
                year_depart = year_depart,
                month_depart = month_depart,
                day_depart = day_depart,
                confirm_code = confirm_code,
                date_depart = date_depart,
                date_added = dt.datetime.now()
            )
        elif table_name == 'airline_info':
            airline, country, iata, icao = data
            query = sq.insert(table).values(
                Airline = airline,
                Country = country,
                IATA = iata,
                ICAO = icao
            )
        ResultProxy = self.cnx.execute(query)
        
    
    def read_info(self, table_name: Literal['location', 'ticket_info', 'airline_info']) -> pd.DataFrame:
        '''
        Retrieves information from {table}
        '''
        if table_name == 'location':
            df = pd.read_sql(table_name, con=self.cnx)
            latest_info = df.loc[len(df)-1,:]
            return latest_info

        elif table_name == 'ticket_info':
            tickets = pd.read_sql("ticket_info",con=self.cnx)
            return tickets

        elif table_name == 'airline_info':
            airline = pd.read_sql("airline_info",con=self.cnx)
            return airline