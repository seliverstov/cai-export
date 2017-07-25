#!/usr/bin/env python3

from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.tz import tzutc, tzlocal
import datetime
import sys


def users_stat():
    team_users = ['Ignecadus', 'locky_kid', 'IFLED', 'justgecko', 'AlexFridman', 'necnec', 'YallenGusev', 'fartuk1',
                  'mryab', 'akiiino', 'vostrjakov', 'chernovsergey', 'latentbot', 'SkifMax', 'VictorPo', 'zhukov94',
                  'Username11235', 'IlyaValyaev', 'lextal', 'MacJIeHok', 'olgalind', 'roosh_roosh', 'davkhech',
                  'mambreyan', 'ashmat98', 'ffuuugor', 'artyomka', 'p_gladkov', 'not_there', 'ad3002', 'gtamazian',
                  'artkorenev', 'sudakovoleg', 'sin_mike', 'ilya_shenbin', 'Vladislavprh', 'AntonAlexeyev',
                  'bekerov', 'EvKosheleva', 'sw1sh', 'SDrapak', 'izmailov', 'dlunin', 'Xsardas', 'sparik'
                  ]
    tl = [t.lower() for t in team_users]
    client = MongoClient()
    db = client['convai-bot']
    dialogs = db.dialogs
    day_id = ObjectId.from_datetime(
        datetime.datetime(2017, 7, 24, 0, 0, 0, 0, tzlocal()).astimezone(tzutc()))
    data = dialogs.find({'_id': {'$gte': day_id}})
    user_dialogs = dict()

    for d in data:
        for u in d['users']:
            if u['username'] not in user_dialogs:
                user_dialogs[u['username']] = 0
            user_dialogs[u['username']] += 1

    for u in user_dialogs:
        user_type = 'T' if u.lower() in tl else 'O'
        print("%s,%s,%s" % (u, user_dialogs[u], user_type))
    client.close()


def daily_stat(alltime=False):
    client = MongoClient()
    db = client['convai-bot']
    dialogs = db.dialogs
    now = datetime.datetime.now(tzlocal())

    if alltime:
        day_id = ObjectId.from_datetime(
            datetime.datetime(2017, 7, 24, 0, 0, 0, 0, tzlocal()).astimezone(tzutc()))
    else:
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
    hourly_bots = set()
    hourly_h2b = 0
    for h in hourly:
        if h['users'][0]['userType'] == 'org.pavlovai.communication.Bot':
            hourly_bots.add(h['users'][0]['username'])
        else:
            hourly_users.add(h['users'][0]['username'])

        if h['users'][1]['userType'] == 'org.pavlovai.communication.Bot':
            hourly_bots.add(h['users'][1]['username'])
        else:
            hourly_users.add(h['users'][1]['username'])

        if h['users'][0]['userType'] == 'org.pavlovai.communication.Bot' or h['users'][1]['userType'] == 'org.pavlovai.communication.Bot':
            hourly_h2b += 1

    print("Dialogs created from beginning of the day: %s (h2b: %s, h2h: %s). Unique users: %s" %
          (daily.count(), daily_h2b, daily.count() - daily_h2b, len(daily_users)))
    print("Dialogs created from last hour: %s (h2b: %s, h2h: %s).  Unique users: %s" %
          (hourly.count(), hourly_h2b, hourly.count() - hourly_h2b, len(hourly_users)))
    print("")
    # print("%s unique users from beginning of the day: %s" % (len(daily_users), daily_users))
    print("Used bots from last hour:")
    for u in hourly_bots:
        print("\t%s" % u)
    # print("%s unique users from last hour: %s" % (len(hourly_users), hourly_users))

    client.close()


def main():
    if len(sys.argv) != 2:
        print("Example: report.py daily_stat | alltime_stat | users_stat")
        sys.exit(1)
    if sys.argv[1] == 'daily_stat':
        daily_stat()
    elif sys.argv[1] == 'users_stat':
        users_stat()
    elif sys.argv[1] == 'alltime_stat':
        daily_stat(True)
    else:
        print("Unknown arg: %s" % sys.argv[1])
        sys.exit(1)

if __name__ == '__main__':
    main()
