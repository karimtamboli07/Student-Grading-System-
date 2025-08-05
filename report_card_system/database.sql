-- database.sql

-- Create database
CREATE DATABASE IF NOT EXISTS report_card_system;
USE report_card_system;

-- Table for users (for admin access)
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE
);

-- Table for categories (e.g., A+, A, B+)
CREATE TABLE IF NOT EXISTS categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL UNIQUE,
    grade_from INT NOT NULL,
    grade_to INT NOT NULL
);

-- Table for subjects (e.g., Math, Science)
CREATE TABLE IF NOT EXISTS subjects (
    subject_id INT AUTO_INCREMENT PRIMARY KEY,
    subject_name VARCHAR(255) NOT NULL UNIQUE
);

-- Table for classes (e.g., Class 1, Class 2)
CREATE TABLE IF NOT EXISTS classes (
    class_id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL UNIQUE
);

-- Table for students
CREATE TABLE IF NOT EXISTS students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    student_name VARCHAR(255) NOT NULL,
    student_roll_number VARCHAR(50) UNIQUE,
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES classes(class_id) ON DELETE SET NULL -- Set class_id to NULL if class is deleted
);

-- Table for marks (linking students and subjects)
CREATE TABLE IF NOT EXISTS marks (
    mark_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    subject_id INT NOT NULL,
    marks_obtained INT NOT NULL,
    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
    FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) ON DELETE CASCADE,
    UNIQUE (student_id, subject_id) -- Ensure each subject mark is unique per student
);

-- Insert a default superuser
INSERT INTO users (username, password, is_superuser) VALUES ('admin', 'password', TRUE);

INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('A+', 90, 100);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('A', 85, 89);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('A-', 80, 84);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('B+', 75, 79);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('B', 70, 74);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('B-', 65, 69);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('C+', 60, 64);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('C', 55, 59);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('C-', 50, 54);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('D', 40, 49);
INSERT INTO categories (category_name, grade_from, grade_to) VALUES ('Fail', 0, 39);
