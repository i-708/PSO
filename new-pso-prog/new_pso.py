# -*- coding: utf-8 -*-

'''
新しくPSOのプログラムを書き直し中
やるべきこと：グローバル変数が粒子ごとに保持されているバグを改善(実際はクラスで一つのグローバルベストを持つ)
'''

import random
import matplotlib.pyplot as plt


class Particle():
    global_best = []
    global_func_ans = float('inf')
    x_max = [5.0, 5.0]
    x_min = [-5.0, -5.0]
    velocity_max = [0.5 * (x_max_elem - x_min_elem)
                    for (x_max_elem, x_min_elem) in zip(x_max, x_min)]
    c = [1.0, 1.0]
    rand = [0.14, 0.14]
    weight = 0.8

    def __init__(self, D, T_MAX):
        T = T_MAX + 1
        self.personal_best = [float('inf') for _ in range(D)]
        self.personal_func_ans = float('inf')
        self.velocity = [[float('inf') for _ in range(D)] for _ in range(T)]
        self.x = [[float('inf') for _ in range(D)] for _ in range(T)]
        for i in range(D):
            self.x[0][i] = random.uniform(self.x_min[i], self.x_max[i])
            self.velocity[0][i] = random.uniform(0, self.velocity_max[i])

    # 位置を更新するメソッド
    def position_update(self, t, D):
        x = self.x[t]
        v = self.velocity[t + 1]

        for i in range(D):
            self.x[t + 1][i] = x[i] + v[i]

    # 速度を更新するメソッド
    def velocity_update(self, t, D):
        w = self.weight
        v = self.velocity[t]
        x = self.x[t]
        pbest = self.personal_best
        gbest = self.global_best
        c1 = self.c[0]
        c2 = self.c[1]

        for i in range(D):
            rand1 = random.uniform(0, self.rand[0])
            rand2 = random.uniform(0, self.rand[1])

            self.velocity[t + 1][i] = w*v[i] + c1*rand1 * \
                (pbest[i] - x[i]) + c2*rand2*(gbest[i] - x[i])

            if self.velocity[t + 1][i] > self.velocity_max[i]:
                self.velocity[t + 1][i] = self.velocity_max[i]

    # パーソナルベストを更新するメソッド
    def personal_best_update(self, f, t):
        pesonal_ans = self.personal_func_ans
        if f < pesonal_ans:
            self.personal_func_ans = f
            self.personal_best = list(self.x[t])

    # グローバルベストを更新するメソッド
    def global_best_update(self):
        pesonal_ans = self.personal_func_ans
        global_ans = self.global_func_ans

        if pesonal_ans < global_ans:
            self.global_func_ans = pesonal_ans
            self.global_best = list(self.personal_best)

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
    T_MAX = 100

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
            plt.xlim(-5, 5)
            plt.ylim(-5, 5)
            plt.plot(0, 0, "o", c="red")
        plt.pause(0.05)
        plt.gca().clear()

    print('最適解:', particles[0].global_best)
    print('最適値:', particles[0].global_func_ans)


if __name__ == '__main__':
    main()
