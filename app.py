from flask import Flask, request, jsonify
import jwt
from src.routes import router

app = Flask(__name__)
app.register_blueprint(router)

@app.route('/penjumlahan/<int:firstNumber>/<int:secondNumber>')
def penjumlahan(firstNumber, secondNumber):
    return jsonify({
        "hasil_jumlah": firstNumber+secondNumber,
        "tv_one": "memang beda"
    })
