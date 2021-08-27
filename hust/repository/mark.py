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
    # printExportor.print()
    return printExportor.drl.get_current_point()
#     # mark_criteria("20194461")


# if __name__ == '__main__':
#     test('20194461', token='30EC875C0B463D0DF4EC1974AEC6E6E4', semester='2020-2')