import requests
import sys
import json, os
import datetime, time
import fake_useragent

Pincode = "395010" # Add you pin code here
nextNoOfDays = 4 # It checks for next 4 days from current time
Age = 45 # Put you r age here
bot_token = "***********************************"  #Create a telegram bot and put its API token here
telegram_userid = "*********" #Enter your telegram userID


def parse_to_string(data):

    # parse dict to readable message
    string = ""
    for (key,value) in data.items():
        if key != "session_id":
            string += "{} = {}\n".format(key, value)
    return string

def fetch_from_cowin():
    CurrentDate = datetime.datetime.today()
    total_centers = 0
    for i in range(0,nextNoOfDays):
        appliedDate = CurrentDate + datetime.timedelta(days=i)
        appliedDate = appliedDate.strftime("%d-%m-%Y")
        try:
            result = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(Pincode, appliedDate), headers={'User-Agent':str(fake_useragent.UserAgent().random)})
            fetched_data = json.loads(result.text).get("sessions") if result.ok else []
        except Exception as e:
            print(e)
            fetched_data = []

        for data in fetched_data:
            try:
                if data.get("min_age_limit") <= Age:
                    center_info = parse_to_string(data)
                    notify(center_info)
                    total_centers += 1
            except Exception as e:
                print(e)

    if total_centers != 0:
        print("Found " + str(total_centers) + " centers with available slots")
    else:
        print("No slots available")


def notify(msg):
    url = f"https://api.telegram.org/bot{bot_token}"
    params = {"chat_id": telegram_userid, "text": msg}
    r = requests.get(url + "/sendMessage", params=params)

while True:
    print("Fetching data from CoWin")
    fetch_from_cowin()
    time.sleep(60) #sleeps for 60 seconds. checks cowin after every minute.
