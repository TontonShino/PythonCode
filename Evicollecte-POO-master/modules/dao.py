#class BDD
import MySQLdb
import re

class DAO:

    def __init__(self): #constructeur par défaut

        #self.bddUrl=""#Url/adresse bdd
        #self.bddUser=""#User BDD
        #self.bddPswd=""#Mot de passe BDD
        #self.bddName=""#nom de la base de donnee
        self.db=MySQLdb.connect(host=self.bddUrl, user=self.bddUser, passwd=self.bddPswd, db=self.bddName)
        self.cli=0
        self.rowid=0
        self.adresse=""
        self.nomClient=""
        self.idpi=0
        
    #def __init__(self, p_url,p_user,p_password,p_name): #constructeur en surchage
       # self.url=p_url
        #self.user=p_user
        #self.password=p_password
        #self.name=p_name
    def getNextPi(self):
        print("Récupération de l'id PI")
        cur=self.db.cursor()
        
        cur.execute("SELECT Max(idpi) as id FROM pi;")
        id=cur.fetchone()
        id=int(id[0])+1
        print("Next Id Pi  =",id)
        self.idpi=id
        return id
    
    def connect(self):
        print("Connexion à la base donnée")
        
    
    def disconnect(self):
        print("Déconnexion de la base de donnée")
    
    def record(self,dbidpi,dbguard,dbalarm,dberreur,dbhy3,dbfxguard,dbstatus):
        print("Enregistrement des données dans la base donnée")
        #db=MySQLdb.connect(host=bddUrl, user=bddUser, passwd=bddPswd, db=bddName)
        self.cur=self.db.cursor()
        self.cur.execute("UPDATE pi SET guard={0},alarm={1}, hy3={2}, erreur={3},statut=('{4}'),fxguard={5}  WHERE idpi=({6})".format(dbguard,dbalarm,dbhy3,dberreur,dbstatus,dbfxguard,dbidpi))#On met à jour les données
        self.db.commit()
        
        self.cur.execute("INSERT INTO history_pi(guard,alarm,hy3,statut,erreur,fxguard,idpi)VALUES({0},{1},{2},('{3}'),{4},{5},{6}".format(dbguard,dbalarm,dbhy3,dbstatus,dberreur,dbfxguard,dbidpi))#On met à jour les données
        self.db.commit()
        
        self.cur.close()
        self.db.close()


    
    def TestRecord(self,pi):
        print("Youpi guard:",pi.guard)
    
    def getPins(self,idpi):
        print("Récupération des pins dans la bdd")
        cur=self.db.cursor()
        cur.execute("SELECT p_guard,p_alarm,p_hy3,p_erreur,p_fxguard FROM pi WHERE idpi={0}".format(idpi))
        res=cur.fetchone()
        print("Pin Guard:"+str(res[0])+", Pin Alarm:"+str(res[1])+", Pin Hy3:"+str(res[2])+", Pin erreur:"+str(res[3])+", Pin Flex:"+str(res[4]))
        return res
        
    
    def getInfos(self,cli):
        print("Récupération info client")
        cur=self.db.cursor()
        cur.execute("select rowid from llx_societe WHERE code_client=('{0}')".format(cli))
        self.rowid=cur.fetchone()
        self.rowid=int(self.rowid[0])
        print("ROW ID Client:",self.rowid)
        
        cur.execute("SELECT nom,address,town,zip,code_client FROM llx_societe WHERE code_client=('{0}')".format(cli))
        res=cur.fetchone()
        self.nomClient=str(res[0])
        self.cli=cli
        self.adresse=str(res[1])+" "+str(res[2])+" "+str(res[3])
        self.adresse=self.RemoveChar(self.adresse)
        self.nomClient=self.RemoveChar(self.nomClient)
        
        print("Nom Client:", self.nomClient)
        print("N° client:",self.cli)
        print("Adresse:",self.adresse)
        
    def RemoveChar(self,toChange):
        toDelete = "!'"
        for char in toDelete:
            toChange=toChange.replace(char," ")
        return toChange
            
    def firstRecord(self,rpi):
        try:
            print("Nouvel enregistrement - First Record")
            cur=self.db.cursor()
            #print("Firt record",int(rpi.idPi),str(rpi.nomClient),str(self.adresse),str(pi.cli),int(self.rowid))
            #id=pi.idPi
            #nomClient=str(pi.nomClient)
            #adresse = str(self.adresse)
            #cli = str(pi.cli)
            #rowid=int(self.rowid)
            #
            print("Before execute")
            cur.execute("INSERT INTO dolibarr.pi(idpi,nomClient,adresse,ref_client,ref_rowid) VALUES({0},'{1}','{2}','{3}','{4}')".format(rpi.idPi,rpi.nomClient,rpi.adresse,rpi.cli,rpi.rowid))
            print("ater execute - before commit")
            self.db.commit()
            print("after commit")

        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print("erreur:",e)
        except:
            print("Erreur d'enregistrement")
        
    def RecordData(self,rpi):
        print("enregistrement des données dans la bdd")
        
        try:
            cur = self.db.cursor()
            #"UPDATE pi SET guard = 1,alarm=0, hy3=0, erreur=0,statut='test',fxguard=0  WHERE idpi=({0})".format(idpi)
            cur.execute("UPDATE dolibarr.pi SET guard={0}, alarm={1},erreur={2},hy3={3},fxguard={4} WHERE idpi={5}".format(rpi.guard,rpi.alarm,rpi.erreur,rpi.hy3,rpi.flexGuard,rpi.idPi))
            self.db.commit()
            
            cur.execute("INSERT INTO dolibarr.history_pi(ref_pi,guard,alarm,hy3,erreur,fxguard,statut) VALUES('{0}','{1}','{2}','{3}','{4}','{5}','{6}')".format(rpi.idPi,rpi.guard,rpi.alarm,rpi.hy3,rpi.erreur,rpi.flexGuard,rpi.statut))
            self.db.commit()
            print("Fin d'enregistrement des états")
        except (MySQLdb.Error, MySQLdb.Warning) as e:
            print("erreur:",e)    
        except:
            print("Erreur record data")
        
    def verif(self, cli,idpi):
        print("Verification de l'existance du client dans la base de donnée")
        
        try:
            #db=MySQLdb.connect(host=bddUrl, user=bddUser, passwd=bddPswd, db=bddName)
            cur=db.cursor()
            cur.execute("select rowid from llx_societe WHERE code_client=('{0}')".format(cli))
            rowid=str(cur.fetchone())

            rowid=rowid.replace(",","")
            rowid=rowid.replace("(","")
            rowid=rowid.replace(")","")
            rowid=rowid.replace(")","")
            rowid=int(rowid)
            print("id row client:",rowid)
            cur.execute("SELECT nom,address,town,zip,code_client FROM llx_societe WHERE code_client=('{0}')".format(cli))
            description=str(cur.fetchone())

            description = description.replace(",","")
            description = description.replace("'","")
            description = description.replace("(","")
            description = description.replace(")","")
            print(description)

            cur.execute("INSERT IGNORE INTO pi(idpi,ref_rowid,ref_client) values({0},{1},('{2}'))".format(idpi,rowid,client))
            print("Test de correspondance client/Raspberry fait")
            db.commit()
            cur.execute("UPDATE pi SET description = ('{1}') WHERE idpi=({0})".format(idpi,description))
            db.commit()
            print("Le client a bien été ajouté dans sa totalité dans la base de donnée")

            cur.close()#Ne pas oublier de fermer le curseur
            db.close()#Ne pas oublier de fermer la connexion à la bdd
        
        except:
            print("Le client existe déjà ou un problème est rencontré")
            cur.close()#Ne pas oublier de fermer le curseur
            db.close()#Ne pas oublier de fermer la connexion à la bdd
    
    

