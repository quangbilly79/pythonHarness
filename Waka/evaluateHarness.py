import harness
import argparse
import random
import datetime
import pytz
from pyspark.sql import *
from pyspark.sql.functions import *
import json

engine_client = harness.QueriesClient(engine_id="waka",
                                     url="http://localhost:9090",
                                     threads=5,
                                     qsize=50
                                     )

spark = SparkSession.builder.getOrCreate()


sqlUserRead = """
select user_id, collect_set(cast(content_id as string)) as content_id from waka.waka_pd_fact_reader
where  data_date_key > 20220631 and data_date_key <= 20220731
group by user_id
order by user_id
"""

# Lay' tat' ca? userid co' trong thang' 7 va` train vs dl thang' 6
# Neu' k co' trong data thi` se~ recommend popular item cho ho.
# The score of 0 means popular items are being returned.
dfAllUserid = spark.sql(sqlUserRead).select(col("user_id")).orderBy(col("user_id"))
listAllUserId = dfAllUserid.collect()
dictUserRecommend = {} # Dict chua' userId va` list item id cua? cac' item dc recommend cho user do'
for row in listAllUserId:

    numOfReturnRecom = 4
    returnQuery = engine_client.send_query({"user": str(row["user_id"]), "num": numOfReturnRecom})
    dictItemScore = json.loads(returnQuery.body.decode("utf-8"))
    # {'itemScores': [{'item': '24671', 'score': 9.247717}, {'item': '369
    listItemScore = dictItemScore["result"]
    #[{'item': '24671', 'score': 9.247717}, {'item': '36986
    listItem = map(lambda x: x["item"], listItemScore)
    # [24671, 36986, ...]
    dictUserRecommend.update({str(row["user_id"]): list(listItem)})
    # {1: [24671, 36986,...], 2: [23245, ...], ...}

with open('userRecommendHarness.txt', 'w+') as f:
    for key, value in dictUserRecommend.items():
        f.write('%s:%s\n' % (key, value))

# Lay' ds cac' userid va` itemid ma` ho. read trong thang' 7
dfUserRead = spark.sql(sqlUserRead)
listUserRead = dfUserRead.collect()
# row[userid: 1, content_id: [24671, 36986,...]]
dictUserRead = {} # Dict chua' cac' userid va` list itemid ma` ho. read trong thang' 7
for row in listUserRead:
    dictUserRead.update({str(row["user_id"]): row["content_id"]})
    # {1: [24671, 36986, ...], 2: [23245, ...], ...}

with open('userReadHarness.txt', 'w+') as f:
    for key, value in dictUserRead.items():
        f.write('%s:%s\n' % (key, value))

# __Recommendations__	__Precision @k's__	        __AP@3__
# [0, 0, 1]	            [0, 0, 1/3]	            (1/3)(1/3) = 0.11
# [0, 1, 1]	            [0, 1/2, 2/3]	        (1/3)[(1/2) + (2/3)] = 0.38
# [1, 1, 1]	            [1/1, 2/2, 3/3]	        (1/3)[(1) + (2/2) + (3/3)] = 1
def averagePrecisionAtK(list1, list2):
    # Average Precision At 4
    averagePrecisionAtK = 0
    j = 1
    for i in range(4):
        if list1[i] in list2:
            averagePrecisionAtK += (1/4)*(j/(i+1))
            #print(list1[i], '-', str(j), '-', str(i+1), '-', str((1/4)*(j/(i+1))))
            j += 1
    return averagePrecisionAtK

# Tuong tu. nhu tren, nhung k quan tam den' thu' tu.
# __Recommendations__	__Precision
# [0, 0, 1]	            1/3
# [0, 1, 1]	            2/3
# [1, 1, 1]	            3/3
def Precision(list1, list2):
    return len(list(set(list1) & set(list2)))/4

dictResult = {} # Dict tong? hop. kq de? debug
totalAveragePrecision = 0 # Total AveragePrecision at 4 of all users
totalPrecision = 0 # Total Precision at 4 of all users
for userid in dictUserRead.keys():
    averagePrecision = averagePrecisionAtK(dictUserRecommend[userid], dictUserRead[userid])
    totalAveragePrecision += averagePrecision

    precision = Precision(dictUserRecommend[userid], dictUserRead[userid])
    totalPrecision += precision

    dictResult.update({str(userid): {"Recommend": dictUserRecommend[userid],
    "Read": dictUserRead[userid], "averagePrecision": averagePrecision, "precision": precision}})
    #{6913688:{'Recommend': ['37064', '1365', '1344', '36920'], 'Purchase':
    # ['37064', '1365', '1344', '36479'], 'precision': 0.75}

with open('debugHarness.txt', 'w+') as f:
    # Sort lai. theo precision cho de~ debug
    for key, value in sorted(dictResult.items(), key=lambda x_y: x_y[1]["precision"],reverse=True):
        f.write('%s:%s\n' % (key, value))

# Mean Average Precision and Mean Precision
MAP = totalAveragePrecision / len(dictUserRead) * 100
MP = totalPrecision / len(dictUserRead) * 100
with open('resultHarness.txt', 'w+') as f:
    f.write("Mean Average Precision: "+ str(MAP)+"%" + "\n" + "Mean Precision: "+ str(MP)+"%")


#train set 6 month
# Mean Average Precision: 4.048065018784152%
# Mean Precision: 5.4095158811475414%