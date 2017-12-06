# -*- coding: utf-8 -*-
from flask import request,jsonify,json

from mongoengine import *

from db import connection

from app.models.models import GameSession

connection()


def postSession():
    createdSession = createSession()
    saveSession(createdSession)
    print("PRIMER POST")
    print (createdSession)
    return jsonify(createdSession)

def putSession(sessionId):
    sessionDict = request.form.to_dict()
    updatedSession = updateSession(sessionId,sessionDict)
    return updatedSession


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