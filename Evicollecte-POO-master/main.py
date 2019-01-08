import modules.pi as pi#on importe le module/la classe PI
import modules.mail as mail
import modules.dao as dao
#import modules.confloader as confloader
import modules.parser as confParser
import time
import modules.timer as timer
import os
#ok test
#Vérification d'une config existante
 #Si config exitante
    #Attribuer a des variables local

 #Sinon faire un premier enregistrement
    #Puis créer fichier local de config
    #Puis enregistrer 

#Fin de vérification existante
path='config/conf.ini' # Fichier de config
#path='../config/conf.ini'
ldata = confParser.ConfParm()

conf=ldata.verifConf(path)
#conf.read(path)
print("Existance d'un fichier de conf:",conf)
if conf==True:
    print("Le fichier existe récupération des donnée")
    print("ID de la raspberry=",ldata.idpi)
    print("Nom client:",ldata.nomClient)
    print("Adresse client:",ldata.adresse)
    print("ID client:",ldata.rowid)
    print("N° CLI client",ldata.cli)
    
    idPi=int(ldata.idpi)
    adresse=str(ldata.adresse)
    nomClient=str(ldata.nomClient)
    rowid=int(ldata.rowid)
    cli=str(ldata.cli)
    adresse=str(ldata.adresse)
    
    
    collect=pi.PI(cli,nomClient,idPi,adresse,rowid)
    data = dao.DAO()
    data.getInfos(cli)

else:
    print("Creation d'un fichier de config")
    
    cli=str(input("Entrez le cli du client: "))
    
    try:
        data = dao.DAO()
        data.getInfos(cli)
        rowid = data.rowid
        nomClient = data.nomClient
        adresse=data.adresse
        print("Infos récupéré: ",rowid,adresse,nomClient)
        idPi=int(data.getNextPi())
        ldata.createConf(path,data)
        #(self,p_clientERP,p_nomClient,p_idPi):
        collect = pi.PI(cli,nomClient,idPi,adresse,rowid)
        data.firstRecord(collect)
        
        
        
    except:
        print("Erreur sur le CLI")
        




#Test du client existant ou non
try:
    pins = data.getPins(idPi)
    print("Test pins:"+str(pins[0]))
    collect.setPins(pins)
        
    while True:
        

        
        collect.checkData()
        collect.rapport()
        data.RecordData(collect)
        timer.chrono()
except:
    print("Sortie du programme")
    del ldata
    
    
    
