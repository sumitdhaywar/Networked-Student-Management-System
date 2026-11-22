from services import student_services as services

# ===== ADDED: Student Credential Management via users table - imports =====
from services import auth_services as auth_services
from repositories import auth_repository as auth_repository
from database.connection import mycon

import random
def test_student_crud():
    student_id = random.randint(10000000,99999999)
    name ="TestStudent"
    age=17

    result = services.add_student_se(student_id, name, age)
    print(result)
    assert result["success"]is True ,"add Student failled"

    try:
        result=services.get_student_se(student_id)
        assert result["success"] is True,"get Student fail"

        student =result["data"]
        assert student[0]==student_id
        assert student[1]==name
        assert student[2]==age

        result =services.get_all_student_se()
        assert result["success"]is True ,"listing all student fail"

        update_name="updated_student"
        update_age=18

        result=services.update_student_se(
            student_id,update_name,update_age
        )
        assert result["success"]is True,"update Student fail"

        result= services.get_student_se(student_id)
        assert result["success"]is True

        student =result["data"]

        assert student[1]==update_name
        assert student[2]==update_age
        result= services.delete_student_se(student_id)
        assert result["success"]is True,"delete student failed"

        result= services .get_student_se(student_id)
        assert result["success"]is  False,"student was not deleted"
    finally:
        services.delete_student_se(student_id)
    print("all student operation passed")


# ===== ADDED: Student Credential Management via users table - test =====
def test_student_login_users_table():
    student_id = random.randint(10000000, 99999999)
    other_student_id = random.randint(10000000, 99999999)
    while other_student_id == student_id:
        other_student_id = random.randint(10000000, 99999999)

    name = "UsersTableStudent"
    user_name = f"user{student_id}"
    new_user_name = f"usernew{student_id}"
    other_user_name = f"userother{other_student_id}"
    password = "UserPass@123"

    try:
        result = services.add_student_se(student_id, name, 18)
        assert result["success"] is True, "add student failed"
        result = services.add_student_se(other_student_id, "OtherStudent", 19)
        assert result["success"] is True, "add second student failed"

        result = auth_services.set_student_login_se(
            student_id, user_name, password
        )
        assert result["success"] is True, result

        user = auth_repository.get_user_by_username(user_name)
        assert user is not None, "student account missing from users table"
        assert user["role"] == "student"
        assert user["reference_id"] == student_id

        result = auth_services.login_user(user_name, password)
        assert result["success"] is True, result
        assert result["role"] == "student"
        assert result["reference_id"] == student_id

        result = auth_services.login_user(user_name, "WrongPass123")
        assert result["success"] is False

        # Existing student account is updated, not duplicated.
        result = auth_services.set_student_login_se(
            student_id, new_user_name, password
        )
        assert result["success"] is True, result

        cur = mycon.cursor()
        cur.execute(
            "SELECT COUNT(*) FROM users WHERE role = 'student' AND reference_id = %s",
            (student_id,),
        )
        count = cur.fetchone()[0]
        cur.close()
        assert count == 1, "duplicate student user account created"

        result = auth_services.login_user(new_user_name, password)
        assert result["success"] is True, result

        # A different student cannot take an existing username.
        result = auth_services.set_student_login_se(
            other_student_id, new_user_name, password
        )
        assert result["success"] is False
        assert result["message"] == "username already exists"

        result = auth_services.set_student_login_se(
            other_student_id, other_user_name, password
        )
        assert result["success"] is True, result

        result = auth_services.login_user(other_user_name, password)
        assert result["success"] is True, result

        result = auth_services.set_student_login_se(
            0, other_user_name, password
        )
        assert result["success"] is False
    finally:
        services.delete_student_se(student_id)
        services.delete_student_se(other_student_id)
        cur = mycon.cursor()
        cur.execute(
            "DELETE FROM users WHERE role = 'student' AND reference_id IN (%s, %s)",
            (student_id, other_student_id),
        )
        mycon.commit()
        cur.close()
# ===== ADDED: Student Credential Management via users table - test END =====


def test_student_login():
    student_id = random.randint(10000000, 99999999)
    name = "LoginStudent"
    age = 17
    user_name = f"test{student_id}"
    password = "TestPass@123"

    try:
        result = services.add_student_se(student_id, name, age)
        assert result["success"] is True

        result = services.set_student_credentials_se(
            student_id, user_name, password
        )
        assert result["success"] is True

        # Test successful login
        result = services.login_student_se(user_name, password)
        assert result["success"] is True
        assert result["student_id"] == student_id

        # Test incorrect password
        result = services.login_student_se(user_name, "WrongPass123")
        assert result["success"] is False

        # Test unknown username
        result = services.login_student_se("unknown_user", password)
        assert result["success"] is False

    finally:
        services.delete_student_se(student_id)