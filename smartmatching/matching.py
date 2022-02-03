import numpy as np
import mip


class Player:

    def __init__(self, name):
        self.name = name
        self.scores = []
        self.positions = set()

    @property
    def mean_score(self):
        return np.mean(self.scores)


class Matching:
    """
    专为5v5匹配开发
    规则如下：
    1、两边近5场的评分大致一样
    2、不会有太多重叠位置（暂未考虑）
    """

    def __init__(self, players):
        self.players = players
        self.blue_side = []
        self.red_side = []
        self.model = mip.Model(solver_name='cbc')
        self.x = {}
        self.y = {}
        self.f = {}  # 人工变量

    def __call__(self, *args, **kwargs):
        self.build_model()
        self.solve()
        self.show_result()

    def build_model(self):
        for i, player in enumerate(self.players):
            self.x[i] = self.model.add_var(var_type=mip.BINARY)
            self.y[i] = self.model.add_var(var_type=mip.BINARY)
            self.model.add_constr(self.x[i] + self.y[i] == 1)
        self.f = self.model.add_var(var_type=mip.CONTINUOUS, lb=0, obj=1)
        self.model.add_constr(mip.quicksum([self.x[i] for i in self.x]) == 5)
        self.model.add_constr(self.f >= mip.quicksum([player.mean_score*(self.x[i] - self.y[i])
                                                      for i, player in enumerate(self.players)]))
        self.model.add_constr(self.f >= mip.quicksum([player.mean_score*(self.y[i] - self.x[i])
                                                      for i, player in enumerate(self.players)]))

    def solve(self):
        status = self.model.optimize()
        if status == mip.OptimizationStatus.OPTIMAL:
            for i, v in self.x.items():
                if v.x == 1:
                    self.blue_side.append(self.players[i].name)
                else:
                    self.red_side.append(self.players[i].name)
        else:
            raise RuntimeError('无法完成匹配')

    def show_result(self):
        assert len(self.blue_side) == len(self.red_side) == 5
        print('蓝方阵营：')
        for i in self.blue_side:
            print(i, ' ')
        print('----------------------------------------------\n')
        print('红方阵营：')
        for i in self.red_side:
            print(i, ' ')
