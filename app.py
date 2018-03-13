from flask import Flask
from flask import request
from flask import jsonify
from flask_sslify import SSLify
import requests

app = Flask(__name__)
sslify = SSLify(app)

token = '' # your bot's token
URL = 'https://api.telegram.org/bot' + token + '/'
wiki_api = 'https://ru.wikipedia.org/w/api.php?action=opensearch&search='
errmessage = 'To take a correct answer, you should input a single word you interested in!'

global last_update_id
last_update_id = 0

def send_message(chat_id, text = ''):
    url = URL +'sendmessage?chat_id={}&text={}'.format(chat_id, text)
    requests.post(url)

@app.route('/', methods = ['POST', 'GET'])
def index():
    if request.method == 'POST':
        answer = request.get_json()
        if answer != None:
            try:
                message = answer['message']['text']
            except KeyError:
                message = 'KeyError'
            chat_id = answer['message']['chat']['id']
            if message == '/start':
                text = 'Hello, I\'m WikiRequestsBot!\nI can help you find information about some words. Just type a word and send it to me, and I\'ll do my job!\nMy creator is @hatingman'
            elif message == '/help':
                text = 'This bot take requests from Wikipedia!'
            elif message == 'KeyError':
                text = errmessage
            else:
                url = wiki_api + message
                try:
                    dic = requests.get(url).json()
                except:
                    text = errmessage
                try:
                    text = dic[2][0] + '\n' + dic[3][0]
                except IndexError:
                    text = errmessage
            send_message(chat_id, text)
        return jsonify(answer)
    return '<h1>^-^</h1>'

if __name__ == '__main__':
    app.run()
