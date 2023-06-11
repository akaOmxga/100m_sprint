### TIPE : limite du 100m sprint

from math import *

### variables globales :
masse = 70 # du sprinteur, en kg
masse_jambe = 15 # de sa jambe, en kg
ltendue = 1.2 # longueur de sa jambe lorsqu'elle est tendue, en m
lpliée = 0.7 # longueur de sa jambe lorsqu'elle est pliée, en m
rayon = 0.15 # rayon de sa jambe, assimilée à un cylindre, en m
fmax = 800 # force maximale de la jambe du sprinteur, en N
vmax = 12 # vitesse maximale du sprinteur, en m.s^(-1)
g = 9.81 # accélération de la pesanteur terrestre, en m.s^(-2)
coef_fatigue = 2 # coefficient de fatigue lors de la fin de la course, en N.s^(-1)
tau = 3.5 # temps caractéristique de la phase A
# longueur des phases A/B/C , en m :
A = 35
B = 40
C = 25


### fonctions auxiliaires :

def J() : ## moment d'inertie de la jambe (en kg.m^2)
    return(0.5*masse_jambe*rayon**2)

def Wo() : ## pulsation propre du mouvement de la jambe (en rad.s^(-1))
    return(sqrt(masse*ltendue*g/(2*J())))

def To() : ## periode propre du mouvement de la jambe (en s)
    return(2*pi/Wo())

def force_jambe(t,position): ## force de la jambe du sprinteur en fonction du temps (en N)
    if position < A :
        return(fmax*(1-exp(-t/tau)))
    elif position > A and position < A + B :
        return(fmax)
    else :
        return(fmax - coef_fatigue*t)

def K(t,position): ## constante du raideur de ressort qui modélise la jambe du sprinteur en fonction du temps (en N/m)
    return(force_jambe(t,position)/(ltendue-lpliée))

def W(t,position) : ## quasi-pulsation du mouvement du pas (en s^(-1))
    return (sqrt(K(t,position)/masse)*sqrt(1-lpliée/ltendue))

def x(t,position,temps_course) : ## longueur d'un pas en fonction du temps t (en m)
    pas = (vmax/W(temps_course,position))*sinh(W(temps_course,position)*t)
    return(pas)


### calcul du temps sur 100m :

def temps100m():
    position = 0 # compris entre 0 et 100, représente l'emplacement du sprinteur, en m
    temps = 0 # le temps pour arriver jusqu'à la ligne d'arrivée
    liste_position = [0] # liste contenant les positions successives
    liste_temps = [0] # liste contenant les temps (auxquels ont calcul la taille d'un pas) successifs
    i = 0 # variant de boucle
    while position < 100 : # calcul de la position du sprinteur, pas par pas
        temps = temps + To()
        liste_temps = liste_temps + [temps]
        position = position + x(To(),position,temps)
        liste_position = liste_position + [position]
        i = i + 1
# précision de calcul concernant le dernier pas
    derniere_position = liste_position[i-1]
    reste_a_courir = 100 - derniere_position
    dernier_temps = liste_temps[i-1]
    dernier_pas = x(To(),derniere_position,dernier_temps)
    temps_restant = (To()/dernier_pas)*reste_a_courir
    temps_100m = dernier_temps + temps_restant
    return (temps_100m)



