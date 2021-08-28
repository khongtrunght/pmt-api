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
    test('20194417', token='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCIsImtpZCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCJ9.eyJhdWQiOiJodHRwczovL2N0c3YuaHVzdC5lZHUudm4iLCJpc3MiOiJodHRwczovL2Fzc28uaHVzdC5lZHUudm4vYWRmcyIsImlhdCI6MTYzMDEyNzUyMywiZXhwIjoxNjMwMTMxMTIzLCJhdXRoX3RpbWUiOjE2MzAxMTI1NjUsIm5vbmNlIjoiMjViODFjZGYtMDQzOS00YTdiLWE0NTQtMmE0NzhmMzZjNmEwIiwic3ViIjoicEVGVEh3dWp5QVNaWkt0T0g3UHl5K3ZLQTNnUWVHazJ4dFdTdFNJNmJsbz0iLCJ1cG4iOiJhbmgubmgxOTQ0MTdAc2lzLmh1c3QuZWR1LnZuIiwidW5pcXVlX25hbWUiOiJIVVNUXFxBTkguTkgxOTQ0MTciLCJwd2RfdXJsIjoiaHR0cHM6Ly9hc3NvLmh1c3QuZWR1LnZuL2FkZnMvcG9ydGFsL3VwZGF0ZXBhc3N3b3JkLyIsInNpZCI6IlMtMS01LTIxLTI3NDYyNTEwMDctMTMyNDU5NTIwNi03ODE2NTQzNTEtNjY5NjMifQ.c8cUVXV0yAMctcCYF8EyalR8uFtU7-BaydOHJVGYdLxQS6zIaxFZ3_qjoOvHWKKsPrl9fMvYN3rfru-itsa4tJvwbrV6E83WIhKYPJ8HZ8L0HT49-xPYT0B0Ld3g6a7ZYZzld_voHirsWKkayKUiRbHIJIkcIndKFsFQKvJ3hWSjseXAmRcRU3HDPItPkCeavg49lHinFNAONYd9I9y8biMVK0yFQdb68A8Lg87dbLbJxpAgYkOcThPveAS2T0aSbM3X5iMzU_-0h1P4mxdkl9gYfDRgmTmzPHjEDTPHJfN0MeufAp0NKXJUgtfo9wJwIWPmPgUkTeZNRbTpgcYknw', semester='2020-2')