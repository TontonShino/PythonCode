#Réponse 5-6
#Transformer le programme-Fonction
#Signature de la fonction
#Exo_Sio(rang:entier):entier

def Exo_Sio(rang):
    # Variables
    u=0
    n=rang
    i=0
    #Début
    
    while i!=n:
        u= 3*u-1
        i=i+1
    print("Le terme de rang",i," vaut:",u)
        
print("Entrez la valeur de n:")
#Lire le rang n
n=int(input())
Exo_Sio(n)
