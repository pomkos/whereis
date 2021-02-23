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
    current_date = dt.datetime.strftime(new_info.loc['current_date'].date(), "%B %d")
    

    st.write(f"""
    * As of {current_date} he is in __{new_info.loc['current_loc'].title()}__.
    * He will be in __{new_info.loc['future_loc'].title()}__ on {future_date}
    """)
    try:
        st.image("images/pete.jpg",use_column_width='auto')
    except:
        st.error("No image found")
        
    with st.beta_expander("Picking Pete up?"):
        try:
            st.image("images/ticket.png", use_column_width='auto')
        except:
            st.error("No image found.")
    
    # admin page
    admin = st.experimental_get_query_params()
    if admin:
        import settings
        settings.app()

app()