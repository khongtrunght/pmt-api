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

    # algorithm = Bipartite()
    algorithm = Backtracking()
    resp = await cham.mark_criteria(algorithm)
    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()

    if resp.RespCode != 0:
        raise ChamException("Co loi khi cham", resp)

    return printExportor.drl.get_current_point()




