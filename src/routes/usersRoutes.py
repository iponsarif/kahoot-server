from flask import request, json, jsonify
import os

from . import router, usersFileLocation

from ..utils.crypt import encrypt, decrypt
from ..utils.file import readFile, writeFile
from ..utils.authorization import generateToken

# registrasi
@router.route('/users', methods=['POST'])
def registration():
    print(os.getenv("API_KEY"))
    body = request.json
    body["password"] = encrypt(body["password"]) # encrypt dulu password sebelum masuk database
    
    userData = []

    if os.path.exists(usersFileLocation) and os.path.getsize(usersFileLocation) > 0:
        userData = readFile(usersFileLocation)

    userData.append(body)

    writeFile(usersFileLocation, userData)

    return jsonify(userData)

@router.route('/users/login', methods=['POST'])
def login():
    body = request.json
    
    usersData = readFile(usersFileLocation)

    isLogin = False
    # passwordMatched = False

    for user in usersData:        
        if user["username"] == body["username"]:
            # userFound = True
            if decrypt(user["password"]) == body["password"]: # password di database di-decrypt dulu
                isLogin = True
                body["token"] = generateToken(body["username"])
                break

    body["status"] = isLogin
    if isLogin:
        body["message"] = "Berhasil Login"
    else:
        body["message"] = "Username atau password tidak sesuai"

    return jsonify(body)