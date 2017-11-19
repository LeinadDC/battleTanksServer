from flask import Flask, render_template, request,jsonify,json
from mongoengine import *

app = Flask(__name__)

connect('test')



class Player(EmbeddedDocument):
    playerId = StringField(required=True, max_length=36)
    tankLife = IntField(min_value=1)

class GameSession(EmbeddedDocument):
    gameId = StringField(required=True,max_length=36)
    players = ListField(EmbeddedDocumentField(Player))
    gameState = StringField(max_length=10)
    gameWinner = StringField(max_length=25)

class Items(Document):
    gameSession = ListField(EmbeddedDocumentField(GameSession))

class Action(Document):
    playerId = StringField(required=True,max_length=36)
    actionId = IntField(min_value=1)
    actionType = StringField(required=True,max_length=10)
    movementCords = StringField(max_length=10)


@app.route('/')
def hello():
    return "Hello world"

@app.route('/gameSessionInit', methods=['POST'])
def testPost():
    test = request.form.to_dict()
    loaded_r = {}
    for key, value in test.items():
        dict = key
        loaded_r = json.loads(key)
    print(loaded_r['Items'][0]['gameState'])
    print(loaded_r ['Items'][0]['players'])
    return "DATA OK"

@app.route('/testGet/<playerId>', methods=['GET'])
def testGet(playerId):

    return "DATA GET"


def createGameSession(jsonData):
    session = Items(
        gameSession = jsonData["Items"]
    )
    session.save()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
