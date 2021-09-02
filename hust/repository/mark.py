import asyncio
from typing import Optional

from hust.ctsv.algo.backtracking import Backtracking, PrintExportor
from hust.ctsv.algo.bipartite import Bipartite
from hust.ctsv.consumer.cham_drl import NonBearerInfoGet, BearerInfoGet, InfoGet
from hust.ctsv.schemas.request_schemas import RqtCriteria
from hust.ctsv.schemas.response_schemas import Response
from hust.ctsv.schemas.schemas import DRL
from hust.exceptions.exceptions import ChamException

TOKEN = ""
MSSV = ""


async def mark_criteria(mssv: str, token: str, semester: Optional[str] = None):
    user = RqtCriteria(TokenCode=token, UserName=mssv, Semester=semester)
    cham: InfoGet
    if token.startswith("Bearer"):
        cham = BearerInfoGet(user)
    else:
        cham = NonBearerInfoGet(user)

    algorithm = Bipartite()
    # algorithm = Backtracking()
    resp = await cham.mark_criteria(algorithm)
    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()

    print("Resp: ", resp)

    if resp.RespCode != 0:
        raise ChamException("Co loi khi cham", resp)

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
        test('20194461', token='39DCA10DED133E960B1DCA6C719FBA2B', semester='2020-2')
        stats = pstats.Stats(profile).sort_stats('cumtime')
        stats.print_stats()