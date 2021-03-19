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



1. Upload an Image: just upload it, nothing special required
1. Upload Tickets
  1. Save a screenshot of your plane ticket, one at a time, with the confirmation code included
    ![image](https://user-images.githubusercontent.com/8731022/111717359-46a4a300-882e-11eb-8a9e-6f7af17ff40d.png)
  * __NOTE:__ OCR was created and tested on MacOS. Assumes that the filename has datetime information when organizing pictures.
  * __NOTE:__ Wait until the running man in the top right stops, then close the tab. Tab must be closed and not refreshed or the picture will be processed again.
2. Update Location: `NYC, NY`
3. Update Plans: location as `Los Angeles; Miami, FL` with date in same order `March 2; June 2, 2022` then click submit.

# Preview

![image](https://user-images.githubusercontent.com/8731022/111718467-57561880-8830-11eb-8c68-b9f3adc73bb6.png)

![image](https://user-images.githubusercontent.com/8731022/111717149-dd249480-882d-11eb-90e5-3bc66c51663e.png)
