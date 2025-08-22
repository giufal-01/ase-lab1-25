import requests, time

from flask import Flask, request, make_response 
from requests.exceptions import ConnectionError, HTTPError
from werkzeug.exceptions import NotFound

ALLOWED_MATH_OPS = ['add', 'sub', 'mul', 'div', 'mod', 'random', 'reduce', 'crash']
ALLOWED_STR_OPS = ['lower', 'upper', 'concat', 'reduce', 'crash']

#CHANGE URLS TO MATCH THE NAMES AND PORTS OF THE SERVICES IN THE DOCKER-COMPOSE FILE
STRING_URL = 'http://string:5000'
CALC1_URL = 'http://calc1:5000'
CALC2_URL = 'http://calc2:5000'
DB_MANAGER_URL = 'http://db-manager:5000'


ids = {} #CAREFUL, THIS IS NOT FOR MULTIUSER AND MULTITHREADING, JUST FOR DEMO PURPOSES

app = Flask(__name__, instance_relative_config=True)

def create_app():
    return app

def reduce(request, url):
    op = request.args.get('op')
    lst = request.args.get('lst')
    return url + f'/reduce?op={op}&lst={lst}'

@app.route('/calc/<op>')
def math(op):
    if op not in ALLOWED_MATH_OPS:
        return make_response('Invalid operation\n', 400)
    try:
        C_URL=getCalcURL()
        if(op == 'crash'):
            URL = C_URL + f'/crash'
        elif op == 'reduce':
            URL = reduce(request, C_URL)
        else:
            a = request.args.get('a')
            b = request.args.get('b')
            if op == 'mod':
                b=1
            URL = C_URL + f'/{op}?a={a}&b={b}'
        x = requests.get(URL)
        x.raise_for_status()
        res = x.json()
        return res
    except (ConnectionError):
        try:
            C_URL=getCalcURL()
            if(op == 'crash'):
                URL = C_URL + f'/crash'
            elif op == 'reduce':
                URL = reduce(request, C_URL)
            else:
                URL = C_URL + f'/{op}?a={a}&b={b}'
            x = requests.get(URL)
            x.raise_for_status()
            res = x.json()
        except ConnectionError:
            return make_response('Calc service is down\n', 404)
        except HTTPError:
            return make_response(x.content, x.status_code)

        return res
    except HTTPError:
        return make_response(x.content, x.status_code)

def getCalcURL():
    id = ids.get('id')
    if id is None:
        id = 0
    id = id + 1
    ids.update({'id':id})
    if id %2 == 0:
        return CALC1_URL
    else:
        return CALC2_URL

@app.route('/str/<op>')
def string(op):
    if op not in ALLOWED_STR_OPS:
        return make_response('Invalid operation\n', 400)
    if op == 'reduce':
        URL = reduce(request, STRING_URL)
        json_response = string_request(URL)
        return json_response
    
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str) + "'"
    
    if op == 'lower':
        json_response = string_request(STRING_URL + f'/{op}?a={a}')
        time.sleep(1)
    elif op == 'crash':
        json_response = string_request(STRING_URL + f'/crash')
    elif op == 'upper':
        json_response = string_request(STRING_URL + f'/{op}?a={a}')
    else:
        json_response = string_request(STRING_URL + f'/{op}?a={a}&b={b}')
    return json_response

def string_request(URL_API):
    x = requests.get(URL_API)
    x.raise_for_status()
    return x.json()

@app.route('/getAll')
def getAll():
    try:
        x = requests.get(DB_MANAGER_URL + '/getAll', verify=False)
        x.raise_for_status()
        return x.json()
    except ConnectionError:
        return make_response('DB Manager service is down\n', 500)
    except HTTPError:
        return make_response(x.content, x.status_code)