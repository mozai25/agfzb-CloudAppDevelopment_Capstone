import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

#Rb-7vF0aa1a20R9RA0YSpHyvp2hZAheKxieZC3ga9qxu
#https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/be2668f0-31ab-43c7-b358-1734d02835ec

def post_request(url, json_payload, **kwargs):
    print(kwargs)
    print("POST to {} ".format(url))
    try:
        response = requests.post(url, params=kwargs, json=json_payload)
        print("ReviewResponse", json_payload)
        print("TestResponse", response)
    except:
        # If any error occurs
        print("Network exception occurred")
        status_code = response
        print("With status {} ".format(status_code))
        #json_data = json.loads(response.text)
    return {}

def get_watson_request(url, kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        
        params = dict()
        params["text"] = kwargs["text"]
        params["version"] = kwargs["version"]
        params["features"] = kwargs["features"]
        params["return_analyzed_text"] = kwargs["return_analyzed_text"]

        response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
                                auth=HTTPBasicAuth('apikey', 'Rb-7vF0aa1a20R9RA0YSpHyvp2hZAheKxieZC3ga9qxu'))
    
    except:
        # If any error occurs
        print("Network watson exception occurred")
    status_code = response.status_code
    print(response)
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data["sentiment"]["document"]["label"]

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler", dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_id_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

def get_dealer_by_state_from_cf(url, state):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result
        
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            print("DEaler",dealer_doc)
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, id=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result
        # For each dealer object
        for review in reviews:
            # Get its content in `doc` object
            dealer_doc = review
            print("REaler",dealer_doc)
            dealer_obj = DealerReview(
                dealership=dealer_doc["dealership"], 
                name=dealer_doc["name"], 
                purchase=dealer_doc["purchase"],
                review=dealer_doc["review"],
                sentiment= analyze_review_sentiments(dealer_doc["review"]), 
                #purchase_date=dealer_doc["purchase_date"], 
                car_make=dealer_doc["car_make"],
                car_model=dealer_doc["car_model"],
                car_year=dealer_doc["car_year"], 
                #id=dealer_doc["id"]
            )
            results.append(dealer_obj)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
def analyze_review_sentiments(text):
    url = "https://api.eu-de.natural-language-understanding.watson.cloud.ibm.com/instances/be2668f0-31ab-43c7-b358-1734d02835ec/v1/analyze"
    
    params = dict()
    params["text"] = text
    params["version"] = "2022-04-07"
    params["features"] = "sentiment"
    params["return_analyzed_text"] = True
    result = get_watson_request(url, params)
    print('Sentiment result', result);
    return result;

# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative



