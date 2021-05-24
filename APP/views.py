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

        dicAvion = b.getNomAvion()
        dicAerodrome = b.getNomAerodrome()

        selectedAerodrome = session['selectedAerodrome']
        selectedAvion = session['selectedAvion']

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
        return render_template("gestion.html", aerodrome=dicAerodrome ,dataAerodrome=dicDataAerodrome, avion = dicAvion, dataAvion=dicDataAvion, info=None)
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
        carb = b.calc_carbu(D,cap,vol)


        #Data nécessaires pour la page recap
        liste_etapes = b.get_etapes(vol)
        data,conso_totale=b.conso_etapes(liste_etapes,carb)

        return render_template("recap.html", table=data, coord_map=coordonnees_generales,conso_totale=conso_totale, carbu=carb, info=session["statut"])
    else:
        return redirect('/login')

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

    info = b.addAvion(nom, masse, rayon, finesse, conso, puissance, vitesse, allongement, surface)

    session['selectedAvion'] = selectedAvion

    return render_template("gestion.html", aerodrome=dicAerodrome, avion=dicAvion,dataAvion=dicDataAvion, info=info)


@app.route("/addAerodrome", methods=['POST'])
def addAerodrome():
    oaci = request.form['oaci']
    nomAerodrome = request.form['nomAerodrome']
    latitude = request.form['latitude']
    longitude = request.form['longitude']
    msg = b.addAerodrome(oaci, nomAerodrome, latitude, longitude)

    selectedAerodrome = request.form.get('selectedAerodrome')
    dicDataAerodrome = {}
    if selectedAerodrome is not None:
        dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)
    dicAvion = b.getNomAvion()
    dicAerodrome = b.getNomAerodrome()

    session['selectedAerodrome'] = selectedAerodrome

    return render_template("/gestion.html",session=session, aerodrome=dicAerodrome ,dataAerodrome=dicDataAerodrome, avion = dicAvion, info = msg)


@app.route("/modifAerodrome", methods=['POST'])
def modifAerodrome():
    dicDataAerodrome={}
    dicDataAerodrome["nom_ad"] = request.form['nomAerodrome']
    dicDataAerodrome["longitude"] = request.form['longitude']
    dicDataAerodrome["latitude"] = request.form['latitude']
    dicDataAerodrome["oaci"] = request.form['oaci']
    selectedAerodrome = session['selectedAerodrome']

    msg = b.modifAerodrome(dicDataAerodrome, selectedAerodrome)

    dicDataAerodrome = {}
    if selectedAerodrome is not None:
        dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

    dicAvion = b.getNomAvion()
    dicAerodrome = b.getNomAerodrome()
    return render_template("gestion.html", aerodrome=dicAerodrome ,dataAerodrome=dicDataAerodrome, avion=dicAvion, info=msg)

@app.route("/modifAvion", methods=['POST'])
def modifAvion():
    dicDataAvion={}
    #dicDataAvion["nom_ad"] = request.form['nomAerodrome']
    #dicDataAvion["longitude"] = request.form['longitude']
    #dicDataAvion["latitude"] = request.form['latitude']
    #dicDataAvion["oaci"] = request.form['oaci']
    selectedAvion = session['selectedAvion']
    print(selectedAvion)

    #msg = b.modifAerodrome(dicDataAvion, selectedAvion)

    dicDataAvion = {}
    if selectedAvion is not None:
        dicDataAvion = b.getDataAvion(selectedAvion)

    dicAvion = b.getNomAvion()
    dicAerodrome = b.getNomAerodrome()
    return render_template("gestion.html", aerodrome=dicAerodrome ,dataAvion=dicDataAvion, avion=dicAvion)

@app.route("/supprimerAvion", methods=['POST'])
def supprimerAvion():
    oaci = session['selectedAvion']

    b.deleteAvion(oaci)

    session['selectedAvion'] = None
    
    dicAvion = b.getNomAvion()
    dicAerodrome = b.getNomAerodrome()
    return render_template("gestion.html", aerodrome=dicAerodrome , avion=dicAvion)

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
