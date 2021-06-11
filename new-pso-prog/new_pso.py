# -*- coding: utf-8 -*-

'''
新しくPSOのプログラムを書き直し中
やるべきこと：計算量の改善及び派生PSOのプログラム作成
'''

import random
import matplotlib.pyplot as plt
import numpy as np


class Particle():
    global_best = []
    global_func_ans = float('inf')
    x_max = np.array([5.0, 5.0])
    x_min = np.array([-5.0, -5.0])
    velocity_max = 0.5 * (x_max-x_min)
    c = np.array([1.0, 1.0])
    rand = np.array([0.14, 0.14])
    weight = 0.5

    def __init__(self, D, T_MAX):
        T = T_MAX + 1
        self.personal_best = np.array([float('inf') for _ in range(D)])
        self.personal_func_ans = float('inf')
        self.velocity = np.array([[float('inf') for _ in range(D)] for _ in range(T)])
        self.x = np.array([[float('inf') for _ in range(D)] for _ in range(T)])
        for i in range(D):
            self.x[0][i] = random.uniform(self.x_min[i], self.x_max[i])
            self.velocity[0][i] = random.uniform(0, self.velocity_max[i])

    # 位置を更新するメソッド
    def position_update(self, t, D):
        x = self.x[t]
        v = self.velocity[t + 1]
        
        self.x[t + 1] = x + v

    # 速度を更新するメソッド
    def velocity_update(self, t, D):
        w = Particle.weight
        v = self.velocity[t]
        x = self.x[t]
        pbest = self.personal_best
        gbest = Particle.global_best
        c1 = Particle.c[0]
        c2 = Particle.c[1]
        rand1 = np.array([random.uniform(0, Particle.rand[0]) for _ in range(D)])
        rand2 = np.array([random.uniform(0, Particle.rand[0]) for _ in range(D)])
        
        self.velocity[t + 1] = w*v + c1*rand1*(pbest - x) + c2*rand2*(gbest - x)
        
        self.velocity[t + 1] = np.where(self.velocity[t + 1] < Particle.velocity_max, self.velocity[t + 1], Particle.velocity_max)


    # パーソナルベストを更新するメソッド
    def personal_best_update(self, f, t):
        pesonal_ans = self.personal_func_ans
        if f < pesonal_ans:
            self.personal_func_ans = f
            self.personal_best = np.array(self.x[t])

    # グローバルベストを更新するメソッド
    def global_best_update(self):
        pesonal_ans = self.personal_func_ans
        global_ans = Particle.global_func_ans

        if pesonal_ans < global_ans:
            Particle.global_func_ans = pesonal_ans
            Particle.global_best = np.array(self.personal_best)

    # 評価関数を計算するメソッド
    def calc_evaluation_func(self, t):
        f = EvaluationFunc.calculate(self.x[t])

        self.personal_best_update(f, t)


class EvaluationFunc():

    def __init__(self):
        pass

    # 評価関数を計算するメソッド
    @staticmethod
    def calculate(x):
        f = pow(x[0], 2) + pow(x[1], 2)
        return f


def main():

    # 粒子数
    N = 30

    # 次元数
    D = 2

    # 最大ステップ数
    T_MAX = 50

    # 粒子のオブジェクト
    particles = [Particle(D, T_MAX) for _ in range(N)]

    # グローバルベストの設定
    Particle.global_best = [float('inf') for _ in range(D)]

    # シミュレーション
    for time in range(T_MAX):
        for particle_num in range(N):
            particles[particle_num].calc_evaluation_func(time)
            particles[particle_num].global_best_update()
            particles[particle_num].velocity_update(time, D)
            particles[particle_num].position_update(time, D)

            x = particles[particle_num].x[time][0]
            y = particles[particle_num].x[time][1]

            plt.plot(x, y, ".", c="blue")
            plt.xlim(-10, 10)
            plt.ylim(-10, 10)
            plt.plot(0, 0, "o", c="red")
        plt.pause(0.05)
        plt.gca().clear()

    print('最適解:', Particle.global_best)
    print('最適値:', Particle.global_func_ans)


if __name__ == '__main__':
    main()
