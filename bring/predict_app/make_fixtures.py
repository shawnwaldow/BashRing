import json
import requests
"""
def list_check(stuff):
    if type(stuff) == list:
        return stuff.pop()
    else:
        return stuff
"""

def get_all_data():
    output = []

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
                event["fields"]["title"] = val["title_tag_line"]+": "+val["short_description"]
            else:
                event["fields"]["title"] = "Event Title TBA"
            event["fields"]["organization"] = "UFC"
            event["fields"]["start_time"] = val["event_dategmt"]
            event["fields"]["end_time"] = val["end_event_dategmt"]
            output.append(event)


    get_champ_data()
    
    with open('all_fix.json', "w") as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    get_all_data()