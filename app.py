from flask import Flask, request, json, jsonify
import requests
from random import randint
import os

from src.routes import router

app = Flask(__name__)
app.register_blueprint(router)            

if __name__ == "__main__":
    app.run(debug=True, port=14045)