from hust.ctsv.algo.backtracking import Backtracking, PrintExportor
from hust.ctsv.consumer.cham_drl import NonBearerInfoGet
from hust.ctsv.schemas.request_schemas import RqtCriteria
from hust.ctsv.schemas.schemas import DRL

TOKEN = ""
MSSV = ""


def non_bearer_mark(mssv, token, semester):
    user = RqtCriteria(TokenCode=token, UserName=mssv, Semester=semester)
    cham = NonBearerInfoGet(user)
    drl = DRL.parse_file('resources/drl.json')
    a_list = cham.get_list_of_activities(drl.get_CId_lst())
    algorithm = Backtracking(drl, a_list)
    algorithm.optimize()
    cham.mark_criteria(algorithm.get_drl_optimal())

    printExportor = PrintExportor()
    printExportor.store(algorithm.get_drl_optimal())
    printExportor.print()

    return printExportor.drl.get_current_point()




