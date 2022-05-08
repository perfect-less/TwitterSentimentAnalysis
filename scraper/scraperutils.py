import sys
import datetime

import pandas as pd
import twint


def CreateConfig(until_date: str, limit: int = 1000):
    #configuration
    config = twint.Config()

    config.Search = "#AbrahamAccords"
    config.Lang = "en"
    
    config.Limit = limit
    config.Min_likes = 50

    config.Until = until_date
    config.Pandas = True
    config.Hide_output = True

    return config

def ScrapDate(current_date: str, loop_count: int, save_count: int, limit: int, filepath: str):

    current_datetime  = StrToDatetime(current_date)
    tomorrow_datetime = current_datetime + datetime.timedelta(days=1)

    # Create config for the day
    config = CreateConfig(
                DatetimeToStr(tomorrow_datetime), 
                limit
            )

    tweet_df = pd.DataFrame()
    initiated = False

    # Itterate over to scrap tweets 
    for i in range(loop_count):
        twint.run.Search(config)

        print (twint.output.panda.Tweets_df.shape[0])
        if twint.output.panda.Tweets_df.shape[0] > 0:
            if initiated == False:
                tweet_df = twint.output.panda.Tweets_df
                initiated = True
                continue
            else:
                tweet_df = pd.concat([tweet_df, twint.output.panda.Tweets_df], ignore_index=True)

    tweet_df = tweet_df.drop_duplicates(subset=["id", "tweet"], ignore_index=True)
    tweet_df = tweet_df.loc[tweet_df["date"] > current_date].reset_index(drop=True)

    # Only pick tweets with the most likes
    tweet_df = tweet_df.nlargest(save_count, columns="nlikes").reset_index(drop=True)
    tweet_df.to_csv(filepath)

    return tweet_df.shape[0]

def DatetimeToStr(dt: datetime.datetime):
    return "{}-{}-{}".format(
                    str(dt.year).rjust(4, '0'),
                    str(dt.month).rjust(2, '0'),
                    str(dt.day).rjust(2, '0')
                )

def StrToDatetime(str_dt: str):
    return datetime.datetime.strptime(str_dt, "%Y-%m-%d")
