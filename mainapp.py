from flask import Flask, render_template, redirect, url_for, session, request
import json
from wtforms import Form, StringField, PasswordField, validators, TextAreaField, IntegerField
# DB Imports
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
# Error Handling
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config.from_file("config.json",load=json.load)

# -----------------------------------------------------------
db = SQLAlchemy(app)
# -----------------------------------------------------------    

class RegisterForm(Form):
    username = StringField("Username",validators=[
        validators.DataRequired()
    ])
    password = PasswordField("Password",validators=[
        validators.DataRequired(),
    ])


@app.route("/", methods = ["GET", "POST"])
def index():
    form = RegisterForm(request.form)
    if request.method == "POST" and form.validate():
        newUser = Users(
            username = form.username.data,
            password = form.password.data
        )
        try:
            db.session.add(newUser)
            db.session.commit()
            return "SUCCESS"
        except IntegrityError as error:
            db.session.rollback()
            return redirect(url_for("index"))
        
    else:
        return render_template("index.html", form = form)
    
@app.route("/user/<int:userid>")
def showUser(userid):
    user = db.get_or_404(Users, userid)
    return f"{user.username} ---- {user.password}"

@app.route("/deleteuser/<int:userid>")
def deleteUser(userid):
    user = db.get_or_404(Users, userid)
    db.session.delete(user)
    db.session.commit()
    return "delet success"
    

if __name__ == "__main__":
    with app.app_context():
        # Oluşturulacak Tablelar class olarak oluşturulur. Table isimleri camelcase'den snake_case haline çevrilir.
        class Users(db.Model):
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            username: Mapped[str] = mapped_column(String(30), nullable=False, unique=True)
            password: Mapped[str] = mapped_column(String(30),nullable=False)

        class Deneme(db.Model):
            id: Mapped[int] = mapped_column(Integer, primary_key=True)
            deneme1 : Mapped[str] = mapped_column(String(19))
        
        db.create_all()
    app.run(debug=True)