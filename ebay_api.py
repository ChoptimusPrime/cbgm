from secrets import EBAY_KEY
from constants import EBAY_URL_ENDPOINT, EBAY_RESULT_COUNT
import requests
from flask import jsonify

def get_recent_prices(card_info):


    resp = requests.get(EBAY_URL_ENDPOINT, params={"keywords" : card_info,
                                      "OPERATION-NAME" : "findCompletedItems",
                                      "SECURITY-APPNAME" : EBAY_KEY,
                                      "paginationInput.entriesPerPage" : EBAY_RESULT_COUNT,
                                      "RESPONSE-DATA-FORMAT" : "JSON",
                                      "siteid" : "0",
                                      "GLOBAL-ID" : "EBAY-US",
                                      "SERVICE-VERSION" : "1.0.0",
                                      "sortOrder" : "EndTimeSoonest"})
    api_results = resp.json()
    result_list = []
    if resp.status_code == 200 and api_results['findCompletedItemsResponse'][0]['searchResult'][0]['@count'] != "0":
        for item in api_results['findCompletedItemsResponse'][0]['searchResult'][0]['item']:
            info = {'title' : item['title'][0],
                'price' : item['sellingStatus'][0]['currentPrice'][0]['__value__'],
                'img_url' : item['galleryURL'][0]}
            result_list.append(info)
        print(result_list)
        return jsonify(results=result_list)
    else: 
        return False