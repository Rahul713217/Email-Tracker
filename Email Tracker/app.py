from flask import Flask, request
from datetime import datetime

app = Flask(__name__)

@app.route('/email_tracker', methods=['GET'])
def email_tracker():
    email = request.args.get('email')
    current_time = datetime.now()

    if email_in_database(email):
        increment_open_count(email)
    else:
        add_email_to_database(email)

    store_opened_email(email, current_time)

    return 'Email tracked!'

################################################3

import sqlite3

def initialize_database():
    connection = sqlite3.connect('email_tracker.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS opened_emails (email TEXT, opened_at TIMESTAMP, open_count INTEGER)')
    connection.commit()
    connection.close()

def email_in_database(email):
    connection = sqlite3.connect('email_tracker.db')
    cursor = connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM opened_emails WHERE email = ?', (email,))
    count = cursor.fetchone()[0]
    connection.close()
    return count > 0

def add_email_to_database(email):
    connection = sqlite3.connect('email_tracker.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO opened_emails (email, opened_at, open_count) VALUES (?, ?, ?)', (email, None, 0))
    connection.commit()
    connection.close()

def increment_open_count(email):
    connection = sqlite3.connect('email_tracker.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE opened_emails SET open_count = open_count + 1 WHERE email = ?', (email,))
    connection.commit()
    connection.close()

def store_opened_email(email, opened_at):
    connection = sqlite3.connect('email_tracker.db')
    cursor = connection.cursor()
    cursor.execute('UPDATE opened_emails SET opened_at = ?, open_count = open_count + 1 WHERE email = ?', (opened_at, email))
    connection.commit()
    connection.close()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)