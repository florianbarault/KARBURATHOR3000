import mysql.connector
from mysql.connector import errorcode
from math import *

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

def getDataAvion(idAvion):
    condition = "idAVion = {}".format(idAvion)
    res = getAllFrom('avion', condition)
    dicDataAvion = {}
    for dic in res:
        if idAvion == dic['idAvion']:
            dicDataAvion["nom"] = dic['reference']
            dicDataAvion["masseVide"] = dic['masseVide']
            dicDataAvion["rayonAction"] = dic['rayonAction']
            dicDataAvion["finesse"] = dic['finesse']
            dicDataAvion["consoHoraire"] = dic['consoHoraire']
            dicDataAvion["puissanceMoteur"] = dic['puissanceMoteur']
            dicDataAvion["vitesseCroisière"] = dic['vitesseCroisière']
            dicDataAvion["allongement"] = dic['allongement']
            dicDataAvion["surfaceReference"] = dic['surfaceReference']
    return dicDataAvion

def getNomAerodrome():
    res = getAllFrom('aerodrome')
    dicNomAerodrome = {}
    for dic in res:
        OACI = dic['OACI']
        dicNomAerodrome[OACI] = dic['nom_ad']
    return dicNomAerodrome

def getDataAerodrome(OACI):
    condition = "OACI = '{}'".format(OACI)
    res = getAllFrom('aerodrome',condition)
    dicDataAerodrome = {}
    for dic in res:
        if OACI == dic['OACI']:
            dicDataAerodrome['OACI'] = dic['OACI']
            dicDataAerodrome["nom_ad"] = dic['nom_ad']
            dicDataAerodrome["latitude"] = dic['latitude']
            dicDataAerodrome["longitude"] = dic['longitude']
    return dicDataAerodrome

def getaerodrome():
    request = "SELECT * FROM aerodrome"
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request)
    res = cursor.fetchall()
    closeConnexion(cnx)
    print(res)
    return res

def get_idVol(login):
    request = "SELECT max(idVol) FROM vol WHERE idUtilisateur =%s  "
    param = (login,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request,param)
    res = cursor.fetchall()
    closeConnexion(cnx)

    return res





def get_dist(idVol):
    request = "SELECT idEtape, dep.latitude AS latitude_depart, dep.longitude AS longitude_depart, arr.latitude AS latitude_arrivee, arr.longitude AS longitude_arrivee, deg.latitude AS latitude_degagement, deg.longitude AS longitude_degagement FROM etapes JOIN vol on vol.idVol = etapes.idVol JOIN aerodrome AS dep ON etapes.OACIdep = dep.OACI JOIN aerodrome AS arr ON etapes.OACIarr = arr.OACI JOIN aerodrome AS deg ON etapes.OACIdeg = deg.OACI WHERE vol.idVol = %s"

    param =(idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request,param)
    res = cursor.fetchall()
    closeConnexion(cnx)

    #Traitement des données
    coordonnees= []
    coordonnees_generales=[]
    for i in range (0,len (res)):
        coordonnees.append((res[i][1],res[i][2]))
        coordonnees_generales.append((res[i][1],res[i][2]))
        coordonnees_generales.append((res[i][5],res[i][6]))
    coordonnees.append((res[-1][3],res[-1][4]))
    coordonnees_generales.append((res[-1][3],res[-1][4]))

    D=[]
    cap = []
    for j in range (len(coordonnees)-1):
        A = coordonnees[j]
        B= coordonnees[j+1]
        latA , longA = A[0], A[1]
        latB, longB = B[0], B[1]

        latA_rad = latA * pi / 180
        longA_rad = longA * pi / 180
        latB_rad = latB * pi / 180
        longB_rad = longB * pi / 180

        dlong = longB_rad - longA_rad
        dlat = latB_rad - latA_rad
        S_ab = acos(sin(latA_rad) * sin(latB_rad) + cos(latA_rad) * cos(latB_rad) * cos(dlong))
        d = S_ab * 6378137

        d = round(d)

        theta = atan(dlat / dlong)
        theta_deg = round(theta * 180 / pi)

        if longB < longA:
            cap.append(270 - theta_deg)
        else:
            cap.append(90 - theta_deg)


        D.append(d)
    return D, cap, coordonnees, coordonnees_generales

def addAvion(nom, masse, rayon, finesse, conso, puissance, vitesse, allongement, surface):
    request = "INSERT INTO avion (reference, masseVide, rayonAction, finesse, consoHoraire, puissanceMoteur, vitesseCroisière, allongement, surfaceReference) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);"
    param = (nom, masse, rayon, finesse, conso, puissance, vitesse,allongement, surface,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
    except mysql.connector.Error as e:
        print("Failed add avion : {}".format(e))
    closeConnexion(cnx)


def ajout_vol(new_flight):
    request =" INSERT INTO vol (idAvion, date, idUtilisateur, vitesseVent, directionVent) values (%s, %s,%s, %s, %s) "
    param = (new_flight[0],new_flight[1],new_flight[2],new_flight[3],new_flight[4],)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    cnx.commit()
    closeConnexion(cnx)

def ajout_etapes(vol,etapes):
    liste_etapes = etapes.split(",")

    request = " INSERT INTO etapes (idVol, OACIdep, OACIarr, OACIdeg, rang) values (%s, %s, %s, %s, %s) "
    param = (vol, liste_etapes[0], liste_etapes[1], liste_etapes[2], 1,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    cnx.commit()
    closeConnexion(cnx)
    test = [i for i in range(1,len(liste_etapes)-2,2)]
    print(liste_etapes)
    print(test)
    for i in range(1,len(liste_etapes)-2,2):
        print(i)
        request =" INSERT INTO etapes (idVol, OACIdep, OACIarr, OACIdeg, rang) values (%s, %s, %s, %s, %s) "
        param = (vol, liste_etapes[i], liste_etapes[i+2],liste_etapes[i+3], (i+1)/2,)
        cnx = createConnexion()
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
        closeConnexion(cnx)

def calc_carbu(coord,idVol):
    request = "SELECT vitesseVent, directionVent, masseVide, rayonAction finesse, consoHoraire, puissanceMoteur, VitesseCroisière, allongement, surfaceReference FROM vol JOIN avion ON avion.idAvion = vol.idAvion WHERE vol.idVol = %s"
    param = (idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    res = cursor.fetchall()
    closeConnexion(cnx)
    print(res)

def get_etapes(idVol):
    request = "SELECT dep.nom_ad AS Depart, arr.nom_ad AS Arrivee, deg.nom_ad AS Degagement FROM etapes JOIN aerodrome AS dep ON etapes.OACIdep = dep.OACI JOIN aerodrome AS arr ON etapes.OACIarr = arr.OACI JOIN aerodrome AS deg ON etapes.OACIdeg = deg.OACI WHERE idVol = %s"
    param = (idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    res = cursor.fetchall()
    closeConnexion(cnx)
    return res