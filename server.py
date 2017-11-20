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
    return createdSession


def createSession():
    sessionDict = request.form.to_dict()
    parsedSession = {}
    for key, value in sessionDict.items():
        dict = key
        parsedSession = json.loads(key)
    saveSession(parsedSession)
    return parsedSession


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

@app.route('/getGameSessions/<sessionId>', methods=['GET'])
def getSession(sessionId):
    session = findSession(sessionId)
    del session['_id']
    print(session)
    return jsonify(session)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
