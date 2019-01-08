#Nom: Evicollecte
#Objectif/Fonctionnalites: Recuperer les états de la Pi connecté au Bandit pour stocker/traiter les données
#Version:OC Bois d'Arcy Home v1.8
#Fonctionne avec python > 3.5.x

#Pre-requis:

print("EviPiCollecte v1.8")
#Import des bibliotheques
import MySQLdb #Gere les Transactions sql
import pigpio #Gere le GPIO
import time # gere le temps
import smtplib # Permet d'envoyer des mails
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime #Permet de prendre l'heure systeme et autres
import csv#Ecriture dans un fichier csv ou texte
import warnings #Gere les warnings

warnings.filterwarnings('error',category=MySQLdb.Warning)

nomPi="Pividensee"
numeroPi=1
nomClient="Evidensee"
client="CLI00976"#976=Evidensee Nom du client - exemple:CLI0085
p_alarm=19#Correspond au numero de pin alarme/alarm
p_erreur=13#Correspond au numero de pin erreur/OkOut
p_guard=26#Correspond au numero de pin guard/surveillance
p_hy3=4#Correspond au numero de pin cartouche hy3 > 30%delai=18000#Correspond au temps en s 18000s--> 5 Heures

warnings.filterwarnings('error',category=MySQLdb.Warning) #Les warnings de MySQLdb deviennent des erreurs
pi= pigpio.pi()
#Definition des modes des pins GPIO Numerotation BCM 13,19,26,6
pi.set_mode(p_erreur, pigpio.INPUT) # 13 ->  Pins Numerique P23 mode erreur
pi.set_mode(p_alarm, pigpio.INPUT) # Pins Numerique P24
pi.set_mode(p_guard, pigpio.INPUT) # Pins Numerique P25 mode surveillance
pi.set_mode(p_hy3, pigpio.INPUT) # Pin numerique p22 mode hy3

hy3=False
rhy3=""
guard=False
rguard=""
erreur=False
rerreur=""
alarm=False
ralarm=""
pointage=False

#Divers Variables
cptMail=0#Compteur de mail
liInf=False#variable contenant liquide inferieur
cptHy3Inf=False#compteurHy3 inferieur
msgInf30="Le liquide hy3 est inferieur à 30%"#msg liquide inferieur
objInf30="Liquide Bandit > 30% "+client+" - "+nomClient#oHy3Inf mail subject/objet du mail liquide inferieur
msgOkScript="Le script tourne correctement"#msgOkscript script tourne correctement
objOkScript="Script OK - Raspberry Bandit "+client+" - "+nomClient#oOkScript
msgGuard="Le mode surveillance sur le bandit n'est pas actif"
objGuard="Guard non actif "+client+" - "+nomClient
msgZero="Le raspberry ne recoit aucune donnée verifiez que le bandit est bien branchée"+client+" - "+nomClient
objZero="Pas de donnée "+client+" - "+nomClient
msgStop="Une erreur est survenue le programme ne tourne plus actuellement. Veuillez rédémarrer la pi."
objStop="Programme stoppé "+client+" - "+nomClient
msgGuard="Le bandit n'est pas armé: mode guard non-actif"
objGuard="Guard non-actif "+client+" - "+nomClient
msgAlarm="Le bandit a été déclenché (alarm:on)"
objAlarm="Alerte: déclenchement "+client+" - "+nomClient
msgErreur="Une erreur est presente sur le bandit. Verifiez que le bandit est bien branchée ou faite appel à un technicien."
objErreur="Erreur Bandit"+client+" - "+nomClient
objRapport="Rapport Raspberry: "+client+" - "+nomClient

nbMailSended=0#NbEnvoiMail nombre d'envoi
nbControl=0#Compteur boucle principale
nbEnvoiGuard=0#Variable qui contiendra le nombre d'envoi pour le mode Guard non-activé
nbEnvoiAlarm=0
nbEnvoiHy3=0
nbErreur=0
nbEnvoi=0

frMail = ''#Addresse Mail Provenance
frMailpwd = ''#Mot de passe mail
toMail=""#Adresse Mail de destination
toMail2=""
srvMail=''#Serveur mail
prtMail=587#Port 587

bddUrl=""#Url/adresse bdd
bddUser=""#User BDD
bddPswd=""#Mot de passe BDD
bddName=""#nom de la base de donnee




def checkDate():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")
pointage=checkDate()#on prend la date
fileCsv="log/"+client+"_"+pointage+'.csv'
print("Creation du fichier:",fileCsv)
"""

with open(fileCsv,'w', newline='') as csvfile:
    f=csv.writer(csvfile,delimiter= ' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #Ecriture de l entete csv
    f.writerow(["Heure/Date","Mode Guard","Mode Alarme","Hy3","Mode erreur"])#Definition de fonction qui ecrira dans un fichier csv
def stockeCsv():
    with open(fileCsv,'a', newline='') as csvfile:
        f=csv.writer(csvfile,delimiter= ';', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        f.writerow([pointage,guard,alarm,hy3,erreur])
"""
#Definition d'une fonction envoiMail(string msg, string object) qui envoie le message entree en parametre
def envoiMail(pMsg,pObject):
    msg= MIMEMultipart('alternative')
    msg['Subject'] = pObject #Objet du mail
    msg['From'] = frMail#Mail de provenance
    msg['To'] = toMail2#Mail de destination
    part=MIMEText(pMsg,'plain')
    msg.attach(part)
    
    server=smtplib.SMTP(srvMail,prtMail)
    server.ehlo()
    server.starttls()
    server.login(frMail,frMailpwd)
    server.sendmail(frMail, toMail, msg.as_string())
    server.quit()
#Definition d'une fonction record() qui enregistre les elements dans la bdd
def record():
    
    print("enregistrement dans db")
    #dbg=guard , dba=alarm , dbe=erreur, dbh=hy3
    db = MySQLdb.connect(host=bddUrl, user=bddUser, passwd=bddPswd, db=bddName)
    cur=db.cursor()
    
    cur.execute("""INSERT IGNORE INTO client(id,nom) VALUES(%s,%s)""",(client,nomClient))
    db.commit()
    
    print("Enregistrement du client table OK - bdd")
    
    cur.execute("""INSERT IGNORE INTO pi(idpi,nom,ref_client) VALUES(%s,%s,%s)""",(numeroPi,nomPi,client))
    db.commit()
    
    print("Enregistrement du pi table OK - bdd")
    
    cur.execute("""INSERT INTO etat(ref_pi,guard,hy3,alarm,erreur) VALUES(%s,%s,%s,%s,%s)""",(numeroPi,guard,hy3,alarm,erreur))
    db.commit() #Valide la modification
    
    print("Enregistrement du etat table OK - bdd")
    
    print("envoi à la base de donnée")
#Definition d'une fonction wait(int sec) temps d'attente
def wait(p_time):
    print("Attente de",p_time,"secondes")
    time.sleep(p_time)
    
#Definition d'une fonction qui affiche dans la console les différentes infos etat heure ...
def display():
    t=time.time()
    print("------")
    print("Client ERP:",client,"-",nomClient)
    print("Heure/Date:",pointage)
    print("Mode Guard:",guard)
    print("Alarme:",alarm)
    print("hy3:", hy3)
    print("Erreur:",erreur)

#Enregistrement/Verification client création
#try:    
#    db=MySQLdb.connect(host=bddUrl, user=bddUser, passwd=bddPswd, db=bddName)
#    cur=db.cursor()
    
    #db.execute("CREATE TABLE IF NOT EXISTS {0} (id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, port1 INT, port2 INT, port3 INT, port4 INT, port5 INT, port6 INT, port7 INT, port8 INT, horaire TIMESTAMP)".format(client))
#    cur.execute("""CREATE TABLE IF NOT EXISTS %s id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, port1 INT, port2 INT, port3 INT, port4 INT, port5 INT, port6 INT, port7 INT, port8 INT, horaire TIMESTAMP""",(client))
#    db.commit()
#    print("Verification table ok")
#    cur.execute("INSERT INTO Client_evicollecte (ref_client) VALUES ('{0}')".format(client))
#    db.commit()
#except:
#    print("le client existe déjà")
print("Fini d'initialisation")
wait(1)
print("Debut du programme")
try:
#Debut du script/programme
    while True:
        #passage des pins a False - pour éviter que les valeurs ne restent inchangées
        hy3=False
        guard=False
        erreur=False
        alarm=False
        pointage=False

        pointage=checkDate()#On prend l'heure actuelle

        #Lecture des pins et affectation aux variables
        erreur=pi.read(p_erreur)
        alarm=pi.read(p_alarm)
        guard=pi.read(p_guard)
        hy3=pi.read(p_hy3)


            
        if guard==1 and alarm==0 and hy3==0 and erreur==0: #Si l'alarme est actif
            #pas besoin d'envoyer de mail On affecte les nouvelles valeurs
            print("Tout est OK")
            rguard="OK"
            rhy3="OK"
            ralarm="non déclenché"
            rerreur="OK"
            
            if nbEnvoi==1:
                nbEnvoi=0
            
        elif (guard==False and alarm==False and hy3==False and erreur==False)or(guard==0 and alarm==0 and hy3==0 and erreur==0):#Si les données sont toujours égale à False c'est qu'aucune valeur n'a pas etre lu donc bandit pas branché
            print("Pas de donnée lu")
            rguard="NoData"
            ralarm="NoData"
            rerreur="NoData"
            rhy3="NoData"
            if nbEnvoi<1:
                nbEnvoi=nbEnvoi+1
            
            envoiMail(rapport+"\n\n"+msgZero,objZero)
        
        else:
            print("Il y a peut être un dysfonctionnement")
            #Dans le cas contraire C'est qu'il faut envoyer un mail : au cas par cas


            if nbEnvoi==1:
                print("L'envoi du mail de rapport a déjà été effectué")
                temps=time.time()

                if chrono+delai < temps:#
                    if hy3 == 1:
                        rhy3="NOK"
                    elif rhy3 == 0:
                        rhy3="OK"                
                    elif alarm == 1:
                        ralarm="déclenché"                         
                    elif alarm==0:
                        ralarm="non déclenché"
                    elif guard==1:
                        rguard="OK"
                    elif guard==0:                      
                        rguard="NOK"
                    elif erreur==1:
                        rerreur="NOK"
                    elif erreur==0:
                        rerreur="OK"
                    rapport="Rapport - "+"Nom Client"+nomClient+" N°Client ERP:"+client+"\n Cartouche HY3:"+str(rhy3)+"\n Mode alarme:"+str(ralarm)+" \n Mode Surveillance:"+str(guard)+"\n Mode Erreur:"+str(rerreur)+"\n Heure du scan:"+str(pointage)
                    #Changer les valeurs avant !!! 1/0 --> ok - nok
                    envoiMail(rapport,objRapport)
                    
                else:
                    tempsRestant=((chrono+delai-temps)/60.00)/60.00
                    print("Temps restant avant renvoi:",tempsRestant,"heures") 
                    if hy3 == 1:
                        rhy3="NOK"
                    if hy3 == 0:
                        rhy3="OK"                
                    if alarm == 1:
                        ralarm="déclenché"                         
                    if alarm==0:
                        ralarm="non délenché"
                    if guard==1:
                        rguard="OK"
                    if guard==0:                      
                        rguard="NOK"
                    if erreur==1:
                        rerreur="NOK"
                    if erreur==0:
                        rerreur="OK"
                    
            elif nbEnvoi<1:
                            
                rapport="Rapport:"
                alerte="[Alerte] "
                if guard==0:
                    rapport="Bandit pas en mode surveillance.\n"
                    alerte=alerte+" -"+" Surveillance"
                if erreur==1:
                    rapport=rapport+"Une erreur est présente dans le bandit. Verifiez que le Bandit est branché à une alimentation\n"
                    alerte=alerte+" -"+" Erreur"
                if alarm==1:
                    rapport=rapport+"Bandit Décleclenché. \n"
                    alerte=alerte+" -"+" Alarme"
                if hy3==1:
                    rapport=rapport+"Liquide Cartouche Bas. \n"
                    alerte=alerte+" -"+" Cartouche"
                    
                envoiMail(rapport,alerte+" "+client+" - "+nomClient)
                nbEnvoi=nbEnvoi+1
                
                print("Premier envoi")
                if hy3 == 1:
                    rhy3="NOK"
                if hy3 == 0:
                    rhy3="OK"                
                if alarm == 1:
                    ralarm="déclenché"                         
                if alarm==0:
                    ralarm="non déclenché"
                if guard==1:
                    rguard="OK"
                if guard==0:                      
                    rguard="NOK"
                if erreur==1:
                    rerreur="NOK"
                if erreur==0:
                    rerreur="OK"
                #rapport="Rapport - "+"Nom Client"+nomClient+" N°Client ERP:"+client+"\n Cartouche HY3:"+str(hy3)+"\n Mode alarme:"+str(alarm)+" \n Mode Surveillance:"+str(guard)+"\n Mode Erreur:"+str(erreur)+"\n Heure du scan:"+str(pointage)
                #envoiMail(rapport,objRapport)
                #nbEnvoi=nbEnvoi+1
                #On prend ici le temps pour le stocker
                chrono=time.time()
                print("Chrono", chrono)

        
        display()#affichage de toutes informations dans la console
        record()#enregistrement dans la bdd
        wait(60)#on attend x secondes
        stockeCsv()#on stock les valeurs dans un fichier log

except:
    print("Sortie du programme")
    envoiMail(msgStop,objStop)#on envoie un email pour pour prévenir que le script s'est arrêté. remarque: il faudrait ajouter le fichier Csv
    print("Message stop script envoyé")

    


#Boucle principale
 






    
 #Liberer les pins GPIOs
 #60 secondes dattente
#Fin de boucle principale

