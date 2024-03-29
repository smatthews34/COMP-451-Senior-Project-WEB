from flask import Flask, request, render_template, flash, redirect, url_for, flash, session
from flask_login import login_manager, login_required
from prayer_group_forms import InviteForm, SignupForm, LoginForm, GroupForm, GuidedForm
import firebase_admin
from firebase_admin import credentials, firestore, auth
import json, requests

# Database setup
cred = credentials.Certificate('prayer-group-fc24c-firebase-adminsdk-xav6o-9d178f3518.json')
app = firebase_admin.initialize_app(cred)
db = firestore.client()
FIREBASE_WEB_API_KEY = "AIzaSyAMBpbtmxZC0nZcsWvvkJi8enndmG9pGIU"
rest_api_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

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
      user = auth.create_user(email = str(sform.email.data), password = str(sform.password.data))
      doc_ref = db.collection(u'User').document(user.uid)
      doc_ref.set({
      'address': sform.home_address.data,
      'email': sform.email.data,
      'firstName': sform.fname.data,
      'lastName': sform.lname.data,
      'phoneNumber': sform.phone_num.data
      })
      r, code = sign_in_with_email_and_password(sform.email.data, sform.password.data)
      uid = r['localId']
      token = r['idToken']
      email = r['email']
      refresh_token = r['refreshToken'] #all info that may be useful for sessions
      return redirect(url_for("home"))
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
    r, code = sign_in_with_email_and_password(lform.email.data, lform.password.data)
    if code == 400:
      flash("Email or password not found, please try again")
      return redirect(url_for("GET_login"))
    else:
      uid = r['localId']
      token = r['idToken']
      email = r['email']
      refresh_token = r['refreshToken'] #all info that may be useful for sessions
      return redirect(url_for("home"))
  else: #basic error handling
    for field, error in lform.errors.items():
      flash(f"{field}: {error}")
      return redirect(url_for("GET_login"))

@app.route("/home")
def home():
  return render_template("main.j2")

@app.route("/prayerlist")
def prayerlist():
  prayer_ref =  db.collection(u'Prayer Request')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("prayerlist.j2", requests=jsonRequests)

@app.route("/admin")
def admin_splash():
  return render_template("adminmain.j2")

@app.route("/admin/prayerlist")
def prayer_list():
  prayer_ref =  db.collection(u'Prayer Request')
  request = prayer_ref.stream()
  jsonRequests = []
  
  # So the requests in the request variable above are of type DocumentSnapshot. Without converting
  # them to dictionaries, we really can't do much with them. Thus, the loop below grabs each DocumentSnapshot
  # and converts it to a dictionary and appends that dictionary to the jsonRequests list.
  # In the HTML document, you will see that we can access the values at a key using request['key'].
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminprayerlist.j2", requests=jsonRequests)

@app.route("/admin/guidedprayers")
def admin_guided_prayers():
  prayer_ref =  db.collection(u'Guided Prayer')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminguidedprayers.j2", requests=jsonRequests)
  
@app.route("/admin/guidedprayers/add" , methods = ["GET","POST"]) #need to figure out how to add something to database in python
def admin_guided_prayers_add():
  prayer_ref =  db.collection(u'Guided Prayer')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminprayeradd.j2", requests=jsonRequests)

@app.route("/admin/guidedprayers/edit" , methods = ["GET","POST"]) #should be similar
def admin_guided_prayers_edit():
  prayer_ref =  db.collection(u'Guided Prayer')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminprayeredit.j2", requests=jsonRequests)

@app.route("/admin/smallgroups")
def admin_small_groups():
  prayer_ref =  db.collection(u'Group')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminsmallgroups.j2", requests=jsonRequests)

@app.route("/admin/smallgroups/add", methods = ["GET","POST"]) #need to figure out how to add something to database in python
def admin_small_groups_add():
  form = GroupForm()
  prayer_ref =  db.collection(u'Users')
  data = prayer_ref.stream()
  jsonRequests = []
  for doc in data:
    jsonRequests.append(doc.to_dict())
  if request.method == "GET":
    return render_template("admingroupadd.j2", data=jsonRequests)
  if request.method == "POST":
    pass

@app.route("/admin/guidedprayers/edit" , methods = ["GET","POST"]) #should be similar
def admin_small_groups_edit():
  prayer_ref =  db.collection(u'Guided Prayer')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminprayeredit.j2", requests=jsonRequests)
  

@app.route("/admin/adminlist")
def admin_admin_list():
  prayer_ref =  db.collection(u'Admin')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminadminlist.j2", requests=jsonRequests)
  

@app.route("/admin/memberlist")
def admin_members_list():
  prayer_ref =  db.collection(u'User')
  request = prayer_ref.stream()
  jsonRequests = []
  for doc in request:
    jsonRequests.append(doc.to_dict())
  return render_template("adminmemberslist.j2", requests=jsonRequests)
  

def sign_in_with_email_and_password(email: str, password: str, return_secure_token: bool = True): #REST API set up with help from https://betterprogramming.pub/user-management-with-firebase-and-python-749a7a87b2b6
  payload = json.dumps({
      "email": email,
      "password": password,
      "returnSecureToken": return_secure_token
  })
  r = requests.post(rest_api_url, params={"key": FIREBASE_WEB_API_KEY}, data=payload)
  return r.json(), r.status_code

if __name__ == "__main__":
  app.run()