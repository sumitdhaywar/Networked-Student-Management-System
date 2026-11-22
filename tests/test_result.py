from services import result_services as ser
from repositories import result_repository as repo
from unittest.mock import patch
import random


def test_get_course_toppers():
    rows = [
        (201, "Math", 102, "Second", 180, 90),
        (201, "Math", 101, "First", 150, 75),
        (202, "Science", 101, "First", 190, 95),
        (202, "Science", 102, "Second", 170, 85),
        (203, "History", None, None, None, None),
    ]
    with patch.object(repo, "get_course_topper_rows", return_value=rows):
        result = ser.get_course_toppers_se()

    assert result["success"] is True
    assert result["data"] == [
        {
            "course_id": 201,
            "course_name": "Math",
            "topper": {"id": 102, "name": "Second", "total": 180.0, "average": 90.0},
        },
        {
            "course_id": 202,
            "course_name": "Science",
            "topper": {"id": 101, "name": "First", "total": 190.0, "average": 95.0},
        },
        {"course_id": 203, "course_name": "History", "topper": None},
    ]


def test_result():
    id = 101
    co_id = 201
    t_id = 301
    marks=random.randint(0,100)
    result=ser.add_result_se(id,co_id,t_id,marks)
    print("added result",result)
    assert result["success"]is True,"add result failed"
    roll=result["roll"]
    
    try:
        result=ser.get_result_se(roll)
        assert result["success"] is True," get result fail"

        res =result["data"]
        assert res[0]==roll
        assert res[1]==id
        assert res[2]==co_id
        assert res[3]==t_id
        assert res[4]==marks

        result =ser.get_all_result_se()
        assert result["success"]is True ,"listing all result fail"

        updated_id = 101
        updated_co_id = 201
        updated_t_id = 301
        updated_marks=random.randint(0,100)

        result=ser.update_result_se(
            roll,updated_id,updated_co_id,updated_t_id,updated_marks
        )
        print("UPDATE RESPONSE:", result)

        assert result["success"]is True,"update result fail"

        result= ser.get_result_se(roll)
        assert result["success"]is True

        res =result["data"]

        assert res[1]==updated_id
        assert res[2]==updated_co_id
        assert res[3]==updated_t_id
        assert res[4]==updated_marks
        result= ser.delete_result_se(roll)
        assert result["success"]is True,"delete result failed"

        result= ser.get_result_se(roll)
        assert result["success"]is  False,"result was not deleted"
    finally:
        ser.delete_result_se(roll)
    print("all course operation passed")

def test_invalid_result_data():


    # Invalid student ID
    result = ser.add_result_se(0, 201, 301, 75)
    assert result["success"] is False

    # Invalid course ID
    result = ser.add_result_se(101, 0, 301, 75)
    assert result["success"] is False

    # Invalid teacher ID
    result = ser.add_result_se(101, 201, 0, 75)
    assert result["success"] is False

    # Invalid marks
    result = ser.add_result_se(101, 201, 301, 101)
    assert result["success"] is False

    print("All validation tests passed")
def test_calculate_result():
    id = 101
    co_id = 201
    t_id = 301

    rolls = []

    try:
        for marks in [75, 80, 65]:
            result = ser.add_result_se(id, co_id, t_id, marks)
            assert result["success"] is True
            rolls.append(result["roll"])

        result = ser.calculate_result_se(id)
        print("calculation response",result)

        assert result["success"] is True

        all_marks = [row[0] for row in repo.get_student_marks(id)]

        assert result["total"] == sum(all_marks)
        assert result["percentage"] == round(
            sum(all_marks) / len(all_marks), 2
        )

        expected_status = (
            "Pass" if all(mark >= 35 for mark in all_marks) else "Fail"
        )
        assert result["status"] == expected_status

        print("Result calculation test passed")

    finally:
        for roll in rolls:
            ser.delete_result_se(roll)
def test_get_topper():
    result = ser.get_topper_se()
    
    assert result["success"] is True, "topper calculation failed"

    topper = result["data"]

    assert topper is not None
    assert isinstance(topper[0], int)       # Student ID
    assert isinstance(topper[1], str)       # Student name
    assert topper[2] >= topper[3]           # Total >= average
    assert 0 <= topper[3] <= 100            # Percentage

    print("Topper test passed:", topper)