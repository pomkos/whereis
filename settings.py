import streamlit as st # type: ignore
import datetime as dt
from apps import db_stuff as d
from apps import ticket_ocr
from typing import Tuple, Union


### Helpers
def save_image(image_name: str, image_file, message: str) -> None:
    with open(f"images/{image_name}", "wb") as f:
        f.write(image_file.getvalue())

    st.success(message)


def get_basic_info(db: d.dbInfo) -> Union[Tuple[str, str, str], None]:
    '''
    Gathers location, date, and profile pic from user
    '''
    with st.form('basic_info'):
        st.write("### __Submit Basic Info__")
        profile_pic = st.file_uploader("Upload new profile pic", type=['png', 'jpg', 'jpeg'])
        # current info
        current_loc = st.text_input("Where are you?")
        current_date = dt.datetime.now()
        
        # future info
        future_loc = st.text_input("Where are you going?")
        future_date = st.text_input("When?")
        submit = st.form_submit_button('Submit')

    if submit:
        # save if pic uploaded
        if profile_pic:
            save_image('profile.jpg', profile_pic, 'New profile pic saved!')
        confirm_code = 'None'
        store_location_info(current_loc, future_loc, future_date, confirm_code, db)

    return None

### Logic
def manual_settings(db: d.dbInfo) -> Tuple[str, str, str]:
    '''
    Allow user to send in travel info by filling out a form
    '''
    airline_info = db.read_info('airline_info')
    airline_info = airline_info.dropna(subset = ['IATA'])
    airline_options = airline_info['Airline'].tolist()
    airline_options.sort()

    airline_iata_map = {}
    for idx, row in airline_info.iterrows():
        airline_iata_map[row['Airline']] = row['IATA']

    with st.form('ticket_info'):
        st.write("### __Submit Ticket Info__")
        col1, col2 = st.columns(2)
        with col1:
            airline = st.selectbox("Airline", options = airline_options)
        with col2:
            flight_num = st.number_input('Flight Number', min_value=0)

        date_depart = st.date_input('Date of Departure')
        confirm_code = st.text_input('Confirmation Code')

        ticket_submit = st.form_submit_button('Submit')

    if not ticket_submit:
        st.stop()

    plane_code = airline_iata_map[airline]
    year_depart = date_depart.year
    month_depart = date_depart.month
    day_depart = date_depart.day

    ticket_data =[
        plane_code, 
        flight_num, 
        year_depart, 
        month_depart,
        day_depart,
        confirm_code,
        date_depart
        ]
    db.write_info('ticket_info', ticket_data)


def auto_settings(db: d.dbInfo) -> None:
    '''
    Use OCR to store and display information from a Google Travel screenshot
    '''
    with st.form('auto_ticket_form'):
        st.write('### __Submit Ticket Info__')
        my_pics = st.file_uploader("Upload plane ticket(s)",type=['png','jpg', 'jpeg'], accept_multiple_files = True)
        submit = st.form_submit_button('Submit')

    if not submit:
        st.stop()
    # run OCR
    if len(my_pics) != 0:
        pic_dict = {}
        for pic in my_pics:
            pic_name = pic.name
            pic_dict[pic_name] = pic
            
            # pic_type = pic.type
            # pic_size = pic.size
        i = 0     
        for pic in sorted(pic_dict):
            i += 1
            save_image(f"ticket_{i}", pic_dict[pic], message=f"Ticket_{i} saved!")
        ticket_ocr.app(num_files = len(my_pics))
    # otherwise get info from db
    else:
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


def store_location_info(current_loc: str, future_loc: str, future_date: str, confirm_code: str, db: d.dbInfo) -> None:
    '''
    Stores user submited information into the database
    '''
    if not current_loc:
        current_loc = 'unknown'
    if len(future_loc)==0:
        future_loc = 'unknown'
    if not future_date:
        future_date = str(dt.datetime.now())
    #try:
    message = 'test'
    data_to_save = current_loc, future_loc, future_date, confirm_code, message
    db.write_info('location',data_to_save)
    st.success("Information submitted!")
    #except:
        #st.error("An error occurred. Might be worth investigating.")
        #st.stop()


def app():
    '''
    GUI to upload status and files
    '''    
    st.title("Admin Page")
    display = st.sidebar.radio('Choose an action', options = ['Location Info', 'Ticket OCR', 'Ticket Manual'])
    db = d.dbInfo()

    if display == 'Ticket OCR':
        auto_settings(db)
    elif display == 'Ticket Manual':
        manual_settings(db)
    else:
        get_basic_info(db)
    

        
app()
