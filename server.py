from flask import Flask, render_template, request,jsonify,json
from mongoengine import *

app = Flask(__name__)

connect('test')

class Player(EmbeddedDocument):
    playerId = StringField(required=False, max_length=36)
    tankLife = IntField(required=False)
    #playerId = StringField(required=True, max_length=36)
    #tankLife = IntField(min_value=1)

class GameSession(Document):
    gameId = StringField(required=True,max_length=36)
    players = ListField(EmbeddedDocumentField(Player))
    gameState = StringField(max_length=10)
    gameWinner = StringField(max_length=25)

class Action(Document):
    playerId = StringField(required=True,max_length=36)
    actionId = IntField(min_value=1)
    actionType = StringField(required=True,max_length=10)
    movementCords = StringField(max_length=10)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/gameSessionInit', methods=['POST'])
def postSession():
    createdSession = createSession()
    saveSession(createdSession)
    print("PRIMER POST")
    print (createdSession)
    return jsonify(createdSession)

@app.route('/sessionUpdate/<sessionId>', methods=['POST'])
def putSession(sessionId):
    sessionDict = request.form.to_dict()
    updatedSession = updateSession(sessionId,sessionDict)
    return updatedSession

@app.route('/getGameSessions/<sessionId>', methods=['GET'])
def getSession(sessionId):
    session = findSession(sessionId)
    del session['_id']
    print("ULTIMO GET")
    print(session)
    return jsonify(session)


def createSession():
    sessionDict = request.form.to_dict()
    parsedSession = converToJson(sessionDict)
    return parsedSession


def converToJson(sessionDict):
    parsedSession = {}
    for key, value in sessionDict.items():
        dict = key
        parsedSession = json.loads(key)
    return parsedSession


def updateSession(gameId,jsonData):
    parsedJson = converToJson(jsonData)
    print("ESTE ES EL DE UPDATE")
    print(parsedJson)
    ##Mejorar este método de actualización
    GameSession.objects(gameId = gameId).update(players=parsedJson['Items'][0]['players'])
    GameSession.objects(gameId = gameId).update(gameState=parsedJson['Items'][0]['gameState'])
    serealizedSession = findSession(gameId)
    del serealizedSession['_id']
    return jsonify(serealizedSession)

def saveSession(jsonData):
    gameSession = GameSession(
        gameId = jsonData['Items'][0]['gameId'],
        players = (jsonData['Items'][0]['players']),
        gameState=jsonData['Items'][0]['gameState'],
        gameWinner = jsonData['Items'][0]['gameWinner']
    )
    gameSession.save()

def findSession(gameId):
    sessionObject = GameSession.objects(gameId = gameId).first()
    parsedSession = sessionObject.to_mongo()
    serealizedSession = parsedSession.to_dict()
    return serealizedSession


if __name__ == '__main__':
    app.run(host='0.0.0.0')
