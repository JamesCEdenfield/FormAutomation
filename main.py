#Date Created - 4/24/2025
import pandas as pd
import json
import requests

#read config file
with open('config/config.json', 'r') as x:
    config = json.load(x)
    x.close()

EXCEL_EXPORT_FILE_PATH = config["excelPath"]
API_KEY =  config["apiKey"]
HEADERS = {
    "Authorization" : f"Bearer {API_KEY}"
}

def getFormData() :

    try : 
        #get json data
        response = requests.get("https://api.fillout.com/v1/api/forms", headers=HEADERS)

        if response.status_code == 200:
            print("Request successful!")
            #get current formId
            formID = response.json()[0]["formId"]
            try :
                formResponse = requests.get(f"https://api.fillout.com/v1/api/forms/{formID}/submissions", headers=HEADERS)
                if response.status_code == 200:
                    return formResponse.json()['responses']
                else :
                    print(f"Request failed with status code: {response.status_code}")
                    print(response.text)
            except Exception as e :
                print("FAILED to get form data")
                print(e)
            #returns list of responses with questions for each
            
        else :
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)
    
    except Exception as e :
        print("FAILED to get form data")
        print(e)



def formatJsonForDF (data) :
    retData = []
    i = 1
    #loop through submissions for current form.
    for each in data :
        #label to seperate submissions.
        curResponse ='RESPONSE # '  + str(i)
        retData.append({'Question' : curResponse })
        #loop through each question
        for question in each['questions'] :
            #print(f"{question['name']} : {question['value']} " )
            #create new row with current question/answer
            retData.append({'Question' : question['name'], 'Answer' : question['value'] })
        retData.append({})
        i+=1
    return retData    


print("-- FORM AUTOMATION JOB STARTED --")
#get form data
data = getFormData() 
#format json to prepare for excel file
data = formatJsonForDF(data)   
#normalize data-types
df = pd.json_normalize(data)
#convert data frame to excel file
df.to_excel(EXCEL_EXPORT_FILE_PATH)
print(f"Excel File Created : ({EXCEL_EXPORT_FILE_PATH})")
print("-- JOB COMPLETED --")































