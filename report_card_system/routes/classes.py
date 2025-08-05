# report_card_system/routes/classes.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .. import dbHelper

bp = Blueprint('classes', __name__, url_prefix='/classes')

@bp.route('/')
def list_classes():
    classes = current_app.fetch_all(dbHelper.get_classes_list_sql())
    return render_template('classes/list.html', classes=classes)

@bp.route('/create', methods=['GET', 'POST'])
def create_class():
    if request.method == 'POST':
        name = request.form['name']
        current_app.execute_query(dbHelper.insert_class_sql(), (name,))
        return redirect(url_for('classes.list_classes'))
    return render_template('classes/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_class(id):
    class_obj = current_app.fetch_one(dbHelper.get_class_by_id_sql(), (id,))
    if request.method == 'POST':
        name = request.form['name']
        current_app.execute_query(dbHelper.update_class_sql(), (name, id))
        return redirect(url_for('classes.list_classes'))
    return render_template('classes/edit.html', class_obj=class_obj)

@bp.route('/delete/<int:id>')
def delete_class(id):
    current_app.execute_query(dbHelper.delete_class_sql(), (id,))
    return redirect(url_for('classes.list_classes'))