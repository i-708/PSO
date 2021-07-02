# -*- coding: utf-8 -*-


class EvaluationFunc():

    def __init__(self):
        pass

    # 評価関数を計算するメソッド
    @staticmethod
    def calculate(x):
        f = pow(x[0], 2) + pow(x[1], 2)
        return f
