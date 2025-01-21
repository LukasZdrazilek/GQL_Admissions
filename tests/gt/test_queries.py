import pytest
import logging
from .gt_utils import (
    createByIdTest2,
    createUpdateTest2,
    createTest2,
    createDeleteTest2,
    getQuery
)

# Initial Environment Validation
myquery = """
{
  me {
    id
    fullname
    email
    roles {
      valid
      group { id name }
      roletype { id name }
    }
  }
}"""

@pytest.mark.asyncio
async def test_result_test(NoRole_UG_Server):
    response = await NoRole_UG_Server(query=myquery, variables={})
    assert "data" in response, f"Expected 'data' in response, got: {response}"
    assert response["data"]["me"] is not None, "Expected 'me' field in response data"
    logging.info(f"User data: {response}")

######################################################################### Admission CRUD Tests

# Create Admission
test_admission_create = createTest2(    # v query pak nastavit povinne program ID !
    tableName="admissions",
    queryName="create",
    variables={
        #"id": "123e4567-e89b-12d3-a456-426614174002",
        "name": "Projektovy den",
        "name_en": "Project day",
        "program_id": "456e7890-e12d-34b5-b678-426614171111",
        "application_start_date": "2024-01-01T09:00:00",
        "application_last_date": "2024-01-01T09:00:00",
        "end_date": "2024-01-01T09:00:00",
        "condition_date": "2024-01-01T09:00:00",
        "request_condition_start_date": "2024-01-01T09:00:00",
        "request_condition_last_date": "2024-01-01T09:00:00",
        "request_exam_start_date": "2024-01-01T09:00:00",
        "request_exam_last_date": "2024-01-01T09:00:00",
        "payment_date": "2024-01-01T09:00:00",
        "request_enrollment_start_date": "2024-01-01T09:00:00",
        "request_enrollment_end_date": "2024-01-01T09:00:00"
    }
)

# Read Admission by ID
test_admission_by_id = createByIdTest2(tableName="admissions")

# Update Admission
test_admission_update = createUpdateTest2(      # povinne parametry update
    tableName="admissions",
    variables={
        #"lastchange": "2024-12-09T09:44:37.262687",
        #"id": "123e4567-e89b-12d3-a456-426614174001",
        "name": "Projektovy den updated",
        "name_en": "Project day updated",
        "program_id": "456e7890-e12d-34b5-b678-426614171111",
        "application_start_date": "2024-01-01T09:00:00",
        "application_last_date": "2024-01-01T09:00:00",
        "end_date": "2024-01-01T09:00:00",
        "condition_date": "2024-01-01T09:00:00",
        "request_condition_start_date": "2024-01-01T09:00:00",
        "request_condition_last_date": "2024-01-01T09:00:00",
        "request_exam_start_date": "2024-01-01T09:00:00",
        "request_exam_last_date": "2024-01-01T09:00:00",
        "payment_date": "2024-01-01T09:00:00",
        "request_enrollment_start_date": "2024-01-01T09:00:00",
        "request_enrollment_end_date": "2024-01-01T09:00:00"
    }
)

# Delete Admission
test_admission_delete = createDeleteTest2(      # povinne parametry jako v create - ne id a lastchange
    tableName="admissions",
    variables={
        #"id": "123e4567-e89b-12d3-a456-426614174002",       ###### PROZATIM TAM HODIT ID DO DELETU #######
        "name": "Projektovy den deleted",
        "name_en": "Project day deleted",
        "program_id": "456e7890-e12d-34b5-b678-426614171111",
        "application_start_date": "2024-01-01T09:00:00",
        "application_last_date": "2024-01-01T09:00:00",
        "end_date": "2024-01-01T09:00:00",
        "condition_date": "2024-01-01T09:00:00",
        "request_condition_start_date": "2024-01-01T09:00:00",
        "request_condition_last_date": "2024-01-01T09:00:00",
        "request_exam_start_date": "2024-01-01T09:00:00",
        "request_exam_last_date": "2024-01-01T09:00:00",
        "payment_date": "2024-01-01T09:00:00",
        "request_enrollment_start_date": "2024-01-01T09:00:00",
        "request_enrollment_end_date": "2024-01-01T09:00:00"
    }
)

# # Custom Tests
# @pytest.mark.asyncio
# async def test_admission_invalid_date_range(SchemaExecutorDemo):
#     variables = {
#         "name": "Admission with Invalid Dates",
#         "application_start_date": "2024-41-11100:00:00",
#         "application_last_date": "2024-41-11100:00:00"
#     }
#     query = getQuery(tableName="admissions", queryName="create")
#     response = await SchemaExecutorDemo(query=query, variable_values=variables)
#     assert "errors" in response, f"Expected errors for invalid date range: {response}"

    ################################################################################## Exam CRUD Tests

    # Create Exam
test_exam_create = createTest2(
    tableName="exams",
    queryName="create",
    variables={
        #"id": "d21a1c6b-5e8f-4b6d-933f-918d39e5e1e6",
        "name": "Projektovy den zkouska",
        "name_en": "Project day exam",
        "exam_date": "2025-03-05T23:59:59",
        "exam_type_id": "f4b3a1fa-3b1e-42bc-bd2d-ef234d7b7c61",
    }
)

# Read Exam by ID
test_admission_by_id = createByIdTest2(tableName="admissions")

# Update Exam
test_exam_update = createUpdateTest2(
    tableName="exams",
    variables={
        #"id": "d21a1c6b-5e8f-4b6d-933f-918d39e5e1e6",
        #"lastchange": "2024-12-03T19:35:59.180099",
        "name": "Projektovy den zkouska updated",
        "name_en": "Project day exam updated",
        "exam_date": "2025-03-05T23:59:59",
        "exam_type_id": "7b0d8b9f-2f4f-45fd-b7d5-ec3e2d4b5b29"
    }
)

# Delete Exam
test_exam_delete = createDeleteTest2(
    tableName="exams",
    variables={
        #"id": "d21a1c6b-5e8f-4b6d-933f-918d39e5e1e6",
        "name": "Projektovy den zkouska deleted",
        "name_en": "Project day exam deleted",
        "exam_date": "2025-03-05T23:59:59",
        "exam_type_id": "f4b3a1fa-3b1e-42bc-bd2d-ef234d7b7c61",
    }
)

# @pytest.mark.asyncio
# async def test_exam_invalid_exam_type(SchemaExecutorDemo):
#     variables = {
#         "name": "Invalid Type Exam",
#         "exam_date": "2024-03-15T10:00:00",
#         "exam_type_id": "1a1bc900-aaaa1-bbbb-cccc-1d9237aae24d"
#     }
#     query = getQuery(tableName="exams", queryName="create")
#     response = await SchemaExecutorDemo(query=query, variable_values=variables)
#     assert "errors" in response, f"Expected errors for invalid exam type: {response}"

# @pytest.mark.asyncio
# async def test_exam_delete_with_results(SchemaExecutorDemo):
#     tableName = "exams"
#     variables = {
#         "id": "d21a1c6b-5e8f-4b6d-933f-918d39e5e1e5",
#         "lastchange": "2024-03-15T10:00:00"
#     }

#     queryRead = getQuery(tableName=tableName, queryName="read")
#     responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": variables["id"]})
#     exam = responseJson.get("data", {}).get("result")
#     assert exam is not None, f"Exam not found: {responseJson}"

#     assert len(exam["examResults"]) > 0, "Expected exam to have results but found none"

#     queryDelete = getQuery(tableName=tableName, queryName="delete")
#     responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
#     assert "errors" in responseJson, "Exam with results should not be deletable"
#     logging.info(f"Delete attempt failed as expected: {responseJson}")

    ########################################################################## Exam Results CRUD Tests

    # Exam Results Tests
test_exam_result_create = createTest2(
    tableName="exam_results",
    queryName="create",
    variables={
        #"id": "1a1bc900-8b48-4a88-883c-1d9237aae24d",
        "score": 95.5,
        "exam_id": "a15d2b5f-3e0f-4f9e-8f1e-9d3a2c2c8b3f",
        "student_admission_id": "89b10735-ef94-49d4-965f-fbd475d65d1f"
    }
)

test_exam_result_by_id = createByIdTest2(
    tableName="exam_results"
)

test_exam_result_update = createUpdateTest2(
    tableName="exam_results",
    variables={
        #"id": "1a1bc900-8b48-4a88-883c-1d9237aae24d",
        #"lastchange": "2024-03-15T10:00:00",
        "score": 69.0,
        "exam_id": "a15d2b5f-3e0f-4f9e-8f1e-9d3a2c2c8b3f",
        "student_admission_id": "89b10735-ef94-49d4-965f-fbd475d65d1f"
    }
)

test_exam_result_delete = createDeleteTest2(
    tableName="exam_results",
    variables={
        #"id": "1a1bc900-8b48-4a88-883c-1d9237aae25d",
        "score": 95.5,
        "exam_id": "a15d2b5f-3e0f-4f9e-8f1e-9d3a2c2c8b3f",
        "student_admission_id": "89b10735-ef94-49d4-965f-fbd475d65d1f"
    }
)

# @pytest.mark.asyncio
# async def test_exam_result_relationships(SchemaExecutorDemo):
#     exam_result_id = "1a1bc900-8b48-4a88-883c-1d9237aae24d"
#     query = getQuery(tableName="exam_results", queryName="read")
#     responseJson = await SchemaExecutorDemo(query=query, variable_values={"id": exam_result_id})
#     result = responseJson.get("data", {}).get("result")
#     assert result is not None, f"ExamResult not found: {responseJson}"
#     assert result["exam"] is not None, f"Expected exam relationship, found: {result['exam']}"
#     assert result["studentAdmission"] is not None, f"Expected studentAdmission relationship, found: {result['studentAdmission']}"

# @pytest.mark.asyncio
# async def test_exam_result_delete_restricted(SchemaExecutorDemo):
#     variables = {
#         "id": "1a1bc900-8b48-4a88-883c-1d9237aae24c",
#         "lastchange": "2024-03-15T10:00:00"
#     }
#     queryDelete = getQuery(tableName="exam_results", queryName="delete")
#     responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
#     assert "errors" in responseJson, "Expected deletion to fail due to dependencies"
#     logging.info(f"Deletion restricted as expected: {responseJson}")

# @pytest.mark.asyncio
# async def test_exam_result_invalid_foreign_keys(SchemaExecutorDemo):
#     variables = {
#         "score": 90.0,
#         "exam_id": "1a1bc900-8b48-4a88-883c-1d9237aae24c",
#         "student_admission_id": "1a1bc900-aaaa-bbbb-cccc-1d9237aae24c"
#     }
#     queryCreate = getQuery(tableName="exam_results", queryName="create")
#     responseJson = await SchemaExecutorDemo(query=queryCreate, variable_values=variables)
#     assert "errors" in responseJson, f"Expected errors for invalid foreign keys: {responseJson}"

    ############################################################################## Exam Types CRUD Tests

# Exam Types Tests
test_exam_type_create = createTest2(
    tableName="exam_types",
    queryName="create",
    variables={
        #"id": "7b0d8b9f-2f4f-45fd-b7d5-ec3e2d4b5b20",
        "name": "Midterm Exam Type",
        "name_en": "Midterm Exam Type EN",
        "min_score": 50.0,
        "max_score": 100.0,
        "admission_id": "123e4567-e89b-12d3-a456-426614174000"
    }
)

test_exam_type_by_id = createByIdTest2(
    tableName="exam_types"
)

test_exam_type_update = createUpdateTest2(
    tableName="exam_types",
    variables={
        #"id": "7b0d8b9f-2f4f-45fd-b7d5-ec3e2d4b5b20",
        #"lastchange": "2024-01-01T00:00:00",
        "name": "Updated Exam Type",
        "name_en": "Updated Exam Type EN",
        "min_score": 55.0,
        "max_score": 95.0
    }
)

test_exam_type_delete = createDeleteTest2(
    tableName="exam_types",
    variables={
        #"id": "7b0d8b9f-2f4f-45fd-b7d5-ec3e2d4b5b20",
        "name": "Midterm Exam Type",
        "name_en": "Midterm Exam Type EN",
        "min_score": 50.0,
        "max_score": 100.0,
        "admission_id": "123e4567-e89b-12d3-a456-426614174000"
    }
)

# @pytest.mark.asyncio
# async def test_exam_type_admission_relationship(SchemaExecutorDemo):
#     tableName = "exam_types"
#     entity_id = "e19b1d5c-7e29-4f38-a609-abc2d233a842"

#     queryRead = getQuery(tableName=tableName, queryName="read")
#     responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
#     result = responseJson.get("data", {}).get("result")
#     assert result is not None, f"ExamType not found: {responseJson}"
#     admission = result.get("admission")
#     assert admission is not None, f"Expected admission relationship, found: {admission}"

# @pytest.mark.asyncio
# async def test_exam_type_delete_with_exams(SchemaExecutorDemo):
#     tableName = "exam_types"
#     entity_id = "e19b1d5c-7e29-4f38-a609-abc2d233a842"

#     variables = {
#         "id": entity_id,
#         "lastchange": "2024-01-01T00:00:00"  # Placeholder
#     }
#     queryDelete = getQuery(tableName=tableName, queryName="delete")
#     responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
#     assert "errors" in responseJson, "Expected deletion to fail due to linked exams"


    ############################################################################ Student Admissions CRUD Tests

# Student Admissions Tests
test_student_admission_create = createTest2(
    tableName="student_admissions",
    queryName="create",
    variables={
        #"id": "d2815b9c-75ee-4d2e-9c8a-ffc8df088136",
        "admission_id": "123e4567-e89b-12d3-a456-426614174000",
        "student_id": "51d101a0-81f1-44ca-8366-6cf51432e8d6",
        "extended_condition_date": "2024-03-20T10:00:00",
        "admissioned": True,
        "enrollment_date": "2024-03-25T10:00:00"
    }
)

test_student_admission_by_id = createByIdTest2(
    tableName="student_admissions"
)

test_student_admission_update = createUpdateTest2(
    tableName="student_admissions",
    variables={
        #"id": "d2815b9c-75ee-4d2e-9c8a-ffc8df088136",
        #"lastchange": "2024-01-01T00:00:00",
        "admission_id": "123e4567-e89b-12d3-a456-426614174000",
        "extended_condition_date": "2024-04-01T10:00:00",
        "admissioned": False,
        "enrollment_date": "2024-04-05T10:00:00"
    }
)

test_student_admission_delete = createDeleteTest2(
    tableName="student_admissions",
    variables={
        #"id": "d2815b9c-75ee-4d2e-9c8a-ffc8df088137",
        "admission_id": "123e4567-e89b-12d3-a456-426614174001",
        "student_id": "51d101a0-81f1-44ca-8366-6cf51432e8d7",
        "extended_condition_date": "2024-03-20T10:00:00",
        "admissioned": True,
        "enrollment_date": "2024-03-25T10:00:00"
    }
)

# @pytest.mark.asyncio
# async def test_student_admission_admission_relationship(SchemaExecutorDemo):
#     tableName = "student_admissions"
#     entity_id = "d2815b9c-75ee-4d2e-9c8a-ffc8df088135"

#     queryRead = getQuery(tableName=tableName, queryName="read")
#     responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
#     result = responseJson.get("data", {}).get("result")
#     assert result is not None, f"StudentAdmission not found: {responseJson}"
#     admission = result.get("admission")
#     assert admission is not None, f"Expected admission relationship, found: {admission}"

# _

# @pytest.mark.asyncio
# async def test_student_admission_exams_and_results(SchemaExecutorDemo):
#     tableName = "student_admissions"
#     entity_id = "d2815b9c-75ee-4d2e-9c8a-ffc8df088135"

#     queryRead = getQuery(tableName=tableName, queryName="read")
#     responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
#     result = responseJson.get("data", {}).get("result")
#     assert result is not None, f"StudentAdmission not found: {responseJson}"

#     exams = result.get("exams", [])
#     assert len(exams) > 0, "Expected at least one linked exam"
#     logging.info(f"Linked exams: {exams}")

#     examResults = result.get("examResults", [])
#     assert len(examResults) > 0, "Expected at least one exam result"
#     logging.info(f"Exam results validated: {examResults}")
