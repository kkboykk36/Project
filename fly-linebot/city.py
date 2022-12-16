import json
with open('1階段.json','r',encoding='utf8') as file:
    first_message = json.load(file)
    print(first_message)