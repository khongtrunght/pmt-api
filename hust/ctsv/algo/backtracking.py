from copy import deepcopy

from hust.ctsv.schemas.schemas import DRL, ActivitiesLst


class Backtracking:
    def __init__(self, drl: DRL, a_list: ActivitiesLst):
        self.drl = drl
        self.a_list = a_list
        self.max_point = 0
        self.drl_optimal = None
        self.a_list_optimal = None

        self.construct_graph()

    def construct_graph(self):
        self.drl.assignActivities(a_list=self.a_list)

    def optimize(self):
        self.a_list.sort(key=lambda a: a.get_length_clist())
        self.back_track()
        self.contruct_optimal_graph()

    def back_track(self, index=0):
        if index == self.a_list.get_length():
            max_curr = self.drl.get_current_point()
            if max_curr > self.max_point:
                self.max_point = max_curr
                self.a_list_optimal = deepcopy(self.a_list)
                self.drl_optimal = self.drl.copy(deep=True)
        else:
            for number in range(self.a_list.get(index).get_length_clist()):
                tieu_chi = self.a_list.get(index).CriteriaLst[number]
                is_dc_chon = tieu_chi.duoc_chon()
                if not tieu_chi.duoc_chon():
                    self.a_list.get(index).set_criteria(number)
                elif (number + 1 == self.a_list.get(index).get_length_clist()):
                    self.a_list.get(index).set_criteria(number)
                else:
                    continue
                self.back_track(index + 1)
                if not is_dc_chon:
                    tieu_chi.bo_chon()

    def contruct_optimal_graph(self):
        criteria_activity = {}
        for activity in self.a_list_optimal.__root__:
            if activity.currentCriteria.CId not in criteria_activity.keys():
                criteria_activity[activity.currentCriteria.CId] = [activity.copy(include={"AId"}), ]
            else:
                criteria_activity[activity.currentCriteria.CId].append(activity.copy(include={"AId"}))

        for ctype in self.drl_optimal.CriteriaTypeDetailsLst:
            for cgroup in ctype.CriteriaGroupDetailsLst:
                for criteria in cgroup.UserCriteriaDetailsLst:
                    if criteria.CId in criteria_activity.keys():
                        criteria.UserCriteriaActivityLst = criteria_activity[criteria.CId]

    def export_optimal(self, exportor):
        exportor.store(self.drl_optimal)

    def get_drl_optimal(self) -> DRL:
        return self.drl_optimal


class PrintExportor:
    def store(self, drl):
        self.drl = drl

    def print(self):
        print("DRL", self.drl.get_current_point())
        for ctype in self.drl.CriteriaTypeDetailsLst:
            print("\tCTYPE", ctype.get_current_point())
            for cgroup in ctype.CriteriaGroupDetailsLst:
                print("\t\tCGROUP", cgroup.get_current_point())
                for criteria in cgroup.UserCriteriaDetailsLst:
                    print("\t\t\tC ", criteria.get_current_point())
                    print("\t\t\t ", criteria.UserCriteriaActivityLst)
