from flask import Flask, request, jsonify
import json
import requests

import datetime

from urllib2 import URLError
from random import randint
from firebase import firebase


app = Flask(__name__)
app.debug = True

users = []
response = {}
@app.route('/test', methods=['POST'])
def test():
    content = request.get_json()

    access_token = content['originalRequest']['data']['user']['accessToken']

    print(content)

    return json.dumps({
        "speech": "According to your previous interest in esports, I found an event that fits into your schedule on August 22nd. The tickets are $795. Do you want to add this to event to your calendar?",
        "displayText": "Barack Hussein Obama II is the 44th and current President of the United States, and the first African American to hold the office. Born in Honolulu, Hawaii, Obama is a graduate of Columbia University   and Harvard Law School, where ",
        "data": {},
        "contextOut": [],
        "source": "DuckDuckGo"
        })

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


@app.route('/get-location', methods=['POST'])
def getLocation():
    lat = request.form['lat']
    lon = request.form['lon']
    radius = request.form['radius']
    price = request.form['price']

    return curl_request(lat, lon, radius, price)

# give it an object, that we just parsed from zomato
def parse_data_zomato(restaurants, price):
    results = []

    for restaurant in restaurants['restaurants']:
        result = {}
        item = restaurant['restaurant']

        result['name'] = item['name']
        result['location'] = item['location']

        # check if the price is below allowed
        if item['average_cost_for_two'] + item['price_range'] < price:
            result['price'] = item['average_cost_for_two'] + item['price_range']

        result['rating'] = item['user_rating']
        result['photo_url'] = item['photos_url'][0]
        result['menu_url'] = item['menu_url']

        results.append(result)

    return json.dumps({'data': results})

def parse_data_foursquare(restaurants, price):
    results = []

    for restaurant in restaurants['response']['venues']:
        result = {}

        restaurant_id = restaurant['id']
        result['lat'] = restaurant['location']['lat']
        result['lon'] = restaurant['location']['lng']
        result['restaurant_name'] = restaurant['name']
        menu_url = ('https://api.foursquare.com/v2/venues/{id}/menu?'
                      'client_id=H2KDEDO03T5D5UZHSG24XXMVP3WST2GWIHPBO2RQIEREJ2OW'
                      '&client_secret=2DHASPBYJDCPPZJHU2AWGKSNHI141CBASPZ5F4LJN5QUNI4H'
                      '&v=20170204').format(id=restaurant_id)
        menu_items_check = json.loads(requests.get(menu_url).content)['response']['menu']['menus']
        menu_items = []
        if menu_items_check['count'] != 0:
            for item in menu_items_check['items']:
                if 'entries' in item:
                    if item['entries']['count'] != 0:
                        for value in item['entries']['items']:
                            food_item = {}
                            food_item['food_name'] = value['name']
                            if 'price' in value:
                                food_item['food_price'] = value['price']
                            else:
                                random_price = randint(5,15)
                                food_item['food_price'] = calculate_tips(calculate_tax(random_price))

                            if food_item['food_price'] <= price:
                                menu_items.append(food_item)

        result['menu_items'] = menu_items

        if 'formattedPhone' in restaurant['contact']:
            result['phone'] = restaurant['contact']['formattedPhone']
        if 'formattedAddress' in restaurant['location']:
            result['address'] = restaurant['location']['formattedAddress']

        if menu_items_check['count'] != 0:
            results.append(result)

    return json.dumps({'data': results})

def calculate_tax(price):
    taxed_price = price * 1.13
    return taxed_price

def calculate_tips(price):
    tipped_price = price * 1.15
    return tipped_price

def curl_request(lat, lon, radius, price):
    zomato_headers = {
        'content-type': 'application/json',
        'user-key': '892a31736bd16f15eedd942201d67ca2'
    }

    foursquare = ('https://api.foursquare.com/v2/venues/search?'
                  'categoryId=4d4b7105d754a06374d81259'
                  '&radius={rad}'
                  '&ll={lat},{lon}'
                  '&client_id=H2KDEDO03T5D5UZHSG24XXMVP3WST2GWIHPBO2RQIEREJ2OW'
                  '&client_secret=2DHASPBYJDCPPZJHU2AWGKSNHI141CBASPZ5F4LJN5QUNI4H'
                  '&v=20170204').format(lat=lat, lon=lon, rad=radius)

    zomato = ('https://developers.zomato.com/api/v2.1/search?'
           'lat={lat}&lon={lon}&radius={rad}&sort=cost'
           '&order=asc').format(lat=lat, lon=lon, rad=radius)

    try:
        zomato_request = requests.get(zomato, headers=zomato_headers).content
        foursquare_request = requests.get(foursquare).content

        zomato_dict = json.loads(zomato_request)
        foursquare_dict = json.loads(foursquare_request)

        zomato_data = parse_data_zomato(zomato_dict, price)
        foursquare_data = parse_data_foursquare(foursquare_dict, price)

        return foursquare_data
    except URLError, e:
        return jsonify('No API!'), e

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(host='0.0.0.0', port=5000, ssl_context='adhoc')
