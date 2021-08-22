[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/pomkos/whereis/main/whereis.py)

# ToC
1. [Description](#description)
2. [Instructions](#instructions)
3. [Screenshots](#preview)

# Description
Simple webgui to update and present travel plans. Webgui thanks to the `streamlit` package. Features include:

* Upload multiple plane tickets from [Google's Travel page](https://www.google.com/travel/?dest_src=ut&tcfs=UgJgAQ&ved=2ahUKEwjN37LalbvvAhXawJ0KHTVmBoYQyJABegQIABAR&ictx=2) extract information using `pytesseract`, and present it
* Uploaded tickets will be stored in images folder as `ticket_1.png` etc
* Manually input where you are and where you plan to be, and when
* Store above information in an sqlite db, so OCR and extraction is not done on each page reload
* Present tracking info: https://www.flightstats.com/v2/flight-tracker/AA/5584

# Instructions

First edit `line 43` of `whereis.py` to change the default name and nickname. Then:

```python
pip install -r requirements.txt # install prereqs
python db_reset.py # initiate sqlite database
streamlit run whereis.py # start the main webpage
streamlit run settings.py # start the settings page
```

## Update the Main Page

* Upload an Image
  * Just upload it, nothing special required
* Upload Tickets
  * Save a screenshot of your plane ticket, one at a time to your desktop, with the confirmation code included
    ![image](https://user-images.githubusercontent.com/8731022/111717359-46a4a300-882e-11eb-8a9e-6f7af17ff40d.png)
  * Drag and drop all plane tickets at once to the appropriate section of settings page
  * __NOTE:__ OCR assumes that tickets were saves alphabetically, so image "a.jpg" will appear as Flight 1 and "b.jpg" as Flight 2.
  * __NOTE:__ Wait until the running man in the top right stops, then close the tab. Tab must be closed and not refreshed or the picture will be processed again.
* Update Location
  * Format: `NYC, NY`
* Update Plans
  * location as `Los Angeles; Miami, FL` <- note separation by `;`
  * date in same order `March 2; June 2, 2022` <- note separation by `;`
  * click submit.

# Preview

![image](https://user-images.githubusercontent.com/8731022/111718467-57561880-8830-11eb-8c68-b9f3adc73bb6.png)

![image](https://user-images.githubusercontent.com/8731022/111717149-dd249480-882d-11eb-90e5-3bc66c51663e.png)
