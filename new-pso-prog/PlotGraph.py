# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from EvaluationFunc import EvaluationFunc
from PSO_Particle import Particle


class PlotGraph():

    def __init__(self, particles, N, T_MAX):
        # 引数の受け取り
        self.particles = particles
        self.N = N
        self.T_MAX = T_MAX

        # 描画間の停止時間
        self.sleep_time = 0.05

        # Figureを追加
        self.fig = plt.figure(figsize=(8, 8))

        # axをfigureに設定する
        self.ax = self.fig.add_subplot(111, projection='3d')

        # 評価関数の準備
        n = 300
        func_x = np.linspace(-5, 5, n)
        func_y = np.linspace(-5, 5, n)
        self.X, self.Y = np.meshgrid(func_x, func_y)
        self.Z = pow(self.X, 2)+pow(self.Y, 2)

    # グラフをプロットするメソッド
    def plot_graph(self):
        # 曲線を描画
        for t in range(self.T_MAX):

            # 描画の設定
            self.__plot_graph_setting()

            # 粒子ごとに描画
            self.__plot_graph_particle(t)

            # 最適解の描画
            self.ax.scatter(0, 0, 0, c="red")

            # 評価関数の描画
            self.ax.plot_wireframe(self.X, self.Y, self.Z, color="gray")

            # 描画
            self.__draw_graph()

    # 描画に関する設定を行うメソッド
    def __plot_graph_setting(self):
        # Axesのタイトルを設定
        self.ax.set_title("PSO_plot", size=20)

        # 軸ラベルを設定
        self.ax.set_xlabel("x", size=14, color="r")
        self.ax.set_ylabel("y", size=14, color="r")
        self.ax.set_zlabel("z", size=14, color="r")

        # 軸目盛を設定
        self.ax.set_xticks([-5.0, -2.5, 0.0, 2.5, 5.0])
        self.ax.set_yticks([-5.0, -2.5, 0.0, 2.5, 5.0])

        # 描画の固定
        self.ax.set_xlim(Particle.x_min[0], Particle.x_max[0])
        self.ax.set_ylim(Particle.x_min[0], Particle.x_max[0])
        self.ax.set_zlim(-1, EvaluationFunc.calculate(Particle.x_max))

    # 粒子をプロットするメソッド
    def __plot_graph_particle(self, t):
        for particle_num in range(self.N):
            x = self.particles[particle_num].x[t]
            self.ax.scatter(x[0], x[1], EvaluationFunc.calculate(x), c="blue")

    # 描画の処理を行うメソッド
    def __draw_graph(self):
        plt.draw()
        # ポーズ
        plt.pause(self.sleep_time)
        # グラフ初期化
        plt.cla()
