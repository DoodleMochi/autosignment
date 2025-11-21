
# A very simple Bottle Hello World app for you to get started with...
from bottle import default_app, route
import os
import requests
import operator
from environs import env, validate
import hashlib
import urllib
import json
import sys
import time
from bottle import route, run, template

run(host='localhost', port=8080)
env.read_env("bingus.env")
listID = []
quotes = '"'
taskNameArray = ["test", "test"]
newTaskSID = []
newTaskID = []
devClassCodes = env.list("CLASS_CODES")
print(devClassCodes)
devCanvasAuth = env("CANVAS")
devApiKey = env("TRELLO_API_KEY")
devAuthToken = env("TRELLO_AUTH_TOKEN")
devURL = env("URL", validate = validate.URL(relative=False, absolute=True, error="It looks like the URL you provided isn't valid. Check that you've included http:// or https:// in your URL."))
print(devURL)
sharedSecret = os.getenv("Secret")
cparam = {'include[]': 'submission'}
allNames = ['']



#Funtion definitions
def canvasGetCourses(checkURL, checkAuth):
    #Checks if the classes in the current array are still open (IE. has a new semester started)
    #If this fails, it'll run a setup GUI
    checkHeader = {'Authorization': f"Bearer {checkAuth}"}
    retrievedCourses = []
    if checkURL[-1] == "/":
        checkURL = checkURL[:-1]
        print("Your URL has a trailing slash. Please remove the slash to improve runtime.")
        print(checkURL)
    checkURL = f"{checkURL}/courses"
    checkFullData = requests.get(url=checkURL, params= {'enrollment_state' : "active", 'include[]' : "favorites"}, headers=checkHeader)
    checkFullJSON = checkFullData.json()
    for jsonObject in checkFullJSON:
        checkFlag = False
        for key, value in jsonObject.items():
            if key == 'is_favorite':
                if value == True:
                    checkFlag = True
            elif key == 'id':
                id = value
        if checkFlag:
            retrievedCourses.append(id)
    print(retrievedCourses)
    return retrievedCourses

def canvasGetJSON(originalJSON, currentClassCode):
    #separates each assignments attributes/ looks at one atribute at a time
    totalDictArray = []
    for object in originalJSON:
            #filters out irrelevent attributes and assigns variables to important attributes
            #to add another relevant attribute, visit https://canvas.instructure.com/doc/api/assignments.html and find the name for the wanted attribute
            #then, in the section of code below, add:
            # elif item == 'ATTRIBUTE NAME':
            #VARIABLE FOR ATTRIBUTE = value
            #And under the "if done" statement add tempDict[KEY] = VARIABLE
        for item, value in object.items():
            tempDict = {}
            if item == 'name':
              name = value
            elif item == 'due_at':
              due_at = value
              #print(due_at)
            elif item == 'updated_at':
              updated_at = value
              #print(updated_at)
            elif item == 'html_url':
              htmlUrl = value
              print(htmlUrl)
            elif item == 'submission':
              for x, y in value.items():
                if x == 'workflow_state':
                  done = y
                  if done == 'unsubmitted' or done == 'graded':
                    tempDict['name'] = name
                    tempDict['done'] = done
                    tempDict['due_at'] = due_at
                    tempDict['updated_at'] = updated_at
                    tempDict['url'] = htmlUrl
                    totalDictArray.append(tempDict)
    return totalDictArray

def canvasCompare(classCodes, ucURL, ucAuth):
    cheader = {'Authorization': f"Bearer {ucAuth}"}
    if ucURL[-1] == "/":
        ucURL = ucURL[:-1]
        print("Your URL has a trailing slash. Please remove the slash to improve runtime.")
        print(ucURL)
  #for each class you have, send a request to canvas to get your assignmetns
    for i in classCodes:
        time.sleep(1)
        #numClass = numClass + 1
        curl = f"{ucURL}/courses/{i}/assignments"
        print(str(curl))
        #numParse = 0
        #sends the actual request
        cFullData = requests.get(url=curl, params=cparam, headers=cheader)
        print(str(cFullData))
        # currentClass = i
        i = f"{quotes}{i}{quotes}"
        cJson = cFullData.json()
        return canvasGetJSON(cJson, i)




@route('/')
def hello_world():
    return canvasCompare(canvasGetCourses(devURL, devCanvasAuth), devURL, devCanvasAuth)

application = default_app()

