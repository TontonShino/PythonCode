#Réponse 5-6
#Transformer le programme-Fonction

#Signature de la fonction
#Exo_Sio(rang:entier):entier

def Exo_Sio(rang)->int:
    # Variables
    n=rang
    i=1
    u=1
    
    #Début
    while i!=n:#Tant i est différent du rang
        u=3*u-1
        i=i+1
    return u;

#Début du programme principale        
print("Entrez la valeur de n:")
n=int(input())#Lire le rang n

result=Exo_Sio(n)#Appel de la fonction qui renvoi le résultat
print("Le terme de rang ",n," vaut:",result)
