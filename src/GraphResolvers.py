from typing import Coroutine, Callable, Awaitable, Union, List
import uuid
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from uoishelpers.resolvers import (
    create1NGetter,
    createEntityByIdGetter,
    createEntityGetter,
    createInsertResolver,
    createUpdateResolver,
)
from uoishelpers.resolvers import putSingleEntityToDb

from src.DBDefinitions import BaseModel


from src.DBDefinitions import (
    AdmissionModel,
    DisciplineModel,
    DisciplineTypeModel,
    ExamModel,
    ExamTypeModel,
    StudentAdmissionModel,
)

# Admission resolvers
resolveAdmissionById = createEntityByIdGetter(AdmissionModel)
resolveAdmissionAll = createEntityGetter(AdmissionModel)
resolveUpdateAdmission = createUpdateResolver(AdmissionModel)
resolveInsertAdmission = createInsertResolver(AdmissionModel)

resolveStudentAdmissionsForAdmission = create1NGetter(
    StudentAdmissionModel, foreignKeyName="admission_id"
)

resolveExamTypeForAdmission = create1NGetter(
    ExamTypeModel, foreignKeyName="admission_id")

# StudentAdmission resolvers
resolveStudentAdmissionById = createEntityByIdGetter(StudentAdmissionModel)
resolveStudentAdmissionAll = createEntityGetter(StudentAdmissionModel)
resolveUpdateStudentAdmission = createUpdateResolver(StudentAdmissionModel)
resolveInsertStudentAdmission = createInsertResolver(StudentAdmissionModel)

resolveExamForStudentAdmission = create1NGetter(
    ExamModel, foreignKeyName="studentadmission_id"
)