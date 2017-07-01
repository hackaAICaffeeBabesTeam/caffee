from flask import Flask, request, jsonify
import json, requests, datetime

app = Flask(__name__)
app.debug = True

users = []
response = {}
@app.route('/test', methods=['POST'])
def test():
    content = request.get_json()

    print(json.dumps(content))

    access_token = content['originalRequest']['data']['user']['accessToken']

    return json.dumps({
        "speech": "According to your previous interest in esports, I found an event that fits into your schedule on August 22nd. The tickets are $795. Do you want to add this event to your calendar?",
        "displayText": "According to your previous interest in esports, I found an event that fits into your schedule on August 22nd. The tickets are $795. Do you want to add this event to your calendar?",
        "data": {},
        "contextOut": [],
        "source": "eventbrite"
        })

@app.route('/caffee', methods=['POST'])
def caffee():
    content = request.get_json()

    print(json.dumps(content))

    conversation = {
        "speech": "According to your previous interest in esports, I found an event that fits into your schedule on August 22nd. The tickets are $795. Do you want to add this event to your calendar?",
        "displayText": "According to your previous interest in esports, I found an event that fits into your schedule on August 22nd. The tickets are $795. Do you want to add this event to your calendar?",
        "data": {},
        "contextOut": [],
        "source": "eventbrite"
        }

    if 'confirmation' in content["result"]["parameters"]:
        if content["result"]["parameters"]['confirmation'] == "yes":
            conversation = {
                "speech": "Awesome! This event has been added to your calendar. Further details for ticket purchasing and navigation have been sent to your phone.",
                "displayText": "Awesome! This event has been added to your calendar. Further details for ticket purchasing and navigation have been sent to your phone.",
                "data": {},
                "contextOut": [],
                "source": "python"
                }

            access_token = content['originalRequest']['data']['user']['accessToken']

            add_to_calendar(access_token)


    city = content["result"]["parameters"]["geo-city"]

    access_token = content['originalRequest']['data']['user']['accessToken']

    return json.dumps(conversation)

def add_to_calendar(access_token):
    # print(access_token)
    event = json.dumps({
    	"end": {
    		"dateTime": "2017-08-23T20:00:00.000",
    		"timeZone": "America/New_York"
    	},
    	"start": {
    		"dateTime": "2017-08-22T17:00:00.000",
    		"timeZone": "America/New_York"
    	},
    	"attendees": [{
    		"email": "jonahchin7@gmail.com"
    	}],
    	"attachments": [{
    		"fileUrl": "eventbrite.ca"
    	}],
    	"reminders": {},
    	"summary": "XLIVE Esports Summit"
    })

    calendar = ('https://www.googleapis.com/calendar/v3/calendars/primary/events?access_token={access_token}').format(access_token=access_token)

    r = requests.post(calendar, data = event)

    print(r.text)

@app.route('/conversation-context', methods=['POST'])
def conversationContext():
    content = request.get_json()
    calendar_content = json.dumps({})
    code = 400

    city = content["result"]["parameters"]["geo-city"]

    user_id = content['originalRequest']['data']['user']['userId']
    # conversation_id = # get session id
    #
    # found = False
    #
    # location_obj = {"city": city, "timestamp": datetime.datetime.now()}
    # user_data = {"id": user_id, "conversations_data": []}
    # conversation_data = {"conversation" : []}
    # current_conversation_context = {"id": session_id , "location": [] , "category": []}
    #
    # isCurrentConversationContextSame = # find an existing conversation id ? boolean attribute
    #
    # conversation_data["conversation"].append(conversation_data)
    # user_data["conversations"].append(conversation_data)
    #
    # user_data["location"].append(location_obj)
    #
    # if len(users) == 0:
    #     users.append(user_data)
    # else:
    #     for user in users:
    #         if user["id"] == user_id:
    #             users.remove(user)
    #             user["location"].append(location_obj)
    #             found = True
    #             break
    #
    # if found == False:
    #     users.append(user_data)

    if city:
        eventbrite_request(city)
    else:
        print("No City!")

    if content['status']['code'] == 200:
        access_token = content['originalRequest']['data']['user']['accessToken']

        calendar = ('https://www.googleapis.com/calendar/v3/calendars/primary/events?access_token={access_token}').format(access_token=access_token)

        calendar_content = requests.get(calendar).content

        code = 200
    print(users)
    return calendar_content, code

def eventbrite_request(location="toronto", lat=None, lon=None):
    eventbrite_token = 'N6AWV37OUJXTCO6MCDTY'
    eventbrite = ('https://www.eventbriteapi.com/v3/events/search/?'
                  'location.address={location}&token={token}').format(location=location ,token=eventbrite_token)

    eventbrite_content = requests.get(eventbrite).content

    return eventbrite_content

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
