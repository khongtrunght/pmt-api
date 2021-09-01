import asyncio
from abc import abstractmethod
from typing import List

import uplink
from uplink.auth import ApiTokenHeader

from hust.ctsv.algo.algorithm import Algorithm
from hust.ctsv.consumer.student import Student
from hust.ctsv.schemas.request_schemas import RqtActivityUserCId, RqtMarkCriteria, RqtCriteria
from hust.ctsv.schemas.schemas import DRL, ActivityViewAlgo, ActivitiesLst
from hust.exceptions.error_code import ErrorCode
from hust.exceptions.exceptions import InvalidTokenException, HetHanDrlException


class InfoGet:
    @abstractmethod
    def initiallize(self):
        pass

    def __init__(self, user: RqtCriteria):
        self.user: RqtCriteria = user
        self.api: Student
        self.syncApi: Student
        self.rootDRL = DRL.parse_file("resources/drl.json")
        self.initiallize()

    async def get_list_of_activities_id(self, cid_lst: List[int]):

        user_copy_cid = RqtActivityUserCId(**self.user.dict())
        out_put = []

        sem = asyncio.Semaphore(30)

        async def safe_fetch(id):
            async with sem:
                user_copy_cid.CId = id
                temp_criteria = await self.api.get_activity_by_cid(user_copy_cid)
                # raise errror 104 dang nhap het han
                if temp_criteria.RespCode == ErrorCode.HET_HAN_DANG_NHAP :
                    raise InvalidTokenException(f"Lay thong tin khong thanh cong : {temp_criteria.RespText}", temp_criteria)
                elif temp_criteria.RespCode == ErrorCode.TIEU_CHI_NOT_EXIST:
                    raise HetHanDrlException(f"Tieu chi {id} khong ton tai")
                for ac in temp_criteria.Activities:
                    out_put.append(ac.AId)
                return temp_criteria

        tasks = [asyncio.ensure_future(safe_fetch(id)) for id in cid_lst]

        rsp = await asyncio.gather(*tasks)
        return out_put

    async def get_list_of_activities(self, cid_lst: List[int]):
        id_lst = await self.get_list_of_activities_id(cid_lst)
        activities_lst = ActivitiesLst(__root__=[])
        tasks = [self.api.get_activity_by_id({**self.user.dict(), 'AId': id}) for id in id_lst]
        resps = await asyncio.gather(*tasks)
        for activity in resps:
            a = activity.Activities[0]
            activities_lst.add_activity(ActivityViewAlgo(**a.dict()))
        return activities_lst

    async def mark_criteria(self, algo:Algorithm):
        a_list = await self.get_list_of_activities(self.rootDRL.get_CId_lst())
        drl = algo.run(self.rootDRL, a_list)
        mark_criteria = RqtMarkCriteria(**drl.dict(), **self.user.dict())
        mark_criteria = mark_criteria.json().encode('utf-8')
        rsp = self.syncApi.mark_criteria_user(mark_criteria)


class BearerInfoGet(InfoGet):
    def initiallize(self):
        token_auth = ApiTokenHeader("Authorization",
                                    self.user.TokenCode)
        self.api = Student(base_url="https://ctsv.hust.edu.vn/", auth=token_auth, client=uplink.AiohttpClient())
        self.syncApi = Student(base_url="https://ctsv.hust.edu.vn/", auth=token_auth)


class NonBearerInfoGet(InfoGet):
    def initiallize(self):
        self.api = Student(base_url="https://ctsv.hust.edu.vn/", client=uplink.AiohttpClient())
        self.syncApi = Student(base_url="https://ctsv.hust.edu.vn/")
