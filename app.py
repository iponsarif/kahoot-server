from flask import Flask, request
import jwt
from src.routes import router

app = Flask(__name__)
app.register_blueprint(router)

@app.route('/encode')
def jwtEncode():
    encoded = jwt.encode({"data": "makers"}, "kucing-merah", algorithm="HS256")
    return encoded

a = "bisa ga ini coy di debug"
print(a)
@app.route('/decode', methods=["POST"])
def jwtDecode():
    decoded = jwt.decode(request.json["token"], "kucing-merah", algorithms=["HS256"])
    return str(decoded)

# @app.errorhandler(403)
# def errorhandler403(e):
#     message = {
#         "status-code"
#     }
#     return "error 403"