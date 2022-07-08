import json

intentss = {
    "hello" : {
        "examples" : [
            "Привет",
            "Здраствуй",
            "здарова",
        ],
        "response" : [
            "Приветики",
            "шалом",
            "Здоровее видали"
        ]
    },
    "howareyuo" : {
        "exampels" :[
            "как дела"
        ],
        "response" : [
            "лучше всех"
        ]
    }
}

with open('Test.json', 'w') as f:
    json.dump(intentss, f)
