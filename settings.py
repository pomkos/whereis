import streamlit as st
import datetime as dt
from apps import db_stuff as d
from apps import ticket_ocr
    
def app():
    '''
    Upload status and files
    '''    
    st.title("Admin Page")
    col1,col2 = st.columns(2)
    with col1:
        my_pics = st.file_uploader("Upload plane ticket",type=['png','jpg', 'jpeg'], accept_multiple_files = True)
    with col2:
        profile_pic = st.file_uploader("Upload new profile pic", type=['png','jpg', 'jpeg'])
    # current info
    current_loc = st.text_input("Where are you?")
    current_date = dt.datetime.now()
    
    # future info
    future_loc = st.text_input("Where are you going?")
    future_date = st.text_input("When?")
    
    if profile_pic:
        with open("images/profile.jpg","wb") as f:
            f.write(profile_pic.getvalue())
        st.success("Saved!")
        
    if len(my_pics) != 0:
        pic_dict = {}
        for pic in my_pics:
            pic_name = pic.name
            pic_dict[pic_name] = pic
            
            pic_type = pic.type
            pic_size = pic.size
        i = 0     
        for pic in sorted(pic_dict):
            i += 1
            with open(f"images/ticket_{i}.png", "wb") as f:
                f.write(pic_dict[pic].getvalue())
            st.success(f"Ticket_{i} saved!")
    
        message = ticket_ocr.app(num_files = len(my_pics))
    else:
        db = d.dbInfo()
        df = db.read_info('ticket_info')
        df = df[df['date_depart'] >= dt.datetime.now()]
        confirm_code = 'none'
#         if len(df) == 0:
#             confirm_code = 'none'
#         else:
#             confirm_code = df.loc[:,'confirm_code'].unique()
#             if len(confirm_code) > 1:
#                 st.error("Two confirmation codes for one trip have not been implemented yet.")
#                 st.stop()
#             else:
#                 confirm_code = list(confirm_code)[0]
        
    if st.button("Submit"):
        if not current_loc:
            current_loc = 'unknown'
        if len(future_loc)==0:
            future_loc = 'unknown'
        if not future_date:
            future_date = str(dt.datetime.now())
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
