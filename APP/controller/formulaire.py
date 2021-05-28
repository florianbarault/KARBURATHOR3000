from flask import session
from APP.data import bdd as b

def addToSession(elt:str, value):
    session[elt] = value

def verifAuth(login, password):
    res, msg = b.verifAuthData(login, password)
    if res is not None:
        for k, v in res.items():
            addToSession(k, v)
    else:
        msg = "erreur"
    return msg

def verifLog():
    return True if session.get('idUtilisateur') else False

def index():
    session["totalUser"] = b.countAllFrom('utilisateurs')
    session['totalFlight'] = b.countAllFrom('vol')
    session['totalDistance'] = b.sumFrom('etapes', 'distance')
    session['totalCarburant'] = b.sumFrom('etapes', 'carburant')

def logout():
    session.clear()
    index()

def signUp(d:dict):
    if d['mdp1'] != d['mdp2']:
        info="errorMdp"
    else:
        msg = b.verifUserEmail(d['email'])
        if msg == "userExist":
            info="errorSignUp"
        else:
            # Ajoute l'utilisateur à la bdd
            b.addUser(d['prenom'], d['nom'], d['email'], d['mdp1'], d['certification'])
            # Crée des données de session pour l'utilisateur
            info = None
    return info

def verifMdp(email, password, mdp1, mdp2):
    msg = b.verifMdp(email, password)
    if msg != "okMdp":
        info = "errorMdp3"
    if mdp1 != mdp2:
        # Nouveaux mot de passe différents
        info = "errorMdp1"
    elif password == mdp1:
        # Ancien et nouveau mot de passe sont similaires
        info = "errorMdp2"
    else:
        msg = b.modifMdp(session['email'], mdp1)
        info = "okMdp"
    return info

def profile():
    Where = "WHERE idUtilisateur = '{}'".format(session['idUtilisateur'])
    InnerJoin = "INNER JOIN vol ON etapes.idVol = vol.idvol "
    session["userTotalCarburant"] = b.sumFrom('etapes', 'carburant', InnerJoin + Where)
    session["userTotalPlane"] = b.countDistinctFrom('vol', 'idAvion', Where)
    session['userTotalFlight'] = b.countAllFrom('vol', Where)
    session['userTotalDistance'] = b.sumFrom('etapes', 'distance', InnerJoin + Where)



    
