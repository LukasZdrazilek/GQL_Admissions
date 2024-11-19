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
    from .AdmissionGQLModel import admission_insert
    admission_insert = admission_insert

    from .ExamTypeGQLModel import exam_type_insert
    exam_type_insert = exam_type_insert


schema = strawberry.federation.Schema(
    query=Query,
    mutation=Mutation,
)