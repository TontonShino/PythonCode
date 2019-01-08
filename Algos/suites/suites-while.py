#Réponse 4
#Remplacer la boucle for par tant que

# Variables
n=0
i=1
u=1

#Début
print("Entrez la valeur de n:")
n=int(input())#Lire le rang n

#Tant que i est différent du rang recherché
while i!=n:
    u= 3*u-1
    i=i+1
print("Le terme de rang",i," vaut:",u)

    
