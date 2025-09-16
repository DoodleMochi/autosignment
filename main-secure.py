import os
import requests
import operator
from environs import env, validate, ValidationError
import hashlib
import urllib
import sys
import time

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
sharedSecret = os.getenv("TRELLO_API_SECRET")
cparam = {'include[]': 'submission'}
allNames = ['']

#start program
def canvasCompare(classCodes, ucURL, ucAuth):
    cheader = {'Authorization': f"Bearer {ucAuth}"}
    if ucURL[-1] == "/":
        ucURL = ucURL[:-1]
        print("Your URL has a trailing slash. Please remove the slash to improve runtime.")
        print(ucURL)
  #for each class you have, send a request to canvas to get your assignmetns
    for i in classCodes:
        time.sleep(0.1)
        #numClass = numClass + 1
        curl = f"{ucURL}/courses/{i}/assignments"
        #print(str(curl))
        #numParse = 0
        #sends the actual request
        cFullData = requests.get(url=curl, params=cparam, headers=cheader)
        #print(str(cFullData))
        # currentClass = i
        i = f"{quotes}{i}{quotes}"
        cJson = cFullData.json()
        #separates each assignment from canvas/ looks at one assignment object at a time
        for object in cJson:
          #numParse = numParse + 1
          #print(str(numParse), str(numClass))
          #separates each assignments attributes/ looks at one atribute at a time
          #filters out irrelevent attributes and assigns variables to important attributes
          #to add another relevant attribute, visit https://canvas.instructure.com/doc/api/assignments.html and find the name for the wanted attribute
          #then, in the section of code below, add:
          # elif item == 'ATTRIBUTE NAME':
          #VARIABLE FOR ATTRIBUTE = value
          #print(VARIABLE FOR ATTRIBUTE)
          for item, value in object.items():
            if item == 'name':
              name = value
            elif item == 'due_at':
              due_at = value
              #print(due_at)
            elif item == 'updated_at':
              updated_at = value
              #print(updated_at)
            elif item == 'submission':
              for x, y in value.items():
                if x == 'workflow_state':
                  done = y
                  if done == 'unsubmitted' or done == 'graded':
                    allNames.append(name)
                    allNames.append(done)
              #print(done)
            elif item == 'html_url':
              htmlUrl = value
              #print(htmlUrl)
    return allNames


names = canvasCompare(devClassCodes, devURL, devCanvasAuth)

trelloParams = {'key': devApiKey, 'token': devAuthToken, "fields" : "all"}

def getAllCards(boardID, getAllCardsParams):
  allCardsResponse = requests.get(url=f"https://api.trello.com/1/boards/{boardID}/cards", params = getAllCardsParams)
  return allCardsResponse.json()
cardsOnBoard = getAllCards("s9gNcnN6",trelloParams)
#cardsOnBoard = cardsOnBoard.json()
cardNames = []

for card in cardsOnBoard.items:
  if card == "name":
    cardNames.append(card)
print(cardNames)