# Zoom Calendar Automation

Problem: after each lecture, I have to manually rename and upload recorded video to google drive.
With this python script, it will fetch the lecture names from your google calendar and make it the name of the recorded video, then upload it to gg drive

## Prerequisites

You will need to download `drive` for desktop: <https://www.google.com/drive/download/>
After downloading drive for desktop, it will mount a directory to your file system, should be at `/Volumes/GoogleDrive`. This directory represents the file systems of your drive account. If you create or move a file into this mount, it will automatically upload that file to drive

Create a new project in google developer console. Create and configure a new oauth client ID credential for **desktop application**. Once done, download the credential json file into this project location and rename it to `credentials.json`

## Instructions

1. Get the calendar ID that you want to fetch the events from. You can see it from within google calendar. You should get the ID of your class calendar

2. Create a `.env` file with the format similar to `.env.example` and put the class calendar ID there

3. Modify the `DEST` and `ZOOM` variable in `main.py`. `DEST` is the destination folder where the zoom video will be copied to, this folder should be inside the google drive mount that we installed earlier. The specific location is up to you, for example, if `DEST` is `Volumes/GoogleDrive/My Drive` then the video will be uploaded to `My Drive` on your google drive account. The `ZOOM` variable is the location where zoom saved your recorded videos. On MacOS, this is: `/Users/your_name/Documents/Zoom`

4. Install the dependencies: `pip install -r requirements.txt`

5. Run the script: `python3 main.py`. The first run, it will ask you to login and consent it to read your calendar. It will ask for `readonly` permission. After authenticated, the script will save your google api tokens in `token.json`. Please keep both this file and `credentials.json` secure.

6. You can also put this script in a cronjob to fully automate this process. Personally, I configured cronjob to run it twice a day, at 13:00 for morning lecture, and at 16:00 for afternoon lectures
