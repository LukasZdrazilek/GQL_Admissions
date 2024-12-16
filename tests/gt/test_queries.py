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


# MOZNA POUZIT NA ZISKANI LASTCHANGE U UPDATE A DELETE, ZATIM NEVIM JAK TO BUDE BRAT
async def get_lastchange(SchemaExecutorDemo, tableName, entity_id):
    """
    Fetch the latest 'lastchange' value for a given entity.
    This ensures the most up-to-date value is used for update or delete operations.
    
    :param SchemaExecutorDemo: The executor for sending GraphQL queries.
    :param tableName: The name of the table/model being queried.
    :param entity_id: The UUID of the entity whose 'lastchange' value is to be fetched.
    :return: The 'lastchange' value as a string.
    """
    queryRead = getQuery(tableName=tableName, queryName="read")
    response = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
    responseData = response.get("data", {})
    entity = responseData.get("result")
    assert entity is not None, f"Entity not found: {response}"
    lastchange = entity.get("lastchange")
    assert lastchange is not None, f"'lastchange' is missing in the fetched entity: {entity}"
    return lastchange


################################################################ Admission CRUD Tests

# Create Admission
test_admission_create = createTest2(
    tableName="admissions",
    queryName="create",
    variables={
        "name": "New Admission",
        "name_en": "New Admission EN",
        "state_id": "state-id",
        "program_id": "program-id",
        "application_start_date": "2024-01-01T00:00:00",
        "application_last_date": "2024-02-01T00:00:00",
        "end_date": "2024-06-01T00:00:00",
        "condition_date": "2024-05-01T00:00:00"
    }
)

# Read Admission by ID
test_admission_by_id = createByIdTest2(tableName="admissions")

# Update Admission
test_admission_update = createUpdateTest2(
    tableName="admissions",
    variables={
        "id": "admission-id",
        "lastchange": "2024-01-01T00:00:00",
        "name": "Updated Admission Name",
        "name_en": "Updated Admission EN"
    }
)

# Delete Admission
test_admission_delete = createDeleteTest2(
    tableName="admissions",
    variables={
        "id": "admission-id",
        "lastchange": "2024-01-01T00:00:00"
    }
)

# Custom Tests
@pytest.mark.asyncio
async def test_admission_invalid_date_range(SchemaExecutorDemo):
    variables = {
        "name": "Admission with Invalid Dates",
        "application_start_date": "2024-02-01T00:00:00",
        "application_last_date": "2024-01-01T00:00:00"
    }
    query = getQuery(tableName="admissions", queryName="create")
    response = await SchemaExecutorDemo(query=query, variable_values=variables)
    assert "errors" in response, f"Expected errors for invalid date range: {response}"

@pytest.mark.asyncio
async def test_admission_delete_with_validation(SchemaExecutorDemo):
    tableName = "admissions"
    variables = {
        "id": "admission-id",
        "lastchange": "2024-01-01T00:00:00"
    }
    queryRead = getQuery(tableName=tableName, queryName="read")
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": variables["id"]})
    admission = responseJson.get("data", {}).get("result")
    assert admission is not None, f"Admission not found: {responseJson}"

    variables["lastchange"] = admission["lastchange"]
    queryDelete = getQuery(tableName=tableName, queryName="delete")
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
    assert "errors" not in responseJson, f"Delete failed: {responseJson}"
    logging.info(f"Successfully deleted admission: {responseJson}")

    ################################################################################## Exam CRUD Tests

    # Create Admission
test_admission_create = createTest2(
    tableName="admissions",
    queryName="create",
    variables={
        "name": "New Admission",
        "name_en": "New Admission EN",
        "state_id": "state-id",
        "program_id": "program-id",
        "application_start_date": "2024-01-01T00:00:00",
        "application_last_date": "2024-02-01T00:00:00",
        "end_date": "2024-06-01T00:00:00",
        "condition_date": "2024-05-01T00:00:00"
    }
)

# Read Admission by ID
test_admission_by_id = createByIdTest2(tableName="admissions")

# Update Admission
test_admission_update = createUpdateTest2(
    tableName="admissions",
    variables={
        "id": "admission-id",
        "lastchange": "2024-01-01T00:00:00",
        "name": "Updated Admission Name",
        "name_en": "Updated Admission EN"
    }
)

# Delete Admission
test_admission_delete = createDeleteTest2(
    tableName="admissions",
    variables={
        "id": "admission-id",
        "lastchange": "2024-01-01T00:00:00"
    }
)

@pytest.mark.asyncio
async def test_exam_invalid_exam_type(SchemaExecutorDemo):
    variables = {
        "name": "Invalid Type Exam",
        "exam_date": "2024-03-15T10:00:00",
        "exam_type_id": "non-existent-id"
    }
    query = getQuery(tableName="exams", queryName="create")
    response = await SchemaExecutorDemo(query=query, variable_values=variables)
    assert "errors" in response, f"Expected errors for invalid exam type: {response}"

@pytest.mark.asyncio
async def test_exam_delete_with_results(SchemaExecutorDemo):
    tableName = "exams"
    variables = {
        "id": "exam-with-results-id",
        "lastchange": "2024-03-15T10:00:00"
    }

    queryRead = getQuery(tableName=tableName, queryName="read")
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": variables["id"]})
    exam = responseJson.get("data", {}).get("result")
    assert exam is not None, f"Exam not found: {responseJson}"

    assert len(exam["examResults"]) > 0, "Expected exam to have results but found none"

    queryDelete = getQuery(tableName=tableName, queryName="delete")
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
    assert "errors" in responseJson, "Exam with results should not be deletable"
    logging.info(f"Delete attempt failed as expected: {responseJson}")

    ########################################################################## Exam Results CRUD Tests

    # Exam Results Tests
test_exam_result_create = createTest2(
    tableName="exam_results",
    queryName="create",
    variables={
        "score": 95.5,
        "exam_id": "exam-id",
        "student_admission_id": "student-admission-id"
    }
)

test_exam_result_by_id = createByIdTest2(
    tableName="exam_results"
)

test_exam_result_update = createUpdateTest2(
    tableName="exam_results",
    variables={
        "id": "exam-result-id",
        "lastchange": "2024-03-15T10:00:00",
        "score": 89.0,
        "exam_id": "updated-exam-id",
        "student_admission_id": "updated-student-admission-id"
    }
)

test_exam_result_delete = createDeleteTest2(
    tableName="exam_results",
    variables={
        "id": "exam-result-id",
        "lastchange": "2024-03-15T10:00:00"
    }
)

@pytest.mark.asyncio
async def test_exam_result_relationships(SchemaExecutorDemo):
    exam_result_id = "valid-exam-result-id"
    query = getQuery(tableName="exam_results", queryName="read")
    responseJson = await SchemaExecutorDemo(query=query, variable_values={"id": exam_result_id})
    result = responseJson.get("data", {}).get("result")
    assert result is not None, f"ExamResult not found: {responseJson}"
    assert result["exam"] is not None, f"Expected exam relationship, found: {result['exam']}"
    assert result["studentAdmission"] is not None, f"Expected studentAdmission relationship, found: {result['studentAdmission']}"

@pytest.mark.asyncio
async def test_exam_result_delete_restricted(SchemaExecutorDemo):
    variables = {
        "id": "linked-exam-result-id",
        "lastchange": "2024-03-15T10:00:00"
    }
    queryDelete = getQuery(tableName="exam_results", queryName="delete")
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
    assert "errors" in responseJson, "Expected deletion to fail due to dependencies"
    logging.info(f"Deletion restricted as expected: {responseJson}")

@pytest.mark.asyncio
async def test_exam_result_invalid_foreign_keys(SchemaExecutorDemo):
    variables = {
        "score": 90.0,
        "exam_id": "invalid-exam-id",
        "student_admission_id": "invalid-student-admission-id"
    }
    queryCreate = getQuery(tableName="exam_results", queryName="create")
    responseJson = await SchemaExecutorDemo(query=queryCreate, variable_values=variables)
    assert "errors" in responseJson, f"Expected errors for invalid foreign keys: {responseJson}"

    ############################################################################## Exam Types CRUD Tests

# Exam Types Tests
test_exam_type_create = createTest2(
    tableName="exam_types",
    queryName="create",
    variables={
        "name": "Midterm Exam Type",
        "name_en": "Midterm Exam Type EN",
        "min_score": 50.0,
        "max_score": 100.0,
        "admission_id": "admission-id"  # Replace with a valid UUID
    }
)

test_exam_type_by_id = createByIdTest2(
    tableName="exam_types"
)

test_exam_type_update = createUpdateTest2(
    tableName="exam_types",
    variables={
        "id": "exam-type-id",
        "lastchange": "2024-01-01T00:00:00",  # Placeholder
        "name": "Updated Exam Type",
        "name_en": "Updated Exam Type EN",
        "min_score": 55.0,
        "max_score": 95.0
    }
)

test_exam_type_delete = createDeleteTest2(
    tableName="exam_types",
    variables={
        "id": "exam-type-id",
        "lastchange": "2024-01-01T00:00:00"  # Placeholder
    }
)

@pytest.mark.asyncio
async def test_exam_type_admission_relationship(SchemaExecutorDemo):
    tableName = "exam_types"
    entity_id = "exam-type-id"

    queryRead = getQuery(tableName=tableName, queryName="read")
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
    result = responseJson.get("data", {}).get("result")
    assert result is not None, f"ExamType not found: {responseJson}"
    admission = result.get("admission")
    assert admission is not None, f"Expected admission relationship, found: {admission}"

@pytest.mark.asyncio
async def test_exam_type_delete_with_exams(SchemaExecutorDemo):
    tableName = "exam_types"
    entity_id = "exam-type-with-exams-id"

    variables = {
        "id": entity_id,
        "lastchange": "2024-01-01T00:00:00"  # Placeholder
    }
    queryDelete = getQuery(tableName=tableName, queryName="delete")
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
    assert "errors" in responseJson, "Expected deletion to fail due to linked exams"


    ############################################################################ Student Admissions CRUD Tests

# Student Admissions Tests
test_student_admission_create = createTest2(
    tableName="student_admissions",
    queryName="create",
    variables={
        "admission_id": "admission-id",
        "user_id": "user-id",
        "state_id": "state-id",
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
        "id": "student-admission-id",
        "lastchange": "2024-01-01T00:00:00",
        "admission_id": "updated-admission-id",
        "user_id": "updated-user-id",
        "state_id": "updated-state-id",
        "extended_condition_date": "2024-04-01T10:00:00",
        "admissioned": False,
        "enrollment_date": "2024-04-05T10:00:00"
    }
)

test_student_admission_delete = createDeleteTest2(
    tableName="student_admissions",
    variables={
        "id": "student-admission-id",
        "lastchange": "2024-01-01T00:00:00"
    }
)

@pytest.mark.asyncio
async def test_student_admission_admission_relationship(SchemaExecutorDemo):
    tableName = "student_admissions"
    entity_id = "student-admission-id"

    queryRead = getQuery(tableName=tableName, queryName="read")
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
    result = responseJson.get("data", {}).get("result")
    assert result is not None, f"StudentAdmission not found: {responseJson}"
    admission = result.get("admission")
    assert admission is not None, f"Expected admission relationship, found: {admission}"

@pytest.mark.asyncio
async def test_student_admission_delete_with_exam_results(SchemaExecutorDemo):
    tableName = "student_admissions"
    entity_id = "student-admission-with-exam-results-id"

    variables = {
        "id": entity_id,
        "lastchange": "2024-01-01T00:00:00"
    }
    queryDelete = getQuery(tableName=tableName, queryName="delete")
    responseJson = await SchemaExecutorDemo(query=queryDelete, variable_values=variables)
    assert "errors" in responseJson, "Expected deletion to fail due to linked exam results"

@pytest.mark.asyncio
async def test_student_admission_exams_and_results(SchemaExecutorDemo):
    tableName = "student_admissions"
    entity_id = "student-admission-id"

    queryRead = getQuery(tableName=tableName, queryName="read")
    responseJson = await SchemaExecutorDemo(query=queryRead, variable_values={"id": entity_id})
    result = responseJson.get("data", {}).get("result")
    assert result is not None, f"StudentAdmission not found: {responseJson}"

    exams = result.get("exams", [])
    assert len(exams) > 0, "Expected at least one linked exam"
    logging.info(f"Linked exams: {exams}")

    examResults = result.get("examResults", [])
    assert len(examResults) > 0, "Expected at least one exam result"
    logging.info(f"Exam results validated: {examResults}")
