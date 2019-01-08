import configparser as cfp

#Lecture fichier de config
#config = cfp.ConfigParser()

#path='../config/parseFile.cfg'
"""
toCreate = '../config/conf.ini'

config.sections()

config.read(path)
config.sections()

print(config['Default']['num'])

#Fin de lecture

#Ecriture
confW = cfp.ConfigParser()
confW['Default'] = {'nom client':'boubakar','age':'26','ville':'Châtillon'}
with open(toCreate,'w') as configfile:
    confW.write(configfile)
#Fin ecriture

def VerifConf(path):
    try:
        with open(path, 'r') as confile:
            conf = cfp.ConfigParser()
            conf.read(confile)
            
            #print(conf['Infos','cli'])
        return True
            
    except:
        print("Fichier non présent")
        return False



def CreateConf(path):
    conf = cfp.ConfigParser()
    conf['Infos'] = {'idpi':'','adresse':'','cli':'','nomclient':'','ref_client':'','ref_rowid':''}
    conf['Pins'] = {'guard':'','alarm':'','hy3':'','erreur':'','fxguard':''}
    
    with open(path,'w') as configfile:
        conf.write(configfile)
    print("Fin de la création de fichier de config")
        
def testModif():
    conf = cfp.ConfigParser()
    conf.read(toCreate)
    conf.set('Infos','ref_client','client turfu')
    
    with open(path,'w') as configfile:
        conf.write(configfile)
  """      
class ConfParm:
    def __init__(self):
        self.idpi=0
        self.adresse=""
        self.cli=""
        self.nomClient=""
        self.ref_client=0
        self.guard=0
        self.alarm=0
        self.hy3=0
        self.erreur=0
        self.fxguard=0
        self.path=''
        self.parsed=0
        self.fnParser = cfp.ConfigParser()
        print("Classe configuration crée")
    
    def loadConf(self):
        print("Chargement de la configuration")
        
    
    def createConf(self,dir,dao):
        print("Création d'un fichier de config")
        
        
        conf = self.fnParser
        conf['Infos'] = {'idpi':dao.idpi,'adresse':dao.adresse,'cli':dao.cli,'nomclient':dao.nomClient,'ref_client':dao.cli,'ref_rowid':dao.rowid}
        conf['Pins'] = {'guard':'','alarm':'','hy3':'','erreur':'','fxguard':''}
    
        with open(dir,'w') as configfile:
            conf.write(configfile)
        
        del conf
        print("Fin de la création de fichier de config")
    
    def readConf(self,path):
        print("Lecture de la configuration")
        
    
    def verifConf(self,path):
        print("Vérification d'une conf existante")
        try:
            """
            with open(path, 'r') as confile:
                conf = cfp.ConfigParser()
                conf.read(confile)
                print(str(conf.get('Infos','cli')))
            
                print(conf['Infos','cli'])
            """
            
            
            cfg=self.fnParser
            cfg.read(path)
            print(str(cfg.get('Infos','cli')))
            
            self.idpi = int(cfg.get('Infos','idpi'))
            self.cli = str(cfg.get('Infos','cli'))
            self.rowid = int(cfg.get('Infos','ref_rowid'))
            self.nomClient = str(cfg.get('Infos','nomClient'))
            self.adresse = str(cfg.get('Infos','adresse'))
            
            del cfg
            #adresse=ldata.adresse
            #nomClient=ldata.nomClient
            #rowid=ldata.rowid
            #cli=ldata.cli
            return True
            
        except:
            print("Fichier non présent")
            del cfg
            return False
        
    
        
        
        
        
    



    
