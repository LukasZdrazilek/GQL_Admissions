import strawberry

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

    from .StudentAdmissionGQLModel import studentadmission_by_id, studentadmission_page
    studentadmission_by_id = studentadmission_by_id
    studentadmission_page = studentadmission_page

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
    
    from.ExamGQLModel import exam_insert, student_exam_link_add, exam_update, exam_delete
    exam_insert = exam_insert
    exam_update = exam_update
    exam_delete = exam_delete
    student_exam_link_add = student_exam_link_add

    from .StudentAdmissionGQLModel import student_admission_insert, student_admission_update, student_admission_delete
    student_admission_insert = student_admission_insert
    student_admission_update = student_admission_update
    student_admission_delete = student_admission_delete

schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
    extensions=[]
)

from uoishelpers.schema import WhoAmIExtension
schema.extensions.append(WhoAmIExtension)