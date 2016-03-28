import json
import requests
###################################
#
#DANGER WILL ROBINSON. WE HAVE YET TO HANDLE
#ALL NULLS WITH GRACE!!!
##################################

###############################################################################################
# YOU MUST DEACTIVATE YOUR VENV when running the script! When loading the venv must be turned back on
#$ python manage.py dumpdata --indent=2 app_name.model_name > app_name/fixtures/file_name.json
#sets up
#$ python manage.py loaddata app_name/fixtures/file_name.json
##############################################################################################
def get_all_data():
    event_dummy_data = [
        {
        "model": "predict_app.fight_card",
        "pk": 1,
        "fields": {
            "title": "Rumble Rumble",
            "short_description": "Dummy description!",
            "organization": "UFC",
            "organizations_id": 0,
            "start_time": "2016-03-30T21:49:10Z",
            "end_time": "2016-03-22T22:54:40.790Z"
            }
        },
        {
        "model": "predict_app.fight_card",
        "pk": 2,
        "fields": {
            "title": "Feral Fight",
            "short_description": "Claws and all!",
            "organization": "UFC",
            "organizations_id": 1,
            "start_time": "2016-03-23T22:25:59Z",
            "end_time": "2016-03-23T22:26:44Z"
            }
        },
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
            "organizations_id": 0,
            "sherdog_id": 0,
            "fighter_status": True,
            "image_url": "static/menu_images/anon_fighter_small.jpg",
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
            "gender": True
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
            "organizations_id": 0,
            "sherdog_id": 0,
            "fighter_status": True,
            "image_url": "static/menu_images/anon_fighter_small.jpg",
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
            "gender": True
            }
        }
    ]



    event_output = event_dummy_data
    fighter_output = fighter_dummy_data

    def get_event_data():
        """Patrick J. McNally's code was the template for this"""
        url = "http://ufc-data-api.ufc.com/api/v1/us/events/"

        r = requests.get(url)
        data = r.json()

        for val in data:
            event = {}
            event["model"] = "predict_app.fight_card"
            event["fields"] = {}
            event["fields"]["organizations_id"] = val["id"]
            if val["title_tag_line"]: 
                event["fields"]["title"] = val["title_tag_line"]
            else:
                event["fields"]["title"] = "Event Title TBA"
            if val["short_description"]:
                event["fields"]["short_description"]=val["short_description"]
            else:
                event["fields"]["short_description"] = " "    
            event["fields"]["organization"] = "UFC"
            event["fields"]["start_time"] = val["event_dategmt"]
            event["fields"]["end_time"] = val["end_event_dategmt"]
            event_output.append(event)

    def get_fighter_data():
        url = "http://ufc-data-api.ufc.com/api/v1/us/fighters"

        r = requests.get(url)
        data = r.json()
        for val in data:
            fighter = {}
            fighter["model"] = "predict_app.fighter"
            fighter["fields"] = {}
            fighter["fields"]["last_name"] = val["last_name"]
            fighter["fields"]["first_name"] = val["first_name"]
            fighter["fields"]["nick_name"] = " "
            if val["statid"]:
                fighter["fields"]["statid"] = val["statid"]
            else:
                fighter["fields"]["statid"] = 0
            fighter["fields"]["organizations_id"] = val["id"]
            fighter["fields"]["sherdog_id"] = 0
            fighter["fields"]["fighter_status"] = (val["fighter_status"] == "Active")
            fighter["fields"]["image_url"] = val["thumbnail"]
            fighter["fields"]["wins"] = val["wins"]
            fighter["fields"]["losses"] = val["losses"]
            fighter["fields"]["draws"] = val["draws"]
            fighter["fields"]["ncs"] = 0
            fighter["fields"]["tkos"] = 0
            fighter["fields"]["kos"] = 0
            fighter["fields"]["decs"] = 0
            fighter["fields"]["subs"] = 0
            fighter["fields"]["days_layoff"] = 0
            fighter["fields"]["fudge"] = 0
            fighter["fields"]["spice"] = 0
            fighter["fields"]["batwings"] = 0
            fighter["fields"]["water"] = 0
            
            if val["weight_class"]:
                if "Women" in val["weight_class"]: 
                    #'f' for female
                    fighter["fields"]["gender"] = False
                else:
                    #'t' for HE has a little tail
                    fighter["fields"]["gender"] = True
            else:
                    #If the weightclass is null then make it a he. ERROR POSSIBLE
                    fighter["fields"]["gender"] = True
            fighter_output.append(fighter)

    get_event_data()
    get_fighter_data()
    
    with open('fight_card_upload', "w") as f:
        json.dump(event_output, f, indent=2)

    
    with open('dump_upload_fighters.json', "w") as f:
        json.dump(fighter_output, f, indent=2)

if __name__ == '__main__':
    get_all_data()