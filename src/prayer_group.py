from flask import Flask, request, render_template, flash, redirect, url_for
from prayer_group_forms import InviteForm, SignupForm, LoginForm
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth

# Database setup
cred = credentials.Certificate('Prayer-Group-WEB\prayer-group-fc24c-firebase-adminsdk-xav6o-9d178f3518.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()

# Flask setup
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
    if sform.validate(): #Make sure that the email does not already exist
      user = auth.create_user(email = sform.email.data)
      doc_ref = db.collection(u'User').document(user.uid)
      doc_ref.set({
      'address': sform.home_address.data,
      'email': sform.email.data,
      'firstName': sform.fname.data,
      'lastName': sform.lname.data,
      'phoneNumber': sform.phone_num.data
      })
      return "All signed up!" #redirect to home page with logged in session
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
    return "This will be completed soon" #IMPORTANT: This is where DB will be checked to ensure that user can be logged in
  else: #basic error handling
        for field, error in lform.errors.items():
            flash(f"{field}: {error}")
        return redirect(url_for("GET_login"))

@app.route("/admin/prayerlist")
def prayer_list():
  list =  db.reference('/Prayer Group')
  return render_template("adminprayerlist.j2")

if __name__ == "__main__":
  app.run()