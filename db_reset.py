# Simple script to reset the sqlite db if it gets screwed up because of testing

import pandas as pd
import sqlalchemy as sq
import datetime as dt
import re

def airline_abbrev_scrape():
    # Read in airline abbreviations
    cols = ['Airline', 'Country', 'IATA/ICAO Codes']
    df = pd.DataFrame(columns = cols)
    airlines = {}

    i = 0
    for x in pd.read_html('https://abbreviations.yourdictionary.com/articles/airline-abbreviations-for-major-carriers.html',header=0):
        i += 1
        try:
            x.columns = cols # some columns had spaces in them
        except:
            pass
        airlines[i] = x

    for i in [1,2,3,4,5,6,7]:
        df = df.append(airlines[i])

    # Split code types
    new = df['IATA/ICAO Codes'].str.split('/', expand = True)
    new.columns = ['IATA', 'ICAO']
    df = pd.concat([df, new], axis=1).drop('IATA/ICAO Codes',axis=1)

    # Add Frontier Airlines, which was missing from tables
    df = df.append({'Airline':'Frontier Airlines','Country':'USA','IATA':'F9','ICAO':'FFT'}, ignore_index=True)

    # Remove spaces
    df['IATA'] = df['IATA'].str.strip()
    return df

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

    # Reset airline abbrevs table
    df = airline_abbrev_scrape()
    df.to_sql('airline_info',con=cnx,index=False,if_exists='replace')
    
    print("The 'location' and 'ticket_info' tables were successfully reset!")
    
except:
    print("An error occurred. Check it out.")