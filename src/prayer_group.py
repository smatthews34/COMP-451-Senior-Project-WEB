from flask import Flask, request, render_template, flash, redirect, url_for
from prayer_group_forms import InviteForm, SignupForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "weareprayergroup" #make secure

@app.route("/") #reroute somewhere
def hello():
  return "Hello World"

@app.get("/invite")
def GET_invite():
  iform = InviteForm()
  return render_template("invite.j2", form=iform)

@app.post("/invite")
def POST_invite():
  iform = InviteForm()
  if iform.validate():
    pass
    # This is where you continue to signup below

@app.get("/signup") #perhaps change route to "/signup"
def GET_signup():
    sform = SignupForm()
    return render_template("signup.j2", form=sform) #add form from above

@app.post("/signup") #perhaps change route to "/signup"
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

if __name__ == "__main__":
  app.run()