# Description
Simple webgui to update and present travel plans. Features include:

* Upload multiple plane tickets from google.com/trips, extract information using `pytesseract`, and present it
* Uploaded tickets will be stored in images folder as `ticket_1.png` etc
* Manually input where you are and where you plan to be, and when
* Store above information in an sqlite db, so OCR and extraction is not done on each page reload
