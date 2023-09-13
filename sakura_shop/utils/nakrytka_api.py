import requests

from data.config import API_KEY


def add_order(service_id, link, quantity):
    s = requests.Session()
    parameters = {
        'key': API_KEY,
        'action': 'add',
        'service': service_id,
        'link': link,
        'quantity': quantity
    }
    h = s.post('https://partner.soc-proof.su/api/v2', params=parameters)
    return h.json()


def order_status(order_id):
    s = requests.Session()
    parameters = {
        'key': API_KEY,
        'action': 'status',
        'order': order_id
    }
    h = s.post('https://partner.soc-proof.su/api/v2', params=parameters)
    return h.json()


def get_balance():
    try:
        s = requests.Session()
        parameters = {
            'key': API_KEY,
            'action': 'balance',
        }
        h = s.post('https://partner.soc-proof.su/api/v2', params=parameters)
        return h.json().get("balance")
    except Exception:
        return None


if __name__ == '__main__':
    print(get_balance())
