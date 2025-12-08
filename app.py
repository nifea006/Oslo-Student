from flask import Flask, render_template, request, redirect
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
import bcrypt
import datetime

load_dotenv()

app = Flask(__name__)

DB_host = os.getenv('DB_host')
DB_user = os.getenv('DB_user')
DB_password = os.getenv('DB_password')
DB_database = os.getenv('DB_database')

def create_db_connection():
    return mysql.connector.connect(
        host = DB_host,
        user = DB_user,
        password = DB_password,
        database = DB_database
    )

def create_user_table():
    try:
        conn = create_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                birthday DATE NOT NULL,
                age INT NOT NULL
            )
        """)
        conn.commit()
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

create_user_table()

@app.route('/login')
def login():
    email = request.args.get('email')
    password = request.args.get('password')

    conn = create_db_connection()
    cursour = conn.cursor()
    cursour.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursour.fetchone()
    cursour.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result[0].encode('utf-8')):
        print("Innlogging vellykket!", "Du er nå logget inn.")
        return redirect('/')
    else:
        print("Innlogging mislyktes!", "Ugyldig e-post eller passord.")
    return render_template('Login/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('Login/register.html')
    
    email = request.form.get('email')

    conn = create_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    if result:
        print("Registrering mislyktes!", "E-posten er allerede registrert.")
        cursor.close()
        return render_template('Register/register.html')
    
    password = request.form.get('password')
    comfirm_password = request.form.get('comfirm-password')
    if comfirm_password != password:
        print("Registrering mislyktes!", "Passordene stemmer ikke overens.")
        password_PyBytes = password.encode('utf-8')
        hashed_password = bcrypt.hashpw(password_PyBytes, bcrypt.gensalt())
        return render_template('Register/register.html')
    
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    birthday = request.form.get('birthday')
    age = datetime.datetime.now().year - datetime.datetime.strptime(birthday, '%Y-%m-%d').year

    cursor.execute("""
        INSERT INTO users (email, password, first_name, last_name, birthday, age)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (email, hashed_password, first_name, last_name, birthday, age))
    conn.commit()
    cursor.close()

    if cursor.rowcount == 1:
        print("Registrering vellykket!", "Du har blitt registrert.")
        return redirect('/')
    return render_template('Register/register.html')

@app.route('/')
def home():
    # Get the information about the user from the login/register page and database    
    return render_template('Main Menu/home.html')

@app.route('/profile')
def user_info():
    conn = create_db_connection()
    cursor = conn.cursor()
    
    email = request.args.get('email')
    
    cursor.execute("""
        SELECT email, first_name, last_name, birthday, age FROM users WHERE email = %s
    """, (email,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    return render_template('User/user-info.html', user=result)

if __name__ == '__main__':
    app.run(debug=True)