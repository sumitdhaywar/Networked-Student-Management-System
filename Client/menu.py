from datetime import date
from getpass import getpass

from Client.request import send_request


def read_int(message):
    try:
        return int(input(message))
    except ValueError:
        print("Please enter a valid number.")
        return None


def read_float(message):
    try:
        return float(input(message))
    except ValueError:
        print("Please enter a valid number.")
        return None


def read_date(message):
    try:
        return date.fromisoformat(input(message))
    except ValueError:
        print("Please enter a valid date (YYYY-MM-DD).")
        return None


def show_response(response):
    print("\n", response, "\n")


def login():
    print("\n===== NETWORKED STUDENT MANAGEMENT SYSTEM =====")
    username = input("Enter username: ")
    password = getpass("Enter password: ")

    response = send_request("Login", {"username": username, "password": password})
    if not response or response.get("success") is not True:
        print("Login failed.")
        return None

    print("\nLogin successful!")
    print("Welcome:", response.get("username"))
    print("Role:", response.get("role"))
    return response


def admin_student_menu():
    while True:
        print("\n====== STUDENT MANAGEMENT ======")
        print("1. Add Student")
        print("2. Search Student")
        print("3. List All Students")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = read_int("Enter student ID: ")
            name = input("Enter student name: ")
            age = read_int("Enter student age: ")
            if student_id is None or age is None:
                continue
            response = send_request("Add_Student", {"id": student_id, "name": name, "age": age})

        elif choice == "2":
            student_id = read_int("Enter student ID: ")
            if student_id is None:
                continue
            response = send_request("Search_Student", {"id": student_id})

        elif choice == "3":
            response = send_request("Display All Student")

        elif choice == "4":
            student_id = read_int("Enter student ID: ")
            name = input("Enter new name: ")
            age = read_int("Enter new age: ")
            if student_id is None or age is None:
                continue
            response = send_request("update_student", {"id": student_id, "name": name, "age": age})

        elif choice == "5":
            student_id = read_int("Enter student ID: ")
            if student_id is None:
                continue
            response = send_request("Delete_Student", {"id": student_id})

        elif choice == "6":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_teacher_menu():
    while True:
        print("\n====== TEACHER MANAGEMENT ======")
        print("1. Add Teacher")
        print("2. Search Teacher")
        print("3. List All Teachers")
        print("4. Update Teacher")
        print("5. Delete Teacher")
        print("6. Allocate Student to Teacher")
        print("7. View All Allocations")
        print("8. Remove Allocation")
        print("9. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            teacher_id = read_int("Enter teacher ID: ")
            teacher_name = input("Enter teacher name: ")
            joining_date = read_date("Enter joining date (YYYY-MM-DD): ")
            salary = read_float("Enter salary: ")
            if (
                teacher_id is None
                or joining_date is None
                or salary is None
                or not teacher_name.strip()
            ):
                print("Please provide valid teacher details.")
                continue
            response = send_request(
                "Add_Teacher",
                {
                    "t_id": teacher_id,
                    "t_name": teacher_name,
                    "j_o_d": joining_date.isoformat(),
                    "salary": salary,
                },
            )

        elif choice == "2":
            teacher_id = read_int("Enter teacher ID: ")
            if teacher_id is None:
                continue
            response = send_request("Search_Teacher", {"t_id": teacher_id})

        elif choice == "3":
            response = send_request("Display All Teachers")

        elif choice == "4":
            teacher_id = read_int("Enter teacher ID: ")
            teacher_name = input("Enter new name: ")
            joining_date = read_date("Enter new joining date (YYYY-MM-DD): ")
            salary = read_float("Enter new salary: ")
            if (
                teacher_id is None
                or joining_date is None
                or salary is None
                or not teacher_name.strip()
            ):
                print("Please provide valid teacher details.")
                continue
            response = send_request(
                "Update_Teacher",
                {
                    "t_id": teacher_id,
                    "t_name": teacher_name,
                    "j_o_d": joining_date.isoformat(),
                    "salary": salary,
                },
            )

        elif choice == "5":
            teacher_id = read_int("Enter teacher ID: ")
            if teacher_id is None:
                continue
            response = send_request("Delete_Teacher", {"t_id": teacher_id})

        elif choice == "6":
            teacher_id = read_int("Enter teacher ID: ")
            student_id = read_int("Enter student ID: ")
            course_id = read_int("Enter course ID: ")
            if None in (teacher_id, student_id, course_id):
                continue
            response = send_request(
                "Allocate_Student",
                {
                    "teacher_id": teacher_id,
                    "student_id": student_id,
                    "course_id": course_id,
                },
            )

        elif choice == "7":
            response = send_request("Display All Allocations")

        elif choice == "8":
            teacher_id = read_int("Enter teacher ID: ")
            student_id = read_int("Enter student ID: ")
            course_id = read_int("Enter course ID: ")
            if None in (teacher_id, student_id, course_id):
                continue
            response = send_request(
                "Remove_Allocation",
                {
                    "teacher_id": teacher_id,
                    "student_id": student_id,
                    "course_id": course_id,
                },
            )

        elif choice == "9":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_course_menu():
    while True:
        print("\n====== COURSE MANAGEMENT ======")
        print("1. Add Course")
        print("2. Search Course")
        print("3. List All Courses")
        print("4. Update Course")
        print("5. Delete Course")
        print("6. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            course_id = read_int("Enter course ID: ")
            course_name = input("Enter course name: ")
            fees = read_float("Enter course fees: ")
            if course_id is None or fees is None or not course_name.strip():
                print("Please provide valid course details.")
                continue
            response = send_request(
                "Add_Course",
                {"co_id": course_id, "co_name": course_name, "fees": fees},
            )

        elif choice == "2":
            course_id = read_int("Enter course ID: ")
            if course_id is None:
                continue
            response = send_request("Search_Course", {"co_id": course_id})

        elif choice == "3":
            response = send_request("Display All Courses")

        elif choice == "4":
            course_id = read_int("Enter course ID: ")
            course_name = input("Enter new course name: ")
            fees = read_float("Enter new course fees: ")
            if course_id is None or fees is None or not course_name.strip():
                print("Please provide valid course details.")
                continue
            response = send_request(
                "Update_Course",
                {"co_id": course_id, "co_name": course_name, "fees": fees},
            )

        elif choice == "5":
            course_id = read_int("Enter course ID: ")
            if course_id is None:
                continue
            response = send_request("Delete_Course", {"co_id": course_id})

        elif choice == "6":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_marks_menu():
    while True:
        print("\n====== MARKS MANAGEMENT ======")
        print("1. Add Marks")
        print("2. Display All Results")
        print("3. Update Marks")
        print("4. Delete Marks")
        print("5. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = read_int("Enter student ID: ")
            course_id = read_int("Enter course ID: ")
            teacher_id = read_int("Enter teacher ID: ")
            marks = read_float("Enter marks: ")
            if None in (student_id, course_id, teacher_id, marks):
                continue
            response = send_request(
                "Add_Marks",
                {
                    "id": student_id,
                    "co_id": course_id,
                    "t_id": teacher_id,
                    "marks": marks,
                },
            )

        elif choice == "2":
            response = send_request("Display All Result")

        elif choice == "3":
            roll = read_int("Enter marks record roll: ")
            student_id = read_int("Enter student ID: ")
            course_id = read_int("Enter course ID: ")
            teacher_id = read_int("Enter teacher ID: ")
            marks = read_float("Enter marks: ")
            if None in (roll, student_id, course_id, teacher_id, marks):
                continue
            response = send_request(
                "Update_Marks",
                {
                    "roll": roll,
                    "id": student_id,
                    "co_id": course_id,
                    "t_id": teacher_id,
                    "marks": marks,
                },
            )

        elif choice == "4":
            roll = read_int("Enter marks record roll: ")
            if roll is None:
                continue
            response = send_request("Delete_Marks", {"roll": roll})

        elif choice == "5":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_result_menu():
    while True:
        print("\n====== RESULT MANAGEMENT ======")
        print("1. Calculate Result")
        print("2. Display Topper")
        print("3. Class Statistics")
        print("4. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = read_int("Enter student ID: ")
            if student_id is None:
                continue
            response = send_request("calculate_result", {"id": student_id})

        elif choice == "2":
            response = send_request("display_topper")

        elif choice == "3":
            response = send_request("result_statistics")

        elif choice == "4":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_login_menu():
    while True:
        print("\n====== STUDENT LOGIN MANAGEMENT ======")
        print("1. Set Student Credentials")
        print("2. Back")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = read_int("Enter student ID: ")
            user_name = input("Enter student username: ")
            password = getpass("Enter student password: ")
            if student_id is None or not user_name.strip():
                print("Please provide a valid student ID and username.")
                continue
            response = send_request(
                "Set_Student_Credentials",
                {"id": student_id, "user_name": user_name, "password": password},
            )

        elif choice == "2":
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def admin_menu():
    while True:
        print("\n========== ADMIN MENU ==========")
        print("1. Student Management")
        print("2. Teacher Management")
        print("3. Course Management")
        print("4. Marks Management")
        print("5. Result Management")
        print("6. Student Login Management")
        print("7. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            admin_student_menu()
        elif choice == "2":
            admin_teacher_menu()
        elif choice == "3":
            admin_course_menu()
        elif choice == "4":
            admin_marks_menu()
        elif choice == "5":
            admin_result_menu()
        elif choice == "6":
            admin_login_menu()
        elif choice == "7":
            response = send_request("Logout")
            show_response(response)
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice.")


def teacher_menu():
    while True:
        print("\n========== TEACHER MENU ==========")
        print("1. Search Student")
        print("2. View My Allocated Students")
        print("3. Add Marks")
        print("4. Calculate Result")
        print("5. Display Topper")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = read_int("Enter student ID: ")
            if student_id is None:
                continue
            response = send_request("Search_Student", {"id": student_id})

        elif choice == "2":
            response = send_request("View_My_Allocated_Students")

        elif choice == "3":
            student_id = read_int("Enter student ID: ")
            course_id = read_int("Enter course ID: ")
            teacher_id = read_int("Enter teacher ID: ")
            marks = read_float("Enter marks: ")
            if None in (student_id, course_id, teacher_id, marks):
                continue
            response = send_request(
                "Add_Marks",
                {
                    "id": student_id,
                    "co_id": course_id,
                    "t_id": teacher_id,
                    "marks": marks,
                },
            )

        elif choice == "4":
            student_id = read_int("Enter student ID: ")
            if student_id is None:
                continue
            response = send_request("calculate_result", {"id": student_id})

        elif choice == "5":
            response = send_request("display_topper")

        elif choice == "6":
            response = send_request("Logout")
            show_response(response)
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def student_menu(reference_id):
    if reference_id is None:
        print("Student account is not linked to a student record.")
        send_request("Logout")
        return

    while True:
        print("\n========== STUDENT MENU ==========")
        print("1. View My Details")
        print("2. Calculate My Result")
        print("3. Display Topper")
        print("4. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            response = send_request("Search_Student", {"id": reference_id})

        elif choice == "2":
            response = send_request("calculate_result", {"id": reference_id})

        elif choice == "3":
            response = send_request("display_topper")

        elif choice == "4":
            response = send_request("Logout")
            show_response(response)
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice.")
            continue

        show_response(response)


def main():
    user = login()
    if not user:
        return

    role = user.get("role")
    reference_id = user.get("reference_id")

    if role == "admin":
        admin_menu()
    elif role == "teacher":
        teacher_menu()
    elif role == "student":
        student_menu(reference_id)
    else:
        print("Invalid user role.")


if __name__ == "__main__":
    main()

