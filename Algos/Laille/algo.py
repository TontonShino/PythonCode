#algo mystere Laille
def mystere(T):
    print(T)
    Taille=len(T)
    tampon=T[Taille-1]

    for i in range(Taille-1,1):
        T[i]=T[i-1]

    T[0]=tampon
    print(T)

t=["a","b","c","d","e"]
mystere(t)
