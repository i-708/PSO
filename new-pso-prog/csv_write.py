import datetime
import os
import csv
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
    
    # csvにデータを書き込む関数
    def csv_writer(self,particles,gbest):
        D = len(particles[0].x[0])
        T_MAX = len(particles[0].x)
        
        # rowの名前を生成
        row_name = ['T','particle_num','x','velocity','pbest','gbest']
        
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
                    x_list = self.read_particles_xv(D,particles[particle_num].x[t])
                    v_list = self.read_particles_xv(D,particles[particle_num].velocity[t])
                    
                    # 書き込むデータを作成
                    write_data = [t, particle_num] + [x_list] + [v_list] + [particles[particle_num].personal_best[t], gbest[t]]
                    
                    # データの書き込み
                    writer.writerow(write_data)
            
    # x,vの値を取得して返す関数
    def read_particles_xv(self,D,data):
        read_data = []
        for d in range(D):
            read_data.append(data[d])
        return array(read_data)
