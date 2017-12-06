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

import uuid
from db import connection
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config')
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
wtforms_json.init()
login_manager = LoginManager()
login_manager.init_app(app)


db = MongoEngine(app)



from app.models.player import Player
from app.models.models import GameSession
from app.models.models import GameUser
from app.models.forms import RegistrationForm
connection()

from app.controllers import auth
from app.controllers import game

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
    return auth.register()

@app.route('/login', methods=['GET', 'POST'])
def login():
    return auth.login()

@app.route('/gameSessionInit', methods=['POST'])
@jwt_required
def postSession():
    return game.postSession()

@app.route('/sessionUpdate/<sessionId>', methods=['POST'])
@jwt_required
def putSession(sessionId):
    return game.putSession(sessionId)


@app.route('/getGameSessions/<sessionId>', methods=['GET'])
@jwt_required
def getSession(sessionId):
    return game.getSession(sessionId)


def createSession():
    return game.createSession()


def converToJson(sessionDict):
    return game.converToJson(sessionDict)

def updateSession(gameId,jsonData):
    return game.updateSession(gameId,jsonData)

def saveSession(jsonData):
    return game.saveSession(jsonData)

def findSession(gameId):
    return game.findSession(gameId)
