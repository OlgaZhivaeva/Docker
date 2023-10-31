import requests

response = requests.post('http://127.0.0.1:5000/adv/',
                         json={'heading': 'Школа танцев',
                         'description': 'Набор девочек и мальчиков. Возраст 7-12 лет',
                         'creator': 'Школа бальных танцев Арт-студия'},
                         )
print(response.status_code)
print(response.json())

# response = requests.patch('http://127.0.0.1:5000/adv/1',
#                           json={'heading': 'Школа бальных танцев', })
# print(response.status_code)
# print(response.json())

# response = requests.delete(
#     "http://127.0.0.1:5000/adv/1",
# )
# print(response.status_code)
# print(response.json())
#
# response = requests.get(
#     "http://127.0.0.1:5000/adv/1",
# )
# print(response.status_code)
# print(response.json())
