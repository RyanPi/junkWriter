import requests
import random


def get_envelope():

    pid = "13989"
    it= "4"
    iv= "15b6f709c16cbb468fcf928683078209cbf0546e31673ad5a7c1a54e63a89e7a"
    ct="3"
    cv="1YNN"
    origin="https://rampycoffee.rampidbestid.com"

    params = {
        "pid": pid,
        "it":it,
        "iv":iv,
        "ct":ct,
        "cv":cv
    }

    headers={
        "origin": origin
    }

    url = "https://api.rlcdn.com/api/identity/v2/envelope"

    try:
        r = requests.get(url,params=params, headers=headers)
        r.raise_for_status() 
        envelope_object = r.json()
        # print(envelope_object)

        envelope = envelope_object["envelopes"][0]["value"]

        if not envelope:
            print("Error: No envelope value foudn in response.")
            return None
        return envelope

    except requests.exceptions.RequstExceptions as e:
        print(f"Error fetching envelope {e}")
        return None
        

#okay now we have the envelope value... what's next? We need to call eCST and generate random data

#code for random data

def fire_ecst():
    music_genres = ["rock", "bossa_nova", "rap", "dubstep", "classical"]
    volume = str(round(random.random()*100))
    noise = random.choice(music_genres)

    #okay so now we cal call eCST?
    pixel_url = "https://di.rlcdn.com/api/segment?pid=713279"

    envelope = get_envelope()
    if not envelope:
        print("Skipping eCST call due to missing envelope.")
        return

    qparams = {
        "it": "19",
        "iv": envelope
    }
    payload = {
        "segments":{
        "noise": noise,
        "volume": volume
        }
    }

    try:
        r = requests.post(pixel_url, json=payload, params=qparams)
        r.raise_for_status
        print("Data sent: ", payload)
        print("Query Params: ", qparams)
        print(f"Response Status Code: {r.status_code}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error senfing eCST request {e}")


# main program execution
while True:
    junk_amount = input("How much junk data should we make?")

    if not junk_amount.isdigit():
        print("Please enter a valid number.")
        continue

    junk_amount = int(junk_amount)
    if junk_amount <= 0:
        print("Please enter a positive integer.")
        continue

    for _ in range(junk_amount):
        fire_ecst()

    break