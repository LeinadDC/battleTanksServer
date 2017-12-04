# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify,json
from flask_mongoengine import MongoEngine
from mongoengine import *
from werkzeug.security import *
import wtforms_json
from flask_login import LoginManager, UserMixin
from wtforms import Form, BooleanField, StringField, PasswordField, validators

from db import connection

app = Flask(__name__)
app.config.from_object('config')
wtforms_json.init()
db = MongoEngine(app)
login_manager = LoginManager()
login_manager.init_app(app)


connection()

class Player(db.EmbeddedDocument):
    playerId = db.StringField(required=False, max_length=36)
    tankLife = db.IntField(required=False)

class GameSession(db.Document):
    gameId = db.StringField(required=True,max_length=36)
    players = db.ListField(db.EmbeddedDocumentField(Player))
    gameState = db.StringField(max_length=10)
    gameWinner = db.StringField(max_length=25)

class GameUser(UserMixin,db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()


class RegistrationForm(Form):
    username = StringField()
    password = PasswordField()
    email = StringField()

@login_manager.user_loader
def load_user(user_id):
    return GameUser.objects(pk=user_id).first()

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        sentForm = request.get_json()
        print(sentForm)
        form = RegistrationForm.from_json(sentForm)
        print("Validando form")
        if form.validate():
            print("Form validado, validando si el usuario existe")
            formMail = form.email.data
            existing_user = GameUser.objects(email = formMail).first()
            if existing_user is None:
                print("Usuario no existe, creando usuario")
                hashpass = generate_password_hash(form.password.data,method='sha256')
                newUser = GameUser(form.username.data,hashpass,form.email.data).save()
                return jsonify("Creacion completada")
            else:
                return jsonify("Usuario ya existe")
        else:
            return jsonify("Form no valido")
    return jsonify("Register")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        sentForm = request.get_json()
        print(sentForm)
        form = RegistrationForm.from_json(sentForm)
        print("Validando form")
        if form.validate():
            print("Form validado, validando si el usuario existe")
            formMail = form.email.data
            check_user = GameUser.objects(email = formMail).first()
            if check_user:
                print("Usuario existe, revisando contraseña")
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return jsonify("Logeado")
            else:
                return jsonify("Error")
        else:
            return jsonify("Form no valido")
    return jsonify("Register")


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
    GameSession.objects()
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
