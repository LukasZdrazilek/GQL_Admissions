import strawberry
from .AdmissionGQLModel import AdmissionGQLModel
from .BaseGQLModel import BaseGQLModel
from .ExamGQLModel import ExamGQLModel
from .ExamResultGQLModel import ExamResultGQLModel
from .ExamTypeGQLModel import ExamTypeGQLModel
from .StudentAdmissionGQLModel import StudentAdmissionGQLModel
from .PaymentInfoGQLModel import PaymentInfoGQLModel
from .PaymentGQLModel import PaymentGQLModel

from .AcProgramGQLModel import AcProgramGQLModel
from .FacilityGQLModel import FacilityGQLModel
from .GroupGQLModel import GroupGQLModel
from .StateGQLModel import StateGQLModel
from .UserGQLModel import UserGQLModel

@strawberry.type(description="""Type for query root""")
class Query:
    @strawberry.field(
        description="""Returns hello world"""
        )
    async def hello(
        self,
        info: strawberry.types.Info,
    ) -> str:
        return "hello world"

    from .AdmissionGQLModel import admission_by_id, admission_page
    admission_by_id = admission_by_id
    admission_page = admission_page

    from .StudentAdmissionGQLModel import student_admission_by_id, student_admission_page
    student_admission_by_id = student_admission_by_id
    student_admission_page = student_admission_page

    from .ExamTypeGQLModel import exam_type_by_id, exam_type_page
    exam_type_by_id = exam_type_by_id
    exam_type_page = exam_type_page

    from .ExamGQLModel import exam_by_id, exam_page
    exam_by_id = exam_by_id
    exam_page = exam_page

    from .ExamResultGQLModel import exam_result_by_id, exam_result_page
    exam_result_by_id = exam_result_by_id
    exam_result_page = exam_result_page

    from .PaymentInfoGQLModel import payment_info_by_id, payment_info_page
    payment_info_by_id = payment_info_by_id
    payment_info_page = payment_info_page

    from .PaymentGQLModel import payment_by_id, payment_page
    payment_by_id = payment_by_id
    payment_page = payment_page

@strawberry.type(description="""Type for mutation root""")
class Mutation:
    from .AdmissionGQLModel import admission_insert, admission_update, admission_delete
    admission_insert = admission_insert
    admission_update = admission_update
    admission_delete = admission_delete

    from .ExamTypeGQLModel import exam_type_insert, exam_type_update, exam_type_delete
    exam_type_insert = exam_type_insert
    exam_type_update = exam_type_update
    exam_type_delete = exam_type_delete

    from .ExamResultGQLModel import exam_result_insert, exam_result_update, exam_result_delete
    exam_result_insert = exam_result_insert
    exam_result_update = exam_result_update
    exam_result_delete = exam_result_delete
    
    from .ExamGQLModel import exam_insert, link_student_to_exam, exam_update, exam_delete
    exam_insert = exam_insert
    exam_update = exam_update
    exam_delete = exam_delete
    link_student_to_exam = link_student_to_exam

    from .StudentAdmissionGQLModel import student_admission_insert, student_admission_update, student_admission_delete
    student_admission_insert = student_admission_insert
    student_admission_update = student_admission_update
    student_admission_delete = student_admission_delete

    from .PaymentInfoGQLModel import payment_info_insert, payment_info_update, payment_info_delete
    payment_info_insert = payment_info_insert
    payment_info_update = payment_info_update
    payment_info_delete = payment_info_delete

    from .PaymentGQLModel import payment_insert, payment_update, payment_delete
    payment_insert = payment_insert
    payment_update = payment_update
    payment_delete = payment_delete

schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    types=[
        AcProgramGQLModel,
        FacilityGQLModel,
        GroupGQLModel,
        StateGQLModel,
        UserGQLModel
    ],
    extensions=[]
)

from uoishelpers.schema import WhoAmIExtension, ProfilingExtension, PrometheusExtension
schema.extensions.append(WhoAmIExtension)
# schema.extensions.append(ProfilingExtension())
# schema.extensions.append(PyInstrument())
# schema.extensions.append(PrometheusExtension(prefix="gql_facilities"))

from aiodataloader import DataLoader
import uuid


def getCacheKey(struct):
    return struct["id"]

class RBACLoader(DataLoader):
    def __init__(self, gqlclient):
        self.index = {}
        self.gqlclient = gqlclient
        super().__init__(
            get_cache_key=getCacheKey
        )

    async def batch_load_fn(self, structlist):
        index = {
            f'h{uuid.uuid4().hex}': item
            for item in structlist
        }
        lines = [
            f'{key}: rbacById(id: "{value["id"]}")'
            '{'
            f'judgement: userCanWithoutState(rolesNeeded: {value["roles"]})'
            '}'
            for key, value in index
        ]
        query = '{' + "\n".join(lines) + '}'
        gqlclient = self.gqlclient
        response = await gqlclient(query=query)
        assert "data" in response, f"get bad response while asking for RBAC {response}"
        responsedata = response["data"]
        result = [
            responsedata[key]["judgement"]
            for key in index.keys()
        ]
        return result

class RBACExtension(WhoAmIExtension):
    async def on_execute(self):
        self.execution_context.context["RBACLoader"] = RBACLoader(gqlclient=self.ug_query)

        # print("->on_execute", self.execution_context.query, flush=True)
        yield
        # print("on_execute->", whoami, flush=True)