from pymongo import MongoClient
from bson.objectid import ObjectId
from dateutil.tz import tzutc, tzlocal
import datetime
import json


def clear_data(data, labeled=False, filtered=False):
    result = []
    index = 0
    item_id = None
    for d in data:
        index += 1
        item_id = d.pop('_id')
        print("#%s, %s, %s: " % (index, item_id, item_id.generation_time.astimezone(tzlocal())), end="")
        if filtered:
            if index % 10 == 3 or index % 10 == 5:
                print("Skip")
                continue
        print("Export")

        d.pop('evaluation')
        for t in d['thread']:
            t.pop('evaluation')
            t['userId'] = "Alice" if t['userId'] == d['users'][0]['id'] else "Bob"
        d['users'][0].pop('username')
        d['users'][1].pop('username')
        d['users'][0]['id'] = "Alice"
        d['users'][1]['id'] = "Bob"
        if labeled:
            d['users'][0]['userType'] = "Human" if d['users'][0]['userType'] == "org.pavlovai.communication.TelegramChat" else "Bot"
            d['users'][1]['userType'] = "Human" if d['users'][1]['userType'] == "org.pavlovai.communication.TelegramChat" else "Bot"
        else:
            d['users'][0].pop('userType')
            d['users'][1].pop('userType')
        result.append(d)
    if item_id is not None:
        print("Last item _id / ts: %s / %s" % (item_id, item_id.generation_time.astimezone(tzlocal())))

    return result


def export_to_file(name, data, labeled=False, filtered=False):

    f = open("export_%s_%s.json" % (name, datetime.datetime.now()), 'w')
    f.write(json.dumps(clear_data(data, labeled, filtered), indent=4, sort_keys=True))
    f.close()


def main():
    client = MongoClient()
    db = client['convai-bot']
    dialogs = db.dialogs
    now = datetime.datetime.now(tzlocal())
    start_id = ObjectId.from_datetime(datetime.datetime(now.year, now.month, now.day, 0, 0, 0, 0, tzlocal()).astimezone(tzutc()))
    end_id = ObjectId.from_datetime(datetime.datetime(now.year, now.month, now.day, 23, 59, 59, 999, tzlocal()).astimezone(tzutc()))
    test_set = dialogs.find({'$and': [{'_id': {'$gte': start_id}}, {'_id': {'$lte': end_id}}]}).sort('_id', 1)
    train_set = dialogs.find().sort('_id', 1)
    print("\nExport test set for day %s\n" % now.date())
    export_to_file('test_set', test_set, labeled=False, filtered=False)
    print("\nExport train set for day %s\n" % now.date())
    export_to_file('train_set', train_set, labeled=True, filtered=True)
    client.close()

if __name__ == '__main__':
    main()
