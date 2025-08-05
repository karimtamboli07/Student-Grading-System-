# report_card_system/routes/users.py
from flask import Blueprint, render_template, request, redirect, url_for, current_app
from .. import dbHelper

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def list_users():
    users = current_app.fetch_all(dbHelper.get_users_list_sql())
    return render_template('users/list.html', users=users)

@bp.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_superuser = 'is_superuser' in request.form
        current_app.execute_query(dbHelper.insert_user_sql(), (username, password, is_superuser))
        return redirect(url_for('users.list_users'))
    return render_template('users/create.html')

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_user(id):
    user = current_app.fetch_one(dbHelper.get_user_by_id_sql(), (id,))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_superuser = 'is_superuser' in request.form
        current_app.execute_query(dbHelper.update_user_sql(), (username, password, is_superuser, id))
        return redirect(url_for('users.list_users'))
    return render_template('users/edit.html', user=user)

@bp.route('/delete/<int:id>')
def delete_user(id):
    current_app.execute_query(dbHelper.delete_user_sql(), (id,))
    return redirect(url_for('users.list_users'))