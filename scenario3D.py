import numpy as np
#import matplotlib

from projectile import Projectile


class Scenario3D():
    def __init__(self, dt=0.001, mass=0.080, rho=1.2, r=0.045, drag_coeff=0.47, wind=None):
        self.dt = dt

        self.mass = mass
        self.rho = rho
        self.A = np.pi * np.square(r)
        self.drag_coeff = drag_coeff
        self.wind = wind

        self.init_pos = np.zeros(3)
        self.init_acc = np.zeros(3)

        self.xyz = None
        self.distance = None

    def _simulate_trajectory(self):
        t = [0]
        x, y, z = map(lambda i: [i], self.init_pos.tolist())
        timer = 0

        while True:
            self.projectile.simulate_step(self.dt, wind=self.wind)
            pos = self.projectile.get_current_pos()
            timer += self.dt

            t.append(timer)

            x.append(pos[0])
            y.append(pos[1])
            z.append(pos[2])
            if z[-1] < 0.0001:
                break

        xyz = np.array([x, y, z])
        return xyz

    def shoot(self, phi_in_deg, theta_in_deg, speed):
        self.phi_in_deg = phi_in_deg
        self.theta_in_deg = theta_in_deg

        phi_rads = np.deg2rad(phi_in_deg)
        theta_rads = np.deg2rad(theta_in_deg)

        x = np.cos(theta_rads) * np.cos(phi_rads) * speed
        y = np.cos(theta_rads) * np.sin(phi_rads) * speed
        z = np.sin(theta_rads) * speed

        init_vel = np.array([x, y, z])

        if self.wind is not None:
            self.projectile = Projectile(
                init_pos=self.init_pos,
                init_vel=init_vel,
                init_acc=self.init_acc,
                mass=self.mass,
                rho=self.rho,
                A=self.A,
                drag_coeff=self.drag_coeff
            )
        else:
            self.projectile = Projectile(
                init_pos=self.init_pos,
                init_vel=init_vel,
                init_acc=self.init_acc,
                mass=None,
                rho=None,
                A=None,
                drag_coeff=None
            )

        self.xyz = self._simulate_trajectory()

        return self.xyz


if __name__ == '__main__':
    mass = 0.32
    r = 0.01
    dt = 0.0001

    phi_in_deg = 89.73
    theta_in_deg = 119.35
    proj_vel = 9098.86

    wind_speed = 138.31
    wind_angle_deg = 335.28

    wind_x = np.cos(np.deg2rad(wind_angle_deg)) * wind_speed
    wind_y = np.sin(np.deg2rad(wind_angle_deg)) * wind_speed
    wind_z = 0

    wind = np.array([wind_x, wind_y, wind_z])

    sc = Scenario3D(mass=mass, r=r, dt=dt, wind=wind)

    xyz = sc.shoot(phi_in_deg, theta_in_deg, proj_vel)

    poi = xyz[:, -1]
    print(poi[0])
    print(poi[1])
