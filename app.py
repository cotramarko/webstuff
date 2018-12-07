import numpy as np

from flask import Flask, jsonify, request
from problems import Problem1, Problem2, Problem3

ANSWERS = {
    'RED': {'Keycode to the RED padlock is': 795},
    'BLUE': {'Keycode to the BLUE padlock is': 949},
    'BLACK': {'Keycode to the BLACK padlock is': 655}
}

PDF_LINKS = {
    'PROBLEM1': "",  # Contains all info up to problem 1
    'PROBLEM2': "",  # Problem 2 info
    'PROBLEM3': ""   # Problem 3 info
}


app = Flask(__name__)
problem1 = Problem1()
problem2 = Problem2()
problem3 = Problem3()


@app.route('/scenario1#656690c0a658fefea3a2033f437bffe8', methods=['GET', 'POST'])
def scenario1():
    if request.method == 'GET':
        # Get scenario_parameters
        return jsonify(problem1.scenario_state)
    if request.method == 'POST':
        content = request.json
        x_guess = content['point of impact (x)']

        xyz = problem1.simulate_scenario()
        x_true = xyz[0, -1]

        delta = np.abs(x_guess - x_true)
        valid_guess = bool(delta < 0.5)

        resp = {
            "Your point of impact": x_guess,
            "True point of impact": x_true,
            "delta": delta,
            "Was your answer within the accepted margin???": valid_guess
        }
        if valid_guess:
            d = ANSWERS['RED']
            resp['Next Problem'] = PDF_LINKS['PROBLEM2']
            for k in d.keys():
                resp[k] = d[k]

        # Create new scenario_parameters
        problem1.setup_scenario()
        resp['The parameters of the scenario have changed!'] = problem1.scenario_state
        return jsonify(resp)


@app.route('/scenario2#1884e8509182844979d1864092796467', methods=['GET', 'POST'])
def scenario2():
    if request.method == 'GET':
        # Get scenario_parameters
        return jsonify(problem2.scenario_state)
    if request.method == 'POST':
        content = request.json
        x_guess = content['point of impact (x)']

        xyz = problem2.simulate_scenario()
        x_true = xyz[0, -1]

        delta = np.abs(x_guess - x_true)
        valid_guess = bool(delta < 0.5)

        resp = {
            "Your point of impact": x_guess,
            "True point of impact": x_true,
            "delta": delta,
            "Was your answer within the accepted margin???": valid_guess
        }

        problem2.setup_scenario()

        if valid_guess:
            d = ANSWERS['BLUE']
            resp['Next Problem'] = PDF_LINKS['PROBLEM3']
            for k in d.keys():
                resp[k] = d[k]

        else:
            resp['The parameters of the scenario have changed!'] = problem2.scenario_state

        # Create new scenario_parameters
        return jsonify(resp)


@app.route('/scenario3#36376971dc4d9fb15505d68ac9b042a2', methods=['GET', 'POST'])
def scenario3():
    if request.method == 'GET':
        # Get scenario_parameters
        return jsonify(problem3.scenario_state)
    if request.method == 'POST':
        content = request.json
        poi_guess = content['point of impact (xyz)']

        xyz = problem3.simulate_scenario()
        poi_true = xyz[:, -1]
        poi_true[2] = 0  # Set z to zero

        distance = np.linalg.norm(poi_guess - poi_true, 2)
        valid_guess = bool(distance < 1)

        resp = {
            "Your point of impact (xyz)": poi_guess,
            "True point of impact (xyz)": poi_true.tolist(),
            "Distance (euqlidian) between your guess and the true point of impact": float(distance),
            "Was your answer within the accepted margin???": valid_guess
        }

        problem3.setup_scenario()

        if valid_guess:
            d = ANSWERS['BLACK']
            for k in d.keys():
                resp[k] = d[k]
        else:
            resp['The parameters of the scenario have changed!'] = problem3.scenario_state

        # Create new scenario_parameters
        return jsonify(resp)


@app.route('/', methods=['GET'])
def base():
    return PDF_LINKS['PROBLEM1']


if __name__ == "__main__":
    app.run(host="0.0.0.0")
