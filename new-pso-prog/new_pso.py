# -*- coding: utf-8 -*-

'''
新しくPSOのプログラムを書き直し中
やるべきこと：変数の値を細かく設定
'''

class Particle():
    global_best = []
    global_func_ans = 0
    velocity_max = 0
    c = []

    def __init__(self):
        self.personal_best = []
        self.personal_func_ans = 0
        self.rand = []
        self.weight = 0
        self.velocity = []
        self.x = []

    # 位置を更新するメソッド
    def position_update(self, t):
        x = self.x[t]
        v = self.velocity[t + 1]

        self.x[t + 1] = x + v

    # 速度を更新するメソッド
    def velocity_update(self, t):
        w = self.weight
        v = self.velocity[t]
        x = self.x[t]
        pbest = self.personal_best
        gbest = self.global_best
        c1 = self.c[0]
        c2 = self.c[1]
        rand1 = self.rand[0]
        rand2 = self.rand[1]

        self.v[t + 1] = w*v + c1*rand1*(pbest - x) + c2*rand2*(gbest - x)
        
        if self.v[t + 1] > self.velocity_max:
            self.v[t + 1] = self.velocity_max

    # パーソナルベストを更新するメソッド
    def personal_best_update(self, f, t):
        pesonal_ans = self.personal_func_ans
        if f < pesonal_ans:
            self.personal_func_ans = f
            self.personal_best = self.x[t]

    # グローバルベストを更新するメソッド
    def global_best_update(self):
        pesonal_ans = self.personal_func_ans
        global_ans = self.global_func_ans

        if pesonal_ans < global_ans:
            self.global_func_ans = pesonal_ans
            self.global_best = self.personal_best

    # 評価関数を計算するメソッド
    def calc_evaluation_func(self, t):
        f = EvaluationFunc.calculate(self.x)

        self.personal_best_update(f, t)

    # 位置,速度を更新するメソッド
    def all_update(self):
        self.position_update()
        self.velocity_update()


class EvaluationFunc():

    def __init__(self):
        pass

    # 評価関数を計算するメソッド
    @staticmethod
    def calculate(self, x):
        z = pow(x[0], 2) + pow(x[1], 2)
        return z


def main():
    
    # 粒子数
    N = 100
    
    # 粒子のオブジェクト
    particles = [Particle() for _ in range(N)]
    
    # 最大ステップ数
    T = 100
    
    # シミュレーション
    for time in range(T):
        for particle_num in range(N):
            particles[particle_num].calc_evaluation_func(time)
            particles[particle_num].global_best_update()
            particles[particle_num].velocity_update(time)
            particles[particle_num].position_update(time)
    
    print('最適解:',particles[0].global_best)
    print('最適値:',particles[0].global_func_ans)

if __name__ == '__main__':
    main()
