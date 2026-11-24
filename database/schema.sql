CREATE DATABASE IF NOT EXISTS SCHOOL_NET;
USE SCHOOL_NET;

CREATE TABLE IF NOT EXISTS student (
    id INT PRIMARY KEY,
    name VARCHAR(20),
    age INT,
    user_name VARCHAR(20),
    password_hash VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS course (
    course_id INT PRIMARY KEY,
    course_name VARCHAR(20),
    course_fees DECIMAL(10,2)
);

CREATE TABLE IF NOT EXISTS teacher (
    teacher_id INT PRIMARY KEY,
    teacher_name VARCHAR(30),
    salary DECIMAL(10,2),
    j_o_d DATE
);

CREATE TABLE IF NOT EXISTS s_data (
    roll INT AUTO_INCREMENT PRIMARY KEY,
    id INT NOT NULL,
    course_id INT NOT NULL,
    teacher_id INT NOT NULL,
    marks DECIMAL(5,2),
    FOREIGN KEY (id) REFERENCES student(id),
    FOREIGN KEY (course_id) REFERENCES course(course_id),
    FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id)
);

CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'teacher', 'student') NOT NULL,
    reference_id INT
);

-- Links a teacher, student, and course for allocation reporting.
CREATE TABLE IF NOT EXISTS teacher_student_allocation (
    teacher_id INT NOT NULL,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (teacher_id, student_id, course_id),
    CONSTRAINT fk_alloc_teacher FOREIGN KEY (teacher_id) REFERENCES teacher(teacher_id),
    CONSTRAINT fk_alloc_student FOREIGN KEY (student_id) REFERENCES student(id),
    CONSTRAINT fk_alloc_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);

CREATE TABLE IF NOT EXISTS student_course_enrollment (
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    CONSTRAINT fk_enrollment_student FOREIGN KEY (student_id) REFERENCES student(id),
    CONSTRAINT fk_enrollment_course FOREIGN KEY (course_id) REFERENCES course(course_id)
);