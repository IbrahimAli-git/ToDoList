from datetime import datetime
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

class Base(DeclarativeBase):
    pass

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Task(db.Model):
    id:Mapped[int]=mapped_column(primary_key=True)
    task:Mapped[str]=mapped_column(nullable=False)
    def __repr__(self):
        return f"Tasks(id={self.id!r}, task={self.task!r})"

with app.app_context():
    db.create_all()

class TaskForm(FlaskForm):
    task = StringField(label="Task", validators=[DataRequired()])
    submit = SubmitField(label="Submit")

@app.route("/")
def home():
    result = db.session.execute(select(Task).order_by(Task.id))
    tasks = result.scalars().all()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["GET", "POST"])
def add():
    form = TaskForm()
    if form.validate_on_submit():
        new_task = Task(task=form.task.data)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('post.html', form=form)

@app.route("/delete/<task_id>", methods=["GET", "POST"])
def delete(task_id):
    task = db.session.execute(select(Task).where(Task.id == task_id)).scalar_one_or_none()
    if task:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)