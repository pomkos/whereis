import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd
import numpy as np
from apps import db_stuff as d

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
<script src="https://cdn.jsdelivr.net/npm/darkmode-js@1.5.7/lib/darkmode-js.min.js"></script>
<script>
  function addDarkmodeWidget() {
    new Darkmode().showWidget();
  }
  window.addEventListener('load', addDarkmodeWidget);
</script>

"""

def message_maker(data, data_type, num=0):
    '''
    Creates message + link to the flight tracker
    '''
    if data_type == 'track':
        # Add next line to message if we want to specify date, but then 404 error if not within 1 week
        # ?year={data['year_depart']}&month={data['month_depart']}&date={data['day_depart']}

        message = f"[Track flight {num+1} here](https://www.flightstats.com/v2/flight-tracker/{data['plane_code']}/{data['flight_num']})!"

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
    name = 'Peter'
    nickname = 'Pete'

    st.title(f"Where in the world is {name}?")
    st.markdown(hide_streamlit_style, unsafe_allow_html=True) # hides the hamburger menu

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
        st.image(f"images/{nickname.lower()}.jpg",use_column_width='auto')
    except:
        st.error("No image found")

    st.write(f"## Picking {nickname} up?")
    tickets, num = check_how_tickets()
    if num == 0:
        st.info("No tickets were bought yet, check back later.")
    else:
        placeholder_dict = {}
        counter = 0
        for code in tickets['confirm_code'].unique():
            # assumes same day connections
            data = tickets[tickets['confirm_code'] == code]
            date = pd.to_datetime(data['date_depart'].unique()[0]) # so that we can get date only
            date = date.date()
            date = date.strftime("%B %d") # format date

            with st.beta_expander(f"Info for {date}"):
                whole_message = ''
                for tick in range(0,len(data)):
                    message = message_maker(data.iloc[tick,:], data_type = 'track', num=tick)
                    whole_message += f"""
                    1. {message}
                    """
                st.write(whole_message)
                for tick in range(0,len(data)):
                    counter += 1
                    st.write(f"### Flight {tick+1}")
                    st.image(f'images/ticket_{counter}.png', use_column_width='auto')


if __name__ == '__main__':
    app()