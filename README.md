# Description
Simple webgui to update and present travel plans. Webgui thanks to the `streamlit` package. Features include:

* Upload multiple plane tickets from https://www.google.com/travel/, extract information using `pytesseract`, and present it
* Uploaded tickets will be stored in images folder as `ticket_1.png` etc
* Manually input where you are and where you plan to be, and when
* Store above information in an sqlite db, so OCR and extraction is not done on each page reload
* Present tracking info: https://www.flightstats.com/v2/flight-tracker/UA/2023

# Instructions

1. Install prerequisites: `pip install -r requirements.txt`
2. Initiate the db `python db_reset.py`
3. Start the app: `streamlit run whereis.py`
4. Start the admin page: `streamlit run settings.py`
5. Follow the admin instructions
