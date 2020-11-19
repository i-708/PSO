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
        self.lbest = self.x #ローカルベスト
        self.gbest = np.array([[float("inf")],[float("inf")]]) #グローバルベスト
        self.w = 0.91 #慣性定数
        self.v = np.array([[0 for i in range(self.n)], [0 for j in range(self.n)]]) #粒子の速度
        self.r1 = 0.14 #乱数の最大値(1)
        self.r2 = 0.14 #乱数の最大値(2)
        self.xEvaluate = np.array([float("inf") for i in range(self.n)]) #現在位置の評価関数の値
        self.lbestEvaluate = np.array([float("inf") for i in range(self.n)]) #ローカルベストの評価関数の値
        #初期設定
        self.lbestUpdate()
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
        self.v = self.w * self.v + r1.T * (self.gbest - self.x) + r2.T * (self.lbest - self.x)

    #ローカルベストの更新を行う関数
    def lbestUpdate(self):
        self.evaluationFunc()
        #ローカルベストの更新
        self.lbest = np.where(self.xEvaluate < self.lbestEvaluate, self.x,self.lbest)
    
    #グローバルベストの更新を行う関数
    def gbestUpdate(self):
        #最小値のローカルベストのインデックスを取得
        index = np.argmin(self.lbestEvaluate)
        #グローバルベストの更新
        self.gbest=[[self.lbest[0][index] for i in range(self.n)],[self.lbest[1][index] for j in range(self.n)]]
                
    #評価関数の計算を行う関数
    def evaluationFunc(self):
        #評価関数：x^2+y^2
        self.xEvaluate = self.x[0,:] * self.x[0,:] + self.x[1,:] * self.x[1,:]
        self.lbestEvaluate = self.lbest[0,:] * self.lbest[0,:] + self.lbest[1,:] * self.lbest[1,:]
    
    #粒子の情報をすべて更新する関数
    def allUpdate(self):
        self.positionUpdate()
        self.velocityUpdate()
        self.lbestUpdate()
        self.gbestUpdate()

start = time.time() #スタート時間

N=10 #粒子数(1)
M=10 #粒子数(2)
L=10 #粒子数(3)

#粒子の設定
x=Particle(N) 
y=Particle(M)
z=Particle(L)

T = 1000 #打ち切り時刻

#シミュレーション
for t in range(T):
    x.allUpdate()
    y.allUpdate()
    z.allUpdate()
    xlist = x.x[0]
    ylist = x.x[1]
    plt.plot(xlist,ylist,".",c="pink")
    xlist = z.x[0]
    ylist = z.x[1]
    plt.plot(xlist,ylist,".",c="blue")
    xlist = y.x[0]
    ylist = y.x[1]
    plt.plot(xlist,ylist,".",c="black")
    #plt.xlim(-5,5)
    #plt.ylim(-5,5)
    plt.plot(xlist,ylist,".")
    plt.plot(0,0,"o",c="red")
    plt.pause(0.00001)
    plt.gca().clear()
#シミュレーションにかかった時間の表示
elapsed_time = time.time() - start
print ("elapsed_time:{0}".format(elapsed_time) + "[sec]")