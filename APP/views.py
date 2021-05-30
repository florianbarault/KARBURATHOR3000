from flask import Flask, render_template, request, redirect, session
from flask.helpers import url_for
from APP.data import bdd as b
from APP.controller import formulaire as f

app = Flask(__name__)
app.static_folder = "static"
app.template_folder = "template"
app.config.from_object('config')


@app.route("/")
def index():
    f.logout()
    f.index()
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route('/logout')
def logout():
    f.logout()
    return render_template("index.html")

@app.route("/new_route")
def new_route():
    if f.verifLog():
        return render_template("new_route.html", data=b.getaerodrome(), avion=b.getNomAvion())
    else:
        return redirect('/login')

@app.route("/historic")
def historic():
    if f.verifLog():
        return render_template("historic.html", data=b.get_histo(session["idUtilisateur"]))
    else:
        return redirect('/login')

@app.route("/comments")
def comments():
    if f.verifLog():
        return render_template("comments.html", data=b.get_comments())
    else:
        return redirect('/login')

@app.route("/profile")
def profile():
    if f.verifLog():
        f.profile()
        return render_template("profile.html")
    else:
        return redirect('/login')

@app.route("/gestion", methods=['POST', 'GET'])
def gestion():
    if f.verifLog():
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
        redirect(url_for('login'))


@app.route("/signIn", methods=['POST'])
def signIn():
    # Récupère les données de connexion
    login = request.form['login']
    password = request.form['password']
    # Vérifie l'authentification
    msg = f.verifAuth(login, password)
    if msg == "okAuth":
        if session['statut'] == "user":
            f.profile()
            return render_template("profile.html")
        elif session['statut'] =="admin":
            
            return redirect(url_for('gestion'))
    else:
        return render_template("login.html", info="errorSignIn")


@app.route("/signUp", methods=['POST'])
def signUp():
    # Récupère les données du formulaire d'inscription
    data={}
    for elt in ['prenom', 'nom', 'email', 'mdp1', 'mdp2', 'certification']:
        data[elt] = request.form["{}".format(elt)]
    info = f.signUp(data)    
    return render_template("profile.html") if info is None else render_template("login.html", info=info)

@app.route("/addflight", methods=['POST'])
def addflight():
    if f.verifLog():

        #Ajout vol

        idUtilisateur = session["idUtilisateur"]
        num_avion = request.form['select_avion']
        dir_vent = request.form['vent_dir']
        vit_vent = request.form['vent_vit']
        date = request.form['date']
        type_vol = request.form['select_type']
        new_flight = [num_avion, date, idUtilisateur, vit_vent, dir_vent, type_vol]
        b.ajout_vol(new_flight)

        #Ajout étapes

        idVol = b.get_idVol(idUtilisateur)
        vol = idVol[0][0]
        etapes = request.form['etapes']
        if len(etapes)<2:
            return render_template("new_route.html", data=b.getaerodrome(), avion=b.getNomAvion(), info="pbEtape")
        else:
            b.ajout_etapes(vol,etapes)

            #Calculs pour les estimations

            dist, carb, coordonnees_generales = b.update_info(vol)

            #Data nécessaires pour la page recap
            liste_etapes = b.get_etapes(vol)
            data, conso_totale, dist_totale=b.conso_dist_etapes(liste_etapes,carb,dist)

            return render_template("recap.html", table=data, coord_map=coordonnees_generales, conso_totale=conso_totale, dist_totale=dist_totale, info=session["statut"])
    else:
        return redirect(url_for('/login'))

@app.route("/addAvion", methods=['POST'])
def addAvion():
    # Récupère les éléments du nouvel avion
    dicAvion={}
    for elt in ['reference', 'rayonAction', 'consoHoraire', 'vitesseCroisiere']:
        dicAvion[elt] = request.form["{}".format(elt)]

    info = b.addAvion(dicAvion)
    print(info)
    session['avion'] = b.getNomAvion()
    avion=session['avion']
    selectedAvion=session['selectedAvion']
    for k, v in avion.items():
        if dicAvion['reference'] == v:
            selectedAvion = k

    # Ajoute les éléments du nouvel avion à la bdd
    dicDataAvion ={}
    if selectedAvion is not None:
        selectedAvion = int(selectedAvion)
        dicDataAvion = b.getDataAvion(selectedAvion)
    session['selectedAvion'] = selectedAvion

    return render_template("gestion.html", info="okAddAvion", dataAvion=dicDataAvion)


@app.route("/addAerodrome", methods=['POST'])
def addAerodrome():
    # Récupère les éléments du nouvel aérodrome
    dicAerodrome={}
    for elt in ['oaci', 'nom_ad', 'latitude', 'longitude']:
        dicAerodrome[elt] = request.form["{}".format(elt)]

    if len(dicAerodrome['oaci']) != 4:
        selectedAerodrome = None
        return render_template("/gestion.html", info = "errorOaci")

    else:
        # Ajoute le séléments du nouvel aérodrome dans la bdd
        msg = b.addAerodrome(dicAerodrome)

        selectedAerodrome=dicAerodrome['oaci']
        dicDataAerodrome = {}
        if selectedAerodrome is not None:
            dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

        session["selectedAerodrome"] = selectedAerodrome
        return render_template("/gestion.html", dataAerodrome=dicDataAerodrome, info = msg)

@app.route("/modifAerodrome", methods=['POST'])
def modifAerodrome():
    # Récypère les éléments modifiés de l'aérodrome
    dicDataAerodrome={}
    for elt in ['nom_ad', 'longitude', 'latitude', 'oaci']:
        dicDataAerodrome[elt] = request.form["{}".format(elt)]
    selectedAerodrome = session["selectedAerodrome"]
    # Effectue la modification dans la bdd
    msg = b.modifAerodrome(dicDataAerodrome, selectedAerodrome)
    # Charge les nouvelles données de l'aérodrome
    selectedAerodrome = dicDataAerodrome['oaci']
    dicDataAerodrome = {}
    if selectedAerodrome is not None:
        dicDataAerodrome = b.getDataAerodrome(selectedAerodrome)

    session['selectedAerodrome'] = selectedAerodrome
    return render_template("gestion.html",dataAerodrome=dicDataAerodrome, info=msg)

@app.route("/modifAvion", methods=['POST'])
def modifAvion():
    # Récupération des données du formulaire
    dicDataAvion={}
    for elt in ['reference', 'rayonAction', 'consoHoraire', 'vitesseCroisiere']:
        dicDataAvion[elt] = request.form["{}".format(elt)]
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
    idAvion = session['selectedAvion']
    # Supprime de la bdd l'aérodrome de code OACI
    msg = b.deleteAvion(idAvion)
    session['selectedAvion'] = None
    session['avion'] = b.getNomAvion()
    return render_template("gestion.html", info=msg)

@app.route("/supprimerAerodrome", methods=['POST'])
def supprimerAerodrome():
    oaci = session['selectedAerodrome']
    # Supprime de la bdd l'aérodrome de code OACI
    msg = b.deleteAerodrome(oaci)
    session['selectedAerodrome'] = None
    return render_template("gestion.html", info=msg)

@app.route("/cv", methods=['GET'])
def cv():
    return render_template("cv.html", photo="cv_jacques.png")

@app.route("/addcomment", methods=['POST', 'GET'])
def addcomment():
    if f.verifLog():
        idUtilisateur = session["idUtilisateur"]
        msg = request.form['comment']
        b.add_comment(idUtilisateur,msg)
        data = b.get_comments()
        return render_template("comments.html", data=data)

    else:
        return redirect(url_for('/login'))

@app.route("/modifMotDePasse", methods=['POST'])
def modifMotDePasse():
    password = request.form['password']
    mdp1 = request.form['mdp1']
    mdp2 = request.form['mdp2']

    info = f.verifMdp(session['email'], password, mdp1, mdp2)

    return render_template("profile.html", info=info)
