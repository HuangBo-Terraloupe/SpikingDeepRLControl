__auther__ = "zhiwei"
import numpy as np
import operator
import matplotlib.pyplot as plt

ARM_LENGTH_1 = 3.0
ARM_LENGTH_2 = 3.0
ARM_LENGTH_3 = 3.0

PI = np.pi


class VirtualArm(object):
    """docstring for VirtualArm"""

    def __init__(self,
                 dim=1,
                 arm_lens=np.array([ARM_LENGTH_1]),
                 upper_bound=None,
                 lower_bound=None,
                 start_angular=np.zeros(1),
                 ziel=(2.12, 2.12)
                 ):
        super(VirtualArm, self).__init__()

        self._dim = dim
        self._arm_len = np.zeros(self._dim)
        for idx, arm_len in enumerate(arm_lens):
            self._arm_len[idx] = arm_len

        # Check the lower and upper bound
        self._upper_bound = upper_bound
        self._lower_bound = lower_bound

        self._ziel = ziel
        self.init(start_angular)

    def _refresh_end_coor(self):
        self._end_coor = [(0.0, 0.0)]

        for angluar, arm_len in zip(self._arm_angulars_in_degree, self._arm_len):
            self._end_coor.append(
                (self._end_coor[-1][0] + arm_len * np.cos((angluar / 180.0) * np.pi),
                 self._end_coor[-1][1] + arm_len * np.sin((angluar / 180.0) * np.pi)))
        self._end_coor = tuple(self._end_coor)

    def init(self, start_angular=None, ziel=None):
        if ziel is not None:
            self._ziel = ziel

        if start_angular is None:
            start_angular = np.zeros(self._dim)
        self._arm_angulars_in_degree = tuple(start_angular)

        self._refresh_end_coor()

        self._visualize()

    def perform_action(self, arm_input):
        accumulation = [0]
        for single_input in arm_input:
            accumulation.append(accumulation[-1] + single_input)
        accumulation.pop(0)
        accumulation = tuple(accumulation)

        position = tuple(map(operator.add, self._arm_angulars_in_degree, accumulation))

        if (self._upper_bound and self._lower_bound):
            for i in xrange(self._dim):
                if position[i] > self._upper_bound[i]:
                    position[i] = self._upper_bound[i]
                if position[i] < self._lower_bound[i]:
                    position[i] = self._lower_bound[i]

        position = tuple([i % 360 for i in position])

        self._arm_angulars_in_degree = position

        self._refresh_end_coor()

        self._visualize()

    def read(self):
        return self._arm_angulars_in_degree

    def _visualize(self):

        linewidth = 1
        markersize = 3

        plt.gcf().clear()

        plt.axis([-10, 10, -10, 10])
        for i in xrange(self._dim):
            plt.plot(
                [self._end_coor[i][0], self._end_coor[i + 1][0]],
                [self._end_coor[i][1], self._end_coor[i + 1][1]],
                'k', linewidth=linewidth)

        for coor in self._end_coor:
            plt.plot(
                coor[0], coor[1],
                'ro', markersize=markersize, markeredgewidth=linewidth)

        plt.plot(self._ziel[0], self._ziel[1], 'ro', markersize=markersize, markeredgewidth=linewidth)
        plt.pause(0.01)


class RobotArm(object):
    """docstring for RobotArm"""

    def __init__(self, arg):
        super(RobotArm, self).__init__()
        self.arg = arg


def main():
    arm = VirtualArm(dim=1,
                     arm_lens=np.array([ARM_LENGTH_1]),
                     upper_bound=None,
                     lower_bound=None,
                     start_angular=np.zeros(1),
                     ziel=(-2.12, -2.12))
    for x in xrange(1, 1000):
        arm.perform_action((10,))
        print "perform 10, 10, 10"
        print arm._arm_angulars_in_degree
        print arm._end_coor


if __name__ == '__main__':
    main()
