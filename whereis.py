import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd
from apps import db_stuff as d

def app():
    st.title("Where in the world is Peter?")
    db = d.dbInfo()
    new_info = db.read_info()
    future_date = dt.datetime.strftime(new_info.loc['future_date'].date(), "%B %d")
    future_loc = new_info.loc['future_loc'].title()
    current_date = dt.datetime.strftime(new_info.loc['current_date'].date(), "%B %d")
    current_loc = new_info.loc['current_loc'].title()
    code = new_info.loc['confirm_code'].upper()
    

    st.write(f"""
    * As of {current_date} he is in __{current_loc}__.
    * He will be in __{future_loc}__ on {future_date}
    """)
#    try:
    st.image("images/pete.jpg",use_column_width='auto')
#    except:
        st.error("No image found")
        
    with st.beta_expander("Picking Pete up?"):
        try:
            airline = 'UA'
            flight_num = '1594'
            year = '2021'
            month = '02'
            day = '28'
            st.write(f"[Find his flight here](https://www.flightstats.com/v2/flight-tracker/{airline}/{flight_num}?year={year}&month={month}&date={day})!")
            st.image("images/ticket.png", use_column_width='auto')
        except:
            st.error("No image found.")
    
    # admin page
    admin = st.experimental_get_query_params()
    if admin:
        import settings
        settings.app()

app()