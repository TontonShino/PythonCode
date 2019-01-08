# Réponse 2
# Programmer algo

# Variables
n=0
i=1
u=1

#Début
print("Entrez la valeur de n:")
n=int(input())#Lire le rang n

#Pour i allant de 1 à n
for i in range(1,n):
    u= 3*u-1
print("Le terme de rang",i," vaut:",u)
