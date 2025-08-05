# report_card_system/routes/students.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .. import dbHelper

bp = Blueprint('students', __name__, url_prefix='/students')

@bp.route('/')
def list_students():
    students = current_app.fetch_all(dbHelper.get_students_list_sql())
    return render_template('students/list.html', students=students)

@bp.route('/create', methods=['GET', 'POST'])
def create_student():
    classes = current_app.fetch_all(dbHelper.get_classes_list_sql())
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        class_id = request.form.get('class_id') # Use get to handle cases where no class is selected
        current_app.execute_query(dbHelper.insert_student_sql(), (name, roll_number, class_id if class_id else None))
        return redirect(url_for('students.list_students'))
    return render_template('students/create.html', classes=classes)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = current_app.fetch_one(dbHelper.get_student_by_id_sql(), (id,))
    classes = current_app.fetch_all(dbHelper.get_classes_list_sql())
    if request.method == 'POST':
        name = request.form['name']
        roll_number = request.form['roll_number']
        class_id = request.form.get('class_id') # Use get to handle cases where no class is selected
        current_app.execute_query(dbHelper.update_student_sql(), (name, roll_number, class_id if class_id else None, id))
        return redirect(url_for('students.list_students'))
    return render_template('students/edit.html', student=student, classes=classes)

@bp.route('/delete/<int:id>')
def delete_student(id):
    current_app.execute_query(dbHelper.delete_student_sql(), (id,))
    return redirect(url_for('students.list_students'))