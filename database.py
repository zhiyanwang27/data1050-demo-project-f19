import logging
import pymongo
import pandas as pds

import utils

client = pymongo.MongoClient()
logger = logging.Logger(__name__)
utils.setup_logger(logger, 'db.log')


def upsert_bpa(df):
    """
    Update MongoDB database `energy` and collection `energy` with the given `DataFrame`.
    """
    db = client.get_database("energy")
    collection = db.get_collection("energy")
    update_count = 0
    for record in df.to_dict('records'):
        result = collection.replace_one(
            filter={'Datetime': record['Datetime']},    # locate the document if exists
            replacement=record,                         # latest document
            upsert=True)                                # update if exists, insert if not
        if result.matched_count > 0:
            update_count += 1
    logger.info(f"rows={df.shape[0]}, update={update_count}, "
                f"insert={df.shape[0]-update_count}")


def fetch_all_bpa():
    db = client.get_database("energy")
    collection = db.get_collection("energy")
    return list(collection.find())


def fetch_all_bpa_as_df():
    data = fetch_all_bpa()
    if len(data) == 0:
        return None
    df = pds.DataFrame.from_records(data)
    df.drop('_id', axis=1, inplace=True)
    return df


if __name__ == '__main__':
    print(fetch_all_bpa_as_df())
