import requests
import os
import json
import pandas as pd


# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    # gets the bearer token saved as an env variable
    return os.environ.get("BEARER_TOKEN")


def create_url(pagination_token):
    # creates a url to pass to the api
    user_id = 8819662
    max_results = 100
    exclude = 'replies'
    if pagination_token == '':
        return "https://api.twitter.com/2/users/{}/tweets?max_results={}".format(user_id, max_results)
    else:
        return "https://api.twitter.com/2/users/{}/tweets?max_results={}&pagination_token={}&exclude={}".format(user_id, max_results, pagination_token, exclude)


def get_params():
    # defined the parameters that will be requested from the api
    # https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
    return {"tweet.fields": "created_at,public_metrics,context_annotations,entities"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    # requesting the data with the other function data
    response = requests.request("GET", url, headers=headers, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def build_full_api_call(pagination_token):
    # build all the pieces to create the full api call
    bearer_token = auth()
    url = create_url(pagination_token)
    headers = create_headers(bearer_token)
    params = get_params()
    return connect_to_endpoint(url, headers, params)


def write_json(json_response):
    # convert the list into a json file
    with open('test_data.json','w') as json_file:
        json.dump(json_response, json_file, ensure_ascii=False, indent=4, sort_keys=True)


def prep_token_string(json_response):
    # gets the next page token and removes the quotes
    pagination_token = json.dumps(json_response['meta']['next_token'])
    pagination_token = pagination_token[1:]
    pagination_token = pagination_token[:-1]
    return pagination_token


def main():
    x = 0
    page = 0
    full_tweet_list = []
    pagination_token = ''
    while x == 0:
        json_response = build_full_api_call(pagination_token)
        tweet_response = json_response['data']
        full_tweet_list = full_tweet_list + tweet_response
        try:
            pagination_token = prep_token_string(json_response)
            print('page: ', page)
            page += 1
        except:
            x = 1
    df = pd.DataFrame(full_tweet_list)
    df.to_csv('robmay_no_rep.csv')

if __name__ == "__main__":
    main()