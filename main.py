import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 48.85341
MY_LONG = 2.3488


def is_my_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.

def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(60)
    if is_my_position() and is_dark():
        my_email = "myemail@gmail.com"
        password = "TEST-0411-test"
        with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email,
                                to_addrs="test.myemail@gmail.com"
                                msg=f"Subject: ISS above head\n\n Hey Elise, look up, the ISS is in the sky!")

