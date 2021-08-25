from hust.ctsv.schemas.request_schemas import *
from hust.ctsv.schemas.response_schemas import RspCriteriaTypeDetails, RspActivityView
from uplink import Consumer, Body, post, headers
from uplink.auth import BearerToken

br = BearerToken(
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCIsImtpZCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCJ9.eyJhdWQiOiJodHRwczovL2N0c3YuaHVzdC5lZHUudm4iLCJpc3MiOiJodHRwczovL2Fzc28uaHVzdC5lZHUudm4vYWRmcyIsImlhdCI6MTYyNjc4ODgyMSwiZXhwIjoxNjI2NzkyNDIxLCJhdXRoX3RpbWUiOjE2MjY3ODg4MjEsIm5vbmNlIjoiODI0ZDM1OTctYWVmZS00OTQzLWI1MWYtMmU5NTA4M2VjODIzIiwic3ViIjoiWWpNc25GNG9yS2NBemcwcS9oMzU1L0J1bVZRSExtSXNiN3FJKzQwVkx0MD0iLCJ1cG4iOiJ0aGFuZy5scTE5NDgzOEBzaXMuaHVzdC5lZHUudm4iLCJ1bmlxdWVfbmFtZSI6IkhVU1RcXFRIQU5HLkxRMTk0ODM4IiwicHdkX3VybCI6Imh0dHBzOi8vYXNzby5odXN0LmVkdS52bi9hZGZzL3BvcnRhbC91cGRhdGVwYXNzd29yZC8iLCJzaWQiOiJTLTEtNS0yMS0yNzQ2MjUxMDA3LTEzMjQ1OTUyMDYtNzgxNjU0MzUxLTY3Mzg0In0.LZKZnejGHjvxc8VbbUaE--CLvYSRA8vn6iVzi0zRtCUyW0kHqxdQMRyXXLtLA0iAvtGFlOi1CUfWuYPZ3eJiSGEbDWn086XQEUIxqGpWHH9lQ2tGHHeibZE68SfkLXWvkg6Qc1DRIGs2-mBu-172mnwglOvvB8YS3s4HOkeKpjekQ8AMKsj664EjNyeh57srCOl-qQrhy5DPhIOLuFMawIeZ_Fp_9jmZShtAuFSSfuN8grrih576Q8Igo6RyDtz4wPXAvVJP6jrGxIEht8jfavnvyyUOxqTYwRkBGzH3vdm3MQ_5hexm8wi9ghg5QAHnw3ltOOpxyFHL7O3AOlRBjw")


class Student(Consumer):

    @post("api-t/Activity/GetActivityById")
    def get_activity_by_id(self, user: Body(type=RqtActivity)) -> RspActivityView:
        """Get detail info for an activity by id"""

    @post("api-t/Activity/GetActivityByCId")
    def get_activity_by_cid(self, user: Body(type=RqtActivityUserCId)) -> RspActivityView:
        pass

    @headers({
        "Content-Type": "application/json; charset=UTF-8",
        # "Accept-Language": "vi,vi-VN;q=0.9,en-US;q=0.8,en;q=0.7,fr-FR;q=0.6,fr;q=0.5"
    })
    @post("api-t/Point/MarkCriteriaUser")
    def mark_criteria_user(self, mark_criteria: Body()):
        pass

    @post("api-t/Criteria/GetCriteriaTypeDetails")
    def get_criteria_type_details(self, user: Body(type=RqtCriteria)) -> RspCriteriaTypeDetails:
        pass

    @post("api-t/Activity/GetActivityByUser")
    def get_activity_by_user(self, user_activity: Body(type=RqtActivityUser)) -> RspActivityView:
        pass

    @post("api-t/User/GetUserInfo")
    def get_user_info(self, user: Body):
        pass
