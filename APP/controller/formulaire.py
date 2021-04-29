from flask import session
from APP.data import bdd as b


def verifAuth(login, password):
    res, msg = b.verifAuthData(login, password)
    if res is not None:
        session["idUtilisateur"] = res["idUtilisateur"]
        session["nom"] = res["nom"]
        session["prenom"] = res["prenom"]
        session["certification"] = res["certification"]
        session["statut"] = res["statut"]
    else:
        msg = "erreur"
    return msg