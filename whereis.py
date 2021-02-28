import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd
from apps import db_stuff as d

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
        
    with st.beta_expander("Picking Pete up?"):
        try:
            from apps import ticket_ocr
            message = ticket_ocr.app()
            st.write(message)
            st.image("images/ticket.png", use_column_width='auto')
        except:
            st.error("No image found.")
    
    # admin page
    admin = st.experimental_get_query_params()
    if admin:
        import settings
        settings.app()

app()