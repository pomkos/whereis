import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd
from apps import db_stuff as d

def message_maker(data):
    '''
    Creates message + link to the flight tracker
    '''
    message = f"[Track this flight here](https://www.flightstats.com/v2/flight-tracker/{data['plane_code']}/{data['flight_num']}?year={data['year_depart']}&month={data['month_depart']}&date={data['day_depart']})!"
    
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
    future_date = dt.datetime.strftime(new_info.loc['future_date'].date(), "%B %d")
    future_loc = new_info.loc['future_loc'].title()
    current_date = dt.datetime.strftime(new_info.loc['current_date'].date(), "%B %d")
    current_loc = new_info.loc['current_loc'].title()
    code = new_info.loc['confirm_code'].upper()
    

    st.write(f"""
    * As of {current_date} he is in __{current_loc}__.
    * He will be in __{future_loc}__ on {future_date}
    """)
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
                    message = message_maker(data)
                    st.write(message)
                    st.image(f"images/ticket_{tick}.png", use_column_width='auto')
        except:
            ''
app()