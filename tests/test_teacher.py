from services import teacher_services as ser
from datetime import date, timedelta

import random
def test_teacher():
   
    t_id=random.randint(10000,999999)
    t_name="test_cname"
    j_o_d = date(2020, 1, 1) + timedelta(days=random.randint(0, 2000))
    sal=random.randint(100000,9999999)
    result=ser.add_teacher_se(t_id,t_name,j_o_d,sal)
    print(result)
    assert result["success"]is True,"add teacher failed"
    

    try:
        result=ser.get_teacher_se(t_id)
        assert result["success"] is True," get teacher fail"

        teacher =result["data"]
        assert teacher[0] == t_id
        assert teacher[1] == t_name
        assert teacher[2] == sal
        assert teacher[3] == j_o_d

        result =ser.get_all_teacher_se()
        assert result["success"]is True ,"listing all teacher fail"

        update_teacher="updated_teacher"
        update_sal=random.randint(1000000,99999999)

        result=ser.update_teacher_se(
            t_id,update_teacher,j_o_d,update_sal
        )
        assert result["success"]is True,"update teacher fail"

        result= ser.get_teacher_se(t_id)
        assert result["success"]is True

        teacher =result["data"]

        assert teacher[1]==update_teacher
        assert teacher[2]==update_sal
        result= ser.delete_teacher_se(t_id)
        assert result["success"]is True,"delete teacher failed"

        result= ser.get_teacher_se(t_id)
        assert result["success"]is  False,"teacher was not deleted"
    finally:
        ser.delete_teacher_se(t_id)
    print("all teacher operation passed")

