from pymongo import MongoClient
import pprint
client = MongoClient()
db = client['alt-convai-bot']
dialogs = db.dialogs
i = 0
f_all = open('export-all.json', 'w')
f_80p = open('export-80p.json', 'w')
f_all.write("[\n")
for dialog in dialogs.find().sort('_id',1):
    #pprint.pprint(dialog)
    res = {}
    i += 1
    if i > 1:
        f_all.write(",\n")
        f_80p.write(",\n")

    users = {}
    users[dialog['users'][0]['id']] = 'Alice'
    users[dialog['users'][1]['id']] = 'Bob'

    res['id'] = i

    res['context'] = dialog['context']

    res['dialogId'] = dialog['dialogId']

    res['thread'] = []

    for t in dialog['thread']:
        item = {}
        item['text'] = t['text']
        item['userId'] = users[t['userId']]
        res['thread'].append(item)
    f_all.write(str(res))

    if i % 10 == 3 or i % 10 == 5:
        f_80p.write(str(res))

f_all.write("\n]")
f_all.close()
f_80p.write("\n]")
f_80p.close()
