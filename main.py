import pandas as pd
import json
import requests


def getFormData() :
    #hit 'fillout' Rest API
    #convert json into DICT and pass to manipulateDict() function.
    pass


def manipulateDict(data:dict) -> dict : 
    for key, value in data.items() :
        #print(f"KEY : {key}, Value : {value}")
        data[key] = str(value).replace("[", "").replace("]", "").replace("{","").replace("}", "")
    return data


#Convert JSON data into Dictionary.
with open("temp/testJson.json", 'r') as x:
    toDictionary = json.load(x)
    x.close()

#assign finalize dictionary to be converted to xlsx
toDictionary = manipulateDict(toDictionary)

#normalize data-types
df = pd.json_normalize(toDictionary)
#convert data frame to excel file
df.to_excel("temp/testExcel.xlsx")































