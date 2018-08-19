# Tank Bro

Library that helps with logging aquarium metrics

## Temperature Monitoring

### Automating

Follow the instructions below to automate the logging of your tank's temperature readings to a Google Spreadsheet.

#### 1. Setup Hardware

Follow steps [here](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview) to wire up the DS18B20 to the Raspberry Pi.

#### 2. Setup Google Spreadsheet

Create a Google Spreadsheet, rename the first sheet to "Temperature", and add the following columns to the first row:

* Date
* C°
* F°

#### 3. Create Zap

Create a [Zapier](https://zapier.com/) account and create a 2 step Zap.

The first step (Trigger) needs to be a webhook. Create the webhook, grab the URL, and run the following command from the project directory to pull in a sample post.

`python ./scripts/temp.py [URL] 1`

After the command is run, return to Zapier and click the "Refresh" button to pull in the sample data.

Once that has been done, the second step (Action) needs to be setup with the Google Sheets app. Select the "Create Spreadsheet Row" option and follow the steps on the screen to link your Google Account and install the Zapier => Google Sheets integration.

#### 4. Schedule

Create a cronjob with the following (replace [URL] with the webhook URL from Zapier).

`*/5 * * * * python /home/pi/Desktop/tankbro/scripts/temp.py [URL] 10 >/dev/null 2>&1`

This will run the temperature monitoring script that will update the Google Sheet every 5 minutes.
