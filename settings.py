import streamlit as st
import datetime as dt
from apps import db_stuff as d

def app():
    '''
    Upload status and files
    '''    
    st.title("Admin Page")
    my_pic = st.file_uploader("Upload plane ticket",type=['png','jpg'])
    # current info
    current_loc = st.text_input("Where are you?")
    current_date = dt.datetime.now()
    
    # future info
    future_loc = st.text_input("Where are you going?")
    future_date = st.date_input("When?", min_value=dt.datetime.now())
    code = st.text_input("Confirmation code?")
    
    if my_pic is not None:
        pic_name = my_pic.name
        pic_type = my_pic.type
        pic_size = my_pic.size
        
        with open("images/ticket.png", "wb") as f:
            f.write(my_pic.getvalue())
        
    if st.button("Submit"):
        if not current_loc:
            current_loc = 'unknown'
        if not future_loc:
            future_loc = 'unknown'
        if not future_date:
            future_date = dt.datetime.now()
        if not code:
            code = 'unknown'
        try:
            db = d.dbInfo()
            db.write_info(current_loc, future_loc, future_date, confirm_code = code)
            st.success("Information submitted!")
        except:
            st.error("An error occurred. Might be worth investigating.")
            st.stop()
    else:
        st.stop()
    
app()