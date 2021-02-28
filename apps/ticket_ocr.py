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

def airline_abbrev_scrape():
    '''
    Saved for posterity. Scrapes and organizes airline abbreviations
    '''
    # Read in airline abbreviations
    cols = ['Airline', 'Country', 'IATA/ICAO Codes']
    df = pd.DataFrame(columns = cols)
    airlines = {}

    i = 0
    for x in pd.read_html('https://abbreviations.yourdictionary.com/articles/airline-abbreviations-for-major-carriers.html',header=0):
        i += 1
        try:
            x.columns = cols # some columns had spaces in them
        except:
            pass
        airlines[i] = x

    for i in [1,2,3,4,5,6,7]:
        df = df.append(airlines[i])

    # Split code types
    new = df['IATA/ICAO Codes'].str.split('/', expand = True)
    new.columns = ['IATA', 'ICAO']
    df = pd.concat([df, new], axis=1).drop('IATA/ICAO Codes',axis=1)

    # Add Frontier Airlines, which was missing from tables
    df = df.append({'Airline':'Frontier Airlines','Country':'USA','IATA':'F9','ICAO':'FFT'}, ignore_index=True)

    # Remove spaces
    df['IATA'] = df['IATA'].str.strip()
    return df



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
    for airline in usa_airlines['Airline']:
        if airline in text_str:
            plane_code = list(usa_airlines[usa_airlines['Airline'] == airline]['IATA'])[0]
            loc = text_str.find(airline) + len(airline)
            flight_num = int(text_str[loc+1:loc+5])


    date = re.findall('\d?\d:\d\d \w+ - \w+, (\w+ \d+)', text_str)[0]
    date = date.split(' ')

    year = dt.datetime.now().year
    month_str = date[0]
    for x in months.keys():
        if month_str in x:
            month = months[x]
    day = date[1]
    
    confirm_code = re.findall('Confirmation code ([A-Z]\w+)',text_str)[0]
    date_str = f'{month}-{day}-{year} 23:59'
    date_depart = dt.datetime.strptime(date_str,'%m-%d-%Y %H:%M')
    
    results = [plane_code, flight_num, year, month, day, confirm_code, date_depart]
    
    return results

def app():
    '''
    Only function is to start the extraction process.
    '''
    
    text_str = ticket_ocr('images/ticket.png')
    
    from apps import db_stuff
    db = db_stuff.dbInfo()
    
    df_abbrev = db.read_info('airline_info')
    data = info_extract(text_str, df_abbrev)
    
    db.write_info('ticket_info',data) # save extracted ocr into db
    
    message = f"[Track his flight here](https://www.flightstats.com/v2/flight-tracker/{data[0]}/{data[1]}?year={data[2]}&month={data[3]}&date={data[4]})!"
    
    return message