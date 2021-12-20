import requests


def send_message_to_telegram(text, chat_id='-1001197468463', proxies=None):
    # Setting Token & Url of Telegram Bot :

    token = '1736566993:AAFye_1c9hBqxPnFzXuE_IGcpC0ZRltSyjk'  # define the access token
    url = 'https://api.telegram.org/bot{}/'.format(token)

    # Sending Log :
    try:
        cmd = 'sendMessage'
        message = {'text': text,
                   'chat_id': chat_id,
                   'parse_mode': 'html'}
        session = requests.session()

        session.proxies = proxies

        resp = session.post(url + cmd, data=message)
    except Exception as ex:
        print(ex)
