#Class pi
import pigpio #Gere le GPIO
import time#Gere le temps


class PI:

    #Constructeur prenant n°ERP, nom du client et l'id de la PI
    def __init__(self,p_clientERP,p_nomClient,p_idPi,p_adresse,p_rowid):

        #Définition des noms/Numero ERP
        self.cli=str(p_clientERP)
        self.nomClient=str(p_nomClient)
        self.idPi=int(p_idPi)
        self.adresse=str(p_adresse)
        self.rowid=int(p_rowid)
        
        #Valeurs des pins [entier] 1-0 / True-False
        self.guard=False
        self.alarm=False
        self.hy3=False
        self.erreur=False
        self.flexGuard=False#pin à définir pour prendre le
        self.statut=""

        #Numerotation des pins
        self.p_guard=26
        self.p_alarm=19
        self.p_hy3=4
        self.p_erreur=13
        self.p_flexGuard=17

        #Utilisation du module GPIO de la PI
        self.gpio=pigpio.pi()
        
        self.time=False

        #Configuration des modes des pins 
        self.gpio.set_mode(self.p_erreur, pigpio.INPUT)
        self.gpio.set_mode(self.p_alarm, pigpio.INPUT)
        self.gpio.set_mode(self.p_guard, pigpio.INPUT)
        self.gpio.set_mode(self.p_hy3, pigpio.INPUT)
        self.gpio.set_mode(self.p_flexGuard,pigpio.INPUT)
        
     
    #Méthode de debug affichant les différentes valeurs    
    def rapport(self):
        print("Rapport:")
        print("Client ERP:",self.cli)
        print("Nom client:",self.nomClient)
        print("Mode guard:",self.guard)
        print("Alarme:", self.alarm)
        print("Mode Erreur", self.erreur)
        print("Cartouche inferieur a 30 %:",self.hy3)
        print("Heure/Date:",time.time())
        print("--------------------")
    #Remise à zero des pins 
    def resetData(self):
        print("Remise à zero des pins")
        self.guard=False
        self.alarm=False
        self.hy3=False
        self.erreur=False
        self.flexGuard=False
        self.statut=""
    
    #Méthode qui prend la valeur des pins    
    def checkData(self):
        self.resetData()
        print("Contrôle des pins")#Message de debug et controle
        self.guard = self.gpio.read(self.p_guard)
        self.alarm = self.gpio.read(self.p_alarm)
        self.hy3 = self.gpio.read(self.p_hy3)
        self.erreur = self.gpio.read(self.p_erreur)
        self.flexGuard = self.gpio.read(self.p_flexGuard)
        time.sleep(1)
    def setPins(self, p):
        self.p_guard=int(p[0])
        self.p_alarm=int(p[1])
        self.p_hy3=int(p[2])
        self.p_erreur=int(p[3])
        self.p_flexGuard=int(p[4])
        print("Pin réatribué")
        print("Pin Guard:"+str(self.p_guard)+", Pin Alarm:"+str(self.p_alarm)+", Pin Hy3:"+str(self.p_hy3)+", Pin erreur:"+str(self.p_erreur)+", Pin Flex:"+str(self.p_flexGuard))
        
    

        




