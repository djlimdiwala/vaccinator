import requests
import json
import datetime, time
import random
import fake_useragent

Pincodes = ["395010", "394210"] # Add all pin codes here
nextNoOfDays = 2 # It checks for next 4 days from current time
Age = 45 # Put you r age here
bot_token = "<bot_token>"  #Create a telegram bot and put its API token here
telegram_userid = "<telegram_user_id>" #Enter your telegram userID
waitBeforeNextFetch = 15 # Time period between two fetches.

def parse_to_string(data):

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

        for Pincode in Pincodes:
            try:
                result = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByPin?pincode={}&date={}".format(Pincode, appliedDate), headers={'User-Agent':str(fake_useragent.UserAgent().random)})
                if result.status_code == 403:
                    notify("Cowin server is blocking your API requests")
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

noOfFetches = 1
while True:
    print("Fetching data from CoWin " + str(noOfFetches) + " times")
    fetch_from_cowin()
    noOfFetches += 1
    time.sleep(waitBeforeNextFetch) #sleeps for 60 seconds. checks cowin after every minute.
