# -*- coding: utf-8 -*-
from flask import request,jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)

from mongoengine import *
from werkzeug.security import *


from app.models.models import GameUser
from app.models.forms import RegistrationForm

import uuid

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