import datetime
import os
import csv
from new_pso import Particle

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
    
    def csv_writer(self,particles):
        D = len(particles[0].x[0])
        T_MAX = len(particles[0].x)

        x_label = []
        v_label = []
        
        # xとvのlabelを生成
        for i in range(D):
            x_label_name = 'x' + str(i)
            v_label_name = 'v' + str(i)
            x_label.append(x_label_name)
            v_label.append(v_label_name)
        
        # rowの名前を生成
        row_name = ['T','particle_num'] + x_label + v_label + ['func_ans','pbest','gbest']
        
        # ファイル名の生成
        file_name = 'result.csv'

        # pathの生成
        file_path = self.dir_path + '/' + file_name

        # csvへ書き込み
        with open(file_path, mode='w') as f:
            writer = csv.writer(f)
            
            # 行の名前を書き込み
            writer.writerow(row_name)
            
            

# w = WriteData()

# w.csv_writer()