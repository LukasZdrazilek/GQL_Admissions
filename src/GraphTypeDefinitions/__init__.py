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

    from .AdmissionGQLModel import admission_by_id
    admission_by_id = admission_by_id

    from .StudentAdmissionGQLModel import studentadmission_by_id
    studentadmission_by_id = studentadmission_by_id

    from .ExamTypeGQLModel import examType_by_id
    examType_by_id = examType_by_id

    from .ExamGQLModel import exam_by_id
    exam_by_id = exam_by_id

    from .ExamResultGQLModel import exam_result_by_id
    exam_result_by_id = exam_result_by_id

schema = strawberry.federation.Schema(
    query=Query
)