import pandas as pd
import streamlit as st
import re
import datetime as dt

def ticket_ocr(my_flight_pic):
    '''
    Use OCR to extract information from an image. Extracts flight info from uploaded pic
    '''
    import pytesseract as tes
    from PIL import Image
    import pandas as pd
    # process the image
    
    text_str = tes.image_to_string(Image.open(my_flight_pic))
    return text_str

def info_extract(text_str,df_abbrev):
    months = {
        'January':'01',
        'February':'02',
        'March':'03',
        'April':'04',
        'May':'05',
        'June':'06',
        'July':'07',
        'August':'08',
        'September':'09',
        'October':'10',
        'November':'11',
        'December':'12'
    }

    usa_airlines = df_abbrev[df_abbrev['Country'] == 'USA']
    usa_airlines['Airline'] = usa_airlines['Airline'].str.replace(' Airlines','')
    text_str = text_str.lower()
    for airline in usa_airlines['Airline']:
        airline = airline.lower()
        if airline in text_str:
            usa_airlines['Airline'] = usa_airlines['Airline'].str.lower()
            plane_code = list(usa_airlines[usa_airlines['Airline'] == airline]['IATA'])[0]
            flight_num = int(re.findall(('\d\d\d\d?'),text_str)[0])


    date = re.findall('\d?\d:\d\d \w+ - \w+, (\w+ \d+)', text_str)[0]
    date = date.split(' ')

    year = dt.datetime.now().year
    month_str = date[0]
    for x in months.keys():
        if month_str.title() in x:
            month = months[x]
    day = date[1]
    
    confirm_code = re.findall('confirmation code ([a-z]\w+)',text_str)[0]

    date_str = f'{month}-{day}-{year} 23:59'
    date_depart = dt.datetime.strptime(date_str,'%m-%d-%Y %H:%M')
    
    results = [plane_code, flight_num, year, month, day, confirm_code, date_depart]
    
    return results

def app(num_files):
    '''
    Only function is to start the extraction process.
    '''
    
    tickets = {}
    for i in range(num_files):
        text_str = ticket_ocr(f'images/ticket_{i+1}.png')
        tickets[f'ticket_{i}'] = text_str

    from apps import db_stuff
    db = db_stuff.dbInfo()
    
    df_abbrev = db.read_info('airline_info')
    
    ticket_extract = {}
    i = 0
    for ticket in tickets.keys():
        i += 1
        data = info_extract(tickets[ticket], df_abbrev)
        ticket_extract[f'ticket_{i}'] = data
    
    
    for ticket in ticket_extract.keys():
        db.write_info('ticket_info',ticket_extract[ticket]) # save extracted ocr into db