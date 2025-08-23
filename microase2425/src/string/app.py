from flask import Flask, request, make_response, jsonify
import time, os, threading, requests

app = Flask(__name__)


@app.route('/concat')
def concat():
    a = request.args.get('a', type=str)
    b = request.args.get('b', type=str)
    if a is not None and b is not None:
        res = a+b
        save_last("concat",(a,b),res)
        return make_response(jsonify(s=res), 200)
    else:
        return make_response('Invalid input\n', 400)

@app.route('/upper')
def upper():
    a = request.args.get('a', type=str)
    if a is None:
        return make_response('Invalid input\n', 400)
    res = a.upper()
    save_last("upper","("+a+")",res)
    return make_response(jsonify(s=res), 200)

@app.route('/lower')
def lower():
    a = request.args.get('a', type=str)
    if a is None:
        return make_response('Invalid input\n', 400)
    res = str(a).lower()
    save_last("lower","("+a+")",res)
    return make_response(jsonify(s=res), 200)

@app.route('/reduce')
def reduce():
    op = request.args.get('op', type=str)
    lst = request.args.get('lst', type=str)
    if op and lst:
        lst = eval(lst)
        if op == 'concat':
            res = ""
            for i in lst:
                res += i
            save_last("reduce",(op,lst),res)
            return  make_response(jsonify(s=res), 200)
    return make_response('Invalid input\n', 400)

@app.route('/crash')
def crash():
    def close():
        time.sleep(1)
        os._exit(0)
    thread = threading.Thread(target=close)
    thread.start()
    ret = str(request.host) + " crashed"
    return make_response(jsonify(s=ret), 200)

mock_save_last = None
def save_last(op,args,res):
    if mock_save_last:
        mock_save_last(op,args,res)
    else:
        timestamp = time.time()
        payload = {'timestamp': timestamp, 'op': op, 'args': args, 'res': res}
        requests.post('http://db-manager:5000/notify', json=payload)

if __name__ == '__main__':
    app.run(debug=True)