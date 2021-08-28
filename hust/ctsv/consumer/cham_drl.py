import asyncio
from abc import abstractmethod
from typing import List

import uplink

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

    async def get_list_of_activities_id(self, cid_lst: List[int]):

        user_copy_cid = RqtActivityUserCId(**self.user.dict())
        out_put = []

        sem = asyncio.Semaphore(3)

        async def safe_fetch(id):
            async with sem:
                user_copy_cid.CId = id
                return await self.api.get_activity_by_cid(user_copy_cid)

        tasks = [asyncio.ensure_future(safe_fetch(id)) for id in cid_lst]


        rsp = await asyncio.gather(*tasks)
        print(rsp)
        for criteria in rsp:
            if len(criteria.Activities) > 0:
                out_put.append(criteria.Activities[0].AId)
        return out_put

    async def get_list_of_activities(self, cid_lst: List[int]):
        # tasks = []
        id_lst = await self.get_list_of_activities_id(cid_lst)
        print(id_lst)
        activities_lst = ActivitiesLst(__root__=[])
        # for id in id_lst:
        #     tasks.append(asyncio.create_task(self.api.get_activity_by_id({**self.user.dict(), 'AId': id})))

        tasks = [self.api.get_activity_by_id({**self.user.dict(), 'AId': id}) for id in id_lst]
        resps = await asyncio.gather(*tasks)
        for activity in resps:
            a = activity.Activities[0]
            activities_lst.add_activity(ActivityViewAlgo(**a.dict()))
        return activities_lst

    def mark_criteria(self, drl: DRL):
        mark_criteria = RqtMarkCriteria(**drl.dict(), **self.user.dict())
        mark_criteria = mark_criteria.json().encode('utf-8')
        self.api.mark_criteria_user(mark_criteria)


class BearerInfoGet(InfoGet):
    def initiallize(self):
        token_auth = ApiTokenHeader("Authorization",
                                    self.user.TokenCode)
        self.api = Student(base_url="https://ctsv.hust.edu.vn/", auth=token_auth, client=uplink.AiohttpClient())



class NonBearerInfoGet(InfoGet):
    def initiallize(self):
        self.api = Student(base_url="https://ctsv.hust.edu.vn/", client=uplink.AiohttpClient())
