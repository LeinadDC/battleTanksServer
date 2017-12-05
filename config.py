# -*- coding: utf-8 -*-
class config:
    DEBUG = True

    # This is a secret key that is used by Flask to sign cookies.
    SECRET_KEY = 'l3in49'  # Change for production
    JWT_SECRET_KEY = 'jwtSECRET'

    # MongoDB configuration parameters
    MONGODB_HOST = '192.168.98.131'
    MONGODB_PORT = 27017
