# -*- coding: utf-8 -*-

'''
新しくPSOのプログラムを書き直し中
やるべきこと：計算量の改善及び派生PSOのプログラム作成
'''

import random
import matplotlib.pyplot as plt
import numpy as np
from csv_write import WriteData

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
        self.personal_best = np.array([[float('inf') for _ in range(D)] for _ in range(T)])
        self.personal_func_ans = float('inf')
        self.velocity = np.array([[float('inf') for _ in range(D)] for _ in range(T)])
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
        rand1 = np.array([random.uniform(0, Particle.rand[0]) for _ in range(D)])
        rand2 = np.array([random.uniform(0, Particle.rand[0]) for _ in range(D)])
        
        self.velocity[t + 1] = w*v + c1*rand1*(pbest - x) + c2*rand2*(gbest - x)
        

        self.velocity[t + 1] = np.where(self.velocity[t + 1] < Particle.velocity_max, self.velocity[t + 1], Particle.velocity_max)


    # パーソナルベストを更新するメソッド
    def personal_best_update(self, f, t):
        pesonal_ans = self.personal_func_ans
        if f < pesonal_ans:
            self.personal_func_ans = f
            self.personal_best[t] = np.array(self.x[t])
        else:
            self.personal_best[t] = self.personal_best[t - 1]


    # グローバルベストを更新するメソッド
    def global_best_update(self,t):
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


class EvaluationFunc():

    def __init__(self):
        pass

    # 評価関数を計算するメソッド
    @staticmethod
    def calculate(x):
        f = pow(x[0], 2) + pow(x[1], 2)
        return f

# 3d描画を行う関数
def plot_graph(particles,N,T_MAX):
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    sleep_time = 0.05
    
    n = 300
    func_x = np.linspace(-5,5,n)
    func_y = np.linspace(-5,5,n)
    X,Y = np.meshgrid(func_x, func_y)
    Z = pow(X,2)+pow(Y,2)
    
    # Figureを追加
    fig = plt.figure(figsize = (8, 8))

    # axをfigureに設定する
    ax = fig.add_subplot(111, projection='3d')
    
    # 曲線を描画
    for t in range(T_MAX):
        # Axesのタイトルを設定
        ax.set_title("PSO_plot", size = 20)
        
        # 軸ラベルを設定
        ax.set_xlabel("x", size = 14, color = "r")
        ax.set_ylabel("y", size = 14, color = "r")
        ax.set_zlabel("z", size = 14, color = "r")
        
        # 軸目盛を設定
        ax.set_xticks([-5.0, -2.5, 0.0, 2.5, 5.0])
        ax.set_yticks([-5.0, -2.5, 0.0, 2.5, 5.0])
        
        # 描画の固定
        ax.set_xlim(Particle.x_min[0],Particle.x_max[0])
        ax.set_ylim(Particle.x_min[0],Particle.x_max[0])
        ax.set_zlim(-1,EvaluationFunc.calculate(Particle.x_max))
        
        # 粒子ごとに描画
        for particle_num in range(N):
            x = particles[particle_num].x[t]
            ax.scatter(x[0], x[1], EvaluationFunc.calculate(x),c = "blue")
            
        # 最適解の描画
        ax.scatter(0, 0, 0,c = "red")
        
        # 評価関数の描画
        ax.plot_wireframe(X,Y,Z,color = "gray")
        
        plt.draw()
        # ポーズ
        plt.pause(sleep_time)
        # グラフ初期化
        plt.cla()

    

def main():

    # 粒子数
    N = 5

    # 次元数
    D = 2

    # 最大ステップ数
    T_MAX = 10
    
    # グローバルベストの設定
    Particle.global_best = np.array([[float('inf') for _ in range(D)] for _ in range(T_MAX + 1)])

    # 粒子のオブジェクト
    particles = [Particle(D, T_MAX) for _ in range(N)]

    # シミュレーション
    for t in range(T_MAX):
        for particle_num in range(N):
            particles[particle_num].calc_evaluation_func(t)
            particles[particle_num].global_best_update(t)
            particles[particle_num].velocity_update(t, D)
            particles[particle_num].position_update(t)
        Particle.next_global_best_update(t)
        
    # 3d描画
    plot_graph(particles,N,T_MAX)
    print('最適解:', Particle.global_best[T_MAX])
    print('最適値:', Particle.global_func_ans)

    # データの保存
    w = WriteData()
    w.csv_writer(particles,Particle.global_best)

if __name__ == '__main__':
    main()
