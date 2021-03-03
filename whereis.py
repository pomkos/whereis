import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd
from apps import db_stuff as d

engine = sq.create_engine('sqlite:///data/find_me.db')
cnx = engine.connect()

df = pd.DataFrame({
    'current_loc':['current city'],
    'current_date':[dt.datetime.now().date()],
    'future_loc':['new city'],
    'future_date':['April 1; April 28'],
    'confirm_code':['unknown'],
    'message':['unknown']
})

df.to_sql('location',con=cnx,if_exists='replace',index=False)

def message_maker(data, data_type):
    '''
    Creates message + link to the flight tracker
    '''
    if data_type == 'track':
        message = f"[Track this flight here](https://www.flightstats.com/v2/flight-tracker/{data['plane_code']}/{data['flight_num']}?year={data['year_depart']}&month={data['month_depart']}&date={data['day_depart']})!"

        return message
    
    elif data_type == 'loc_current':
        message = f"""
        * As of {data[0]} he is in __{data[1]}__."""
        return message
    
    elif data_type == 'loc_future':
        message = f"""
        * He will be in __{data[1]}__ on {data[0]}"""
        
        return message

def check_how_tickets():
    '''
    Double checks how many tickets to show and generate links for
    '''
    db = d.dbInfo()
    tickets = db.read_info('ticket_info')
    
    tickets = tickets[tickets['date_depart'] >= dt.datetime.now()]
    
    return tickets, len(tickets)
    
def app():
    st.title("Where in the world is Peter?")
    db = d.dbInfo()
    new_info = db.read_info(table='location')
    
    future_loc = new_info.loc['future_loc'].title()
    future_date = new_info.loc['future_date'].title()
    
    current_date = dt.datetime.strftime(new_info.loc['current_date'].date(), "%B %d")
    current_loc = new_info.loc['current_loc'].title()
    
    code = new_info.loc['confirm_code'].upper()
    
    message = message_maker([current_date, current_loc], data_type = "loc_current")
        
    future_date = future_date.split(';')
    future_loc = future_loc.split(";")
        
    if len(future_date) == len(future_loc):
        for i in range(len(future_date)):
            message += message_maker([future_date[i], future_loc[i]], data_type = "loc_future")
            
    st.write(message)
        
    try:
        st.image("images/pete.jpg",use_column_width='auto')
    except:
        st.error("No image found")
        
    st.write("## Picking Pete up?")
    tickets, num = check_how_tickets()
    
    if num == 0:
        st.info("No tickets were bought yet, check back later.")
        
    else:
        try:
            for tick in range(1,num):
                data = dict(tickets.iloc[tick,:])
                with st.beta_expander(f"Ticket {tick}"):
                    message = message_maker(data, data_type = 'track')
                    st.write(message)
                    st.image(f"images/ticket_{tick}.png", use_column_width='auto')
        except:
            ''
app()