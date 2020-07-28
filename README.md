# tuition-database-manager
An app for managing the records for classes and fees payments for tuition instructors.

## Instructions for Installing/Editing this software
1. You need to have a google spreadsheet on any of your google accounts. (the template for the same can be viewed [here](https://docs.google.com/spreadsheets/d/1JGXJ8gW3xF6omqGWyPJ9cL0pg8pNGbmczyroMP6EKMw/edit?usp=sharing))
2. Now go to [this link](https://console.cloud.google.com/getting-started), click `select project` on the top left of your page and create a new project. Name your project and for organization you can leave it as is. Once created open/view the project page, click on go to `APIs overview`, now go to `Library` and search for Google Drive and enable `Google Drive API`. Once enabled click on `CREATE CREDENTIALS`. Select `Google Drive API` and `Web server (e.g. node.js, Tomcat)` from the dropdown and select `Application Data` and `No, I'm not using them`. Next click on the blue button and give it some name and for role select `Select a role > Project > Editor`. Make sure `JSON` is selected and click continue, it should download a JSON file with the required credentials. Rename this file as `creds.json` and replace the placeholder file in the project directory with it.
3. Go back to the `APIs overview` and `Library` and search for Google sheets, select `Google Sheets API` and enable it.
4. Open the `creds.json` file and copy the `client_email`, go to your google sheets and share the sheet with this email.
5. To run this software on Windows you need to have python 3.x installed, then open up the command prompt and run the following commands to install all dependencies.

`pip install gspread oauth2client`

`python -m pip install --upgrade pip wheel setuptools`

`python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew`

`python -m pip install kivy.deps.gstreamer`

`python -m pip install kivy.deps.angle`

`python -m pip install kivy`

`python -m pip install kivymd`

6. Open `db_manager.py` and replace `<Insert name of google_sheet>` with the name of your google sheet (the name of the entire document, not individual sheet) at the 4 marked lines.
7. You can now start using the app by running `test.bat` file


### IMP_NOTE: 
this app is still under development and may have bugs, you may need to have one record filled in the document before you launch the app 
