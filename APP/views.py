from flask import Flask, render_template, request, redirect, session
from APP.data import bdd as b
from APP.controller import formulaire as f

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "template"
app.config.from_object('config')


@app.route("/")
def index():
    session["totalUser"] = b.countAllFrom('utilisateurs', condition="statut='user'")
    session['totalFlight'] = b.countAllFrom('vol')
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    session["totalUser"] = b.countAllFrom('utilisateurs',condition="statut='user'")
    session['totalFlight'] = b.countAllFrom('vol')
    return render_template("index.html")


@app.route("/new_route")
def new_route():
    if session.get("idUtilisateur"):

        liste = b.getaerodrome()
        dicNomAvion = b.getNomAvion()
        return render_template("new_route.html", info=session["statut"], data=liste, avion=dicNomAvion)
    else:
        return redirect('/login')

@app.route("/historic")
def historic():
    if session.get("idUtilisateur"):
        histo = b.get_histo(session["idUtilisateur"])
        return render_template("historic.html", data=histo, info=session["statut"])
    else:
        return redirect('/login')


@app.route("/comments")
def comments():
    if session.get("idUtilisateur"):
        return render_template("comments.html", info=session["statut"])
    else:
        return redirect('/login')

@app.route("/profile")
def profile():
    if session.get("idUtilisateur"):
        return render_template("profile.html", info=session["statut"])
    else:
        return redirect('/login')

@app.route("/gestion")
def gestion():
    liste = b.getaerodrome()
    dicNomAvion = b.getNomAvion()
    return render_template("gestion.html", data=liste, avion=dicNomAvion)

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

@app.route("/addflight", methods=['POST'])
def addflight():
    if session.get("idUtilisateur"):
        idVol= b.get_idVol(session["idUtilisateur"])
        print(int(idVol[0][0]))
        return render_template("index.html",  info=session["statut"])

    else:
        return redirect('/login')
    # num_avion = request.form['select_avion']
    # avion = b.getNomAvion()[int(num_avion)]
    # return avion