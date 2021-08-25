from abc import abstractmethod
from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Set

from pydantic import BaseModel


class UAStatusClass(int, Enum):
    reject = 0
    pending = 1
    accept = 2


class PointCal(BaseModel):
    CurrentPoint: Optional[int] = 0

    @abstractmethod
    def get_max_point(self):
        pass

    def get_current_point(self):
        self.re_caculate_current_point()
        return min(self.get_max_point(), self.CurrentPoint)

    def set_current_point(self, value):
        self.CurrentPoint = value
        self.re_caculate_current_point()

    @abstractmethod
    def re_caculate_current_point(self):
        pass


class Criteria(BaseModel):
    CGroupId: int
    CId: int
    CName: str
    CType: int
    CMaxPoint: int
    CStatus: int


class ActivityId(BaseModel):
    AId: int

    def __eq__(self, other):
        return self.AId == other.AId

    def __hash__(self):
        return hash(self.AId)


class CriteriaView(PointCal):
    def re_caculate_current_point(self):
        self.UCPoint = self.CurrentPoint

    def get_current_point(self):
        return self.UCPoint

    CGroupId: int = None
    CId: int
    CName: str
    CMaxPoint: int
    UCPoint: Optional[int] = 10
    UserCriteriaActivityLst: List[ActivityId] = []
    Choose: Optional[bool] = False

    def get_max_point(self):
        return max(self.CMaxPoint, 0)

    def duoc_chon(self):
        return self.Choose

    def chon(self):
        self.Choose = True
        self.set_current_point(self.get_max_point())

    def set_current_point(self, value):
        self.UCPoint = value

    def bo_chon(self):
        self.Choose = False
        self.set_current_point(0)


class Activity(BaseModel):
    AID: int
    ACode: str
    AName: str
    AType: str
    ADesc: str
    StartTime: datetime
    FinishTime: datetime
    APlace: str
    GId: int
    GName: str
    AGId: int
    Data: str
    CreateDate: datetime
    CreateUser: str
    AStatus: int
    UAStatus: UAStatusClass
    ARefId: str
    ACriteriaLst: str
    AGDesc: str
    UserRole: int
    Publish: int
    Avatar: str
    Deadline: datetime
    CriteriaLst: List[Criteria]
    Signature: str


class ActivityView(ActivityId):
    AName: str
    StartTime: datetime
    FinishTime: datetime
    CriteriaLst: List[CriteriaView] = None
    UAStatus: UAStatusClass


class CriteriaGroup(PointCal):
    CGId: int
    CGName: str
    CGMaxPoint: int  # moi sua
    UserCriteriaDetailsLst: List[CriteriaView]

    def get_max_point(self):
        return max(0, self.CGMaxPoint)

    def re_caculate_current_point(self):
        self.CurrentPoint = min(sum([cv.get_current_point() for cv in self.UserCriteriaDetailsLst]),
                                self.get_max_point())


class CriteriaType(PointCal):
    CTId: int
    CTName: str
    CTPoint: int
    CTMaxPoint: int
    CriteriaGroupDetailsLst: List[CriteriaGroup]

    def get_max_point(self):
        return max(0, self.CTMaxPoint)

    def re_caculate_current_point(self):
        self.CurrentPoint = min(sum([cg.get_current_point() for cg in self.CriteriaGroupDetailsLst]),
                                self.get_max_point())


class ActivityViewAlgo(ActivityView):
    currentCriteria: Optional[CriteriaView]

    def get_length_clist(self):
        return len(self.CriteriaLst)

    def set_criteria(self, index):
        assert index < self.get_length_clist()
        self.currentCriteria = self.CriteriaLst[index]
        self.currentCriteria.chon()

    def reset_criteria(self, index, value):
        assert index < self.get_length_clist()
        self.currentCriteria.set_current_point(value)


class ActivitiesLst(BaseModel):
    __root__: List[ActivityViewAlgo]

    def reassign_criteria(self, criteria_dict: Dict[int, CriteriaView]) -> None:
        for activity in self.__root__:
            new_list = []
            for criteria in activity.CriteriaLst:
                if criteria.CId in criteria_dict.keys():
                    new_list.append(criteria_dict[criteria.CId])
            activity.CriteriaLst = new_list

    def add_activity(self, a: object) -> None:
        if a not in self.__root__:
            self.__root__.append(a)

    def get_activities_lst(self):
        return self.__root__

    def sort(self, key=None, reverse: bool = False):
        self.__root__.sort(key=key, reverse=reverse)

    def get_length(self):
        return len(self.__root__)

    def get(self, index: int):
        assert index < self.get_length()
        return self.__root__[index]


class DRL(PointCal):
    CriteriaTypeDetailsLst: List[CriteriaType]
    MaxPoint: int = 100

    def re_caculate_current_point(self):
        self.CurrentPoint = min(sum([ct.get_current_point() for ct in self.CriteriaTypeDetailsLst]),
                                self.get_max_point())

    def get_max_point(self):
        return self.MaxPoint

    def get_CId_lst(self):
        cid_list = []
        for ctype in self.CriteriaTypeDetailsLst:
            for cgroup in ctype.CriteriaGroupDetailsLst:
                for criteria in cgroup.UserCriteriaDetailsLst:
                    cid_list.append(criteria.CId)
        return cid_list

    def assignActivities(self, a_list: ActivitiesLst):
        criteria_dict = {}
        for ctype in self.CriteriaTypeDetailsLst:
            for cgroup in ctype.CriteriaGroupDetailsLst:
                for criteria in cgroup.UserCriteriaDetailsLst:
                    criteria_dict[criteria.CId] = criteria
        a_list.reassign_criteria(criteria_dict)
