import streamlit as st
import datetime as dt
from apps import db_stuff as d
from apps import ticket_ocr
    
def app():
    '''
    Upload status and files
    '''    
    st.title("Admin Page")
    col1,col2 = st.beta_columns(2)
    with col1:
        my_pics = st.file_uploader("Upload plane ticket",type=['png','jpg'], accept_multiple_files = True)
    with col2:
        profile_pic = st.file_uploader("Upload new profile pic", type=['png','jpg'])
    # current info
    current_loc = st.text_input("Where are you?")
    current_date = dt.datetime.now()
    
    # future info
    future_loc = st.text_input("Where are you going?").split(';')
    future_date = st.text_input("When?").split(';')
    
    if profile_pic:
        with open("images/pete.jpg","wb") as f:
            f.write(profile_pic.getvalue())
        st.success("Saved!")
    if len(my_pics) != 0:
        i = 0
        for pic in my_pics:
            i += 1
            pic_name = pic.name
            pic_type = pic.type
            pic_size = pic.size
            with open(f"images/ticket_{i}.png", "wb") as f:
                f.write(pic.getvalue())
            st.success(f"Ticket_{i} saved!")
    
        message = ticket_ocr.app(num_files = len(my_pics))
    else:
        db = d.dbInfo()
        df = db.read_info('ticket_info')
        df = df[df['date_depart'] >= dt.datetime.now()]
        if len(df) == 0:
            confirm_code = 'none'
        else:
            confirm_code = df.loc[:,'confirm_code'].unique()
            if len(confirm_code) > 1:
                st.error("Two confirmation codes for one trip have not been implemented yet.")
                st.stop()
            else:
                confirm_code = list(confirm_code)[0]
        
    if st.button("Submit"):
        if not current_loc:
            current_loc = 'unknown'
        if not future_loc:
            future_loc = 'unknown'
        if not future_date:
            future_date = dt.datetime.now()
        #try:
        message = 'test'
        data = current_loc, future_loc, future_date, confirm_code, message
        db.write_info('location',data)
        st.success("Information submitted!")
        #except:
            #st.error("An error occurred. Might be worth investigating.")
            #st.stop()
    else:
        st.stop()
    
app()