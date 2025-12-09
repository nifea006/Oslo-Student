# Project Assignment
I am planning to create a social media platform specifically for schoolchildren in Oslo.  
The platform will only allow students from Oslo schools to join by verifying their school email domain: **"@osloskolen.no"**.  
I got the idea from the movie *"The Social Network (2010)"*, where Mark Zuckerberg created a social network exclusively for Harvard students.

---

## How to Run the App

### 1. Install Dependencies
After opening the project folder in your code editor, install the required Python dependencies.

Using a virtual environment is recommended (but optional) to avoid cluttering your global Python installation.

Example:

    python -m venv venv
    source venv/bin/activate        # macOS/Linux
    venv\Scripts\activate           # Windows

Then install the dependencies:

    pip install -r requirements.txt

If you don’t have a `requirements.txt` file, install them manually:

    pip install flask mysql-connector python-dotenv dotenv requests

---

## Database Setup (MariaDB / MySQL)
To run the webpage, you must use a MySQL-based database such as MariaDB.

1. Create a new database in MariaDB/MySQL.  
2. Fill in your database connection settings inside **app.py**.

Example from [`app.py`](/app.py):

    def create_db_connection():
        return mysql.connector.connect(
            host = DB_host or "localhost",
            user = DB_user or "your_user",
            password = DB_password or "your_password",
            database = DB_database or "your_database"
        )

Make sure these settings match your local database configuration.

---

## Running the Project
After installing dependencies and configuring the database, run the server with:

    python app.py

Then open your browser and visit:

    http://127.0.0.1:5000/
