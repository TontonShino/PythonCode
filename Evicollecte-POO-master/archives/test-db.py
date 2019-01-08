import MySQLdb #Gere les Transactions sql
import re
#import PyMySQL



client="CLI00976"#976=Evidensee Nom du client - exemple:CLI0085
idpi=2
bddUrl=""#Url/adresse bdd
bddUser=""#User BDD
bddPswd=""#Mot de passe BDD
bddName=""#nom de la base de donnee



db=MySQLdb.connect(host=bddUrl, user=bddUser, passwd=bddPswd, db=bddName)
cur=db.cursor()

print("Récupération de l'id PI")
        
cur.execute("SELECT Max(idpi) as id FROM pi;")
id=cur.fetchone()
id=int(id[0]+1)


print("Next Id Pi  =",id)

cur.execute("select rowid from llx_societe WHERE code_client=('{0}')".format(client))
rowid=str(cur.fetchone())

rowid=rowid.replace(",","")
rowid=rowid.replace("(","")
rowid=rowid.replace(")","")
rowid=rowid.replace(")","")
rowid=int(rowid)
print("id row client:",rowid)
cur.execute("SELECT nom,address,town,zip,code_client FROM llx_societe WHERE code_client=('{0}')".format(client))
description=str(cur.fetchone())

description = description.replace(",","")
description = description.replace("'","")
description = description.replace("(","")
description = description.replace(")","")
print(description[0])

cur.execute("INSERT IGNORE INTO pi(idpi,ref_rowid,ref_client,description) values({0},{1},('{2}'),('{3}'))".format(idpi,rowid,client,description))
db.commit()

cur.execute("UPDATE pi SET description = ('{1}') WHERE idpi=({0})".format(idpi,description))
db.commit()

#on met à jour les infos
cur.execute("UPDATE pi SET guard = 1,alarm=0, hy3=0, erreur=0,statut='test',fxguard=0  WHERE idpi=({0})".format(idpi))
db.commit()

#On ajoute les données à la table historique
cur.execute("INSERT INTO history_pi(ref_pi,guard,alarm,hy3,erreur,fxguard,statut) VALUES({0},{1},{2},{3},{4},{5},('{6}'))".format(idpi,1,0,0,0,0,"test"))
db.commit()



