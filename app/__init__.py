# -*- coding: utf-8 -*-
from flask import Flask, render_template, request,jsonify,json
from flask_mongoengine import MongoEngine
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from mongoengine import *
from werkzeug.security import *
import wtforms_json
from flask_login import LoginManager, UserMixin
from wtforms import Form, BooleanField, StringField, PasswordField, validators

import uuid

from db import connection




app = Flask(__name__)
app.config.from_object('config')
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
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
    user_id = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()


class RegistrationForm(Form):
    username = StringField()
    password = PasswordField()
    email = StringField()

@jwt.user_claims_loader
def add_claims_to_access_token(user):
    return {'user_id': user.user_id}

@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.username

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
                userId = str(uuid.uuid1())
                newUser = GameUser(userId,form.username.data,hashpass,form.email.data)
                newUser.save()
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
                    access_token = create_access_token(identity=check_user)

                    ret = {'access_token': access_token}
                    return jsonify(ret), 200
            else:
                return jsonify("Error")
        else:
            return jsonify("Form no valido")
    return jsonify("Register")


@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    ret = {
        'current_identity': get_jwt_identity()
    }
    return jsonify(ret), 200

@app.route('/gameSessionInit', methods=['POST'])
@jwt_required
def postSession():
    createdSession = createSession()
    saveSession(createdSession)
    print("PRIMER POST")
    print (createdSession)
    return jsonify(createdSession)

@app.route('/sessionUpdate/<sessionId>', methods=['POST'])
@jwt_required
def putSession(sessionId):
    sessionDict = request.form.to_dict()
    updatedSession = updateSession(sessionId,sessionDict)
    return updatedSession

@app.route('/getGameSessions/<sessionId>', methods=['GET'])
@jwt_required
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
