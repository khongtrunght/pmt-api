from hust.ctsv.algo.backtracking import Backtracking, PrintExportor
from hust.ctsv.consumer.cham_drl import NonBearerInfoGet, BearerInfoGet, InfoGet
from hust.ctsv.schemas.request_schemas import RqtCriteria
from hust.ctsv.schemas.schemas import DRL

TOKEN = ""
MSSV = ""


def mark_criteria(mssv: str, token: str, semester: str):
    user = RqtCriteria(TokenCode=token, UserName=mssv, Semester=semester)
    cham: InfoGet
    if token.startswith("Bearer"):
        cham = BearerInfoGet(user)
    else:
        cham = NonBearerInfoGet(user)
    drl = DRL.parse_file("resources/drl.json")
    a_list = cham.get_list_of_activities(drl.get_CId_lst())
    algorithm = Backtracking(drl, a_list)
    algorithm.optimize()
    cham.mark_criteria(algorithm.get_drl_optimal())

    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()

    return printExportor.drl.get_current_point()


# if __name__ == '__main__':
#     mark_criteria("20194838",
#                   "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCIsImtpZCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCJ9.eyJhdWQiOiJodHRwczovL2N0c3YuaHVzdC5lZHUudm4iLCJpc3MiOiJodHRwczovL2Fzc28uaHVzdC5lZHUudm4vYWRmcyIsImlhdCI6MTYzMDAyNDcyNSwiZXhwIjoxNjMwMDI4MzI1LCJhdXRoX3RpbWUiOjE2MzAwMjQ3MjUsIm5vbmNlIjoiOWU2NzRhMjItYTNmZS00MGY5LTg2YWMtZTgyMGI2ODI1NjlkIiwic3ViIjoiWWpNc25GNG9yS2NBemcwcS9oMzU1L0J1bVZRSExtSXNiN3FJKzQwVkx0MD0iLCJ1cG4iOiJ0aGFuZy5scTE5NDgzOEBzaXMuaHVzdC5lZHUudm4iLCJ1bmlxdWVfbmFtZSI6IkhVU1RcXFRIQU5HLkxRMTk0ODM4IiwicHdkX3VybCI6Imh0dHBzOi8vYXNzby5odXN0LmVkdS52bi9hZGZzL3BvcnRhbC91cGRhdGVwYXNzd29yZC8iLCJzaWQiOiJTLTEtNS0yMS0yNzQ2MjUxMDA3LTEzMjQ1OTUyMDYtNzgxNjU0MzUxLTY3Mzg0In0.BNhgPPOBsraHBZ785BVXKh9cC8ShDvrQGAn4qNWnp3nKebufGrdgIdwIxJO6o_b5pewkZTs-7gd9SYkXTD1-kshifmc22xZzdDaaULwBUKVpnGg0kziAsD6Q8rq6YjrdvSFCOzafAY7Aty_q8BrJR6evG4o5m1rC21FTObN2GPQeaiD1dAFkxYnu4z9KW_BHkClv0TBwDIxGHDES_PMLA76l8YRgWE5Ds8ErrU_uogFEAL8K7LhI6X8ALuNSQo1138qzcJngEDjVU6HoFc0281MW316gasz0m0wrCOon8srl9AqNBxA-j5Ibn146xKvE9DvOnVEVxqhk7J9NabKwRA",
#                   "2020-2")
#
#     # mark_criteria("20194461")
