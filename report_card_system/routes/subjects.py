# report_card_system/routes/subjects.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .. import dbHelper

bp = Blueprint('subjects', __name__, url_prefix='/subjects')

@bp.route('/')
def list_subjects():
    subjects = current_app.fetch_all(dbHelper.get_subjects_list_sql())
    return render_template('subjects/list.html', subjects=subjects)

@bp.route('/create', methods=['GET', 'POST'])
def create_subject():
    if request.method == 'POST':
        name = request.form['name']
        current_app.execute_query(dbHelper.insert_subject_sql(), (name,))
        return redirect(url_for('subjects.list_subjects'))
    return render_template('subjects/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_subject(id):
    subject = current_app.fetch_one(dbHelper.get_subject_by_id_sql(), (id,))
    if request.method == 'POST':
        name = request.form['name']
        current_app.execute_query(dbHelper.update_subject_sql(), (name, id))
        return redirect(url_for('subjects.list_subjects'))
    return render_template('subjects/edit.html', subject=subject)

@bp.route('/delete/<int:id>')
def delete_subject(id):
    current_app.execute_query(dbHelper.delete_subject_sql(), (id,))
    return redirect(url_for('subjects.list_subjects'))