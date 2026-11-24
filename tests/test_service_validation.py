import importlib
import sys
import types
from contextlib import contextmanager
from unittest.mock import Mock, patch


@contextmanager
def _services_with_stubbed_repositories():
    service_names = (
        "student_services",
        "teacher_services",
        "course_services",
        "result_services",
    )
    repository_names = (
        "student_repository",
        "teacher_repository",
        "courses_repository",
        "result_repository",
    )

    repositories = types.ModuleType("repositories")
    repositories.__path__ = []
    mocked_repositories = {}
    modules = {"repositories": repositories}
    for name in repository_names:
        module_name = f"repositories.{name}"
        repository = types.ModuleType(module_name)
        mocked_repositories[name] = repository
        setattr(repositories, name, repository)
        modules[module_name] = repository

    service_package = importlib.import_module("services")
    previous_services = {}
    previous_attributes = {}
    for name in service_names:
        module_name = f"services.{name}"
        previous_services[module_name] = sys.modules.pop(module_name, None)
        previous_attributes[name] = getattr(service_package, name, None)
        if hasattr(service_package, name):
            delattr(service_package, name)

    try:
        with patch.dict(sys.modules, modules):
            services = {
                name: importlib.import_module(f"services.{name}")
                for name in service_names
            }
            yield services, mocked_repositories
    finally:
        for name in service_names:
            module_name = f"services.{name}"
            sys.modules.pop(module_name, None)
            if hasattr(service_package, name):
                delattr(service_package, name)
            previous = previous_services[module_name]
            if previous is not None:
                sys.modules[module_name] = previous
            previous_attribute = previous_attributes[name]
            if previous_attribute is not None:
                setattr(service_package, name, previous_attribute)


def test_student_service_rejects_names_longer_than_database_column():
    with _services_with_stubbed_repositories() as (services, repositories):
        repository = repositories["student_repository"]
        repository.add_student = Mock()

        result = services["student_services"].add_student_se(
            101, "x" * 21, 18
        )

        assert result["success"] is False
        repository.add_student.assert_not_called()


def test_teacher_and_course_services_reject_non_finite_amounts():
    from datetime import date

    with _services_with_stubbed_repositories() as (services, repositories):
        teacher_repo = repositories["teacher_repository"]
        teacher_repo.add_teacher = Mock()
        course_repo = repositories["courses_repository"]
        course_repo.add_course = Mock()

        teacher_result = services["teacher_services"].add_teacher_se(
            301, "Teacher", date(2020, 1, 1), float("nan")
        )
        course_result = services["course_services"].add_course_se(
            201, "Course", float("inf")
        )

        assert teacher_result["success"] is False
        assert course_result["success"] is False
        teacher_repo.add_teacher.assert_not_called()
        course_repo.add_course.assert_not_called()


def test_result_service_rejects_non_finite_marks():
    with _services_with_stubbed_repositories() as (services, repositories):
        result_repo = repositories["result_repository"]
        result_repo.add_result = Mock()

        result = services["result_services"].add_result_se(
            101, 201, 301, float("nan")
        )

        assert result["success"] is False
        result_repo.add_result.assert_not_called()


def test_result_service_handles_null_marks_without_crashing():
    with _services_with_stubbed_repositories() as (services, repositories):
        result_service = services["result_services"]
        result_repo = repositories["result_repository"]
        result_repo.get_student_marks = Mock(return_value=[(None,)])
        result_repo.get_topper = Mock(return_value=(101, "Student", None, None))
        result_repo.get_course_topper_rows = Mock(
            return_value=[(201, "Course", 101, "Student", None, None)]
        )
        result_repo.get_result_statistics_rows = Mock(
            return_value=[(101, "Student", 0, None, None, 0)]
        )

        assert result_service.calculate_result_se(101)["message"] == "no marks found"
        assert result_service.get_topper_se()["message"] == "topper not found"
        assert result_service.get_course_toppers_se()["data"] == [
            {"course_id": 201, "course_name": "Course", "topper": None}
        ]
        assert result_service.get_result_statistics_se()["message"] == "no results found"
