import numpy as np

from flask import Flask, jsonify, request
from scenario2D import Scenario2D
from scenario3D import Scenario3D
from parameters import Parameters


class Problem1():
    # Point of impact for a 2D projectile with drag but no wind
    def __init__(self):
        self.params = Parameters(
            mass_lb=0.05,
            mass_ub=1,
            radius_lb=0.001,
            radius_ub=0.1,
            wind_vel_lb=0,
            wind_vel_ub=300,
            proj_vel_lb=100,
            proj_vel_ub=1000
        )
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, _ = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'projectile angle [deg]': proj_angle,
            'projectile velocity [m/s]': proj_vel,
            'delta T (used when simulating server-side)': 0.0001,
        }
        return self.scenario_state

    def simulate_scenario(self):
        scenario = Scenario2D(
            target=800,
            tolerance=5,
            dt=0.0001,
            mass=self.scenario_state["projectile mass [kg]"],
            r=self.scenario_state["projectile radius [m]"],
            wind=np.zeros(3)
        )
        _, _, xyz = scenario.shoot(
            self.scenario_state['projectile angle [deg]'],
            self.scenario_state["projectile velocity [m/s]"]
        )
        return xyz


class Problem2():
    # 2D. Wind in x direction, but with drag as well
    def __init__(self):
        self.params = Parameters(
            mass_lb=0.05,
            mass_ub=1,
            radius_lb=0.001,
            radius_ub=0.1,
            wind_vel_lb=0,
            wind_vel_ub=300,
            proj_vel_lb=100,
            proj_vel_ub=1000
        )
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, _ = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'wind (x) [m/s]': np.round(self.params.polar_to_carth(wind_vel, wind_angle)[0], 2),
            'projectile angle [deg]': proj_angle,
            'projectile velocity [m/s]': proj_vel,
            'delta T (used when simulating server-side)': 0.0001,
        }
        return self.scenario_state

    def simulate_scenario(self):
        scenario = Scenario2D(
            target=800,
            tolerance=5,
            dt=0.0001,
            mass=self.scenario_state["projectile mass [kg]"],
            r=self.scenario_state["projectile radius [m]"],
            wind=np.array([
                self.scenario_state['wind (x) [m/s]'],
                0,
                0
            ])
        )
        _, _, xyz = scenario.shoot(
            self.scenario_state['projectile angle [deg]'],
            self.scenario_state["projectile velocity [m/s]"]
        )
        return xyz


class Problem3():
    def __init__(self):
        self.params = Parameters(
            mass_lb=0.05,
            mass_ub=1,
            radius_lb=0.001,
            radius_ub=0.1,
            wind_vel_lb=0,
            wind_vel_ub=300,
            proj_vel_lb=100,
            proj_vel_ub=10000
        )
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, proj_angle_2 = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'wind velocity [m/s]': wind_vel,
            'wind direction [deg]': wind_angle,
            'projectile theta angle [deg]': proj_angle,
            'projectile phi angle [deg]': proj_angle_2,
            'projectile velocity [m/s]': proj_vel,
            'delta T (used when simulating server-side)': 0.0001,
        }
        return self.scenario_state

    def simulate_scenario(self):
        wind_vel = self.scenario_state['wind velocity [m/s]']
        wind_dir = self.scenario_state['wind direction [deg]']
        wind = self.params.polar_to_carth(wind_vel, wind_dir)

        phi_in_deg = self.scenario_state['projectile phi angle [deg]']
        theta_in_deg = self.scenario_state['projectile theta angle [deg]']

        scenario = Scenario3D(
            dt=0.0001,
            mass=self.scenario_state["projectile mass [kg]"],
            r=self.scenario_state["projectile radius [m]"],
            wind=wind
        )
        xyz = scenario.shoot(
            phi_in_deg,
            theta_in_deg,
            self.scenario_state["projectile velocity [m/s]"]
        )
        return xyz


app = Flask(__name__)
problem1 = Problem1()
problem2 = Problem2()
problem3 = Problem3()


@app.route('/scenario1', methods=['GET', 'POST'])
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
            resp['Access code'] = 444

        # Create new scenario_parameters
        problem1.setup_scenario()
        resp['The parameters of the scenario have changed!'] = problem1.scenario_state
        return jsonify(resp)


@app.route('/scenario2', methods=['GET', 'POST'])
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
            resp['Access code'] = 555
        else:
            resp['The parameters of the scenario have changed!'] = problem2.scenario_state

        # Create new scenario_parameters
        return jsonify(resp)


@app.route('/scenario3', methods=['GET', 'POST'])
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
            resp['Access code'] = 555
        else:
            resp['The parameters of the scenario have changed!'] = problem3.scenario_state

        # Create new scenario_parameters
        return jsonify(resp)


@app.route('/', methods=['GET'])
def base():
    return 'base'


if __name__ == "__main__":
    app.run(host="0.0.0.0")
