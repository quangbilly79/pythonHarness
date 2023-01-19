import json
import os
with open("../importEventJson/mergedRateEvent.json", "r+") as f7:
    line = [json.loads(line) for line in f7.readlines()]
    # string to json, then create a json-like list
with open("../importEventJson/mergedRateEventHarness.json", "w+") as f8:
    json.dump(line, f8) # dump json-like list into a json file
    print('done')

with open("../importEventJson/mergedReadEvent.json", "r+") as f:
    line = [json.loads(line) for line in f.readlines()]
    # string to json, then create a json-like list
with open("../importEventJson/mergedReadEventHarness.json", "w+") as f1:
    json.dump(line, f1) # dump json-like list into a json file
    print('done1')
#
with open("../importEventJson/mergedWishlistEvent.json", "r+") as f2:
    line = [json.loads(line) for line in f2.readlines()]
    # string to json, then create a json-like list
with open("../importEventJson/mergedWishlistEventHarness.json", "w+") as f3:
    json.dump(line, f3) # dump json-like list into a json file
    print('done2')

with open("../importEventJson/mergedPropertiesEvent.json", "r+", encoding="utf8") as f4:
    line = [json.loads(line) for line in f4.readlines()]

    #string to json, then create a json-like list
with open("../importEventJson/mergedPropertiesEventHarness.json", "w+", encoding="utf8") as f5:
    json.dump(line, f5, ensure_ascii=False) # dump json-like list into a json file.
    # Some minor fix cho tieng' viet. co' dau'
    print('done3')

os.remove("../importEventJson/mergedPropertiesEvent.json")
os.remove("../importEventJson/mergedWishlistEvent.json")
os.remove("../importEventJson/mergedReadEvent.json")
os.remove("../importEventJson/mergedRateEvent.json")