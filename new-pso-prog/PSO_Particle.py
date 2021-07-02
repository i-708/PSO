# -*- coding: utf-8 -*-

import numpy as np
import random
from EvaluationFunc import EvaluationFunc


class Particle():
    global_func_ans = float('inf')
    x_max = np.array([5.0, 5.0])
    x_min = np.array([-5.0, -5.0])
    velocity_max = 0.5 * (x_max-x_min)
    c = np.array([1.0, 1.0])
    rand = np.array([0.14, 0.14])
    weight = 0.5

    def __init__(self, D, T_MAX):
        T = T_MAX + 1
        self.personal_best = np.array(
            [[float('inf') for _ in range(D)] for _ in range(T)])
        self.personal_func_ans = float('inf')
        self.velocity = np.array(
            [[float('inf') for _ in range(D)] for _ in range(T)])
        self.x = np.array([[float('inf') for _ in range(D)] for _ in range(T)])
        for i in range(D):
            self.x[0][i] = random.uniform(self.x_min[i], self.x_max[i])
            self.velocity[0][i] = random.uniform(0, self.velocity_max[i])

    # 位置を更新するメソッド
    def position_update(self, t):
        x = self.x[t]
        v = self.velocity[t + 1]

        self.x[t + 1] = x + v

    # 速度を更新するメソッド
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

    # パーソナルベストを更新するメソッド

    def personal_best_update(self, f, t):
        pesonal_ans = self.personal_func_ans
        if f < pesonal_ans:
            self.personal_func_ans = f
            self.personal_best[t] = np.array(self.x[t])
        else:
            self.personal_best[t] = self.personal_best[t - 1]

    # グローバルベストを更新するメソッド
    def global_best_update(self, t):
        pesonal_ans = self.personal_func_ans
        global_ans = Particle.global_func_ans

        if pesonal_ans < global_ans:
            Particle.global_func_ans = pesonal_ans
            Particle.global_best[t] = np.array(self.personal_best[t])

    # 次のグローバルベストの初期化
    @staticmethod
    def next_global_best_update(t):
        Particle.global_best[t + 1] = Particle.global_best[t]

    # 評価関数を計算するメソッド
    def calc_evaluation_func(self, t):
        f = EvaluationFunc.calculate(self.x[t])

        self.personal_best_update(f, t)
