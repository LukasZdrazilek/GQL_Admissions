import strawberry
from .AdmissionGQLModel import AdmissionGQLModel
from .BaseGQLModel import BaseGQLModel
from .ExamGQLModel import ExamGQLModel
from .ExamResultGQLModel import ExamResultGQLModel
from .ExamTypeGQLModel import ExamTypeGQLModel
from .StudentAdmissionGQLModel import StudentAdmissionGQLModel

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
    
    from.ExamGQLModel import exam_insert, link_student_to_exam, exam_update, exam_delete
    exam_insert = exam_insert
    exam_update = exam_update
    exam_delete = exam_delete
    link_student_to_exam = link_student_to_exam

    from .StudentAdmissionGQLModel import student_admission_insert, student_admission_update, student_admission_delete
    student_admission_insert = student_admission_insert
    student_admission_update = student_admission_update
    student_admission_delete = student_admission_delete

from uoishelpers.schema import WhoAmIExtension
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

schema.extensions.append(WhoAmIExtension)