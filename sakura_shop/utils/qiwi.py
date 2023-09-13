import requests

from utils.db_api.db_commands import select_settings


async def payment_history_last(my_login, api_access_token, rows_num, next_txn_id, next_txn_date):
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + api_access_token
    parameters = {'rows': rows_num, 'nextTxnId': next_txn_id, 'nextTxnDate': next_txn_date}
    h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + my_login + '/payments', params=parameters)
    return h.json()


async def balance():
    try:
        settings = await select_settings()
        s = requests.Session()
        s.headers['Accept'] = 'application/json'
        s.headers['authorization'] = 'Bearer ' + settings[1]
        b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + settings[0] + '/accounts')
        return b.json()["accounts"][0]["balance"]["amount"]
    except Exception as e:
        print(e)
        return "0"


async def payment_status(bill_id):
    settings = await select_settings()
    s = requests.Session()
    s.headers['authorization'] = 'Bearer ' + settings[3]
    s.headers['accept'] = "application/json"
    h = s.get(f'https://api.qiwi.com/partner/bill/v1/bills/{bill_id}')
    return h.json()


async def check_payment_p2p(bill_id):
    status = await payment_status(bill_id)
    if status.get("status"):
        if status.get("status").get("value") == "PAID":
            return True


async def check_payment(user_id, cost, balance_past):
    settings = await select_settings()
    history = await payment_history_last(settings[0], settings[1], "50", "", "")
    try:
        for i in range(10):
            if str(history['data'][i]['comment']) == str(user_id):
                if float(history["data"][i]["total"]["amount"]) >= float(cost):
                    if float(await balance()) > float(balance_past):
                        return True
    except IndexError:
        return False
