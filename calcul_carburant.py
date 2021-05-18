from math import *
#Raymer
M4_M3=0.995
M2_M1=0.985
M1_M0=0.970
g=9.81
def conso_carbu(M0,M4_M0):
    return 1.06*M0*(1-M4_M0) #masses en kg

def calcul_M3_M2(distance,conso_specifique,vitesse_croisiere,finesse):
    return exp(-1*((distance*g*conso_specifique)/(vitesse_croisiere*finesse)))#distance en mètres, conso spé en kg/s/N, vitesse en m/s
    
def calcul_conso_spe(conso_horaire,puissance,rendement_helice):
    return conso_horaire/(puissance*rendement_helice) #puissance en Watt,conso en kg/s
def calcul_M4_M0(distance,conso_specifique,vitesse_croisiere,finesse):
    return M4_M3*calcul_M3_M2(distance,conso_specifique,vitesse_croisiere,finesse)*M2_M1*M1_M0

def calcul_Mcarb_M0(M4_M0):
    return 1.06*(1-M4_M0)

def Mvide_M0(M0):
    return 0.32 + 0.6446*M0**-0.13*(Allongement)**0.3*rapport_Pmg**0.06*M_al**-0.05*(mach_max)**0.05
def calcul_M0(Mvide,M_marchande,M_equipage,Mcar_M0):
    M0_i= 1000
                
    Mv_M0= Mvide_M0(M0_i)
    M0_v= int((M_marchande+M_equipage)/(1-Mcar_M0-Mv_M0))# masses à renseigner 
    while M0_i != M0_v:
            M0_i+=1
            Mv_M0= Mvide_M0(M0_i)
            M0_v= int((M_marchande+M_equipage)/(1-Mcar_M0-Mv_M0))
        
    return M0_i    


print('M4_M0_DR400=',calcul_M4_M0(10000,0.0048,59.72,10))
print('mc/m0_dr400=',calcul_Mcarb_M0(0.45))
print('Modr400=',calcul_M0(580,0,200,0.583))

