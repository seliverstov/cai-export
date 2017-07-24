from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.tz import tzutc, tzlocal
import datetime


def main():
    client = MongoClient()
    db = client['convai-bot']
    dialogs = db.dialogs
    now = datetime.datetime.now(tzlocal())
    day_id = ObjectId.from_datetime(
        datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0, tzlocal()).astimezone(tzutc()))
    hour_id = ObjectId.from_datetime(
        datetime.datetime(now.year, now.month, now.day, now.hour - 1, now.minute, now.second, now.microsecond, tzlocal()).astimezone(tzutc()))

    daily = dialogs.find({'_id': {'$gte': day_id}})
    hourly = dialogs.find({'_id': {'$gte': hour_id}})

    daily_users = set()
    for d in daily:
        daily_users.add(d['users'][0]['id'])
        daily_users.add(d['users'][1]['id'])

    hourly_users = set()
    for h in hourly:
        hourly_users.add(h['users'][0]['id'])
        hourly_users.add(h['users'][1]['id'])

    print("Dialogs created from beginning of the day: %" % daily.count())
    print("Dialogs created from last hour: %" % hourly.count())
    print("%s unique users from beginning of the day: %s" % (len(daily_users), daily_users))
    print("%s unique users from last hour: %s" % (len(hourly_users), hourly_users))



if __name__ == '__main__':
    main()