import os
import threading
import time
from flask import Flask, request, make_response, jsonify
from flask_restx import Api, Resource

app = Flask(__name__)
api = Api(app, version='1.0', title='Math Operations API',
          description='A simple API for basic math operations')

# @app.route('/add')
# def add():
#     a = request.args.get('a', type=float)
#     b = request.args.get('b', type=float)
#     if a and b:
#         return make_response(jsonify(s=a+b), 200) #HTTP 200 OK
#     else:
#         return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST
    
@api.route('/add')
class Add(Resource):
    def get(self):
        a = request.args.get('a', type=float)
        b = request.args.get('b', type=float)
        if a is not None and b is not None:
            return make_response(jsonify(s=a+b), 200) #HTTP 200 OK
        else:
            return make_response('Invalid input\n', 400)

#Endpoint /sub for subtraction which takes a and b as query parameters.
@app.route('/sub')
def sub():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        return make_response(jsonify(s=a-b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST


#Endpoint /mul for multiplication which takes a and b as query parameters.

@app.route('/mul')
def mul():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        return make_response(jsonify(s=a*b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /div for division which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.

@app.route('/div')
def div():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero is not allowed\n', 400) #HTTP 400 BAD REQUEST
        return make_response(jsonify(s=a/b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST

#Endpoint /mod for modulo which takes a and b as query parameters. Returns HTTP 400 BAD REQUEST also for division by zero.
@app.route('/mod')
def mod():
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a and b:
        if b == 0:
            return make_response('Division by zero is not allowed\n', 400) #HTTP 400 BAD REQUEST
        return make_response(jsonify(s=a%b), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST  

#Endpoint /random which takes a and b as query parameters and returns a random number between a and b included. Returns HTTP 400 BAD REQUEST if a is greater than b.

@app.route('/random')
def random_number():
    import random
    a = request.args.get('a', type=float)
    b = request.args.get('b', type=float)
    if a is not None and b is not None:
        if a > b:
            return make_response('Invalid range: a should be less than or equal to b\n', 400) #HTTP 400 BAD REQUEST
        return make_response(jsonify(s=random.uniform(a, b)), 200) #HTTP 200 OK
    else:
        return make_response('Invalid input\n', 400) #HTTP 400 BAD REQUEST


# Applicazioni delle rest API per operazioni matematiche di base.

@app.route('/concat')
def concat():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a and b:
        res = a+b
        save_last("concat",(a,b),res)
        return make_response(jsonify(s=res), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/upper')
def upper():
    a = request.args.get('a', 0, type=str)
    res = a.upper()
    save_last("upper","("+a+")",res)
    return make_response(jsonify(s=res), 200)

@app.route('/lower')
def lower():
    a = request.args.get('a', 0, type=str)
    res = a.lower()
    save_last("lower","("+a+")",res)
    return make_response(jsonify(s=res), 200)


@app.route('/reduce')
def reduce():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=str)
    if op and lst:
        lst = eval(lst)
        if op == 'add':
            res = sum(lst)
            response =  make_response(jsonify(s=res), 200)
        elif op == 'sub':
            res = lst[0] - sum(lst[1:])
            response = make_response(jsonify(s=res), 200)
        elif op == 'mul':
            res = 1
            for i in lst:
                res *= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'div':
            res = lst[0]
            for i in lst[1:]:
                if i == 0:
                    return make_response('Division by zero\n', 400)
                res /= i
            response = make_response(jsonify(s=res), 200)
        elif op == 'concat':
            res = ''
            for i in lst:
                res += i
            response = make_response(jsonify(s=res), 200)
        else:
            return make_response(f'Invalid operator: {op}', 400)
        save_last("reduce",(op,lst),res)
        return response
    else:
        return make_response('Invalid operator\n', 400)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

@app.route('/last')
def last():
    try:
        with open('last.txt', 'r') as f:
            return make_response(jsonify(s=f.read()), 200)
    except FileNotFoundError:
        return make_response('No operations yet\n', 404)


def save_last(op,args,res):
    with open('last.txt', 'w') as f:
            f.write(f'{op}{args}={res}')


if __name__ == '__main__':
    app.run(debug=True)