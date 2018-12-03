import numpy as np


def rounded_uni(lb, ub, precision=2):
    r = np.round(
        np.random.uniform(lb, ub),
        2
    )
    return r


class Parameters():
    def __init__(self,
                 mass_lb,
                 mass_ub,
                 radius_lb,
                 radius_ub,
                 wind_vel_lb,
                 wind_vel_ub,
                 proj_vel_lb,
                 proj_vel_ub):
        self.mass_lb = mass_lb
        self.mass_ub = mass_ub

        self.radius_lb = radius_lb
        self.radius_ub = radius_ub

        self.wind_vel_lb = wind_vel_lb
        self.wind_vel_ub = wind_vel_ub

        self.proj_vel_lb = proj_vel_lb
        self.proj_vel_ub = proj_vel_ub

    def new(self):
        mass = rounded_uni(self.mass_lb, self.mass_ub)
        radius = rounded_uni(self.radius_lb, self.radius_ub)

        wind_vel = rounded_uni(self.wind_vel_lb, self.wind_vel_ub)
        wind_angle = rounded_uni(0, 360)

        proj_vel = rounded_uni(self.proj_vel_lb, self.proj_vel_ub)
        proj_angle = rounded_uni(15, 175)

        proj_angle_2 = rounded_uni(15, 175)

        return mass, radius, wind_vel, wind_angle, proj_vel, proj_angle, proj_angle_2

    @staticmethod
    def polar_to_carth(mag, angle):
        rads = np.deg2rad(angle)
        x = mag * np.cos(rads)
        y = mag * np.sin(rads)
        z = 0
        return x, y, z
