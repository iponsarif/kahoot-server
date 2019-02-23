from flask import Flask, request, json, jsonify
import requests
from random import randint
import os

app = Flask(__name__)

quizzesFilePath = './quizzes-file.json'
questionsFilePath = './question-file.json'
gamesFilePath = './games-file.json'
usersFilePath = './users-file.json'


# bikin kuis baru
@app.route('/quiz', methods=['POST'])
def createQuiz():
    body = request.json

    quizData = {
        "totalQuizAvailable": 0,
        "quizzes": []
    }    

    if os.path.exists(quizzesFilePath) and os.path.getsize(quizzesFilePath) > 0:
        quizzesFile = open(quizzesFilePath, 'r')
        quizData = json.load(quizzesFile)

    quizData["totalQuizAvailable"] += 1
    quizData["quizzes"].append(body)

    quizzesFile = open(quizzesFilePath, 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    return jsonify(quizData)

# bikin soal untuk kuis yang udah ada
@app.route('/question', methods=['POST'])
def createQuestion():
    body = request.json

    questionData = {
        "questions": []
    }

    if os.path.exists(questionsFilePath) and os.path.getsize(quizzesFilePath) > 0:
        questionFile = open(questionsFilePath, 'r')
        questionData = json.load(questionFile)

    questionFile = open(questionsFilePath, 'w')
    questionData["questions"].append(body)
    questionFile.write(str(json.dumps(questionData)))

    return jsonify(questionData)

# meminta data kuis dan soalnya
@app.route('/quizzes/<quizId>')
def getQuiz(quizId):
    # nyari quiznya
    quizzesFile = open(quizzesFilePath)
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        if quiz["quiz-id"] == int(quizId):
            quizData = quiz
            break

    # nyari soalnya
    questionsFile = open(questionsFilePath)
    questionData = json.load(questionsFile)

    for question in questionData["questions"]:
        if question["quiz-id"] == int(quizId):
            quizData["question-list"].append(question)

    return jsonify(quizData)

# minta data sebuah soal untuk kuis tertentu
@app.route('/quizzes/<quizId>/questions/<questionNumber>') # methods=["GET", "PUT", "DELETE"] PUT = edit
def getThatQuestion(quizId, questionNumber):
    quizData = getQuiz(int(quizId)).json

    for question in quizData["question-list"]:
        if question["question-number"] == int(questionNumber):
            return jsonify(question)

@app.route('/game', methods=['POST'])
def createGame():
    body = request.json

    # dapetin info quiz
    quizzesFile = open(quizzesFilePath)
    quizzesData = json.load(quizzesFile)

    for quiz in quizzesData["quizzes"]:
        quiz = json.loads(quiz)
    
        if quiz["quiz-id"] == int(body["quiz-id"]):
            gameInfo = quiz
    
    gameInfo["game-pin"] = randint(100000,999999)
    gameInfo["user-list"] = []
    gameInfo["leaderboard"] = []

    gamesData ={
        "game-list":[]
    }    

    # simpen data game nya
    if os.path.exists(gamesFilePath):
        gamesFile = open(gamesFilePath, 'r')
        gamesData = json.load(gamesFile)

    with open(gamesFilePath, 'w') as gamesFile:
        gamesData["game-list"].append(gameInfo)        
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(gameInfo)

@app.route('/game/join', methods=['POST'])
def joinGame():
    body = request.json

    # open game data information
    gamesFile = open(gamesFilePath)
    gamesData = json.load(gamesFile)

    position = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if body["username"] not in game["user-list"]: # kalau usernamenya udah ada, jangan di append
                game["user-list"].append(body["username"])
                game["leaderboard"].append({
                    "username": body["username"],
                    "score": 0
                })

                gameInfo = game
                position = i
                break
            # todo : error kalau usernya udah dipake

    with open(gamesFilePath, 'w') as gamesFile:
        gamesData["game-list"][position] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))

    return jsonify(request.json)

@app.route('/game/answer', methods=['POST'])
def submitAnswer():    
    isTrue = False
    body = request.json

    #buka file question
    questionsFile = open(questionsFilePath)
    questionData = json.load(questionsFile)

    for question in questionData["questions"]:
        question = json.loads(question)        

        if question["quiz-id"] == int(body["quiz-id"]) and question["question-number"] == int(body["question-number"]):
            if question["answer"] == body["answer"]:
                isTrue = True

    # todo: update skor/leaderboard
    gamesFile = open(gamesFilePath)
    gamesData = json.load(gamesFile)

    gamePosition = 0
    for i in range(len(gamesData["game-list"])):
        game = gamesData["game-list"][i]

        if game["game-pin"] == int(body["game-pin"]):
            if isTrue:                
                userPosition = 0
                for j in range(len(game["leaderboard"])):
                    userData = game["leaderboard"][j]
                    
                    if userData["username"] == body["username"]:                        
                        userData["score"] += 100
                        
                        userInfo = userData
                        userPosition = j
                        break
                
                game["leaderboard"][userPosition] = userInfo
                gameInfo = game
                gamePosition = i
                break

    with open(gamesFilePath, 'w') as gamesFile:
        gamesData["game-list"][gamePosition] = gameInfo
        gamesFile.write(str(json.dumps(gamesData)))
                
    return jsonify(request.json)


@app.route('/game/<gamePin>/leaderboard')
def getLeaderboard(gamePin):
    #body = request.json
    gamesFile = open(gamesFilePath)
    gamesData = json.load(gamesFile)

    for game in gamesData["game-list"]:
        if game["game-pin"] == int(gamePin): #body["game-pin"]
            leaderboard = game["leaderboard"]
            break
    
    # todo: sorting dari score terbesar ke terkecil (selection sort)        
    for i in range(len(leaderboard)):
        largest = leaderboard[i]["score"]
        largestPosition = leaderboard[i]
        for j in range(i,len(leaderboard)):
            if leaderboard[j]["score"] >= largest:
                largest = leaderboard[j]["score"]
                largestPosition = leaderboard[j]
                positionCounter = j

        leaderboard[i], leaderboard[positionCounter] = largestPosition, leaderboard[i] # swap posisi pertama setiap looping dengan posisi largest

    return jsonify(leaderboard)

@app.route('/registration', methods=['POST'])
def registration():
    body = request.json
    body["password"] = encrypt(body["password"]) # encrypt dulu password sebelum masuk database
    
    userData = []

    if os.path.exists(usersFilePath) and os.path.getsize(usersFilePath) > 0:
        usersFile = open(usersFilePath)
        userData = json.load(usersFile)     

    userData.append(body)

    usersFile = open(usersFilePath, 'w')
    usersFile.write(str(json.dumps(userData)))

    return jsonify(body)


@app.route('/login', methods=['POST'])
def login():
    body = request.json
    
    usersFile = open(usersFilePath)
    usersData = json.load(usersFile)

    userFound = False
    passwordMatched = False
    result = ""

    for user in usersData:        
        if user["username"] == body["username"]:
            userFound = True
            if decrypt(user["password"]) == body["password"]: # password di database di-decrypt dulu
                passwordMatched = True

    if userFound and passwordMatched:
        result = "Selamat datang, " + body["username"]        
    else:
        result = "Username atau password tidak sesuai"

    return result

# encrypt pake caesar chiper
shift = 2
def encrypt(password):
    alphanumeric = 'abcdefghijklmnopqrstuvwxyz0123456789'
    listAlphanumeric = list(alphanumeric)
    listPassword = list(password)    
    
    for i in range(len(listPassword)):
        charPosition = listAlphanumeric.index(listPassword[i])
        newPosition = (charPosition + shift) % len(listAlphanumeric)
        listPassword[i] = listAlphanumeric[newPosition]
    
    encryptedPassword = ''.join(listPassword)    
    return encryptedPassword

# decrypt pake caesar chiper
def decrypt(password):
    alphanumeric = 'abcdefghijklmnopqrstuvwxyz0123456789'
    listAlphanumeric = list(alphanumeric)
    listPassword = list(password)
    
    for i in range(len(listPassword)):
        charPosition = listAlphanumeric.index(listPassword[i])
        newPosition = (charPosition - shift) % len(listAlphanumeric)
        listPassword[i] = listAlphanumeric[newPosition]
    
    decryptedPassword = ''.join(listPassword)    
    return decryptedPassword

# delete quis sama edit informasi tentang kuisnya
@app.route('/quizzes/<quizId>', methods=["PUT", "DELETE"])
def editDeleteQuiz(quizId):
    if request.method == "DELETE":
        return deleteQuiz(quizId)
    elif request.method == "PUT":
        return editQuiz(quizId)

# fungsi hapus quiz berdasarkan quiz-id
def deleteQuiz(quizId):
    # nyari lalu hapus quiz
    quizzesFile = open(quizzesFilePath)
    quizData = json.load(quizzesFile)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == int(quizId): # nyari indeks quiz yg akan dihapus
            del quizData["quizzes"][i] # hapus quiz
            quizData["totalQuizAvailable"] -= 1 # kurangi total quiz
            message = "Berhasil menghapus quiz id " + quizId
            break
        else:
            message = "Gagal menghapus. Tidak ada quiz-id " + quizId

    quizzesFile = open(quizzesFilePath, 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    # nyari question sesuai quiz-id lalu hapus 
    questionsFile = open(questionsFilePath)
    questionData = json.load(questionsFile)

    message2 = ""
    # looping ini sisa 1 question dg quiz-id sama, belum bisa semua hapus dalam 1 for(karena out of range)
    for i in range(len(questionData["questions"])):
        if i < len(questionData["questions"]):
            question = questionData["questions"][i]

            if question["quiz-id"] == int(quizId):
                del questionData["questions"][i]
                message2 = " dan menghapus semua questionnya "

    # looping untuk hapus 1 question sisa
    for j in range(i-2,len(questionData["questions"])):
        question = questionData["questions"][j]

        if question["quiz-id"] == int(quizId):
            del questionData["questions"][j]
            message2 = " dan menghapus semua questionnya "
            break

    questionsFile = open(questionsFilePath, 'w')
    questionsFile.write(str(json.dumps(questionData)))

    return message + message2

# fungsi ubah quiz berdasarkan quiz-id
def editQuiz(quizId):
    body = request.json

    quizzesFile = open(quizzesFilePath)
    quizData = json.load(quizzesFile)

    for i in range(len(quizData["quizzes"])):
        quiz = quizData["quizzes"][i]

        if quiz["quiz-id"] == int(quizId): # nyari indeks quiz yg akan didelete
            quiz["quiz-id"] = body["quiz-id"] # hapus line ini kalau quiz-id ga bisa diubah
            quiz["quiz-name"] = body["quiz-name"]
            quiz["quiz-category"] = body["quiz-category"]
            
            quizData["quizzes"][i] = quiz
            message = "Berhasil mengubah quiz id " + quizId
            break
        else:
            message = "Gagal mengubah. Tidak ada quiz-id " + quizId

    quizzesFile = open(quizzesFilePath, 'w')
    quizzesFile.write(str(json.dumps(quizData)))

    return message

# def deleteQuestion(quizId, questionId):

if __name__ == "__main__":
    app.run(debug=True, port=14045)