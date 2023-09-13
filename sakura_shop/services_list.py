import requests

from data.config import API_KEY


def services():
    s = requests.Session()
    parameters = {
        'key': API_KEY,
        'action': 'services'
    }
    h = s.post('https://partner.soc-proof.su/api/v2', params=parameters)
    return h.json()


service = services()
print(len(service) % 4)
