# report_card_system/routes/marks.py
from flask import Blueprint, render_template, request, redirect, url_for, send_file, current_app
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from .. import dbHelper
from reportlab.graphics.shapes import Drawing, Rect
from reportlab.graphics import renderPDF

bp = Blueprint('marks', __name__, url_prefix='/marks')

@bp.route('/', methods=['GET', 'POST'])
def list_marks():
    classes = current_app.fetch_all(dbHelper.get_classes_list_sql())
    subjects = current_app.fetch_all(dbHelper.get_subjects_list_sql())
    selected_class_id = request.form.get('class_id') if request.method == 'POST' else None

    if selected_class_id:
        students = current_app.fetch_all(dbHelper.get_students_by_class_sql(), (selected_class_id,))
    else:
        students = current_app.fetch_all(dbHelper.get_students_list_sql())

    marks = current_app.fetch_all(dbHelper.get_marks_list_sql())

    return render_template('marks/list.html', marks=marks, students=students, subjects=subjects, classes=classes, selected_class_id=selected_class_id)


@bp.route('/marks/add', methods=['POST'])
def add_mark():
    print("Request Form Data in /marks/add:", request.form) # Debug print
    if 'student_id' not in request.form:
        print("Error: student_id is missing in the form submission.") # Debug message
        return redirect(url_for('marks.list_marks'))
    student_id = request.form['student_id']
    subject_id = request.form['subject_id']
    marks_obtained = request.form['marks_obtained']
    existing_mark = current_app.fetch_one(dbHelper.get_existing_mark_sql(), (student_id, subject_id))
    if existing_mark:
        current_app.execute_query(dbHelper.update_mark_sql(), (marks_obtained, student_id, subject_id))
    else:
        current_app.execute_query(dbHelper.insert_mark_sql(), (student_id, subject_id, marks_obtained))
    return redirect(url_for('marks.list_marks'))

@bp.route('/marks/edit/<int:id>', methods=['GET', 'POST'])
def edit_mark(id):
    mark = current_app.fetch_one(dbHelper.get_mark_by_id_sql(), (id,))
    students = current_app.fetch_all(dbHelper.get_students_list_sql())
    subjects = current_app.fetch_all(dbHelper.get_subjects_list_sql())
    if request.method == 'POST':
        student_id = request.form['student_id']
        subject_id = request.form['subject_id']
        marks_obtained = request.form['marks_obtained']
        current_app.execute_query(dbHelper.update_mark_sql(), (student_id, subject_id, marks_obtained, id))
        return redirect(url_for('marks.list_marks'))
    return render_template('marks/edit.html', mark=mark, students=students, subjects=subjects)


@bp.route('/marks/delete/<int:id>')
def delete_mark(id):
    current_app.execute_query(dbHelper.delete_mark_sql(), (id,))
    return redirect(url_for('marks.list_marks'))


# Report Card Generation - Keep in marks blueprint as it's related to marks data
@bp.route('/report_card/<int:student_id>')
def generate_report_card(student_id):
    student = current_app.fetch_one(dbHelper.get_student_for_report_card_sql(), (student_id,))
    marks_data = current_app.fetch_all(dbHelper.get_marks_for_report_card_sql(), (student_id,))

    if not student:
        return "Student not found"

    file_name_relative = f"report_card_{student['student_id']}.pdf" # Relative file name
    file_path_absolute = os.path.join(current_app.root_path, file_name_relative) # Get absolute path

    doc = SimpleDocTemplate(file_path_absolute, pagesize=letter) # Use absolute path to save
    styles = getSampleStyleSheet()
    Story = []

    # Logo Placeholder (50x50 pixels at top left)
    logo_path = os.path.join(current_app.root_path, "logo.png") # Logo path relative to app root
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=50, height=50)
        Story.append(logo)
    else:
        # Placeholder rectangle if logo.png is not found
        logo_placeholder_width = 50
        logo_placeholder_height = 50

        # Create a Drawing object to hold shapes
        logo_drawing = Drawing(logo_placeholder_width, logo_placeholder_height)
        # Use Rect from reportlab.graphics.shapes
        rect = Rect(0, 0, logo_placeholder_width, logo_placeholder_height) # x, y, width, height
        rect.strokeColor = colors.black
        rect.strokeWidth = 1
        logo_drawing.add(rect) # Add the Rect to the Drawing

        Story.append(logo_drawing) # Append the Drawing to the Story


    Story.append(Spacer(1, 0.2*inch))


    ptext = f"<font size=12><b>Report Card</b></font>"
    Story.append(Paragraph(ptext, styles["Heading1"]))
    Story.append(Spacer(1, 0.2*inch))

    ptext = f"<font size=12><b>Student Name:</b> {student['student_name']}</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    ptext = f"<font size=12><b>Roll Number:</b> {student['student_roll_number']}</font>"
    Story.append(Paragraph(ptext, styles["Normal"]))
    if student['class_name']: # Only show class if it exists
        ptext = f"<font size=12><b>Class:</b> {student['class_name']}</font>"
        Story.append(Paragraph(ptext, styles["Normal"]))
    Story.append(Spacer(1, 0.2*inch))

    table_data = [['Subject', 'Marks Obtained', 'Category']]
    for mark in marks_data:
        table_data.append([mark['subject_name'], str(mark['marks_obtained']), mark['category_name'] if mark['category_name'] else 'N/A'])


    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 1, colors.black)
    ]))
    Story.append(table)

    doc.build(Story)

    return send_file(file_path_absolute, as_attachment=True, download_name=file_name_relative) # Send absolute path, specify download name