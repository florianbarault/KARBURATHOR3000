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
        data = b.get_comments()
        return render_template("comments.html", data=data, info=session["statut"])
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
        dicDataAvion = {}
        dicDataAerodrome = {}
        # Crée les dictionnaires de tout les ids et noms des avions et des aéroports
        session['avion'] = b.getNomAvion()
        session['aerodrome'] = b.getNomAerodrome()

        selectedAerodrome = None
        selectedAvion = None

        selectedAvion = request.form.get("selectedAvion")
        if selectedAvion == "":
            selectedAvion = None
        elif selectedAvion is not None:
            selectedAvion = int(selectedAvion)
            dicDataAvion = b.getDataAvion(selectedAvion)

        selectedAerodrome = request.form.get('selectedAerodrome')
        if selectedAerodrome == "":
            selectedAerodrome = None
        elif selectedAerodrome is not None:
            selectedAvion = request.form.get('selectedAvion')
            dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

        session['selectedAerodrome'] = selectedAerodrome
        session['selectedAvion'] = selectedAvion
        return render_template("gestion.html", dataAerodrome=dicDataAerodrome, dataAvion=dicDataAvion, info=None)
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
    # Récupère les données du formulaire d'inscription
    prenom = request.form['prenom']
    nom = request.form['nom']
    email = request.form['email']
    mdp1 = request.form['mdp1']
    mdp2 = request.form['mdp2']
    certif = request.form['certif']
    certification = b.getCertification(certif)
    # Vérifie que les deux mots de passe concordent
    if mdp1 != mdp2:
        return render_template("login.html", info="errorMdp")
    else:
        msg = b.verifUserEmail(email)
        print(msg)
        if msg == "userExist":
            return render_template("login.html", info="errorSignUp", )
        else:
            # Ajoute l'utilisateur à la bdd
            b.addUser(prenom, nom, email, mdp1, certification)
            # Crée des données de session pour l'utilisateur
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
        carb = b.calc_carbu(D,cap,vol)


        #Data nécessaires pour la page recap
        liste_etapes = b.get_etapes(vol)
        data,conso_totale=b.conso_etapes(liste_etapes,carb)

        return render_template("recap.html", table=data, coord_map=coordonnees_generales,conso_totale=conso_totale, carbu=carb, info=session["statut"])
    else:
        return redirect('/login')

@app.route("/addAvion", methods=['POST'])
def addAvion():
    # Récupère les éléments du nouvel avion
    nom = request.form['nom']
    rayon = request.form['rayon']
    conso = request.form['conso']
    vitesse = request.form['vitesse']
    # Ajoute les éléments du nouvel avion à la bdd
    dicDataAvion ={}
    selectedAvion = request.form.get('selectedAvion')
    if selectedAvion is not None:
        selectedAvion = int(selectedAvion)
        dicDataAvion = b.getDataAvion(selectedAvion)

    info = b.addAvion(nom, rayon, conso, vitesse)

    session['selectedAvion'] = selectedAvion

    return render_template("gestion.html",dataAvion=dicDataAvion, info=info)


@app.route("/addAerodrome", methods=['POST'])
def addAerodrome():
    # Récupère les éléments du nouvel aérodrome
    oaci = request.form['oaci']
    nomAerodrome = request.form['nomAerodrome']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    # Ajoute le séléments du nouvel aérodrome dans la bdd
    msg = b.addAerodrome(oaci, nomAerodrome, latitude, longitude)

    selectedAerodrome = session['selectedAerodrome']
    dicDataAerodrome = {}
    if selectedAerodrome is not None:
        dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

    return render_template("/gestion.html",session=session, dataAerodrome=dicDataAerodrome, info = msg)


@app.route("/modifAerodrome", methods=['POST'])
def modifAerodrome():
    # Récypère les éléments modifiés de l'aérodrome
    dicDataAerodrome={}
    dicDataAerodrome["nom_ad"] = request.form['nomAerodrome']
    dicDataAerodrome["longitude"] = request.form['longitude']
    dicDataAerodrome["latitude"] = request.form['latitude']
    dicDataAerodrome["oaci"] = request.form['oaci']

    selectedAerodrome = session['selectedAerodrome']
    # Effectue la modification dans la bdd
    msg = b.modifAerodrome(dicDataAerodrome, selectedAerodrome)
    # Charge les nouvelles données de l'aérodrome
    dicDataAerodrome = {}
    if selectedAerodrome is not None:
        dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

    return render_template("gestion.html",dataAerodrome=dicDataAerodrome, info=msg)

@app.route("/modifAvion", methods=['POST'])
def modifAvion():
    # Récupération des données du formulaire
    dicDataAvion={}
    dicDataAvion["reference"] = request.form["reference"]
    dicDataAvion["rayonAction"] = request.form["rayonAction"]
    dicDataAvion["consoHoraire"] = request.form["consoHoraire"]
    dicDataAvion["vitesseCroisiere"] = request.form["vitesseCroisiere"]
    # Récupère l'avion selectionné
    selectedAvion = session['selectedAvion']
    # Effectue la modification dans la bdd
    msg = b.modifAvion(dicDataAvion, selectedAvion)
    # Charge les nouvelles données de l'avion
    dicDataAvion = {}
    if selectedAvion is not None:
        dicDataAvion = b.getDataAvion(selectedAvion)

    return render_template("gestion.html",dataAvion=dicDataAvion)

@app.route("/supprimerAvion", methods=['POST'])
def supprimerAvion():
    oaci = session['selectedAvion']
    # Supprime de la bdd l'aérodrome de code OACI
    b.deleteAvion(oaci)

    session['selectedAvion'] = None
    
    return render_template("gestion.html")

@app.route("/cv", methods=['GET'])
def cv():
    return render_template("cv.html")

@app.route("/addcomment", methods=['POST', 'GET'])
def addcomment():
    if session.get("idUtilisateur"):
        idUtilisateur = session["idUtilisateur"]
        msg = request.form['comment']
        b.add_comment(idUtilisateur,msg)
        data = b.get_comments()
        return render_template("comments.html", data=data, info=session["statut"])

    else:
        return redirect('/login')

@app.route("/modifMotDePasse", methods=['POST'])
def modifMotDePasse():
    password = request.form['password']
    mdp1 = request.form['mdp1']
    mdp2 = request.form['mdp2']
    msg = b.verifMdp(session['email'], password)
    if msg != "okMdp":
        # Mauvais mot de passe
        return render_template("profile.html", info="errorMdp3", )
    else:
        # Bon mot de passe
        if mdp1 != mdp2:
            # Nouveaux mot de passe différents
            return render_template("profile.html", info="errorMdp1")
        elif password == mdp1:
            # Ancien et nouveau mot de passe sont similaires
            return render_template("profile.html", info="errorMdp2")
        else:
            # Tout est bon
            msg = b.modifMdp(session['email'], mdp1)
            return render_template("profile.html")
