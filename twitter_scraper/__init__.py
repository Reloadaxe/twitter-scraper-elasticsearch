# TwitterScraper
# Copyright 2016-2019 Ahmet Taspinar
# See LICENSE for details.
"""
Twitter Scraper tool
"""

__version__ = '1.4.0'
__author__ = 'Ahmet Taspinar'
__license__ = 'MIT'


from twitter_scraper.query import query_tweets
from twitter_scraper.query import query_tweets_from_user
from twitter_scraper.query import query_user_info
from twitter_scraper.tweet import Tweet
from twitter_scraper.user import User
from twitter_scraper.ts_logger import logger as ts_logger
