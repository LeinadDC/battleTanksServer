# -*- coding: utf-8 -*-
from config import config
from mongoengine import *

def connection():

    connect('test',host=config.MONGODB_HOST,port=config.MONGODB_PORT)