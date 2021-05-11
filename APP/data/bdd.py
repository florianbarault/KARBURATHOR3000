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

def countAllFrom(table:str, condition=None):
    if condition is None:
        request = "SELECT COUNT(*) FROM {}".format(table)
    else:
        request = "SELECT COUNT(*) FROM {} WHERE ".format(table) + condition
        print(request)
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

def get_histo(login):
    request = "SELECT OACIdep, OACIarr , etapes.idVol, rang, vol.date, avion.reference FROM etapes " \
               "INNER JOIN vol ON etapes.idVol = vol.idVol " \
               "INNER JOIN avion ON vol.idAvion = avion.idAvion " \
               "WHERE vol.idUtilisateur = %s order BY etapes.idVol ASC, etapes.rang ASC "
    param = (login,)
    cnx = createConnexion()
    cursor = cnx.cursor(dictionary=True)
    cursor.execute(request,param)
    res = cursor.fetchall()

    #Traitement des données
    liste_vol = []
    idVolOld = 0
    i = 0 #indice d'étape

    try:
        j = res[i]["idVol"] - 1 #pour calculer le décalage nécessaire de sorte que tous les id de vol d'un utilisateur commencent à 1
        while i < len(res):
            idVol = res[i]["idVol"] - j
            if idVol != idVolOld:
                liste_vol.append([])

                type_avion = res[i]["reference"]
                liste_vol[idVol-1].append(type_avion)

                date = res[i]["date"]
                liste_vol[idVol-1].append(date)

                OACIdep = res[i]["OACIdep"]
                liste_vol[idVol-1].append(OACIdep)

                if idVolOld != 0:
                    OACIarr = res[i-1]["OACIarr"]
                    liste_vol[idVol-2].append(OACIarr)

                idVolOld = idVol
            i+=1

        OACIarr = res[i - 1]['OACIarr']
        liste_vol[idVol-1].append(OACIarr)

        closeConnexion(cnx)
        return liste_vol

    except IndexError:
        return [[]]

def getAllFrom(table:str, condition =None):
    if condition is None:
        request = "SELECT * FROM {}".format(table)
    else:
        request = "SELECT * FROM {} WHERE ".format(table) + condition
        print(request)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request)
        res = cursor.fetchall()
    except mysql.connector.Error as e:
        res = None
    closeConnexion(cnx)
    return res

def getNomAvion():
    res = getAllFrom('avion')
    dicNomAvion = {}
    for dic in res:
        idAvion = dic['idAvion']
        dicNomAvion[idAvion] = dic['reference']
    return dicNomAvion

def getaerodrome():
    request = "SELECT * FROM aerodrome"
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request)
    res = cursor.fetchall()
    closeConnexion(cnx)
    return res
