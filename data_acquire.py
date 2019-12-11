"""
Spotify
"""
import time
import tqdm
from datetime import datetime, timedelta
import sched
import pandas
import logging
import requests
import charts
from io import StringIO
import spotipy
import spotipy.util as util
import sys

import utils
from database import upsert_bpa
from database import upsert_spotify


BPA_SOURCE = "https://transmission.bpa.gov/business/operations/Wind/baltwg.txt"
MAX_DOWNLOAD_ATTEMPT = 5
DOWNLOAD_PERIOD = 3600         # second
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'data.log')


def download_bpa(url=BPA_SOURCE, retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns BPA text from `BPA_SOURCE` that includes power loads and resources
    Returns None if network failed
    """
    text = None
    for i in range(retries):
        try:
            req = requests.get(url, timeout=0.5)
            req.raise_for_status()
            text = req.text
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if text is None:
        logger.error('download_bpa too many FAILED attempts')
    return text

def download_spotify(datetime=datetime.today(), retries=MAX_DOWNLOAD_ATTEMPT):
    """Returns BPA text from `BPA_SOURCE` that includes power loads and resources
    Returns None if network failed
    """
    chart = None
    for i in range(retries):
        try:
            today = datetime.today()
            today= today.strftime("%Y-%m-%d")
            lastweek = datetime.today() - timedelta(days = 6)
            lastweek = lastweek.strftime("%Y-%m-%d")
            chart = charts.get_charts(lastweek, today,region='nl')
        except requests.exceptions.HTTPError as e:
            logger.warning("Retry on HTTP Error: {}".format(e))
    if chart is None:
        logger.error('download_bpa too many FAILED attempts')
    return chart


def filter_bpa(text):
    """Converts `text` to `DataFrame`, removes empty lines and descriptions
    """
    # use StringIO to convert string to a readable buffer
    df = pandas.read_csv(StringIO(text), skiprows=11, delimiter='\t')
    df.columns = df.columns.str.strip()             # remove space in columns name
    df['Datetime'] = pandas.to_datetime(df['Date/Time'])
    df.drop(columns=['Date/Time'], axis=1, inplace=True)
    df.dropna(inplace=True)             # drop rows with empty cells
    return df

def filter_spotify(chart):
    """append genre information to the data 
    """

    ### get spotify token 
# define authentication
    username = 'zhiyanwang27'
    scope = 'user-read-private'

    CLIENT_ID = '1d35e049282a4f198bd09ff07e105784'
    CLIENT_SECRET = '54850e7841cb47c5bc6c8970457dee89'

# playlist_id = '6watTtiqGlxPj2cxy6Sk8U'

    token = util.prompt_for_user_token(username, 
                                   scope,
                                   client_id=CLIENT_ID,
                                   client_secret=CLIENT_SECRET,
                                   redirect_uri='http://localhost/8000/')

    sp = spotipy.Spotify(auth=token)
    # use IO to convert it into dataframe 
    df = chart
    df['date'] = pandas.to_datetime(df['date'])
    df['ID'] = 'default value'
    df['genre'] = 'default value'
    df['follwers'] = 'default value'
    for i in tqdm.tqdm(range(df.shape[0])):
        track_id = df.iloc[i,4][31:]
        df.iloc[i,7] = track_id
        artist_id = sp.track(track_id)['artists'][0]['id']
        if len(sp.artist(artist_id)['genres']) > 0:
            gr = sp.artist(artist_id)['genres'][0]
        else:
            gr = 'None'
        fl = sp.artist(artist_id)['followers']['total']
        df.iloc[i,8] = gr
        df.iloc[i,9] = fl
        time.sleep(0.01)
    return df


# def update_once():
#     t = download_bpa()
#     df = filter_bpa(t)
#     upsert_bpa(df)
def update_once():
    t = download_spotify()
    df = filter_spotify(t)
    upsert_spotify(df)

def main_loop(timeout=DOWNLOAD_PERIOD):
    scheduler = sched.scheduler(time.time, time.sleep)

    def _worker():
        try:
            update_once()
        except Exception as e:
            logger.warning("main loop worker ignores exception and continues: {}".format(e))
        scheduler.enter(timeout, 1, _worker)    # schedule the next event

    scheduler.enter(0, 1, _worker)              # start the first event
    scheduler.run(blocking=True)


if __name__ == '__main__':
    main_loop()


