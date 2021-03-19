# Description
Simple webgui to update and present travel plans. Webgui thanks to the `streamlit` package. Features include:

* Upload multiple plane tickets from https://www.google.com/travel/, extract information using `pytesseract`, and present it
* Uploaded tickets will be stored in images folder as `ticket_1.png` etc
* Manually input where you are and where you plan to be, and when
* Store above information in an sqlite db, so OCR and extraction is not done on each page reload
* Present tracking info: https://www.flightstats.com/v2/flight-tracker/UA/2023

# Instructions


```python
pip install -r requirements.txt # install prereqs
python db_reset.py # initiate sqlite database
streamlit run whereis.py # start the main webpage
streamlit run settings.py # start the settings page
```
