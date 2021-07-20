# -*- coding: utf-8 -*-

import numpy as np
import random
from EvaluationFunc import EvaluationFunc
from PSO_Particle import Particle
import math


class Particle(Particle):
    a1 = 0.05
    a2 = 0.1
    T1 = 0
    T2 = 0
    D = 0

    def velocity_update(self, t, D):
        w = Particle.weight
        v = self.velocity[t]
        x = self.x[t]
        pbest = self.personal_best[t]
        gbest = Particle.global_best[t]
        c1 = Particle.c[0]
        c2 = Particle.c[1]
        rand1 = np.array([random.uniform(0, Particle.rand[0])
                          for _ in range(D)])
        rand2 = np.array([random.uniform(0, Particle.rand[0])
                          for _ in range(D)])

        self.velocity[t + 1] = w*v + c1*rand1 * \
            (pbest - x) + c2*rand2*(gbest - x)

        self.velocity[t + 1] = np.where(self.velocity[t + 1] < Particle.velocity_max,
                                        self.velocity[t + 1], Particle.velocity_max)

    def global_best_update(self, t):
        pesonal_ans = self.personal_func_ans
        global_ans = Particle.global_func_ans

        if pesonal_ans < global_ans:
            Particle.global_func_ans = pesonal_ans
            Particle.global_best[t] = np.array(self.personal_best[t])

    def position_update(self, k):
        super(Particle, self).position_update(k)
        d1 = self.get_distance1(k + 1)
        gbest_x_dist = self.get_gbest_to_x_distance(k + 1)
        if gbest_x_dist <= d1:
            self.velocity_plus_random(k)

    def personal_best_update(self, f, k):
        d2 = self.get_distance2(k)
        gbest_x_dist = self.get_gbest_to_x_distance(k)
        if gbest_x_dist >= d2:
            super(Particle, self).personal_best_update(f, k)
        else:
            self.personal_best[k] = self.personal_best[k - 1]

    def get_gbest_to_x_distance(self, k):
        D = Particle.D
        diff_total = 0
        for i in range(D):
            x = self.x[k][i]
            gbest_x = Particle.global_best[k][i]
            diff_total += pow((x - gbest_x), 2)
        return math.sqrt(diff_total)

    def velocity_plus_random(self, k):
        x = self.get_adjustment_variable(k)
        n = np.random.randn()
        v = self.v[k + 1] * x * n

    def get_adjustment_variable(self, k):
        if k > Particle.T1:
            return 0
        a1 = Particle.a1
        x = ((Particle.T1 - k) * 0.5 *
             self.max_min_square_difference()) / Particle.T1
        return x

    def get_distance1(self, k):
        if k > Particle.T1:
            return 0
        a1 = Particle.a1
        d1 = ((Particle.T1 - k) * a1 *
              math.sqrt(self.max_min_square_difference())) / Particle.T1
        return d1

    def get_distance2(self, k):
        if k > Particle.T2:
            return 0
        a2 = Particle.a2
        d2 = ((Particle.T2 - k) * a2 *
              math.sqrt(self.max_min_square_difference())) / Particle.T2
        return d2

    def max_min_square_difference(self):
        diff_total = 0
        D = Particle.D
        for i in range(D):
            x_max = Particle.x_max[i]
            x_min = Particle.x_min[i]
            diff_total += pow((x_max - x_min), 2)
        return diff_total

        # 次のグローバルベストの初期化をするメソッド
    @staticmethod
    def next_global_best_update(t):
        Particle.global_best[t + 1] = Particle.global_best[t]
# print(np.random.randn())
