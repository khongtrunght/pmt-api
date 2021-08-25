from abc import abstractmethod
from typing import List

from hust.ctsv.consumer.student import Student
from hust.ctsv.schemas.request_schemas import RqtActivityUserCId, RqtMarkCriteria, RqtCriteria
from hust.ctsv.schemas.schemas import DRL, ActivityViewAlgo, ActivitiesLst
from uplink.auth import ApiTokenHeader


class InfoGet:
    @abstractmethod
    def initiallize(self):
        pass

    def __init__(self, user: RqtCriteria):
        self.user: RqtCriteria = user
        self.api: Student
        self.initiallize()

    def get_list_of_activities_id(self, cid_lst: List[int]):
        user_copy_cid = RqtActivityUserCId(**self.user.dict())
        out_put = []
        for id in cid_lst:
            user_copy_cid.CId = id
            op = self.api.get_activity_by_cid(user_copy_cid).Activities
            for activity in op:
                out_put.append(activity.AId)
        return out_put

    def get_list_of_activities(self, cid_lst: List[int]):
        id_lst = self.get_list_of_activities_id(cid_lst)
        activities_lst = ActivitiesLst(__root__=[])
        for id in id_lst:
            activity = self.api.get_activity_by_id({**self.user.dict(), 'AId': id}).Activities[0]
            activities_lst.add_activity(ActivityViewAlgo(**activity.dict()))
        return activities_lst

    def mark_criteria(self, drl: DRL):
        mark_criteria = RqtMarkCriteria(**drl.dict(), **self.user.dict())
        mark_criteria = mark_criteria.json().encode('utf-8')
        self.api.mark_criteria_user(mark_criteria)


class BearerInfoGet(InfoGet):
    def initiallize(self):
        token_auth = ApiTokenHeader("Authorization",
                                    self.user.TokenCode)
        self.api = Student(base_url="https://ctsv.hust.edu.vn/", auth=token_auth)


class NonBearerInfoGet(InfoGet):
    def initiallize(self):
        self.api = Student(base_url="https://ctsv.hust.edu.vn/")
