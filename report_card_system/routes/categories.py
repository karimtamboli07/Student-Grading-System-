# report_card_system/routes/categories.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .. import dbHelper

bp = Blueprint('categories', __name__, url_prefix='/categories')

@bp.route('/')
def list_categories():
    categories = current_app.fetch_all(dbHelper.get_categories_list_sql())
    return render_template('categories/list.html', categories=categories)

@bp.route('/create', methods=['GET', 'POST'])
def create_category():
    if request.method == 'POST':
        name = request.form['name']
        grade_from = request.form['grade_from']
        grade_to = request.form['grade_to']
        current_app.execute_query(dbHelper.insert_category_sql(), (name, grade_from, grade_to))
        return redirect(url_for('categories.list_categories'))
    return render_template('categories/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = current_app.fetch_one(dbHelper.get_category_by_id_sql(), (id,))
    if request.method == 'POST':
        name = request.form['name']
        grade_from = request.form['grade_from']
        grade_to = request.form['grade_to']
        current_app.execute_query(dbHelper.update_category_sql(), (name, grade_from, grade_to, id))
        return redirect(url_for('categories.list_categories'))
    return render_template('categories/edit.html', category=category)

@bp.route('/delete/<int:id>')
def delete_category(id):
    current_app.execute_query(dbHelper.delete_category_sql(), (id,))
    return redirect(url_for('categories.list_categories'))