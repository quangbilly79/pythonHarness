import harness
import argparse
import random
import datetime
import pytz
import json

engine_client = harness.QueriesClient(engine_id="waka",
                                     url="http://localhost:9090",
                                     threads=5,
                                     qsize=50
                                     )

returnQuery = engine_client.send_query({"user": "2684333", "num": 4})
str1 = json.loads(returnQuery.body.decode("utf-8"))
print(str1["result"])