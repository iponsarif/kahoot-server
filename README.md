![Foto profile](https://avatars1.githubusercontent.com/u/25398885?s=96&v=4)
# Kahoot Server
A Python implementation of [Kahoot](https://kahoot.it/) using [Flask](http://flask.pocoo.org) as framework, [JSON](https://www.json.org/) as data format and [Insomnia](https://insomnia.rest/) as REST Client.

## Installing
### Python
Install with pip:
```
pip install python
```
### Flask
Install with pip:
```
pip install flask
```
### Insomnia
Install Insomnia REST Client from https://insomnia.rest/


## Usage

### Register
Open Insomnia, create a request POST to `/registration` with JSON body:

```json
{
	"user-id": 1,
	"username": "iponsarif",
	"password": "1dong",
	"email": "iponsarif@gmail.com"
}
```

### Login
Open Insomnia, create a request POST to `/login` with JSON body:
```json
{
	"username": "iponsarif",
	"password": "1dong"
}
```

### Create Quiz
Open Insomnia, create a request POST to `/quiz` with JSON body:
```json
{
	"quiz-id": 123,
	"quiz-name": "Name of the quiz",
	"quiz-category": "Category of the quiz",
	"question-list": []
}
```

### Get Quiz
Open Insomnia, create a request Get from `/quizzes/<quiz-id>`.

### Update Quiz
Open Insomnia, create a request PUT to `/quizzes/<quiz-id>` with JSON body:
```json
{
	"quiz-id": 125,
	"quiz-category": "Category of the quiz updated",
	"quiz-name": "Name of the quiz updated"
}
```

### Create Game
Open Insomnia, create a request POST to `/game` with JSON body:
```json
{
    "quiz-id": 123
}
```

### Join Game
Open Insomnia, create a request POST to `/game/join` with JSON body:
```json
{
	"game-pin": 927102,
	"username": "Danurannisa"
}
```

## Feature
### Basic
- [x] Register
- [x] Login
- [x] Create quiz
- [x] Get quiz
- [x] Update quiz
- [x] Delete quiz
- [x] Create question
- [x] Get question
- [x] Update question
- [x] Delete question
- [x] Create game
- [x] Join game
- [x] Answer the question
- [x] Get leaderboard

### More
- [ ] Not yet
- [x] README

## 6. Donasi
No. Rek BRI: