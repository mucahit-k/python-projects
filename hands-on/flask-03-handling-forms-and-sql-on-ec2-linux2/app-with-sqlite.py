# Import Flask modules
from flask import Flask, request, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
# Create an object named app
app = Flask(__name__)
# Configure sqlite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./email.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create users table within MySQL db and populate with sample data
# Execute the code below only once.
# Write sql code for initializing users table..
drop_table = 'DROP TABLE IF EXISTS users;'
users_table = """
CREATE TABLE users(
username VARCHAR NOT NULL PRIMARY KEY,
email VARCHAR);
"""
data = """
INSERT INTO users
VALUES
    ("Buddy Rich", "buddy@clarusway.com" ),
    ("Candido", "candido@clarusway.com"),
    ("Charlie Byrd", "charlie.byrd@clarusway.com");
"""

db.session.execute(drop_table)
db.session.execute(users_table)
db.session.execute(data)
db.session.commit()


# Write a function named `find_emails` which find emails using keyword from the user table in the db,
# and returns result as tuples `(name, email)`.
def find_emails(keyword):
    query = f"""
    SELECT * FROM users WHERE username LIKE '%{keyword}%';
    """
    result = db.session.execute(query)
    user_emails = [(row[0], row[1]) for row in result]
    if not any(user_emails):
        user_emails = [('Not Found', 'Not Found')]
    return user_emails

# Write a function named `insert_email` which adds new email to users table the db.
    # if user input are None (null) give warning
    # if there is no same user name in the db, then insert the new one
    # if there is user with same name, then give warning
def insert_email(name, email):
    query_name = f"""
    SELECT * FROM users WHERE username = '{name}';
    """
    result = db.session.execute(query_name)
    response = 'Error occured..'
    if name == None or email == None:
        response = 'Username or email cannot be empty!!'
    elif not any(result):
        query = f"""
        INSERT INTO users VALUES ('{name}', '{email}')
        """
        result = db.session.execute(query)
        db.session.commit()
        response = f'User {name} added successfully.'
    else: 
        response = f'User {name} already exist.'

    return response

# Write a function named `emails` which finds email addresses by keyword using `GET` and `POST` methods,
# using template files named `emails.html` given under `templates` folder
# and assign to the static route of ('/')
@app.route('/', methods = ['GET', 'POST'])
def emails():
    if request.method == 'POST':
        user_name = str(request.form['username'])
        user_emails = find_emails(user_name)
        return render_template('emails.html', name_emails = user_emails, keyword = user_name, show_result = True)
    else:
        return render_template('emails.html', show_result = False)
# Write a function named `add_email` which inserts new email to the database using `GET` and `POST` methods,
# using template files named `add-email.html` given under `templates` folder
# and assign to the static route of ('add')
@app.route('/add', methods = ['GET', 'POST'])
def add_email():
    if request.method == 'POST':
        user_name = str(request.form['username'])
        user_email = str(request.form['useremail'])
        result = insert_email(user_name, user_email)
        return render_template('add-email.html', result = result, show_result = True)
    else:
        return render_template('add-email.html', show_result = False)

# Add a statement to run the Flask application which can be reached from any host on port 80.
if __name__ == '__main__':
    app.run(debug=True)