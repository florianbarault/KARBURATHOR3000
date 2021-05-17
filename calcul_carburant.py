from math import *
#Raymer
M4_M3=0.995
M2_M1=0.985
M1_M0=0.970
g=9.81
def conso_carbu(M0,M4_M0):
    return 1.06*M0*(1-_M4_M0) #masses en kg

def calcul_M4_M0(distance,conso_specifique,vitesse_croisiere,finesse):
    return exp(-1*((distance*g*conso_specifique)/(vitesse_croisiere*finesse)))#distance en mètres, conso spé en kg/s/N, vitesse en m/s
    
def calcul_conso_spe(conso_horaire,puissance,rendement_helice):
    return conso_horaire/(puissance*rendement_helice) #puissance en Watt,conso en kg/s

def calcul_Mcarb_M0(M4_M0):
    return 1.06*(1-M4_M0)

def calcul_M0(Mvide,M_marchande,M_equipage,Mcar_M0,Mv_M0):
    M0_i= 1000
        
        
    Mv_M0= Mvide_M0(M0_i)
    M0_v= int((M_marchande+M_equipage)/(1-Mcar_M0-Mv_M0))# masses à renseigner 
    while M0_i != M0_v:
            M0_i+=1
            Mv_M0= Mvide_M0(M0_i)
            M0_v= int((M_marchande+M_equipage)/(1-Mcar_M0-Mv_M0))
        
    return M0_i    
carb_DR400=conso_carbu(M0_DR400,M4_M0_DR400)
#MO_DR400=
#M4_M0_DR400=

