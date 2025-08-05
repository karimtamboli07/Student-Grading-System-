from flask import Flask, render_template
import mysql.connector
import os


def create_app(): # Encapsulate app creation in a function for clarity
    app = Flask(__name__, template_folder='templates') # Explicitly set template folder

    # Database configuration
    app.config['DATABASE_CONFIG'] = {
        'user': 'root',
        'password': 'password', # Replace with your MySQL password
        'host': 'localhost',
        'database': 'report_card_system'
    }
    # app.config['DATABASE_CONFIG'] = {
    #     'host': os.environ.get('DATABASE_HOST'),           # Read from environment variable DATABASE_HOST
    #     'port': int(os.environ.get('DATABASE_PORT', 3306)), # Read DATABASE_PORT, default to 3306 if not set
    #     'user': os.environ.get('DATABASE_USER'),           # Read DATABASE_USER
    #     'password': os.environ.get('DATABASE_PASSWORD'),     # Read DATABASE_PASSWORD
    #     'database': os.environ.get('DATABASE_NAME'),       # Read DATABASE_NAME
    # }

    # Function to get database connection (remains the same)
    def get_db_connection():
        config = app.config['DATABASE_CONFIG']
        conn = mysql.connector.connect(**config)
        return conn

    app.db_connection = get_db_connection

    # Utility database functions (remains the same)
    def fetch_all(query, params=None):
        conn = app.db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        conn.close()
        return results

    def fetch_one(query, params=None):
        conn = app.db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        result = cursor.fetchone()
        conn.close()
        return result

    def execute_query(query, params=None):
        conn = app.db_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        conn.close()

    app.fetch_all = fetch_all
    app.fetch_one = fetch_one
    app.execute_query = execute_query

    # Import and register blueprints (imports are now relative within package)
    #from .routes import categories, subjects, students, marks, users, classes
    from report_card_system.routes import categories_bp, subjects_bp, students_bp, marks_bp, users_bp, classes_bp # Import the blueprint instances
    app.register_blueprint(categories_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(marks_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(classes_bp)

    @app.route('/')
    def home():
        return render_template('home.html')

    return app # Return the created app instance

#app = create_app() # Create the app instance

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0') # Ensure host='0.0.0.0' is present