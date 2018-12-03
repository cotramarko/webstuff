import numpy as np
# import matplotlib
# matplotlib.use('TkAgg')

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


def set_axes_equal(ax):
    '''Make axes of 3D plot have equal scale so that spheres appear as spheres,
    cubes as cubes, etc..  This is one possible solution to Matplotlib's
    ax.set_aspect('equal') and ax.axis('equal') not working for 3D.

    Input
      ax: a matplotlib axis, e.g., as output from plt.gca().
    '''

    x_limits = ax.get_xlim3d()
    y_limits = ax.get_ylim3d()
    z_limits = ax.get_zlim3d()

    x_range = abs(x_limits[1] - x_limits[0])
    x_middle = np.mean(x_limits)
    y_range = abs(y_limits[1] - y_limits[0])
    y_middle = np.mean(y_limits)
    z_range = abs(z_limits[1] - z_limits[0])
    z_middle = np.mean(z_limits)

    # The plot bounding box is a sphere in the sense of the infinity
    # norm, hence I call half the max range the plot radius.
    plot_radius = 0.5*max([x_range, y_range, z_range])

    ax.set_xlim3d([x_middle - plot_radius, x_middle + plot_radius])
    ax.set_ylim3d([y_middle - plot_radius, y_middle + plot_radius])

    d = z_middle - plot_radius
    ax.set_zlim3d([z_middle - plot_radius - d, z_middle + plot_radius - d])


class Projectile():
    def __init__(self, init_pos, init_vel, init_acc, mass, rho, A, drag_coeff, g=9.82):
        # init_pos np.array with shape (3, ), ordered by x, y, z
        # init_vel np.array with shape (3, ), ordered by x, y, z

        (self.xk, self.yk, self.zk) = init_pos
        (self.xk_dot, self.yk_dot, self.zk_dot) = init_vel
        (self.xk_dotdot, self.yk_dotdot, self.zk_dotdot) = init_acc

        self.mass = mass
        self.g = g

        self.rho = rho  # mass density of fluid
        self.A = A  # reference area
        self.drag_coeff = drag_coeff  # drag coefficient

    def _drag_acc(self, v_wind, v):
        if self.drag_coeff is None:
            drag_acc = 0
        else:
            scaling = (self.rho * self.drag_coeff * self.A) / (2 * self.mass)
            dv = v_wind - v
            drag_acc = scaling * np.square(dv) * np.sign(dv)
        return drag_acc
#        return 0

    def simulate_step(self, dt, wind=None):
        # wind np.array with shape (3, ), ordered by x, y, z
        if wind is not None:
            (x_wind, y_wind, z_wind) = wind
        else:
            (x_wind, y_wind, z_wind) = (None, None, None)

        self.xk_dotdot = self._drag_acc(x_wind, self.xk_dot)
        self.xk_dot = self.xk_dot + dt * self.xk_dotdot
        self.xk = self.xk + dt * self.xk_dot

        self.yk_dotdot = self._drag_acc(y_wind, self.yk_dot)
        self.yk_dot = self.yk_dot + dt * self.yk_dotdot
        self.yk = self.yk + dt * self.yk_dot

        self.zk_dotdot = self._drag_acc(z_wind, self.zk_dot) - self.g
        self.zk_dot = self.zk_dot + dt * self.zk_dotdot
        self.zk = self.zk + dt * self.zk_dot

    def get_current_pos(self):
        p = [self.xk, self.yk, self.zk]
        return np.array(p)

    def get_current_vel(self):
        v = [self.xk_dot, self.yk_dot, self.zk_dot]
        return np.array(v)

    def get_current_acc(self):
        a = [self.xk_dotdot, self.yk_dotdot, self.zk_dotdot]
        return np.array(a)


def ms_to_kmh(ms):
    kmh = (ms / 1000) * 3600
    return kmh


def set_proper_ticks(old_ticks):
    number_of_ticks = len(old_ticks)
    ticks = ['', ] * number_of_ticks

    ticks[0] = str(old_ticks[1])
    ticks[-1] = str(old_ticks[-1])
    return []


"""
if __name__ == '__main__':
    init_pos = np.array([0, 0, 0]).astype(np.int32)
    init_vel = np.array(
        [630,
         0,
         460])
    init_acc = np.array([0, 0, 0])
    mass = 0.080  # 80 gram bullet
    rho = 1.2
    r = 0.0045  # 9mm bullet
    A = np.pi * np.square(r)
    drag_coeff = 0.47

    print(f'x velocity {ms_to_kmh(init_vel[0])} km/h')
    print(f'y velocity {ms_to_kmh(init_vel[1])} km/h')
    print(f'z velocity {ms_to_kmh(init_vel[2])} km/h')

    projectile = Projectile(init_pos, init_vel, init_acc, mass, rho, A, drag_coeff)

    dt = 0.001
    wind = np.array([0, -100, 0])

    t = [0]
    x = [init_pos[0]]
    y = [init_pos[1]]
    z = [init_pos[2]]

    z_acc = [0]
    timer = 0
    while True:
        projectile.simulate_step(dt, wind)
        pos = projectile.get_current_pos()
        vel = projectile.get_current_vel()
        acc = projectile.get_current_acc()
        timer += dt
        print(timer, end='\t|\t')

        t.append(timer)

        z_acc.append(acc[2])
        x.append(pos[0])
        y.append(pos[1])
        z.append(pos[2])
        print(z[-1])
        if z[-1] < 0.0001:
            break

    print(timer)
    fig = plt.figure(constrained_layout=True, figsize=(12, 8))
    gs = fig.add_gridspec(3, 3)
    ax = fig.add_subplot(gs[0:2, :], projection='3d')
    ax.set_aspect('equal')

    ax.plot(x, y, z, ':')

    init = map(lambda x: [x], init_pos)
    ax.plot(*init, 'ro')

    poi = map(lambda x: [x], [x[-1], y[-1], z[-1]])
    ax.plot(*poi, 'k.')

    target = map(lambda x: [x], [10042, 5073, 0])
    ax.plot(*target, 'g.')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    xticks = ax.get_xticks()
    ax.set_xticklabels(set_proper_ticks(xticks))

    yticks = ax.get_yticks()
    ax.set_yticklabels(set_proper_ticks(yticks))

    zticks = ax.get_zticks()
    ax.set_zticklabels(set_proper_ticks(zticks))

    ax.set_title(
        f'point of impact:\n{int(x[-1]), int(y[-1])}', horizontalalignment='center')
    set_axes_equal(ax)

    ax = fig.add_subplot(gs[2, 0])
    ax.plot(x, y, '.')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.axis('equal')

    ax = fig.add_subplot(gs[2, 1])
    ax.plot(x, z, '.')
    ax.set_xlabel('x')
    ax.set_ylabel('z')
    ax.axis('equal')

    ax = fig.add_subplot(gs[2, 2])
    ax.plot(y, z, '.')
    ax.set_xlabel('y')
    ax.set_ylabel('z')
    ax.axis('equal')

    plt.figure()
    plt.plot(t, z_acc, 'r--')
    plt.plot(t, -9.82 * np.ones_like(t), 'g-')
    plt.title(f'max z_acc: {np.max(z_acc)}')
    plt.xlabel('t')
    plt.ylabel('z_acc')
    plt.show()
"""
