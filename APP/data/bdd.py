import mysql.connector
from mysql.connector import errorcode

config = {
        'user': 'ienac',
        'password': 'ienac',
        'host': 'localhost',
        'port': 3306,
        'database': 'bddCarburantGroupeC',
        'raise_on_warnings': True
    }

#################################################################################################################
# connexion au serveur de la base de données


def createConnexion():
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Mauvais login ou mot de passe")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("La Base de données n'existe pas.")
        else:
            print(err)
    return cnx


def closeConnexion(cnx):
    cnx.close()


def addUser(prenom, nom, email, mdp, certif):
    request = "INSERT INTO utilisateurs (prenom, nom, email, mdp, certification, statut) VALUES (%s, %s, %s, %s, %s, 'user');"
    param = (prenom, nom, email, mdp, certif,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
    except mysql.connector.Error as e:
        print("Failed add user : {}".format(e))
    closeConnexion(cnx)


def verifUserEmail(email):
    request = "SELECT * FROM utilisateurs WHERE email = %s LIMIT 1"
    param = (email,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        res = cursor.fetchone()
        return "userNoExist" if res is None else "userExist"
    except mysql.connector.Error as e:
        print("Failed verif email : {}".format(e))
    closeConnexion(cnx)


def verifAuthData(login, mdp):
    request = "SELECT * FROM utilisateurs WHERE email=%s and mdp=%s LIMIT 1"
    param = (login, mdp,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request, param)
        res = cursor.fetchone()
        msg = "okAuth"
    except mysql.connector.Error as e:
        res = None
        msg = "Failed authentification : {}".format(e)
    closeConnexion(cnx)
    return res, msg


def getCertification(certif):
    if certif == "1":
        return "LAPL"
    if certif == "2":
        return "PPL"
    if certif == "3":
        return "CPL"
    if certif == "4":
        return "ATPL"
    else:
        return None

def getNumberUser():
    request = "SELECT COUNT(*) FROM utilisateurs WHERE statut='user'"
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request)
        res = cursor.fetchone()
        print(res)
    except mysql.connector.Error as e:
        res = None
    closeConnexion(cnx)
    return str(res['COUNT(*)'])