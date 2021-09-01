from typing import List
import networkx as nx
from hust.ctsv.algo.algorithm import Algorithm
from hust.ctsv.schemas.schemas import ActivitiesLst, DRL, CriteriaView, ActivityId
from networkx.algorithms.matching import max_weight_matching
from collections import defaultdict


class Bipartite(Algorithm):
    def __init__(self):
        pass

    def get_list_criteria_view(self, drl: DRL) -> List[CriteriaView]:
        tieu_chi_lst : List[CriteriaView] = []
        for ctype in drl.CriteriaTypeDetailsLst:
            for cgroup in ctype.CriteriaGroupDetailsLst:
                for criteria in cgroup.UserCriteriaDetailsLst:
                    tieu_chi_lst.append(criteria)
        return tieu_chi_lst


    def optimize(self):
        # matching = bipartite.matching.minimum_weight_full_matching(self.graph, self.hoat_dong_id, "weight")
        matching = max_weight_matching(self.graph)
        matching_dict = {(tc if hd > 999 else hd) : (hd if hd > 999 else tc) for tc,hd in matching}
        not_hoat_dong_id = [id  for id in self.hoat_dong_id if id not in matching_dict.values()]
        assign_not_match = {self.hoat_dong_dict[id].CriteriaLst[0].CId:id for id in not_hoat_dong_id}

        self.assign = defaultdict(list)
        for d in (matching_dict, assign_not_match):
            for key, value in d.items():
                self.assign[key].append(value)
        self.contruct_optimal_graph()

    def contruct_optimal_graph(self):
        for ctype in self.drl_optimal.CriteriaTypeDetailsLst:
            for cgroup in ctype.CriteriaGroupDetailsLst:
                for criteria in cgroup.UserCriteriaDetailsLst:
                    if criteria.CId in self.assign.keys():
                        criteria.set_current_point(criteria.CMaxPoint)
                        criteria.UserCriteriaActivityLst = [ActivityId(AId = id) for id in self.assign[criteria.CId]]

    def get_drl_optimal(self) -> DRL:
        return self.drl_optimal

    def initiate(self, drl:DRL, a_list: ActivitiesLst):
        self.tieu_chi_lst = self.get_list_criteria_view(drl)
        self.tieu_chi_id_lst = [tieu_chi.CId for tieu_chi in self.tieu_chi_lst]
        self.tieu_chi_dict = dict(zip(self.tieu_chi_id_lst, self.tieu_chi_lst))

        self.hoat_dong = a_list.get_activities_lst()
        self.hoat_dong_id = [hd.AId for hd in self.hoat_dong]
        self.hoat_dong_dict = dict(zip(self.hoat_dong_id, self.hoat_dong))

        self.graph = nx.Graph()
        self.graph.add_nodes_from(self.hoat_dong_id, bipartite='activities')
        self.graph.add_nodes_from(self.tieu_chi_id_lst, bipartite='criteria')

        self.drl_optimal = drl.copy(deep=True)

        for id in self.hoat_dong_id:
            for criteria in self.hoat_dong_dict[id].CriteriaLst:
                self.graph.add_edge(id, criteria.CId, weight=criteria.CMaxPoint)

    def run(self, drl:DRL, a_list: ActivitiesLst):
        self.initiate(drl, a_list)
        self.optimize()
        return self.get_drl_optimal()




