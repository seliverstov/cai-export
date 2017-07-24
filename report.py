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
    daily_h2b = 0
    for d in daily:
        daily_users.add(d['users'][0]['username'])
        daily_users.add(d['users'][1]['username'])
        if d['users'][0]['userType'] == 'org.pavlovai.communication.Bot' or d['users'][1]['userType'] == 'org.pavlovai.communication.Bot':
            daily_h2b += 1

    hourly_users = set()
    hourly_h2b = 0
    for h in hourly:
        hourly_users.add(h['users'][0]['username'])
        hourly_users.add(h['users'][1]['username'])
        if h['users'][0]['userType'] == 'org.pavlovai.communication.Bot' or h['users'][1]['userType'] == 'org.pavlovai.communication.Bot':
            hourly_h2b += 1

    print("Dialogs created from beginning of the day: %s (h2b: %s, h2h: %s)" % (daily.count(), daily_h2b, daily.count() - daily_h2b))
    print("Dialogs created from last hour: %s (h2b: %s, h2h: %s)" % (hourly.count(), hourly_h2b, hourly.count() - hourly_h2b))
    print("")
    print("%s unique users from beginning of the day: %s" % (len(daily_users), daily_users))
    print("%s unique users from last hour: %s" % (len(hourly_users), hourly_users))

    client.close()

if __name__ == '__main__':
    main()