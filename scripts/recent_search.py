import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN")


def create_url():
    # 
    query = "from:friedberg -is:retweet -is:reply" #investment
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    tweet_fields = "tweet.fields=author_id,created_at,entities,referenced_tweets" # add in once stable: context_annotations,
    # other query options
    start_time='2020-12-14T00:00:00.000Z'
    end_time='2020-12-16T00:00:00.000Z'
    # if more than 100 tweets in 7 day period add next token from meta data

    next_token='b26v89c19zqg8o3foshs3zie7rxlzr48spi91izsqle9p'
    max_results = 100
    url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&max_results={}".format(
        query, tweet_fields, max_results
    )
    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    bearer_token = auth()
    url = create_url()
    print(url)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    # save the file as a json
    with open('test_data2.json','w') as json_file:
        json.dump(json_response, json_file, ensure_ascii=False, indent=4, sort_keys=True)
    # print(json.dumps(json_response, indent=4, sort_keys=True))

if __name__ == "__main__":
    main()