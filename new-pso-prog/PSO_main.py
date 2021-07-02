# -*- coding: utf-8 -*-

import numpy as np
from WriteData import WriteData
from PSO_Particle import Particle
from PlotGraph import PlotGraph


def main():

    # 粒子数
    N = 10

    # 次元数
    D = 2

    # 最大ステップ数
    T_MAX = 40

    # グローバルベストの設定
    Particle.global_best = np.array(
        [[float('inf') for _ in range(D)] for _ in range(T_MAX + 1)])

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
    pg = PlotGraph(particles, N, T_MAX)
    pg.plot_graph()

    # 最適解と最適値の出力
    print('最適解:', Particle.global_best[T_MAX])
    print('最適値:', Particle.global_func_ans)

    # データの保存
    w = WriteData()
    w.csv_writer(particles, Particle.global_best)


if __name__ == '__main__':
    main()
