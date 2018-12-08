import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

from projectile import Projectile
#from draw import Draw


class Scenario2D():
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

    def shoot(self, angle_in_deg, speed):
        self.angle_in_deg = angle_in_deg

        rads = np.deg2rad(angle_in_deg)
        x, z = np.cos(rads) * speed, np.sin(rads) * speed
        init_vel = np.array([x, 0, z])

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
    mass = 0.95
    r = 0.17
    dt = 0.0001

    angle = 82.33
    vel = 176.43

    wind = np.array([-253.33, 0, 0])

    sc = Scenario2D(mass=mass, r=r, dt=dt, wind=wind)

    xyz = sc.shoot(angle, vel)

    poi = xyz[:, -1]
    print(poi[0])
    print(poi[1])
