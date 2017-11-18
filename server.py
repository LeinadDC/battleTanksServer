from flask import Flask, render_template, request,jsonify
from mongoengine import *

app = Flask(__name__)

connect('test')

class Player(Document):
    id = StringField(required=True,max_length=25)
    xPosition = StringField(max_length=50)
    yPosition = StringField(max_length=50)

class Action(Document):
    playerId = StringField(required=True,max_length=25)
    actionId = IntField(min_value=1)
    actionType = StringField(required=True,max_length=10)
    movementCords = StringField(max_length=10)

class unityTest(Document):
    tankLife = IntField(min_value=1)
    playerId = StringField(required=True, max_length=25)
    actionId = IntField(min_value=1)
    actionType = StringField(required=True, max_length=10)
    movementCords = StringField(max_length=10)


@app.route('/')
def hello():
    return "Hello world"

@app.route('/testPost', methods=['POST'])
def testPost():
    test = request.get_json()
    print(test)
    createTest(test)
    return "DATA OK"

@app.route('/testGet/<playerId>', methods=['GET'])
def testGet(playerId):
    test = unityTest.objects(playerId = playerId)
    print(test)
    return "DATA GET"


def createTest(jsonData):
    action = unityTest(
        tankLife = jsonData["tankLife"],
        playerId = jsonData["playerId"],
        actionId = jsonData["actionId"],
        actionType = jsonData["actionType"],
        movementCords = jsonData["movementCords"],

    )
    action.save()

if __name__ == '__main__':
    app.run(host='0.0.0.0')
