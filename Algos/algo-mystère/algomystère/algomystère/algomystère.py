#Algo Mystère
def algoMyst(T,k):

    #Variables
    L=1
    r=len(T)
    i=int(round((L+r)/2))

    #Début
    while((k!=T[i]) and (L<=r)):
        print("-----------")
        print("Tant que:")
        print("i:",i)
        print("r",r)
        print("L:",L)
        if(k < T[i]):
            r=i-1
            print("if k< t[i]")
            print("i:",i)
            print("r",r)
            print("L:",L)

        else:
            L=i+1
            print("else]")
            print("i:",i)
            print("r",r)
            print("L:",L)
        
        print("apres controle condition")
        i=int(round((L+r)/2))
        print("i",i)
    #FTQ
    print("FTQ")
    if (k==T[i]):
        return i
    else:
        return -1

#Début du programme principal
lst=[22,53,78,100,143,177,202]
k=177

result=algoMyst(lst,k)

if result==-1:
    print("Le nombre recherché n'a pas été trouvé dans le tableau.")

else:
    print("Le nombre ", k," correspond à la l'indice n°",result," du tableau.")
