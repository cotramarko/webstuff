import numpy as np

from scenario2D import Scenario2D
from scenario3D import Scenario3D
from parameters import Parameters

PARAMS = Parameters(
    mass_lb=0.05,
    mass_ub=1,
    radius_lb=0.001,
    radius_ub=0.1,
    wind_vel_lb=0,
    wind_vel_ub=300,
    proj_vel_lb=100,
    proj_vel_ub=1000
)

DELTA_T = 0.0001


class Problem1():
    # Point of impact for a 2D projectile with drag but no wind
    def __init__(self):
        self.params = PARAMS
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, _ = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'projectile angle [deg]': proj_angle,
            'projectile speed [m/s]': proj_vel,
            'delta T (used when simulating server-side)': DELTA_T,
        }
        return self.scenario_state

    def simulate_scenario(self):
        scenario = Scenario2D(
            dt=0.0001,
            mass=self.scenario_state["projectile mass [kg]"],
            r=self.scenario_state["projectile radius [m]"],
            wind=np.zeros(3)
        )
        xyz = scenario.shoot(
            self.scenario_state['projectile angle [deg]'],
            self.scenario_state["projectile speed [m/s]"]
        )
        return xyz


class Problem2():
    # 2D. Wind in x direction, but with drag as well
    def __init__(self):
        self.params = PARAMS
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, _ = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'wind (x) [m/s]': np.round(self.params.polar_to_carth(wind_vel, wind_angle)[0], 2),
            'projectile angle [deg]': proj_angle,
            'projectile speed [m/s]': proj_vel,
            'delta T (used when simulating server-side)': DELTA_T,
        }
        return self.scenario_state

    def simulate_scenario(self):
        scenario = Scenario2D(
            dt=DELTA_T,
            mass=self.scenario_state["projectile mass [kg]"],
            r=self.scenario_state["projectile radius [m]"],
            wind=np.array([
                self.scenario_state['wind (x) [m/s]'],
                0,
                0
            ])
        )
        xyz = scenario.shoot(
            self.scenario_state['projectile angle [deg]'],
            self.scenario_state["projectile speed [m/s]"]
        )
        return xyz


class Problem3():
    def __init__(self):
        self.params = PARAMS
        self.scenario_state = self.setup_scenario()

    def setup_scenario(self):
        mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, proj_angle_2 = self.params.new()
        self.scenario_state = {
            'projectile mass [kg]': mass,
            'projectile radius [m]': radius,
            'wind speed [m/s]': wind_vel,
            'wind direction [deg]': wind_angle,
            'projectile theta angle [deg]': proj_angle,
            'projectile phi angle [deg]': proj_angle_2,
            'projectile speed [m/s]': proj_vel,
            'delta T (used when simulating server-side)': DELTA_T,
        }
        return self.scenario_state

    def simulate_scenario(self):
        wind_vel = self.scenario_state['wind speed [m/s]']
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
            self.scenario_state["projectile speed [m/s]"]
        )
        return xyz
