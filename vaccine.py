import requests
from datetime import datetime
import time
from notify_run import Notify


notify = Notify()
PINCODE = 247667 #Write your PINCODE here!
AGE = 18  # Write the minimum age group for which you wanna get notified!
headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
ENDPOINT = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin"
todays_date = datetime.now()
DATE = f"{todays_date.day}-{todays_date.month}-{todays_date.year}"


def check_vaccine():
    response = requests.get(f"{ENDPOINT}?pincode={PINCODE}&date={DATE}",headers=headers)

    vaccine_slots = response.json()
    #print(vaccine_slots)
    slot_available = False
    center_count = 1
    slots_data = ""
    for center in vaccine_slots["centers"]:
        for session in center["sessions"]:
            print(session)
            if session["min_age_limit"] <= AGE and len(session["slots"]) > 0 and session['available_capacity'] > 0:
                slot_available = True
                slots_data += f"\n{center_count}) {center['name']} on {session['date']}"
                center_count += 1
                print(f"Center Name\t{center['name']}")
                print(f"Slots available\t{session['slots']}")
                print("-----------------------------------")
                break

    if slot_available:
       print(f"HURRY! Vaccine is availabe for age {AGE} at these centers: {slots_data}")

    else:
        print(f"\nNO Slot Available for age {AGE} in this week as of {datetime.now()} for Pin: {PINCODE}")
        return False

    return True

if __name__ == "__main__":
    while True:
        if check_vaccine():
            break
        time.sleep(1)  # Check for vaccine availability every Second 
