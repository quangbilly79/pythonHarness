import harness
import json
engine_client = harness.QueriesClient(engine_id="test_ur",
                                     url="http://localhost:9090",
                                     threads=5,
                                     qsize=50
                                     )
userid = "u1"
result = engine_client.send_query({"user": str(userid), "num": 2})
print("user recommend", engine_client.send_query({"user": str(userid), "num": 2}))

with open("sample-mobile-device-ur-data.csv", "r+") as f:
    listItem=[]
    for line in f.readlines():
        data = line.rstrip('\r\n').split(",")
        listItem.append(data[2])

for item in listItem:
    itemid = item
    result = engine_client.send_query({"item": str(itemid), "num": 4})
    # AsyncResponse Class, tim` trong file source code tai.
    # /usr/local/lib/python3.7/site-packages/harness-0.5.0-py3.7.egg/harness
    # result.body la` byte string, result.body.decode la` string, json.loads(json.loads(result.body.decode) la` dict
    resulstDict = json.loads(result.body.decode("utf-8"))
    # Sau do' cv thanh` list va iterated
    resultList = resulstDict["result"]
    #[{'item': 'Pixel Slate', 'score': 2.991049289703369}, {'item': 'USB-C Ear Buds', 'score': 2.991049289703369}]
    if resultList[0]["score"] != 0:
        print(itemid, resultList)


#python3 examples/ur/getPrediction.py