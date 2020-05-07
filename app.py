from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
import sys

# Create Flask application
app = Flask(__name__)
# Configure Flask to connect to particulat db 
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://James@localhost:5432/todoapp'
# Link SQLAlchemy to Flask app 
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

# Sync model with database 
db.create_all()

# Get JSON that comes back from AJAX request
@app.route('/todos/create', methods=['POST'])
def create_todo():
    error = False
    body = {}
    try:
        description = request.get_json()['description']
        # use description to create new todo object 
        todo = Todo(description=description)
        db.session.add(todo) # adds but doesnt commit
        db.session.commit()
        body['description'] = todo.description
    except:
        error = True
        db.session.rollback()
        print(sys.exc_info()) 
    finally:
        db.session.close()
    if not error:
        return jsonify(body)

# Create index route 
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())