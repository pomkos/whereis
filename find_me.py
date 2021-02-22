import streamlit as st
import datetime as dt
import sqlalchemy as sq
import pandas as pd

def settings():
    '''
    Upload status and files
    '''    
    my_pic = st.file_uploader("Upload plane ticket",type=['png','jpg'])
    # current info
    current_loc = st.text_input("Where are you?")
    current_date = dt.datetime.now()
    
    # future info
    future_loc = st.text_input("Where are you going?")
    future_date = st.date_input("When?", min_value=dt.datetime.now())
    
    if my_pic is not None:
        pic_name = my_pic.name
        pic_type = my_pic.type
        pic_size = my_pic.size
        
        with open("ticket.png", "wb") as f:
            f.write(my_pic.getvalue())
        
    if not st.button("Submit"):
        st.stop()

    if not current_loc:
        current_loc = 'unknown'
    if not future_loc:
        future_loc = 'unknown'
    if not future_date:
        future_date = dt.datetime.now()
        
    d = dbInfo()
    d.write_info(current_loc, future_loc, future_date)

class dbInfo():
    def __init__(self):
        engine = sq.create_engine("sqlite:///find_me.db")
        cnx = engine.connect()
        
        self.engine = engine
        self.cnx = cnx
        
    def write_info(self,current_loc, future_loc, future_date):
        meta = sq.MetaData()
        meta.reflect(bind = self.engine)
        table = meta.tables['location']
        query = sq.insert(table).values(current_loc = current_loc, 
                                       current_date = dt.datetime.now().date(),
                                       future_loc = future_loc,
                                       future_date = future_date
                                      )
        ResultProxy = self.cnx.execute(query)
    
    def read_info(self):
        df = pd.read_sql("location",con=self.cnx)
        latest_info = df.loc[len(df)-1,:]
        self.df = df
        return latest_info

def app():
    st.title("Where in the world is Peter?")
    d = dbInfo()
    new_info = d.read_info()
    future_date = dt.datetime.strftime(new_info.loc['future_date'].date(), "%B %d")
    current_date = dt.datetime.strftime(new_info.loc['current_date'].date(), "%B %d")
    

    st.write(f"""
    * As of {current_date} he is in __{new_info.loc['current_loc'].title()}__.
    * He will be in __{new_info.loc['future_loc'].title()}__ on {future_date}
    """)

    st.image("pete.jpg")

    with st.beta_expander("Picking Pete up?"):
        try:
            st.image("ticket.png")
        except:
            st.error("No image found.")
    
    # admin page
    admin = st.experimental_get_query_params()
    if admin:
        settings()
