import requests
import json

def requirements():
    f = open("requirements.json")
    api_data = json.load(f)
    key = api_data["api_key"]
    token = api_data["api_token"]
    return key, token

def boardReqTemp(key, token): # see the id of boards and take the id of your board "Test"
    board_url = "https://api.trello.com/1/members/me/boards?key={}&token={}".format(key, token)
    return board_url

def listReqTemp(boardId, key, token): #finds the id of lists in your board "id"
    list_url = "https://api.trello.com/1/boards/{}/lists?key={}&token={}".format(boardId, key, token)
    return list_url

def listOfCardsTemp(listId, key, token):    # find the cards in  the list
    listOfCardUrl = "https://api.trello.com/1/lists/{}/cards?key={}&token={}".format(listId, key, token)
    return listOfCardUrl

def cardMemberTemp(idmember, key, token):
    memberUrl = "https://api.trello.com/1/members/{}?key={}&token={}".format(idmember, key, token)
    return memberUrl

#makes request and returns response body
def makeRequest(url):
    response = requests.get(url)
    data = response.text
    data = json.loads(data)
    return data
    
#takes lists of boards and returns the id of necessary board
def extractBoardId(data):
    for i in data:
        if i["name"] == "Test":
            return i["id"]

#takes the card infos as json and returns the member names of the card as a list
def extractCardOwners(card, key, token):
    try:
        nameList = []
        for i in card["idMembers"]:
            memberUrl = cardMemberTemp(i, key, token)
            memberInfo = makeRequest(memberUrl)
            nameList.append(memberInfo["fullName"])
        return nameList
    except KeyError as error:
        if "Exceeded rate limit " in memberInfo["message"]:
            print("Too many request in a definit time interval")
        else:
            print("An error occured")
            return

#takes board id and the name of the person whose Story Points will be calculated and returns the amount of story points
def extractCardSP(boardId, someName, key, token):
    doneSP = 0
    personSP = 0
    totalSP = 0
    url = listReqTemp(boardId, key, token)
    lists = makeRequest(url)
    
    for mylist in lists:
        #mylist["id"] = list id's
        url = listOfCardsTemp(mylist["id"], key, token)
        cardList = makeRequest(url)
        for cards in cardList:
            nameList = extractCardOwners(cards, key, token)
            if mylist["name"] == "Done" and nameList != None:
                #we are extracting the sp whihc was done from the card name
                totalSP += int(cards["name"][-2:-1])
                #search the name we are looking for in the name list
                for name in nameList:
                    if someName == name:
                        doneSP += int(cards["name"][-2:-1])

                        personSP +=  int(cards["name"][-2:-1])
            elif nameList != None:
                #we are extracting the sp from the card name
                totalSP += int(cards["name"][-2:-1])
                for name in nameList:
                    if name == someName:
                        personSP += int(cards["name"][-2:-1])
    print(totalSP, doneSP, personSP)
    return totalSP, doneSP, personSP

#takes board id and returns the ids of lists
def calculatePercentage(done, burden):
    print(done, burden)
    return done / burden * 100

#shows the Story point information of the person
def show(person, total, burdenSP, done, percentage,):
    print("Total \t\t= {}".format(total))
    print("Person \t\t= {}".format(person))
    print("Burden \t\t= {}".format(burdenSP))
    print("Done \t\t= {}".format(done))
    print("Percentage\t= {}".format(percentage))
    # print("""total amount of story point = {}\nSP burden of {} = {}\nStroy Point done by {} = {}\nPercentage of done tasks which belongs to {} = {}""".format(totalSp, name, personSP, name, doneSP, name, percentage))


def main():
    key, token = requirements()
    name = "Hakan EVKURAN"  #name can be taken from requirements if necessary
    boardUrl = boardReqTemp(key, token)
    mainBoardUrl = makeRequest(boardUrl)
    boardId = extractBoardId(mainBoardUrl)
    totalSp, doneSP, burdenSP = extractCardSP(boardId, name, key, token)
    percentage = calculatePercentage(doneSP, burdenSP)
    show(name, totalSp, burdenSP, doneSP,percentage)

main()