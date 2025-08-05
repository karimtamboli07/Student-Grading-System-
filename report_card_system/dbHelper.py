# report_card_system/dbHelper.py
def get_categories_list_sql():
    return "SELECT * FROM categories"

def insert_category_sql():
    return "INSERT INTO categories (category_name, grade_from, grade_to) VALUES (%s, %s, %s)"

def get_category_by_id_sql():
    return "SELECT * FROM categories WHERE category_id = %s"

def update_category_sql():
    return "UPDATE categories SET category_name=%s, grade_from=%s, grade_to=%s WHERE category_id=%s"

def delete_category_sql():
    return "DELETE FROM categories WHERE category_id=%s"

def get_subjects_list_sql():
    return "SELECT * FROM subjects"

def insert_subject_sql():
    return "INSERT INTO subjects (subject_name) VALUES (%s)"

def get_subject_by_id_sql():
    return "SELECT * FROM subjects WHERE subject_id = %s"

def update_subject_sql():
    return "UPDATE subjects SET subject_name=%s WHERE subject_id=%s"

def delete_subject_sql():
    return "DELETE FROM subjects WHERE subject_id=%s"

def get_classes_list_sql():
    return "SELECT * FROM classes"

def insert_class_sql():
    return "INSERT INTO classes (class_name) VALUES (%s)"

def get_class_by_id_sql():
    return "SELECT * FROM classes WHERE class_id = %s"

def update_class_sql():
    return "UPDATE classes SET class_name=%s WHERE class_id=%s"

def delete_class_sql():
    return "DELETE FROM classes WHERE class_id=%s"

def get_students_list_sql():
    return """
        SELECT students.*, classes.class_name
        FROM students
        LEFT JOIN classes ON students.class_id = classes.class_id
    """

def insert_student_sql():
    return "INSERT INTO students (student_name, student_roll_number, class_id) VALUES (%s, %s, %s)"

def get_student_by_id_sql():
    return "SELECT * FROM students WHERE student_id = %s"

def update_student_sql():
    return "UPDATE students SET student_name=%s, student_roll_number=%s, class_id=%s WHERE student_id=%s"

def delete_student_sql():
    return "DELETE FROM students WHERE student_id=%s"

def get_users_list_sql():
    return "SELECT * FROM users"

def insert_user_sql():
    return "INSERT INTO users (username, password, is_superuser) VALUES (%s, %s, %s)"

def get_user_by_id_sql():
    return "SELECT * FROM users WHERE user_id = %s"

def update_user_sql():
    return "UPDATE users SET username=%s, password=%s, is_superuser=%s WHERE user_id=%s"

def delete_user_sql():
    return "DELETE FROM users WHERE user_id=%s"

def get_marks_list_sql():
    return """
        SELECT marks.*, students.student_name, subjects.subject_name
        FROM marks
        JOIN students ON marks.student_id = students.student_id
        JOIN subjects ON marks.subject_id = subjects.subject_id
    """

def get_marks_for_report_card_sql():
    return """
        SELECT marks.*, subjects.subject_name, categories.category_name
        FROM marks
        JOIN subjects ON marks.subject_id = subjects.subject_id
        LEFT JOIN categories ON marks.marks_obtained BETWEEN categories.grade_from AND categories.grade_to
        WHERE student_id = %s
    """

def get_student_for_report_card_sql():
    return """
        SELECT students.*, classes.class_name
        FROM students
        LEFT JOIN classes ON students.class_id = classes.class_id
        WHERE student_id=%s
    """

def insert_mark_sql():
    return "INSERT INTO marks (student_id, subject_id, marks_obtained) VALUES (%s, %s, %s)"

def get_mark_by_id_sql():
    return """
        SELECT marks.*, students.student_name, subjects.subject_name
        FROM marks
        JOIN students ON marks.student_id = students.student_id
        JOIN subjects ON marks.subject_id = subjects.subject_id
        WHERE mark_id = %s
    """

def update_mark_sql():
    return "UPDATE marks SET student_id=%s, subject_id=%s, marks_obtained=%s WHERE mark_id=%s"

def delete_mark_sql():
    return "DELETE FROM marks WHERE mark_id=%s"

def get_existing_mark_sql():
    return "SELECT * FROM marks WHERE student_id = %s AND subject_id = %s"

def get_students_by_class_sql():
    return "SELECT * FROM students WHERE class_id = %s"