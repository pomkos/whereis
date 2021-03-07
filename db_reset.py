# Simple script to reset the sqlite db if it gets screwed up because of testing

import pandas as pd
import sqlalchemy as sq
import datetime as dt

try:
    engine = sq.create_engine('sqlite:///data/find_me.db')
    cnx = engine.connect()

    # Reset the location table
    df_loc = pd.DataFrame({
        'current_loc':['current city'],
        'current_date':[dt.datetime.now().date()],
        'future_loc':['new city'],
        'future_date':['April 1; April 28'],
        'confirm_code':['unknown'],
        'message':['unknown']
    })
    df_loc.to_sql('location',con=cnx,if_exists='replace',index=False)

    # Reset the ticket info table
    df_ticket = pd.DataFrame({
        'plane_code':['unknown'],
        'flight_num':['unknown'],
        'year_depart':['unknown'],
        'month_depart':['unknown'],
        'day_depart':['unknown'],
        'confirm_code':['unknown'],
        'date_depart':[dt.datetime.strptime('02-27-2021 23:59','%m-%d-%Y %H:%M')],
        'date_added':[dt.datetime.now()]
    })
    df_ticket.to_sql('ticket_info',con=cnx,if_exists='replace',index=False)
    
    print("The 'location' and 'ticket_info' tables were successfully reset!")
    
except:
    print("An error occurred. Check it out.")