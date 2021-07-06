# -*- coding: utf-8 -*-

import datetime
import os
import csv
import json
from numpy import array


class WriteData():

    def __init__(self):
        # 現在の日時を取得
        self.now = datetime.datetime.now()

        # ディレクトリ名の生成
        self.new_dir_name = self.now.strftime('%Y%m%d_%H%M%S')

        # pathの生成
        self.dir_path = 'PSO/new-pso-prog/result/' + self.new_dir_name

        # ディレクトリの生成
        os.mkdir(self.dir_path)

    def json_write(self,particles):
        # パラメータ準備
        D = len(particles[0].x[0])
        D_list = list(range(D))
        c_list = list(range(2))
        param_dict = {
            'N' : len(particles),
            'D' : D,
            'T_MAX' : len(particles[0].x) - 1,
            'x_max' : dict(zip(D_list,particles[0].x_max)),
            'x_min' : dict(zip(D_list,particles[0].x_min)),
            'velocity_max' : dict(zip(D_list,particles[0].velocity_max)),
            'c' : dict(zip(c_list,particles[0].c)),
            'rand' : dict(zip(D_list,particles[0].rand)),
            'weight' : particles[0].weight
        }
        
        # ファイル名の生成
        file_name = 'param.json'

        # pathの生成
        file_path = self.dir_path + '/' + file_name
        
        # jsonへ書き込み
        with open(file_path, mode='w') as f:
            json.dump(param_dict, f)

    # csvにデータを書き込むメソッド
    def csv_writer(self, particles, gbest):
        D = len(particles[0].x[0])
        T_MAX = len(particles[0].x) - 1

        # rowの名前を生成
        row_name = ['T', 'particle_num', 'x', 'velocity', 'pbest', 'gbest']

        # ファイル名の生成
        file_name = 'result.csv'

        # pathの生成
        file_path = self.dir_path + '/' + file_name

        # csvへ書き込み
        with open(file_path, mode='w', newline='') as f:
            writer = csv.writer(f)

            # 行の名前を書き込み
            writer.writerow(row_name)

            # データの書き込み
            for t in range(T_MAX):
                for particle_num in range(len(particles)):
                    # x,vの取得
                    x_list = self.read_particles_xv(
                        D, particles[particle_num].x[t])
                    v_list = self.read_particles_xv(
                        D, particles[particle_num].velocity[t])

                    # 書き込むデータを作成
                    write_data = [t, particle_num] + [x_list] + [v_list] + \
                        [particles[particle_num].personal_best[t], gbest[t]]

                    # データの書き込み
                    writer.writerow(write_data)

    # x,vの値を取得して返すメソッド
    def read_particles_xv(self, D, data):
        read_data = []
        for d in range(D):
            read_data.append(data[d])
        return array(read_data)
