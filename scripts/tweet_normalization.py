import pandas as pd
import json

def read_json_df(input_file):
    tweet_data = json.load(open(input_file))
    # full file
    df = pd.DataFrame(tweet_data['data'])
    # if it is just the data
    df = pd.DataFrame(tweet_data)

    return df

def main():
    df = read_json_df('test_data.json')
    df.to_csv('test_csv.csv')
    
if __name__=="__main__":
    main()