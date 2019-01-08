#Réponse 7
#Transformer en fonction récursive

def Exo_Sio(p_n,p_i,p_u)->int:
    # Variables
    n=p_n
    i=p_i
    u=p_u
    #Début
    
    #Si i est différent du rang
    if i!=n:
        u=3*u-1
        i=i+1
        return Exo_Sio(n,i,u)
    else:
        return u;
        
print("Entrez la valeur de n:")#Lire le rang n
n=int(input())

result=Exo_Sio(n,1,1)#Appel de la fonction qui renvoi le résultat
print("Le terme de rang ",n," vaut:",result)
