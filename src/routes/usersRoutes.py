from flask import request, json, jsonify
import os

from . import router, usersFileLocation

from ..utils.crypt import encrypt, decrypt
from ..utils.file import readFile, writeFile
from ..utils.authorization import generateToken

# registrasi
@router.route('/users', methods=['POST'])
def registration():
    isUsernameOrEmailUsed = False
    body = request.json
    
    response = {
        "error": False
    }
    
    usersData = {
        "total-user-registered": 0,
        "user-list": []
    }

    try:
        usersData = readFile(usersFileLocation)
    except:
        print("file ga ketemu/error")
    else:
        for data in usersData["user-list"]:
            if data["username"] == body["username"] or data["email"] == body["email"]:
                isUsernameOrEmailUsed = True
    
    if not isUsernameOrEmailUsed:
        usersData["total-user-registered"] += 1
        body["password"] = encrypt(body["password"])
        usersData["user-list"].append(body)        
        
        response["data"] = body
        writeFile(usersFileLocation, usersData)
        del body["password"]
    else:
        del body["password"]
        response["message"] = "username of email is used"

    return jsonify(response)

@router.route('/users/login', methods=['POST'])
def login():
    body = request.json
    
    usersData = readFile(usersFileLocation)

    isLogin = False
    # passwordMatched = False

    for user in usersData["user-list"]:        
        if user["username"] == body["username"]:
            # userFound = True
            if decrypt(user["password"]) == body["password"]: # password di database di-decrypt dulu
                isLogin = True
                body["token"] = generateToken(body["username"])
                break

    body["status"] = isLogin
    if isLogin:
        body["message"] = "Berhasil Login"
        del body["password"]
    else:
        del body["password"]
        body["message"] = "Username atau password tidak sesuai"

    return jsonify(body)