from hust.ctsv.algo.backtracking import Backtracking, PrintExportor
from hust.ctsv.algo.bipartite import Bipartite
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
    a_list = cham.get_list_of_activities(drl.get_CId_lst())
    algorithm = Bipartite(drl, a_list)
    algorithm.optimize()

    cham.mark_criteria(algorithm.get_drl_optimal())

    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()
    return printExportor.drl.get_current_point()
#     # mark_criteria("20194461")


if __name__ == '__main__':
    test('20194417', token='Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCIsImtpZCI6IlllRjZtZWZoWVM1ZmpLYXk4QlByNEhHVDRBMCJ9.eyJhdWQiOiJodHRwczovL2N0c3YuaHVzdC5lZHUudm4iLCJpc3MiOiJodHRwczovL2Fzc28uaHVzdC5lZHUudm4vYWRmcyIsImlhdCI6MTYzMDA4MTI3NSwiZXhwIjoxNjMwMDg0ODc1LCJhdXRoX3RpbWUiOjE2MzAwNjQ5MTMsIm5vbmNlIjoiOTBiZWE2MmUtYmI4ZS00MjhkLTk4NDctNTkzYTZlOTJhZmI0Iiwic3ViIjoicEVGVEh3dWp5QVNaWkt0T0g3UHl5K3ZLQTNnUWVHazJ4dFdTdFNJNmJsbz0iLCJ1cG4iOiJhbmgubmgxOTQ0MTdAc2lzLmh1c3QuZWR1LnZuIiwidW5pcXVlX25hbWUiOiJIVVNUXFxBTkguTkgxOTQ0MTciLCJwd2RfdXJsIjoiaHR0cHM6Ly9hc3NvLmh1c3QuZWR1LnZuL2FkZnMvcG9ydGFsL3VwZGF0ZXBhc3N3b3JkLyIsInNpZCI6IlMtMS01LTIxLTI3NDYyNTEwMDctMTMyNDU5NTIwNi03ODE2NTQzNTEtNjY5NjMifQ.o3-WbK34oxmqGN-CwewrZr7wZqoNtX0IX4SG3O8ZtqfyR-pDGMSwVo7-LGqgQhkCQb8CDbUVTKdCw52UwQk0S7-FFPcC9ZlzgPXfCcfvz4Nb7iD724TlpQDgX4Qe723QMcCXPdjs6mVkpDgDeMIaGkE3m9CJhl1kDkgX1-7i5jomEn59Ap42312BNhDNCG6ElR8L5B4efzN7bt5TqRH2VvnXLIktFkqkHQGc3UiIsA3x1j5N_-g45jrlZtMbhs7yKAQnJmYvsY8Mc6jQs2-oC6bwi6pWG10WtJDSdZaOJqdHu--efKc1icDDFrMNg08EwWNaqLY5s4JygPvASbr8nw', semester='2020-2')