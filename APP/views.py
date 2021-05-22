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

@app.route("/gestion", methods=['POST', 'GET'])
def gestion():
    if session.get("idUtilisateur"):
        selectedAvion = request.form.get('selectedAvion')
        selectedAerodrome = request.form.get('selectedAerodrome')
        dicDataAvion = {}
        dicDataAerodrome = {}
        if selectedAvion is not None:
            selectedAvion = int(selectedAvion)
            dicDataAvion = b.getDataAvion(selectedAvion)
        if selectedAerodrome is not None:
            dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)
        dicAvion = b.getNomAvion()
        dicAerodrome = b.getNomAerodrome()
        return render_template("gestion.html", aerodrome=dicAerodrome ,dataAerodrome=dicDataAerodrome, avion = dicAvion, dataAvion=dicDataAvion, selectedAvion=selectedAvion)
    else:
        return redirect('/login')

@app.route("/signIn", methods=['POST'])
def signIn():
    login = request.form['login']
    password = request.form['password']
    msg = f.verifAuth(login, password)
    if msg == "okAuth":
        if session['statut'] == "user":
            return redirect('/profile')
        elif session['statut'] =="admin":
            return redirect('/gestion')
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

        #Ajout vol

        idUtilisateur = session["idUtilisateur"]
        num_avion = request.form['select_avion']
        dir_vent = request.form['vent_dir']
        vit_vent = request.form['vent_vit']
        date = request.form['date']
        new_flight = [num_avion, date, idUtilisateur, vit_vent, dir_vent]
        b.ajout_vol(new_flight)

        #Ajout étapes

        idVol = b.get_idVol(idUtilisateur)
        vol = idVol[0][0]
        etapes = request.form['etapes']
        b.ajout_etapes(vol,etapes)

        #Calculs pour les estimations

        D,cap,coordonnees_generales = b.get_dist(vol)
        #b.calc_carbu(coord,vol)


        #Data nécessaires pour la page recap
        liste_etapes = b.get_etapes(vol)

        return render_template("recap.html", table=liste_etapes, coord_map=coordonnees_generales, info=session["statut"])
    else:
        return redirect('/login')
    # num_avion = request.form['select_avion']
    # avion = b.getNomAvion()[int(num_avion)]
    # return avion

@app.route("/addAvion", methods=['POST'])
def addAvion():
    nom = request.form['nom']
    masse = request.form['masse']
    rayon = request.form['rayon']
    finesse = request.form['finesse']
    conso = request.form['conso']
    puissance = request.form['puissance']
    vitesse = request.form['vitesse']
    allongement = request.form["allongement"]
    surface = request.form["surface"]

    dicAerodrome = b.getNomAerodrome()
    dicAvion = b.getNomAvion()
    dicDataAvion ={}
    selectedAvion = request.form.get('selectedAvion')
    if selectedAvion is not None:
        selectedAvion = int(selectedAvion)
        dicDataAvion = b.getDataAvion(selectedAvion)

    b.addAvion(nom, masse, rayon, finesse, conso, puissance, vitesse, allongement, surface)

    return render_template("gestion.html", aerodorme=dicAerodrome, avion=dicAvion,dataAvion=dicDataAvion, selectedAvion=selectedAvion)
