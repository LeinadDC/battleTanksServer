# -*- coding: utf-8 -*-
from app import db

class Player(db.EmbeddedDocument):
    playerId = db.StringField(required=False, max_length=36)
    tankLife = db.IntField(required=False)
