import json

data = {
    1: {
    'id': 1,
    'name': 'Денчик',
    'grade': 11, 
    'tariff': 'pro',
    },
    2: {
    'id': 2,
    'name': 'Артур',
    'grade': 7, 
    'tariff': 'mini',
    },
}

with open('students.json', 'w') as f:
    json.dump(data, f, indent=4)