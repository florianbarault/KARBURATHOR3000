from math import *
#Raymer
M4_M3=0.995
M2_M1=0.985
M1_M0=0.970
g=9.81
rapport_Pmg=0.3 #Estimation
def calcul_masse_carburant(v_avion,v_vent,d_vent,distance,finesse,allongement,surface_ref,conso_horaire,rendement_helice,puissance,M_fret,nb_passagers,M_vide):
    vitesse_vraie=v_avion-(v_vent*cos(d_vent))#vitesse en km/h,direction en degrés
    machmax=(vitesse_vraie/3.6)/340 #nous négligeons la variation de la vitesse du son avec l'altitude
    conso_spe=conso_horaire/(puissance*rendement_helice) #puissance en Watt,conso en kg/s
    M3_M2=exp(-1*((distance*g*conso_spe)/(vitesse_vraie*finesse)))#distance en mètres, conso spé en kg/s/N, vitesse en m/s   
    M4_M0=M4_M3*M3_M2*M2_M1*M1_M0 #masses en kg
    Mcarb_M0=1.06*(1-M4_M0)
    M_pass=nb_passagers*100 #masses de l'équipage et des passagers
    def Mvide_M0(M0,allongement,surface_ref,machmax): #surface en m²
            return 0.32 + 0.6446*M0**-0.13*(allongement)**0.3*rapport_Pmg**0.06*(M0/surface_ref)**-0.05*machmax**0.05
    def calcul_M0(M_marchande,M_equipage,Mcar_M0,allongement,surface_ref,machmax):
            M0_i= 1000


            Mv_M0 = Mvide_M0(M0_i,allongement,surface_ref,machmax)
            M0_v= int((M_marchande+M_equipage)/(1-Mcar_M0-Mv_M0))# masses à renseigner 
            while M0_i != M0_v:
                    M0_i+=1
                    Mv_M0= Mvide_M0(M0_i,allongement,surface_ref,machmax)
                    M0_v= int((M_fret+M_equipage)/(1-Mcar_M0-Mv_M0))
                
            return M0_i 


    return 1.06*calcul_M0(M_fret,M_pass,Mcarb_M0,allongement,surface_ref,machmax)*(1-M4_M0)

print ("masse_carb_dr400=",calcul_masse_carburant(215,10,0,10000,10,5.35,14.2,38,0.8,160,0,2,580))