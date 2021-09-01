from abc import abstractmethod

from hust.ctsv.schemas.schemas import DRL, ActivitiesLst


class Algorithm:
    @abstractmethod
    def initiate(self, drl: DRL, a_list: ActivitiesLst):
        pass

    @abstractmethod
    def optimize(self):
        pass

    @abstractmethod
    def get_drl_optimal(self) -> DRL:
        pass

    @abstractmethod
    def contruct_optimal_graph(self):
        pass

    @abstractmethod
    def run(self, drl:DRL, a_list: ActivitiesLst):
        pass
