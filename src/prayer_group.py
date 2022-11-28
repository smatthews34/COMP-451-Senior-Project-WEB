from flask import Flask, request, render_template, flash, redirect, url_for
from prayer_group_forms import InviteForm, SignupForm, LoginForm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('Prayer-Group-WEB\prayer-group-fc24c-firebase-adminsdk-xav6o-9d178f3518.json')
firebase_admin.initialize_app(cred)

#How to access a node reference: ref = db.reference('Database reference')
#print(ref.get())

app = Flask(__name__)
app.config["SECRET_KEY"] = "weareprayergroup" #make secure

@app.route("/")
def hello():
  return redirect(url_for("GET_invite"))

@app.get("/invite")
def GET_invite():
  iform = InviteForm()
  return render_template("invite.j2", form=iform)

@app.post("/invite")
def POST_invite():
  iform = InviteForm()
  if iform.validate():
    return redirect(url_for("GET_signup"))  # IMPORTANT: This will be changed to allow for code valdation before the redirect
  else: #basic error handling
        for field, error in iform.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("GET_invite"))

@app.get("/signup")
def GET_signup():
    sform = SignupForm()
    return render_template("signup.j2", form=sform)

@app.post("/signup")
def POST_signup():
    sform = SignupForm()
    if sform.validate():
      pass
      # This is where a new user is created and added to db
        # temp = Student(
        #     fname=sform.fname.data,
        #     lname=sform.lname.data,
        #     mintial=sform.mintial.data,
        #     student_id=sform.student_id.data,
        #     gender=sform.gender.data,
        #     grad_year=sform.grad_year.data,
        #     email=sform.email.data,
        #     phone_num=sform.phone_num.data,
        #     password=sform.password.data,
        # )
        # db.session.add(temp)
        # db.session.commit()
        # return redirect(url_for("main_page"))
    else: #basic error handling
        for field, error in sform.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("GET_signup"))

@app.get("/login")
def GET_login(): #Get login form
  lform = LoginForm()
  return render_template("login.j2", form=lform)

@app.post("/login")
def POST_login(): #Post login form
  lform = LoginForm()
  if lform.validate:
    pass #IMPORTANT: This is where DB will be checked to ensure that user can be logged in
  else: #basic error handling
        for field, error in lform.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("GET_login"))

if __name__ == "__main__":
  app.run()