import asyncio

from hust.ctsv.algo.backtracking import Backtracking, PrintExportor
from hust.ctsv.algo.bipartite import Bipartite
from hust.ctsv.consumer.cham_drl import NonBearerInfoGet, BearerInfoGet, InfoGet
from hust.ctsv.schemas.request_schemas import RqtCriteria
from hust.ctsv.schemas.schemas import DRL

TOKEN = ""
MSSV = ""


async def mark_criteria(mssv: str, token: str, semester: str):
    user = RqtCriteria(TokenCode=token, UserName=mssv, Semester=semester)
    cham: InfoGet
    if token.startswith("Bearer"):
        cham = BearerInfoGet(user)
    else:
        cham = NonBearerInfoGet(user)
    drl = DRL.parse_file("resources/drl.json")
    # a_list = asyncio.run(cham.get_list_of_activities(drl.get_CId_lst()))
    a_list = await cham.get_list_of_activities(drl.get_CId_lst())
    algorithm = Bipartite(drl, a_list)
    algorithm.optimize()
    cham.mark_criteria(algorithm.get_drl_optimal())

    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()

    return printExportor.drl.get_current_point()


def test(mssv: str, token: str, semester:str):
    user = RqtCriteria(TokenCode=token, UserName=mssv, Semester=semester)
    cham: InfoGet
    if token.startswith("Bearer"):
        cham = BearerInfoGet(user)
    else:
        cham = NonBearerInfoGet(user)
    drl = DRL.parse_file("../../resources/drl.json")
    a_list = asyncio.run(cham.get_list_of_activities(drl.get_CId_lst()))
    algorithm = Bipartite(drl, a_list)
    algorithm.optimize()

    cham.mark_criteria(algorithm.get_drl_optimal())

    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()
    return printExportor.drl.get_current_point()
#     # mark_criteria("20194461")


if __name__ == '__main__':
    import cProfile
    import pstats
    with cProfile.Profile() as profile:
        test('20194417', token='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCIsImtpZCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCJ9.eyJhdWQiOiJodHRwczovL2N0c3YuaHVzdC5lZHUudm4iLCJpc3MiOiJodHRwczovL2Fzc28uaHVzdC5lZHUudm4vYWRmcyIsImlhdCI6MTYzMDEzMTI0OCwiZXhwIjoxNjMwMTM0ODQ4LCJhdXRoX3RpbWUiOjE2MzAxMTI1NjUsIm5vbmNlIjoiMjJjNGE0MzktOGUyMS00Y2JlLTlmMjctNDVlYjE4MjdkYTJjIiwic3ViIjoicEVGVEh3dWp5QVNaWkt0T0g3UHl5K3ZLQTNnUWVHazJ4dFdTdFNJNmJsbz0iLCJ1cG4iOiJhbmgubmgxOTQ0MTdAc2lzLmh1c3QuZWR1LnZuIiwidW5pcXVlX25hbWUiOiJIVVNUXFxBTkguTkgxOTQ0MTciLCJwd2RfdXJsIjoiaHR0cHM6Ly9hc3NvLmh1c3QuZWR1LnZuL2FkZnMvcG9ydGFsL3VwZGF0ZXBhc3N3b3JkLyIsInNpZCI6IlMtMS01LTIxLTI3NDYyNTEwMDctMTMyNDU5NTIwNi03ODE2NTQzNTEtNjY5NjMifQ.myHNKKAVMBQ1aSoVCKQZAqlzgHWu9Ngxp8Ohj8OouqgDdgMOySNyH63kLc7viZklFBAVPmoO573pNsfx9xZpl2bPILtjmuMBrQ-Kw2hM7-9AMAXjN_nO5OTPVQwNwbnoAjpeIRUZ56PNEhufNWfVR2NSf5P1wURYRamMukGYbl1nBnWDCN6MwmAMttiMM0im4G9TjUtNkr5q4Vl6BtzGxqizJ1OdFJUbkK0DDC_QimDImt8c4Ngew9HooTKkUevENmF7p4z0THB8s0ApDigFmXrydCocELBojMJYRpYwQEr_7hZ_Z07cQNMMrRz92t-xCUM9IfjRJic6QzZHxsMWlQ', semester='2020-2')
        stats = pstats.Stats(profile).sort_stats('cumtime')
        stats.print_stats()