#escalar a quantidade de container desejado
#executar esse script


import requests
import random
import uuid


url = 'http://localhost:8080/migration'
payload_quantity = 1000
payload_test = {
        "person_type": "PF",
        "current_email_address": "teste@globo.com.br",
        "alias_email_address": "",
        "password": "Passwordtotest@2021",
        "name": "globo teste",
        "company_name": "globo",
        "cpf": "03374110509",
        "cnpj": "00002375149902",
        "rg": "",
        "phones": [
            {
                "number": "71992035822"
            }
        ],
        "emails": [
            {
                "address": "teste@globo.com",
                "main": True,
                "confirmed": True
            }
        ],
        "address": {
            "city": "Blumenau",
            "state": "SC",
            "postal_code": "89025969",
            "country": "BR",
            "number": "23",
            "street": "rua dois"
        }
    }

payload_list = []
for i in range(0, payload_quantity):
    payload = {}
    id_globo = f'{str(uuid.uuid4())}/{random.randint(0,9999999)}'
    payload.update({'id_globo': id_globo})
    payload_list.append(payload)

migration_list = []
for item in payload_list:
    payload = {}
    payload.update(payload_test)
    payload.update({'id_globo': item['id_globo']})
    migration_list.append(payload)


response = requests.post(url, json=migration_list)
response.raise_for_status()


    




