# -*- coding: utf-8 -*-

#モジュールのインポート
import random
import matplotlib.pyplot as plt
import numpy as np
import time

#粒子群クラス
class Particle:
    #コンストラクタ
    def __init__(self,N):
        self.n = N #粒子数
        self.x = np.array([[random.uniform(-5, 5)for i in range(self.n)], [random.uniform(-5, 5)for j in range(self.n)]]) #粒子位置
        self.pbest = self.x #パーソナルベスト
        self.gbest = np.array([[float("inf")],[float("inf")]]) #グローバルベスト
        self.w = 0.5 #慣性定数
        self.v = np.array([[0 for i in range(self.n)], [0 for j in range(self.n)]]) #粒子の速度
        self.r1 = 0.14 #乱数の最大値(1)
        self.r2 = 0.14 #乱数の最大値(2)
        self.xEvaluate = np.array([float("inf") for i in range(self.n)]) #現在位置の評価関数の値
        self.pbestEvaluate = np.array([float("inf") for i in range(self.n)]) #パーソナルベストの評価関数の値
        #初期設定
        self.pbestUpdate()
        self.gbestUpdate()

    #粒子の位置を更新する関数
    def positionUpdate(self):
        self.x += self.v
    
    #速度の更新を行う関数
    def velocityUpdate(self):
        #乱数の設定
        r1 = np.array([[random.uniform(0, self.r1)] for i in range(self.n)])
        r2 = np.array([[random.uniform(0, self.r2)] for i in range(self.n)])
        #速度の計算
        self.v = self.w * self.v + r1.T * (self.gbest - self.x) + r2.T * (self.pbest - self.x)

    #パーソナルベストの更新を行う関数
    def pbestUpdate(self):
        self.evaluationFunc()
        #パーソナルベストの更新
        self.lbest = np.where(self.xEvaluate < self.pbestEvaluate, self.x,self.pbest)
    
    #グローバルベストの更新を行う関数
    def gbestUpdate(self):
        #最小値のパーソナルベストのインデックスを取得
        index = np.argmin(self.pbestEvaluate)
        #グローバルベストの更新
        self.gbest=[[self.pbest[0][index] for i in range(self.n)],[self.pbest[1][index] for j in range(self.n)]]
                
    #評価関数の計算を行う関数
    def evaluationFunc(self):
        #評価関数：x^2+y^2
        self.xEvaluate = self.x[0,:] * self.x[0,:] + self.x[1,:] * self.x[1,:]
        self.pbestEvaluate = self.pbest[0,:] * self.pbest[0,:] + self.pbest[1,:] * self.pbest[1,:]
    
    #粒子の情報をすべて更新する関数
    def allUpdate(self):
        self.positionUpdate()
        self.velocityUpdate()
        self.pbestUpdate()
        self.gbestUpdate()

start = time.time() #スタート時間

N=30 #粒子数

#粒子の設定
p = Particle(N)

T = 50 #打ち切り時刻

#シミュレーション
for t in range(T):
    p.allUpdate()
    x = p.x[0]
    y = p.x[1]
    plt.plot(x,y,".",c="blue")
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    plt.plot(0,0,"o",c="red")
    plt.pause(0.05)
    plt.gca().clear()
#シミュレーションにかかった時間の表示
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")