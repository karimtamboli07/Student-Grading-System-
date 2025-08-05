# Student Grading System

A web-based application built with Flask for managing student records and generating report cards. This system connects to a MySQL database to store student information and uses ReportLab to create printable PDF reports.

## Features

*   **Student Management:** Add, view, and update student details.
*   **Grading:** Input marks for various subjects.
*   **PDF Report Generation:** Automatically generate and download student report cards in PDF format.
*   **Containerized:** Fully containerized with Docker for easy setup and deployment.

## Tech Stack

*   **Backend:** Python, Flask
*   **Database:** MySQL (`mysql-connector-python`)
*   **PDF Generation:** ReportLab, Pillow
*   **WSGI Server:** Gunicorn
*   **Containerization:** Docker

## Getting Started

To run this application, you will need to have Docker installed on your machine.

### Running with Docker

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/karimtamboli07/student-grading-system-.git
    cd student-grading-system-
    ```

2.  **Build the Docker image:**
    ```sh
    docker build -t student-grading-system .
    ```

3.  **Run the Docker container:**
    The application will be exposed on port `5000`.
    ```sh
    docker run -p 5000:5000 student-grading-system
    ```

4.  **Access the application:**
    Open your web browser and navigate to `http://localhost:5000`.

## Project Structure

```
.
├── Dockerfile              # Defines the Docker container environment
├── requirements.txt        # Python dependencies for the project
└── report_card_system/     # Main Flask application source code
