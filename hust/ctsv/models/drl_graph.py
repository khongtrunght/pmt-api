from schemas.schemas import DRL


class Graph:
    def __init__(self, drl: DRL, activities_lst):
        self.drl = drl
        self.activities_lst = activities_lst
        self.construct_graph()

    def construct_graph(self):
        self.activities_lst
