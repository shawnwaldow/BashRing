import json
import requests
###################################
#DANGER WILL ROBINSON. WE HAVE YET TO HANDLE
#ALL NULLS WITH GRACE!!!
##################################
def get_all_data():
    dummy_data=[
        {
            "model": "predict_app.fight_card",
            "pk": 1,
            "fields": {
            "title": "liyg",
            "organization": "UFC",
            "start_time": "2016-03-30T21:49:10Z",
            "end_time": "2016-03-22T22:54:40.790Z",
            "organizations_id": 0
            }
        },
        {
            "model": "predict_app.fight_card",
            "pk": 3,
            "fields": {
            "title": "FiestaFight",
            "organization": "UFC",
            "start_time": "2016-03-23T22:25:59Z",
            "end_time": "2016-03-23T22:26:44Z",
            "organizations_id": 22
            }
        }
    ]
 
    fighter_dummy_data =[
        {
        "model": "predict_app.fighter",
        "pk": 1,
        "fields": {
            "last_name": "chump",
            "first_name": "weak",
            "nick_name": "glass jaw",
            "statid": 1,
            "fighter_status": true,
            "image": "static/menu_images/anon_fighter_small.jpg",
            "wins": 0,
            "losses": 1,
            "draws": 0,
            "ncs": 0,
            "tkos": 0,
            "kos": 0,
            "decs": 0,
            "subs": 0,
            "days_layoff": 30,
            "fudge": 1.0,
            "spice": 1.0,
            "batwings": 1,
            "water": 1.0,
            "gender": true
            }
        },
        {
        "model": "predict_app.fighter",
        "pk": 2,
        "fields": {
            "last_name": "surley",
            "first_name": "damien",
            "nick_name": "stone hands",
            "statid": 3,
            "fighter_status": true,
            "image": "static/menu_images/anon_fighter_small.jpg",
            "wins": 1,
            "losses": 0,
            "draws": 0,
            "ncs": 0,
            "tkos": 0,
            "kos": 1,
            "decs": 0,
            "subs": 0,
            "days_layoff": 30,
            "fudge": 1.0,
            "spice": 1.0,
            "batwings": 1,
            "water": 1.0,
            "gender": true
        }
        }
    ]



    output = dummy_data
    fighter_output = fighter_dummy_data

    def get_champ_data():
        url = "http://ufc-data-api.ufc.com/api/v1/us/events/"
        #payload = {'api_key': API_KEY}

        r = requests.get(url)
        data = r.json()
        #version = data["version"]
        # output = []
        for val in data:
            event = {}
            event["organizations_id"] = val["id"]
            event["model"] = "predict_app.fight_card"
            event["fields"] = {}
            if val["title_tag_line"] and val["short_description"]:
                event["fields"]["title"] = (val["title_tag_line"]+": "+val["short_description"])[0:122] + "..."
            else:
                event["fields"]["title"] = "Event Title TBA"
            event["fields"]["organization"] = "UFC"
            event["fields"]["start_time"] = val["event_dategmt"]
            event["fields"]["end_time"] = val["end_event_dategmt"]
            output.append(event)

    def get_fighter_data():
        url = "http://ufc-data-api.ufc.com/api/v1/us/fighters"

        r = requests.get(url)
        data = r.json()
        for val in data:
            fighter = {}
            fighter["pk"] = val["id"]
            fighter["model"] = "predict_app.fighter"
            fighter["fields"] = {}
            fighter["fields"]["last_name"] = val["last_name"]
            fighter["fields"]["first_name"] = val["first_name"]
            fighter["fields"]["nick_name"] = val[" "]
            fighter["fields"]["statid"] = val["statid"]
            fighter["fields"]["fighter_status"] = (val["fighter_status"] == "Active")
            fighter["fields"]["image"] = "static/menu_images/anon_fighter_small.jpg"
            fighter["fields"]["wins"] = val["wins"]
            fighter["fields"]["losses"] = val["losses"]
            fighter["fields"]["draws"] = val["draws"]
            fighter["fields"]["ncs"] = 0
            fighter_output.append(fighter)

    get_champ_data()
    
    with open('Fight_Card', "w") as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    get_all_data()