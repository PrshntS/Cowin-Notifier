import requests
import schedule
import time
from datetime import datetime
from datetime import date
import email
import smtplib

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"}


def get_state_id(headers):
    r=requests.get("https://cdn-api.co-vin.in/api/v2/admin/location/states",headers=headers)
    r_dict=r.json()["states"]
    state_name=input("Enter the state name: ")
    a=-1
    for states in r_dict:
        if states["state_name"].lower()==state_name.lower():
           a=states["state_id"]
    return a

def get_district_id(headers,state_id):
    url="https://cdn-api.co-vin.in/api/v2/admin/location/districts/"+str(state_id)
    # print(url)
 
    r=requests.get(url,headers=headers)
    r_dict=r.json()["districts"]
    dist=input("Enter the district name: ")
    for district in r_dict:
        if district["district_name"].lower()==dist.lower():
            a=district["district_id"]
    return a

def is_valid(session):
    return session["capacity"]>0 and session["age_limit"]==18


def get_sessions(r_dict):
    directory=list()
    for center in r_dict["centers"]:
        for session in center["sessions"]:
            dict={
            "center_name":center["name"],
            "date":session["date"],
            "capacity":session["available_capacity"],
            "min_age_limit":session["min_age_limit"]
                    }
            if dict["min_age_limit"]==18 and dict["capacity"]>0:
                directory.append(dict)
    return directory



def get_calender(district_id,headers):
    url="https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    today=date.today().strftime("%d-%m-%Y")
    params={"district_id":district_id,"date":today}
    r=requests.get(url,headers=headers,params=params)
    r_dict=r.json()
    dict=get_sessions(r_dict)
    # print(dict)
    return dict
        
def job(district_id,headers):
    directory=get_calender(district_id,headers)
    # print(directory)


    content = "\n".join([format(element) for element in directory])

   
    username = "Sainiprashant232@gmail.com"
    password = "djsccppczsbcqjmx"

    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)
    print(content)
    print(" ")

    if not content:
        print("No availability")
       
    else:
        email_msg = email.message.EmailMessage()
        email_msg["Subject"] = "Vaccination Slot Open"
        email_msg["From"] = username
        email_msg["To"] = username
        email_msg.set_content(content)

        with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email_msg, username, username)
    
        
   


def format(element):
    return f"{element['date']} - {element['center_name']} ({element['capacity']})"


id=int(get_state_id(headers))
district_id=get_district_id(headers,id)


job(district_id,headers)

schedule.every(10).seconds.do(job,district_id=district_id,headers=headers)

while True:
    schedule.run_pending()
    time.sleep(1)

