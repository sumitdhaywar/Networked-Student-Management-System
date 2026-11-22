from services import course_services as ser
import random
def test_course():
    co_id=random.randint(100000,999999)
    co_name="test_cname"
    fees=random.randint(100000,9999999)
    result=ser.add_course_se(co_id,co_name,fees)
    assert result["success"]is True,"add course failed"
    

    try:
        result=ser.get_course_se(co_id)
        assert result["success"] is True," get course fail"

        course =result["data"]
        assert course[0]==co_id
        assert course[1]==co_name
        assert course[2]==fees

        result =ser.get_all_course_se()
        assert result["success"]is True ,"listing all course fail"

        update_name="updated_course"
        update_fees=random.randint(10000,999999)

        result=ser.update_course_se(
            co_id,update_name,update_fees
        )
        assert result["success"]is True,"update course fail"

        result= ser.get_course_se(co_id)
        assert result["success"]is True

        course =result["data"]

        assert course[1]==update_name
        assert course[2]==update_fees
        result= ser.delete_course_se(co_id)
        assert result["success"]is True,"delete course failed"

        result= ser.get_course_se(co_id)
        assert result["success"]is  False,"course was not deleted"
    finally:
        ser.delete_course_se(co_id)
    print("all course operation passed")

