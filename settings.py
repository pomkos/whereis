import streamlit as st # type: ignore
import datetime as dt
from apps import db_stuff as d
from apps import ticket_ocr
from typing import Tuple, Union, List, Any


### Helpers
def save_image(image_name: str, image_file, message: str) -> None:
    with open(f"images/{image_name}", "wb") as f:
        f.write(image_file.getvalue())

    st.success(message)

def process_tickets(ticket_list: List[Any], ocr: bool = False, ticket_num: Union[int, None] = None) -> None:
    if not ticket_num:
        pic_dict = {}
        for pic in ticket_list:
            pic_name = pic.name
            pic_dict[pic_name] = pic
            
            # pic_type = pic.type
            # pic_size = pic.size
        i = 0

        for pic in sorted(pic_dict):
            i += 1
            save_image(f"ticket_{i}.png", pic_dict[pic], message=f"Ticket_{i} saved!")
    else:
        save_image(f"ticket_{ticket_num}.png", ticket_list[0], message=f"Ticket_{ticket_num} saved!")
    
    if ocr:
        ticket_ocr.app(num_files = len(ticket_list))


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
def manual_settings(db: d.dbInfo) -> None:
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
        # in list for compatibility with functions
        ticket_pics = [st.file_uploader('Upload Ticket', type = ['png', 'jpg','jpeg'], accept_multiple_files=False)]
        col1, col2, col3 = st.columns(3)
        with col1:
            ticket_num = st.number_input('This is ticket number', min_value=1)
        with col2:
            airline = st.selectbox("Airline", options = airline_options)
        with col3:
            flight_num = st.number_input('Flight Number', min_value=0)

        date_depart = st.date_input('Date of Departure')
        confirm_code = st.text_input('Confirmation Code')

        ticket_submit = st.form_submit_button('Submit')

    if not ticket_submit:
        st.stop()

    if len(ticket_pics) != 0:
        process_tickets(ticket_list=ticket_pics, ocr=False, ticket_num=ticket_num)
    else:
        st.warning("Please upload a screenshot of the ticket")
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
        process_tickets(ticket_list = my_pics, ocr = True)
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

def add_airline(db: d.dbInfo) -> None:
    '''
    GUI to allow user to add airline info to db
    '''
    
    st.write('## Submit New Airline')
    with st.expander('All airline data'):
        st.write(db.read_info('airline_info'))

    with st.form('airline_info'):
        airline = st.text_input('Airline Name').title().strip()
        col1, col2 = st.columns(2)
        with col1:
            iata = st.text_input('IATA Code').upper().strip()
        with col2:
            icao = st.text_input('ICAO Code').upper().strip()
        country = st.text_input('Country', help='Country where headquarters are located').title().strip()

        submit = st.form_submit_button('Submit')
    
    if not submit:
        st.stop()
    
    airline_data = [
        airline,
        country,
        iata,
        icao
    ]

    if not no_duplicate_airline_data(airline_data, db):
        st.stop()

    try:
        db.write_info(table_name = 'airline_info', data = airline_data)
        st.success('Submitted!')
    except:
        st.error('An error occurred')

def no_duplicate_airline_data(airline_data: List[str], db: d.dbInfo) -> bool:
    '''
    Checks whether the airline data has been added before
    '''
    df = db.read_info('airline_info')
    if airline_data[0].lower() in df['Airline'].str.lower().tolist():
        st.error('Airline already in dataframe')
        return False
    
    elif airline_data[2].lower() in df['IATA'].str.lower().tolist():
        st.error('IATA already in dataframe')
        return False
    
    elif airline_data[3].lower() in df['ICAO'].str.lower().tolist():
        st.error('ICAO already in dataframe')
        return False
    
    else:
        return True
    

def app():
    '''
    GUI to upload status and files
    '''    
    st.title("Admin Page")
    display = st.sidebar.radio('Choose an action', options = ['Location Info', 'Ticket OCR', 'Ticket Manual', 'Add Airline to DB'])
    db = d.dbInfo()

    if display == 'Ticket OCR':
        auto_settings(db)
    elif display == 'Ticket Manual':
        manual_settings(db)
    elif display == 'Add Airline to DB':
        add_airline(db)
    else:
        get_basic_info(db)
    

        
app()
