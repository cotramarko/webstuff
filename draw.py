"""
import numpy as np
import matplotlib
# matplotlib.use('TkAgg')

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from projectile import Projectile


class Draw():
    def __init__(self, scenarios):
        self.scenarios = scenarios

    def __call__(self):
        fig = plt.figure(constrained_layout=True, figsize=(12, 8))
        gs = fig.add_gridspec(2, 4)
        # Launcher view
        ax = fig.add_subplot(gs[0, 0:2])
        for angle_in_deg in map(lambda x: x.angle_in_deg, self.scenarios):
            rads = np.deg2rad(angle_in_deg)
            x = np.cos(rads)
            z = np.sin(rads)

            xd = 0.5 * np.cos(np.linspace(0, rads))
            yd = 0.5 * np.sin(np.linspace(0, rads))
            ax.plot(xd, yd, ':k')

            ax.plot([0, x], [0, z], '-o')

        ax.plot([0, 1], [0, 0], color=(0.7,) * 4)
        ax.plot([0, 0], [0, 1], color=(0.7,) * 4)

        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('z')

        # Impact view
        ax = fig.add_subplot(gs[0, 2:4])
        for xyz, target, tolerance in map(lambda x: (x.xyz, x.target, x.tolerance), self.scenarios):

            ax.plot(xyz[0, -1], 0, 'bx', zorder=5)
            ax.plot(target, 0, 'go', zorder=10)
            ax.plot([target - tolerance, target + tolerance], [0, 0], 'g-|', zorder=15)

        xlim_min, xlim_max = ax.get_xlim()
        ax.plot([xlim_min, xlim_max], [0, 0], color=(0.7,) * 4, zorder=0)
        ax.set_xlim([xlim_min, xlim_max])

        ax.set_xlabel('x')
        ax.set_ylabel('z')

        # Trajectory view
        ax = fig.add_subplot(gs[1, :])
        for xyz, target, tolerance in map(lambda x: (x.xyz, x.target, x.tolerance), self.scenarios):
            ax.plot(xyz[0, :], xyz[2, :], ':k')

        ax.set_aspect('equal')
        ax.set_xlabel('x')
        ax.set_ylabel('z')
        plt.show()
"""
