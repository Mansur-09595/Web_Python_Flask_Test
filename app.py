import re
from flask.globals import request
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route("/", methods=("GET", "POST"))
def home():
    form = []
    try:    
        form = Users.query.all()
        
        user = Users(name=request.form['name'], 
                        number=request.form['number'],
                        distance=request.form['distance']
            )
        db.session.add(user)
        db.session.commit()
    except:
        db.session.rollback()
        print("Ошибка добавления в БД")
    
    page = request.args.get('page', 1, type=int)
    posts = Users.query.order_by(Users.date.desc()).paginate(page=page, per_page=3)

    if request.form.get("submit_a"):
	    form = Users.query.order_by(Users.number.asc())
    elif request.form.get("submit_b"):
        form = Users.query.order_by(Users.number.desc())
    else:
        print("Ошибка добавления")

    return render_template("home.html", title="Главная страница", form=form, posts=posts)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    name = db.Column(db.String(50), nullable=True)
    number = db.Column(db.Integer)
    distance = db.Column(db.Float)

    def __repr__(self):
        return f"{self.date} | {self.name} | {self.number} | {self.distance}"


if __name__ == "__main__":
    app.run(debug=True, use_debugger=False, use_reloader=False)