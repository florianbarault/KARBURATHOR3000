from flask import Flask, render_template, request, redirect, session
from APP.data import bdd as b
from APP.controller import formulaire as f

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "template"
app.config.from_object('config')


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return render_template("index.html")


@app.route("/new_route")
def new_route():
    return render_template("new_route.html", info=session["statut"])


@app.route("/historic")
def historic():
    return render_template("historic.html", info=session["statut"])


@app.route("/comments")
def comments():
    return render_template("comments.html", info=session["statut"])


@app.route("/profile")
def profile():
    return render_template("profile.html", info=session["statut"])


@app.route("/signIn", methods=['POST'])
def signIn():
    login = request.form['login']
    password = request.form['password']
    msg = f.verifAuth(login, password)
    if msg == "okAuth":
        return redirect('/profile')
    else:
        return render_template("login.html", info="errorSignIn")


@app.route("/signUp", methods=['POST'])
def signUp():
    prenom = request.form['prenom']
    nom = request.form['nom']
    email = request.form['email']
    mdp1 = request.form['mdp1']
    mdp2 = request.form['mdp2']
    certif = request.form['certif']
    certification = b.getCertification(certif)
    if mdp1 != mdp2:
        return render_template("login.html", info="errorMdp")
    else:
        msg = b.verifUserEmail(email)
        print(msg)
        if msg == "userExist":
            return render_template("login.html", info="errorSignUp", )
        else:
            b.addUser(prenom, nom, email, mdp1, certification)
            session["nom"] = nom
            session["prenom"] = prenom
            session["email"] = email
            session["certification"] = certification
            session["statut"] = "user"
            return render_template("profile.html", info=session["statut"])
