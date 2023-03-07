from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6dofnzWlSihBXox7C0sKR6b'
Bootstrap(app)

# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class TodoForm(FlaskForm):
    name = StringField('', validators=[DataRequired()], render_kw={'autofocus': True, "placeholder": "Add task:"})


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    done = db.Column(db.Boolean, default=False)


@app.route("/", methods=["GET", "POST"])
def home():
    form = TodoForm()
    if form.validate_on_submit():
        new_todo = Todo(
            name=form.name.data)
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for('home'))

    all_todo = db.session.query(Todo).all()
    return render_template('index.html', form=form, data=all_todo)


@app.route("/delete", methods=["GET", "POST"])
def delete_todo():
    todo_id = request.args.get('todo_id')
    todo_to_delete = Todo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/check", methods=["GET", "POST"])
def check_todo():
    todo_id = request.args.get('todo_id')
    todo_to_check = Todo.query.get(todo_id)
    if todo_to_check.done:
        todo_to_check.done = False
    else:
        todo_to_check.done = True
    db.session.commit()
    return redirect(url_for('home'))


with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
