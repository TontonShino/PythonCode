def lettre(l):
    return ord(l)-65

def num(nombre):
    return chr(nombre)+65

def cesar(message):
    chiffre=" "
    for c in message:
        x=(num(c)+3)%26
        chiffre=chiffre+lettre(x)
    return (chiffre)


def chiffrement(message):
    chiffre=" "
    for c in message:
        x=(ord(c)+3)%26
        chiffre=chiffre+chr(x)
    return(chiffre)



while(1==1):
    print("Entrez une valeur entre guillemets:")
    entree=input()
    print("chiffrement = ",chiffrement(entree))