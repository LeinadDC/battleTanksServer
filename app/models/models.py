# -*- coding: utf-8 -*-
from app import db
from flask_login import UserMixin

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