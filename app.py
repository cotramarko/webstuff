from flask import Flask, jsonify
app = Flask(__name__)


st = {
    'wind': '4 m/s',
    'wind direction': 'NW',
    'Air density': 42.2,
    'Projectile circular radius [m]': 0.25,
}


@app.route('/')
def hello_world():
    return 'Hello, Nanette!'


@app.route('/state')
def state():
    return jsonify(st)
