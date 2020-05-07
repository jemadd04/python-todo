from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

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

# Create route 
@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())