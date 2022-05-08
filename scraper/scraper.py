"""Run this code to scrap the data"""

import os
import sys
import datetime

import twint
import pandas as pd

from scraperutils import ScrapDate, DatetimeToStr, StrToDatetime


START_DATE = "2020-09-14" # Exclusive
END_DATE   = "2021-02-28" # Inclusive
TOTAL_DAYS = 167

TWEET_PER_DAY = 14
SEARCH_PER_DAY = 80
SEARCH_LIMIT = 2000

SPECIAL_CASES_DAYS = 10 # First 10 days are the special cases
SPECIAL_CASES_DAYS_MULT = 4


def CreateDir():
    file_dir = os.path.dirname(os.path.realpath(__file__))
    savedata_dir = os.path.abspath(os.path.join(file_dir, os.pardir, 'Data', 'Raw'))
    if not os.path.exists(savedata_dir):
        os.makedirs(savedata_dir)
    
    return savedata_dir
        

def main():
    if not END_DATE > START_DATE:
        return 1

    savedata_dir = CreateDir()

    ntweet_df = pd.DataFrame(columns=["date", "ntweet"])
    current_datetime = StrToDatetime(END_DATE)
    days = 0

    while DatetimeToStr(current_datetime) > START_DATE:
        mult = 1
        if days > (TOTAL_DAYS-SPECIAL_CASES_DAYS):
            mult = SPECIAL_CASES_DAYS_MULT

        resuls = ScrapDate(
            DatetimeToStr(current_datetime),
            SEARCH_PER_DAY*mult,
            TWEET_PER_DAY*mult,
            SEARCH_LIMIT*mult,
            os.path.join(
                savedata_dir, 
                "{}.csv".format(
                    DatetimeToStr(current_datetime)
                    )
            )
        )
        # Append Results
        new_df = pd.DataFrame([[DatetimeToStr(current_datetime), resuls]], columns=["date", "ntweet"])
        ntweet_df = pd.concat([ntweet_df, new_df], ignore_index=True)

        # Go to the next day
        days += 1
        current_datetime = current_datetime + datetime.timedelta(days=-1) 
        print (DatetimeToStr(current_datetime))
        print ("days = {}".format(days))

    ntweet_df.to_csv(os.path.join(savedata_dir, 'Results.csv'))


if __name__ == "__main__":
    sys.exit(main())
