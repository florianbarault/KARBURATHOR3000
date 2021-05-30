from typing import Dict
import mysql.connector
from mysql.connector import errorcode
from math import *
from datetime import datetime

from mysql.connector import cursor

config = {
        'user': 'ienac',
        'password': 'ienac',
        'host': 'localhost',
        'port': 3306,
        'database': 'IENAC20_KARBURATHOR3000',
        'raise_on_warnings': True
    }

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

def getIdUser(email):
    request = "SELECT idUtilisateur FROM utilisateurs WHERE email = %s"
    param = (email, )
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        res = cursor.fetchall()
    except mysql.connector.Error as e:
        res = None
        print("Failed get idUtilisateur : {}".format(e))
        closeConnexion(cnx)
    return res

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

def countAllFrom(table:str, condition=""):
    request = "SELECT COUNT(*) FROM {} ".format(table) + condition
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request)
        res = cursor.fetchone()
    except mysql.connector.Error as e:
        res = None
    closeConnexion(cnx)
    return str(res['COUNT(*)'])

def countDistinctFrom(table, colonne, condition):
    request = "SELECT COUNT(DISTINCT {}) FROM {} ".format(colonne, table) + condition
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request)
        res = cursor.fetchone()
    except mysql.connector.Error as e:
        res = None
    closeConnexion(cnx)
    return str(res['COUNT(DISTINCT {})'.format(colonne)])

def sumFrom(table,attribut, condition=""):
    request = "SELECT SUM({}) FROM {} ".format(attribut, table) + condition
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request)
        res = cursor.fetchone()
    except mysql.connector.Error as e:
        res = None
    closeConnexion(cnx)
    if str(res['SUM({})'.format(attribut)]) == "None":
        return 0
    else:
        return str(res['SUM({})'.format(attribut)])

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
    closeConnexion(cnx)

    #Traitement des données

    try :
        liste_vol = []
        idVolOld = 0
        i = 0 #indice d'étape
        j = res[0]["idVol"] - 1 #pour calculer le décalage nécessaire de sorte que tous les id de vol d'un utilisateur commencent à 1
        k=0
        while i < len(res):
            idVol = res[i]["idVol"] - j
            if idVol != idVolOld:
                liste_vol.append([])

                type_avion = res[i]["reference"]
                liste_vol[k].append(type_avion)

                date = res[i]["date"]
                liste_vol[k].append(date)

                OACIdep = res[i]["OACIdep"]
                liste_vol[k].append(OACIdep)

                if idVolOld != 0:
                    OACIarr = res[i-1]["OACIarr"]
                    liste_vol[k - 1].append(OACIarr)

                k+=1
                idVolOld = idVol
            i+=1

        OACIarr = res[i - 1]['OACIarr']
        liste_vol[k-1].append(OACIarr)

        #Ajout des distances & conso totales par vol:

        data = info_vols(login)
        for i in range (len(liste_vol)):
            liste_vol[i].append(round(data[i][1]))
            liste_vol[i].append(data[i][0])
        return liste_vol
    except IndexError:
        return



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
            dicDataAvion["rayonAction"] = dic['rayonAction']
            dicDataAvion["consoHoraire"] = dic['consoHoraire']
            dicDataAvion["vitesseCroisiere"] = dic['vitesseCroisiere']
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


def update_info(idVol):
    request = "SELECT idEtape, dep.latitude AS latitude_depart, dep.longitude AS longitude_depart, arr.latitude AS latitude_arrivee, arr.longitude AS longitude_arrivee, deg.latitude AS latitude_degagement, deg.longitude AS longitude_degagement FROM etapes JOIN vol on vol.idVol = etapes.idVol JOIN aerodrome AS dep ON etapes.OACIdep = dep.OACI JOIN aerodrome AS arr ON etapes.OACIarr = arr.OACI JOIN aerodrome AS deg ON etapes.OACIdeg = deg.OACI WHERE vol.idVol = %s"

    param =(idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request,param)
    res = cursor.fetchall()
    closeConnexion(cnx)

    #Traitement des données
    id_etapes = []
    for i in range(len(res)):
        id_etapes.append(res[i][0])

    coordonnees= []
    coordonnees_generales=[]
    for i in range (0,len (res)):
        coordonnees.append((res[i][1],res[i][2]))
        coordonnees_generales.append((res[i][1],res[i][2]))
        coordonnees_generales.append((res[i][5],res[i][6]))
    coordonnees.append((res[-1][3],res[-1][4]))
    coordonnees_generales.append((res[-1][3],res[-1][4]))

    coordonnees_deg = []
    for x in coordonnees_generales:
        if x not in coordonnees:
            coordonnees_deg.append(x)

    def calc_dist(A, B):
        latA, longA = A[0], A[1]
        latB, longB = B[0], B[1]
        latA_rad = latA * pi / 180
        longA_rad = longA * pi / 180
        latB_rad = latB * pi / 180
        longB_rad = longB * pi / 180

        dlong = longB_rad - longA_rad
        dlat = latB_rad - latA_rad
        S_ab = acos(sin(latA_rad) * sin(latB_rad) + cos(latA_rad) * cos(latB_rad) * cos(dlong))
        D = round(S_ab * 6378137)/1000

        theta = atan(dlat / dlong)
        theta_deg = theta * 180 / pi

        if longB < longA:
            return (270 - theta_deg, D)
        else:
            return (90 - theta_deg, D)

    def calcul_carbu(D, conso_h, Vcroisiere, cap_avion, dir_vent, v_vent):
            # on met D en km

            cap_avion_rad, direction_vent_rad = cap_avion * pi / 180, dir_vent * pi / 180
            vitesse_vraie = Vcroisiere - (v_vent * cos(cap_avion_rad - direction_vent_rad))  # en km/h

            carbu_supp = 9  # carburant qui concerne le roulage et l'intégration à l'aérodrome

            Tv = D / vitesse_vraie  # temps de vol en h

            Vcarb = Tv * conso_h + carbu_supp

            return Vcarb

    dist=[]
    cap = []
    compteur = 0
    for j in range (len(coordonnees)-1):
        A = coordonnees[j]
        B= coordonnees[j+1]
        C = coordonnees_deg[compteur]
        c1, d1  = calc_dist(A,B)
        c2, d2 = calc_dist(A,C)
        if d2 < d1:
            dist.append(d1)
            cap.append(c1)
        else:
            dist.append(d2)
            cap.append(c2)
        compteur +=1

    request = "SELECT vitesseVent, directionVent, rayonAction, consoHoraire, VitesseCroisiere FROM vol JOIN avion ON avion.idAvion = vol.idAvion WHERE vol.idVol = %s"
    param = (idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    res = cursor.fetchall()
    closeConnexion(cnx)
    carb = []

    for i in range(len(dist)):
        x = calcul_carbu(dist[i], res[0][3], res[0][4], cap[i], res[0][1], res[0][0])
        carb.append(round(x))


    for i in range (len(id_etapes)):
        request = "UPDATE etapes SET distance = %s, carburant = %s WHERE idVol = %s AND idEtape = %s"
        param = (dist[i], carb[i] ,idVol,id_etapes[i],)
        cnx = createConnexion()

        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()

    return dist, carb, coordonnees_generales

def addAvion(d:dict):
    request = "INSERT INTO avion (reference, rayonAction, consoHoraire, vitesseCroisiere) VALUES (%s, %s, %s, %s);"
    param = tuple(d.values(),)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
    except mysql.connector.Error as e:
        print("Failed add avion : {}".format(e))
    closeConnexion(cnx)

def modifAvion(dataAvion, selectedAvion):
    request = "UPDATE avion SET {} = %s WHERE idAvion = %s"
    for k, v in dataAvion.items():
        msg = ""
        if v != "":
            param = (v, selectedAvion,)
            cnx = createConnexion()
            try:
                cursor = cnx.cursor()
                cursor.execute(request.format(k), param)
                cnx.commit()
                msg = "ok"
            except mysql.connector.Error as e:
                msg="fail"
                print("Failed add {} at avion : {}".format(k, e))
            closeConnexion(cnx)
    return msg

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

    request = " INSERT INTO etapes (idVol, OACIdep, OACIarr, OACIdeg, rang, distance, carburant) values (%s, %s, %s, %s, %s,0,0) "
    param = (vol, liste_etapes[0], liste_etapes[1], liste_etapes[2], 1,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    cnx.commit()
    closeConnexion(cnx)

    for i in range(1,len(liste_etapes)-2,2):
        request =" INSERT INTO etapes (idVol, OACIdep, OACIarr, OACIdeg, rang,distance, carburant) values (%s, %s, %s, %s, %s,0,0) "
        param = (vol, liste_etapes[i], liste_etapes[i+2],liste_etapes[i+3], (i+3)/2,)
        cnx = createConnexion()
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
        closeConnexion(cnx)

def addAerodrome(d:dict):
    request = "INSERT INTO aerodrome (OACI, nom_ad, latitude, longitude) VALUES (%s, %s, %s, %s);"
    param = tuple(d.values(),)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
        msg = "ok"
    except mysql.connector.Error as e:
        msg="fail"
        print("Failed add aerodrome : {}".format(e))
    closeConnexion(cnx)
    return msg

def modifAerodrome(dataAerodrome, selectedAerodrome):
    request = "UPDATE aerodrome SET {} = %s WHERE OACI = %s"
    for k, v in dataAerodrome.items():
        msg=""
        if v != "":
            param = (v, selectedAerodrome,)
            cnx = createConnexion()
            try:
                cursor = cnx.cursor()
                print(request.format(k),param)
                cursor.execute(request.format(k), param)
                cnx.commit()
                msg = "ok"
            except mysql.connector.Error as e:
                msg="fail"
                print("Failed add {} a aerodrome : {}".format(k, e))
            closeConnexion(cnx)
    return msg

def deleteAvion(oaci):
    request = "DELETE FROM avion WHERE idAvion = %s"
    param = (oaci,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
        msg = "ok"
    except mysql.connector.Error as e:
        msg="fail"
        print("Failed delete aerodrome : {}".format(e))
    closeConnexion(cnx)
    return msg

def get_etapes(idVol):
    request = "SELECT dep.nom_ad AS Depart, arr.nom_ad AS Arrivee, deg.nom_ad AS Degagement FROM etapes JOIN aerodrome AS dep ON etapes.OACIdep = dep.OACI JOIN aerodrome AS arr ON etapes.OACIarr = arr.OACI JOIN aerodrome AS deg ON etapes.OACIdeg = deg.OACI WHERE idVol = %s"
    param = (idVol,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    res = cursor.fetchall()
    closeConnexion(cnx)
    return res

def conso_dist_etapes(liste_etapes,carb,dist):
    data = []
    for i in range(len(liste_etapes)):
        data.append([liste_etapes[i][0],liste_etapes[i][1],liste_etapes[i][2],carb[i],round(dist[i])])
    conso_totale = sum(carb)
    dist_totale = round(sum(dist))
    return data, conso_totale, dist_totale

def info_vols(idUtilisateur):
    request = "SELECT sum(carburant), sum(distance) FROM etapes JOIN vol ON vol.idvol = etapes.idVol WHERE vol.idUtilisateur = %s GROUP BY etapes.idVol"
    param = (idUtilisateur,)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request,param)
    res = cursor.fetchall()
    closeConnexion(cnx)
    return res

def add_comment(idUtilisateur,msg):
    f = datetime.now().date()
    request ="INSERT INTO messages (date, idUtilisateur, contenu) values (%s, %s, %s)"
    param=(str(f),idUtilisateur,msg)
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request, param)
    cnx.commit()
    closeConnexion(cnx)

def get_comments():
    request ="SELECT nom,prenom,date,contenu FROM messages JOIN utilisateurs ON messages.idUtilisateur = utilisateurs.idUtilisateur"
    cnx = createConnexion()
    cursor = cnx.cursor()
    cursor.execute(request)
    res = cursor.fetchall()
    closeConnexion(cnx)
    return res

def verifMdp(email, mdp):
    request = "SELECT mdp FROM utilisateurs WHERE email=%s LIMIT 1"
    param = (email,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute(request, param)
        res = cursor.fetchone()
        password = res['mdp']
        if mdp == password:
            msg = "okMdp"
        else:
            msg='error'
    except mysql.connector.Error as e:
        res = None
        msg = "Failed authentification : {}".format(e)
    closeConnexion(cnx)
    return msg

def modifMdp(email, mdp):
    request = "UPDATE utilisateurs SET mdp = %s WHERE email = %s"
    print(email, mdp)
    param = (mdp, email,)
    cnx = createConnexion()
    try:
        cursor = cnx.cursor()
        cursor.execute(request, param)
        cnx.commit()
        msg = "ok"
    except mysql.connector.Error as e:
        msg="fail"
        print("Failed : {}".format(e))
    closeConnexion(cnx)
    return msg


    