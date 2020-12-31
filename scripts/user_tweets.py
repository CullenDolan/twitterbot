import requests
import os
import json

# To set your environment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url():
    # Replace with user ID below
    user_id = 41609220
    max_results = 10
    pagination_token= '7140dibdnow9c7btw3w2ofy5kw8qv6vl0q3pi6m1c2zw9'
    return "https://api.twitter.com/2/users/{}/tweets?max_results={}&pagination_token={}".format(user_id, max_results, pagination_token)


def get_params():
    # https://developer.twitter.com/en/docs/twitter-api/tweets/timelines/api-reference/get-users-id-tweets
    return {"tweet.fields": "created_at,public_metrics,context_annotations,entities"}


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers, params):
    response = requests.request("GET", url, headers=headers, params=params)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    # get the bearer token
    bearer_token = auth()
    # create the url to pass to api
    url = create_url()
    # pass the bearer token to api
    headers = create_headers(bearer_token)
    # pass params to api
    params = get_params()
    # full api call
    json_response = connect_to_endpoint(url, headers, params)
    # prints the reposnce in json
    print((json.dumps(json_response, indent=4, sort_keys=True)))
    # print the next token
    print(json.dumps(json_response['meta']['next_token']))


if __name__ == "__main__":
    main()